"""
WORLD CUP 2026 — Monte Carlo del CUADRO (odds de ganar el torneo / llegar a cada ronda). ISOLATED.

READ-ONLY sobre el modelo: usa los ratings/predicción L3 actuales; NO toca las predicciones por
partido; NO mercado. Proyección FORWARD (no liquidable -> sin leakage). Flag TOURNAMENT_SIM.

BRACKET: los 32 vivos + los 16 cruces de R32 salen de los fixtures REALES (API, ya en caché fresco).
El cuadro es FIJO (sin re-sorteo): encodeamos el mapa de slots R32->R16->cuartos->semis->final.
GUARDA DE VALIDACIÓN (crítica): el mapa debe REPRODUCIR EXACTAMENTE los octavos YA poblados en los
fixtures (a partir de los ganadores reales de R32). Si NO reproduce -> NO se publican odds.

MONTE CARLO: N iteraciones (seed fijo). Cada cruce: P(avanza a)=P(gana 90')+P(empate)*0.5 del modelo
(ratings actuales, NEUTRAL). Los R32 ya jugados se toman como HECHOS (el ganador real avanza). Se
propaga por el árbol -> P(gana Mundial)/P(final)/P(semis) por selección viva. Eliminados -> 0.

HONESTO: proyección del modelo, incertidumbre que se ACUMULA ronda a ronda; cuadro validado contra
los octavos conocidos. Nunca "certeza".
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

OUT_DIR = Path(__file__).resolve().parent
ROOT = OUT_DIR.parents[1]
sys.path.insert(0, str(OUT_DIR))
sys.path.insert(0, str(ROOT / "scripts"))

# ---- flag (reversible): False -> el briefing no muestra la sección (Δ0).
TOURNAMENT_SIM = True
N_ITERS = 20000
SEED = 20260701

# Cuadro OFICIAL FIJO WC-2026 (fuente FIFA / Wikipedia "2026 FIFA World Cup knockout stage").
# Mapa de OCTAVOS por índice de R32 ordenado por FECHA (0..15): qué 2 fixtures de R32 alimentan cada
# slot de octavos. VALIDADO en runtime contra los octavos ya poblados (guarda). Cuartos/semis/final =
# adyacencia estándar de eliminatoria (slot de octavos 2k,2k+1 -> cuarto k; etc.).
R16_MAP = [(0, 3), (1, 4), (2, 5), (6, 9), (7, 10), (8, 11), (12, 15), (13, 14)]

FINISHED = {"FT", "AET", "PEN"}


def _round(f):
    return (f.get("league") or {}).get("round")


def _teams(f):
    tm = f.get("teams") or {}
    return (tm.get("home") or {}).get("name"), (tm.get("away") or {}).get("name")


def _winner(f):
    """Real winner name if the match is finished (API teams.*.winner), else None."""
    tm = f.get("teams") or {}
    if (tm.get("home") or {}).get("winner"):
        return (tm.get("home") or {}).get("name")
    if (tm.get("away") or {}).get("winner"):
        return (tm.get("away") or {}).get("name")
    return None


def load_wc_fixtures(client=None):
    """WC fixtures from the shared client (cache; the briefing refreshes it). [] on soft-fail."""
    try:
        if client is None:
            from api_football_client import APIFootballClient
            client = APIFootballClient()
        return client.request("/fixtures", {"league": 1, "season": 2026}, ttl_hours=6).get("response") or []
    except Exception:
        return []


# ------------------------------------------------------------------ bracket
def build_bracket(fixtures):
    """From the real fixtures build the R32 layer (date-ordered) + the fixed R16/QF/SF/Final tree.
    Returns a dict, or None if there is no usable R32 layer. Pure (no API)."""
    r32 = [f for f in fixtures if _round(f) == "Round of 32"]
    r16 = [f for f in fixtures if _round(f) == "Round of 16"]
    if len(r32) < 16:
        return None
    r32.sort(key=lambda f: ((f.get("fixture") or {}).get("date") or "",
                            (f.get("fixture") or {}).get("id") or 0))
    slots = []
    for f in r32[:16]:
        h, a = _teams(f)
        st = ((f.get("fixture") or {}).get("status") or {}).get("short")
        slots.append({"home": h, "away": a, "played": st in FINISHED, "winner": _winner(f)})
    # real R16 fixtures -> set of frozenset(teams) for the guard
    real_r16 = []
    for f in r16:
        h, a = _teams(f)
        if h and a:
            real_r16.append(frozenset((h, a)))
    return {"r32": slots, "r16_map": list(R16_MAP), "real_r16": real_r16}


def validate_guard(bracket):
    """CRÍTICA: cada octavo YA poblado en los fixtures debe salir EXACTAMENTE del mapa encodeado a
    partir de los ganadores reales de R32. Devuelve (ok, detalle). ok=False -> NO publicar odds."""
    if not bracket:
        return False, "sin bracket (R32 incompleto)"
    slots = bracket["r32"]
    win = [s["winner"] for s in slots]
    # producir el conjunto de octavos que el mapa deduce SOLO cuando ambos feeders están decididos
    produced = {}
    for k, (a, b) in enumerate(bracket["r16_map"]):
        if win[a] and win[b]:
            produced[frozenset((win[a], win[b]))] = k
    checked = matched = 0
    misses = []
    for real in bracket["real_r16"]:
        checked += 1
        if real in produced:
            matched += 1
        else:
            misses.append(tuple(sorted(real)))
    ok = (checked > 0 and matched == checked)
    detail = f"octavos reales poblados={checked} · reproducidos por el cuadro={matched}"
    if misses:
        detail += f" · DESAJUSTE en: {misses}"
    if checked == 0:
        detail = "aún no hay octavos poblados que validar (checked=0) -> no publico"
    return ok, detail


# ------------------------------------------------------------------ probabilities
def build_pmatrix(teams, predict):
    """P[i,j] = P(i vence a j) NEUTRAL = 0.5*(adv(i,j) + (1-adv(j,i))), adv(x,y)=P(x gana 90')+P(empate)*0.5
    de predict(x,y). Simétrica (P[i,j]+P[j,i]=1). predict(a,b)->{our_home,our_draw,...} o None."""
    m = len(teams)
    P = np.full((m, m), 0.5)

    def adv(x, y):
        try:
            r = predict(teams[x], teams[y])
            if not r:
                return None
            return float(r["our_home"]) + 0.5 * float(r["our_draw"])
        except Exception:
            return None
    for i in range(m):
        for j in range(i + 1, m):
            a_ij, a_ji = adv(i, j), adv(j, i)
            if a_ij is None and a_ji is None:
                p = 0.5
            elif a_ji is None:
                p = a_ij
            elif a_ij is None:
                p = 1 - a_ji
            else:
                p = 0.5 * (a_ij + (1 - a_ji))
            p = min(max(float(p), 0.01), 0.99)
            P[i, j] = p; P[j, i] = 1 - p
    return P


# ------------------------------------------------------------------ Monte Carlo
def simulate(bracket, teams, P, n=N_ITERS, seed=SEED):
    """Vectorized forward sim. Played R32 -> winner FIXED (fact). Unplayed + all later rounds -> sim.
    Returns {team: {p_champ, p_final, p_semi}} for the ALIVE teams (R32 participants)."""
    idx = {t: i for i, t in enumerate(teams)}
    rng = np.random.default_rng(seed)
    slots = bracket["r32"]

    def match(a_idx, b_idx):
        """a_idx,b_idx: int arrays (n,). Winner per iter using P and one uniform draw."""
        pa = P[a_idx, b_idx]
        u = rng.random(len(a_idx))
        return np.where(u < pa, a_idx, b_idx)

    # R32 winners (16 arrays of shape n)
    w32 = []
    for s in slots:
        hi, ai = idx.get(s["home"]), idx.get(s["away"])
        if hi is None or ai is None:
            # a slot we cannot resolve (missing rating) -> degrade: keep 'home' if present
            fixed = hi if hi is not None else ai
            w32.append(np.full(n, fixed if fixed is not None else 0))
            continue
        if s["played"] and s["winner"] in idx:
            w32.append(np.full(n, idx[s["winner"]]))          # FACT: real winner advances
        else:
            w32.append(match(np.full(n, hi), np.full(n, ai)))  # simulate
    # R16 (quarterfinalists), QF (semifinalists), SF (finalists), Final (champion)
    w16 = [match(w32[a], w32[b]) for a, b in bracket["r16_map"]]
    wqf = [match(w16[2 * k], w16[2 * k + 1]) for k in range(4)]   # semifinalists
    wsf = [match(wqf[2 * k], wqf[2 * k + 1]) for k in range(2)]   # finalists
    champ = match(wsf[0], wsf[1])

    m = len(teams)
    c_semi = np.zeros(m); c_final = np.zeros(m); c_champ = np.zeros(m)
    for arr in wqf:
        np.add.at(c_semi, arr, 1)      # reached SF (won QF)
    for arr in wsf:
        np.add.at(c_final, arr, 1)     # reached Final (won SF)
    np.add.at(c_champ, champ, 1)
    out = {}
    alive = set()
    for s in slots:
        alive.add(s["home"]); alive.add(s["away"])
    for t in alive:
        i = idx.get(t)
        if i is None:
            continue
        out[t] = {"p_champ": c_champ[i] / n, "p_final": c_final[i] / n, "p_semi": c_semi[i] / n}
    return out


def run_sim(client=None, predict=None, n=N_ITERS, seed=SEED):
    """Full pipeline: fixtures -> bracket -> GUARD -> pmatrix -> simulate. Returns
    (odds_or_None, guard_ok, guard_detail). odds=None if the guard fails (never publish a wrong tree)."""
    fixtures = load_wc_fixtures(client)
    bracket = build_bracket(fixtures)
    ok, detail = validate_guard(bracket)
    if not ok:
        return None, ok, detail
    teams = sorted({t for s in bracket["r32"] for t in (s["home"], s["away"]) if t})
    if predict is None:
        import l3_offline
        pred = l3_offline.load_predictor()
        predict = pred.predict
    P = build_pmatrix(teams, predict)
    odds = simulate(bracket, teams, P, n=n, seed=seed)
    return odds, ok, detail


# ------------------------------------------------------------------ briefing section
def tournament_block(top=8):
    """Clean briefing section (list of lines) or [] (flag off / guard fail / soft-fail -> nothing)."""
    if not TOURNAMENT_SIM:
        return []
    try:
        odds, ok, _detail = run_sim()
        if not ok or not odds:
            return []
        try:
            from build_worldcup_full_card import es_name
        except Exception:
            es_name = str
        ranked = sorted(odds.items(), key=lambda kv: -kv[1]["p_champ"])
        ranked = [(t, v) for t, v in ranked if v["p_champ"] > 0][:top]
        if not ranked:
            return []
        lines = ["🏆 Quién gana el Mundial (simulación del modelo, "
                 f"{N_ITERS // 1000}k · cuadro oficial):"]
        for i, (t, v) in enumerate(ranked, 1):
            lines.append(f"   {i}. {es_name(t)} {v['p_champ']*100:.0f}% "
                         f"(final {v['p_final']*100:.0f}% · semis {v['p_semi']*100:.0f}%)")
        lines.append("   ⚠️ Proyección del modelo (ratings actuales), NO certeza · la incertidumbre "
                     "se acumula ronda a ronda (menos fiable cuanto más lejos).")
        lines.append("   Cuadro oficial validado contra los octavos ya conocidos. Sin cuotas.")
        return lines
    except Exception:
        return []


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["guard", "sim", "block"])
    a = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    if a.cmd == "guard":
        fx = load_wc_fixtures()
        br = build_bracket(fx)
        ok, detail = validate_guard(br)
        print("GUARDA:", "PASA" if ok else "FALLA", "|", detail)
        if br:
            slots = br["r32"]
            print("R32 (orden fecha) ganadores:", [s["winner"] for s in slots])
    elif a.cmd == "sim":
        odds, ok, detail = run_sim()
        print("guard:", ok, detail)
        if odds:
            for t, v in sorted(odds.items(), key=lambda kv: -kv[1]["p_champ"])[:16]:
                print(f"  {t:24s} gana {v['p_champ']*100:5.1f}% | final {v['p_final']*100:5.1f}% | semis {v['p_semi']*100:5.1f}%")
            print("suma p_champ:", round(sum(v["p_champ"] for v in odds.values()), 4))
    else:
        print("\n".join(tournament_block()))
