"""
WORLD CUP 2026 — QUALIFICATION-CONTEXT adjustment in SHADOW MODE. ISOLATED · heurístico · NO validado.

Idea: a team's GROUP SCENARIO before a match (already qualified / eliminated / must-win / a draw is
enough / decisive / dead rubber) MIGHT bend its goal output (rotation, caution, chasing). This module
computes an ALTERNATIVE prediction that nudges the L3 xG by a small, EXPLICIT, documented multiplier
per scenario, recomputes 1X2/OU with the SAME Poisson + the SAME (untouched) L3 calibration, logs BOTH
the pure L3 and the context-adjusted version, and SCORES the adjustment against pure L3 — but NEVER
shows it live until it earns it.

THE MULTIPLIERS ARE HYPOTHESES, NOT TRUTHS. The sign is genuinely ambiguous: 'already-qualified' may
rotate OR play normally; 'must-win' may attack more OR sit cautious. We do NOT assume it helps; the
scorecard is the judge.

Scenario -> multiplier on THAT team's own attacking xG (documented defaults, see MULT):
  ya_clasificado    ×0.92   (menos intensidad / rotación)
  eliminado         ×0.95   (poco que jugar)
  debe_ganar        ×1.08   (va por detrás, sale a por el partido)
  le_vale_empate    ×0.97   (le sirve el empate, algo más conservador)
  partido_decisivo  ×1.00   (todo en juego, intensidad normal -> sin cambio)
  intrascendente    ×0.90   (AMBOS equipos ya resueltos: amistoso de facto, menos goles)
  knockout/unknown  ×1.00   (sin contexto de grupo -> sin ajuste)

Subcommands:  predict (NS only, anti-hindsight, lock-at-KO) · settle (after FT) ·
              scorecard (context-adjusted VS pure L3, ONLY over NON-TRIVIAL scenarios).

SAFEGUARDS: does NOT touch L3 / calibration / lock-at-KO / briefing / props. Anti-hindsight (predict
pre-KO, freeze at KO, settle only after FT; never touches settled/result_*). API store-guarded
(/standings cached per day; settle reuses the cached /fixtures). NO betting endpoints. NOT shown on
Telegram, NOT in the ficha. Explicit git add (log + scorecard only).
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(OUT_DIR))
sys.path.insert(0, str(ROOT / "scripts"))
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

import l3_offline  # noqa: E402  (reuse the exact L3 Poisson + calibration machinery)

CARDS = OUT_DIR / "worldcup_cards.csv"
LOG = OUT_DIR / "worldcup_context_shadow_log.csv"
SCORECARD = OUT_DIR / "worldcup_context_shadow_scorecard.txt"
STORE_DIR = ROOT / "data" / "processed" / "worldcup" / "context"   # gitignored standings cache

LEAGUE, SEASON = 1, 2026
ADVANCE = 2                       # top-2 of each group advance (best-thirds ignored -> documented)
KO_BUFFER = timedelta(minutes=5)  # freeze a fixture this long BEFORE kickoff (anti-hindsight margin)
EPS = 1e-15
SMALL_N = 20                      # graduation threshold over NON-TRIVIAL scenarios
FINISHED = {"FT", "AET", "PEN"}

# scenario -> multiplier on the team's OWN attacking xG. EXPLICIT hypotheses (sign ambiguous).
MULT = {
    "ya_clasificado": 0.92, "eliminado": 0.95, "debe_ganar": 1.08, "le_vale_empate": 0.97,
    "partido_decisivo": 1.00, "intrascendente": 0.90, "knockout": 1.00, "unknown": 1.00,
}

LOG_COLUMNS = [
    "fixture_id", "kickoff_utc", "home", "away", "round", "home_group", "away_group",
    "scenario_home", "scenario_away", "mult_home", "mult_away", "nontrivial",
    "l3_home", "l3_draw", "l3_away", "l3_xg_home", "l3_xg_away", "l3_over25",
    "ctx_home", "ctx_draw", "ctx_away", "ctx_xg_home", "ctx_xg_away", "ctx_over25",
    "logged_at_utc", "pred_policy", "pred_lead_min",
    "result_ft_gh", "result_ft_ga", "result_1x2", "result_status", "settled", "settled_at_utc",
]


def _now_iso():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _parse_ko(s):
    if s is None or (isinstance(s, float) and pd.isna(s)):
        return None
    try:
        return datetime.strptime(str(s).strip()[:16], "%Y-%m-%d %H:%M").replace(tzinfo=timezone.utc)
    except Exception:
        return None


# --------------------------------------------------------------- store-guarded standings
def _client():
    from api_football_client import APIFootballClient  # noqa: E402
    return APIFootballClient()


def _store_path(name):
    return STORE_DIR / f"{name}.json"


def _load_store(name):
    p = _store_path(name)
    if p.exists():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            return None
    return None


def _save_store(name, data):
    STORE_DIR.mkdir(parents=True, exist_ok=True)
    _store_path(name).write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")


def fetch_standings(client, day=None):
    """Store-guarded /standings(league=1) for today (cached per UTC date). Returns the raw
    'response' list or None (soft-fail). NOT a betting endpoint."""
    day = day or datetime.now(timezone.utc).strftime("%Y-%m-%d")
    name = f"standings_{day}"
    cached = _load_store(name)
    if cached is not None:
        return cached
    try:
        resp = client.request("/standings", {"league": LEAGUE, "season": SEASON}, ttl_hours=2)
    except Exception:
        return None
    data = (resp.get("response") if isinstance(resp, dict) else None) or []
    if data:
        _save_store(name, data)
    return data or None


def build_status_maps(standings_resp):
    """(groups, team_group) from a /standings response. groups: name -> [team rows]; team_group:
    team -> group name. Prefers the real lettered group over the aggregate 'Group Stage' table."""
    groups, team_group = {}, {}
    for blk in (standings_resp or []):
        tables = (blk.get("league") or {}).get("standings") or []
        for grp in tables:
            for t in grp:
                name = ((t.get("team") or {}).get("name"))
                if not name:
                    continue
                gname = str(t.get("group") or "")
                lettered = gname.startswith("Group ") and len(gname.split()) == 2 and len(gname.split()[-1]) == 1
                row = {"name": name, "points": _num(t.get("points")),
                       "played": _num((t.get("all") or {}).get("played")), "gd": _num(t.get("goalsDiff"))}
                # prefer lettered group; don't overwrite a lettered entry with the aggregate
                if name in team_group and not lettered:
                    continue
                team_group[name] = gname
                groups.setdefault(gname, [])
                groups[gname] = [r for r in groups[gname] if r["name"] != name] + [row]
    return groups, team_group


def _num(v):
    try:
        return float(v) if v is not None else 0.0
    except (TypeError, ValueError):
        return 0.0


# --------------------------------------------------------------- scenario classification
def _team_status(name, table, advance=ADVANCE):
    """(qualified, eliminated, remaining, rank_by_points) using clinch/elimination point bounds
    (tiebreakers/best-thirds IGNORED -> conservative, documented simplification)."""
    G = len(table)
    per_team = max(G - 1, 1)
    me = next((r for r in table if r["name"] == name), None)
    if me is None:
        return False, False, None, None
    rem = max(per_team - me["played"], 0)
    my_best = me["points"] + 3 * rem
    my_worst = me["points"]
    can_pass = clinched_above = 0
    for o in table:
        if o["name"] == name:
            continue
        o_rem = max(per_team - o["played"], 0)
        o_best = o["points"] + 3 * o_rem
        if o_best >= my_worst:          # o could end at/above my floor -> could pass me (conservative)
            can_pass += 1
        if o["points"] > my_best:       # o already guaranteed strictly above my ceiling
            clinched_above += 1
    qualified = can_pass < advance      # at most advance-1 others can reach me -> I'm in (conservative)
    eliminated = clinched_above >= advance
    order = sorted(table, key=lambda r: (-r["points"], -r["gd"]))
    rank = 1 + [r["name"] for r in order].index(name)
    return qualified, eliminated, rem, rank


def classify_fixture(round_str, home, away, groups, team_group, advance=ADVANCE):
    """(scenario_home, scenario_away, mult_home, mult_away, nontrivial). Knockouts / missing
    standings -> 'knockout'/'unknown' (mult 1.0 -> trivial). Dead rubber (both resolved) ->
    'intrascendente' for both."""
    if "group" not in str(round_str).lower():
        return "knockout", "knockout", 1.0, 1.0, False

    def scen(name):
        g = team_group.get(name)
        table = groups.get(g) if g else None
        if not table:
            return "unknown", True  # (scenario, resolved?) — unknown counts as not-resolved
        q, e, rem, rank = _team_status(name, table, advance)
        if q:
            return "ya_clasificado", True
        if e:
            return "eliminado", True
        if rem == 1:                                   # last group game, still alive
            return ("le_vale_empate" if (rank is not None and rank <= advance) else "debe_ganar"), False
        return "partido_decisivo", False               # earlier group game, full stakes

    sh, rh = scen(home)
    sa, ra = scen(away)
    # dead rubber: BOTH teams already resolved (qualified OR eliminated) -> de-facto friendly
    if rh and ra and sh != "unknown" and sa != "unknown":
        sh = sa = "intrascendente"
    mh, ma = MULT.get(sh, 1.0), MULT.get(sa, 1.0)
    nontrivial = (mh != 1.0) or (ma != 1.0)
    return sh, sa, mh, ma, nontrivial


# --------------------------------------------------------------- prediction (pure math)
def _over25(lh, la):
    lam = max(float(lh) + float(la), 1e-9)
    return float(1.0 - np.exp(-lam) * (1.0 + lam + lam * lam / 2.0))


def context_predict(pred, home, away, mult_home, mult_away):
    """Pure L3 vs context-adjusted via the SAME machinery (raw_xg -> Poisson wdl -> L3 isotonic).
    The ONLY difference is the per-team xG multiplier. None if a team has no rating."""
    sh = pred.strength.get(home)
    sa = pred.strength.get(away)
    if sh is None or sa is None:
        return None
    lh, la = l3_offline.raw_xg(sh - sa, pred.a0, pred.a1, pred.total_mean)

    def cal(lhh, laa):
        raw = l3_offline.wdl(lhh, laa)
        c = np.array([np.interp(raw[k], pred.iso[k]["ux"], pred.iso[k]["uf"]) for k in range(3)])
        c = np.clip(c, 1e-6, None)
        return c / c.sum()

    l3 = cal(lh, la)
    clh, cla = lh * float(mult_home), la * float(mult_away)
    ctx = cal(clh, cla)
    return {
        "l3_home": round(float(l3[0]), 4), "l3_draw": round(float(l3[1]), 4),
        "l3_away": round(float(l3[2]), 4), "l3_xg_home": round(float(lh), 3),
        "l3_xg_away": round(float(la), 3), "l3_over25": round(_over25(lh, la), 4),
        "ctx_home": round(float(ctx[0]), 4), "ctx_draw": round(float(ctx[1]), 4),
        "ctx_away": round(float(ctx[2]), 4), "ctx_xg_home": round(float(clh), 3),
        "ctx_xg_away": round(float(cla), 3), "ctx_over25": round(_over25(clh, cla), 4),
    }


# --------------------------------------------------------------- log helpers
def _read_log():
    if LOG.exists():
        df = pd.read_csv(LOG)
        for c in LOG_COLUMNS:
            if c not in df.columns:
                df[c] = np.nan
        return df[LOG_COLUMNS]
    return pd.DataFrame(columns=LOG_COLUMNS)


# hooks for tests / monkeypatching
load_predictor = l3_offline.load_predictor


def _fixture_status_index(client):
    """fid -> status short from the cached /fixtures call (~0 marginal API)."""
    idx = {}
    try:
        resp = client.request("/fixtures", {"league": LEAGUE, "season": SEASON}, ttl_hours=6)
    except Exception:
        return idx
    for f in ((resp.get("response") if isinstance(resp, dict) else None) or []):
        fx = f.get("fixture") or {}
        fid = fx.get("id")
        if fid is None:
            continue
        goals = f.get("goals") or {}
        score = f.get("score") or {}
        ft = score.get("fulltime") or {}
        gh = ft.get("home") if ft.get("home") is not None else goals.get("home")
        ga = ft.get("away") if ft.get("away") is not None else goals.get("away")
        idx[int(fid)] = {"status": (fx.get("status") or {}).get("short"), "gh": gh, "ga": ga}
    return idx


# --------------------------------------------------------------- predict
def cmd_predict(now=None):
    if not CARDS.exists():
        print("context_shadow predict: no cards.csv; nothing to do."); return
    cards = pd.read_csv(CARDS)
    pred = load_predictor()
    if pred is None:
        print("context_shadow predict: L3 predictor unavailable (no ratings/calibration); skip."); return
    client = _client()
    standings = fetch_standings(client)
    groups, team_group = build_status_maps(standings)
    now = now or datetime.now(timezone.utc)
    log = _read_log()

    SNAP = [c for c in LOG_COLUMNS if c not in
            ("fixture_id", "kickoff_utc", "home", "away", "round",
             "result_ft_gh", "result_ft_ga", "result_1x2", "result_status", "settled", "settled_at_utc")]
    for c in SNAP:
        if c in log.columns:
            log[c] = log[c].astype(object)
    idx_by_fid = {int(f): i for i, f in zip(log.index, log["fixture_id"]) if pd.notna(f)}

    def snapshot(r, ko):
        home, away = str(r.get("home")), str(r.get("away"))
        sh, sa, mh, ma, nt = classify_fixture(r.get("round"), home, away, groups, team_group)
        cp = context_predict(pred, home, away, mh, ma)
        if cp is None:
            return None
        lead = int((ko - now).total_seconds() / 60) if ko is not None else np.nan
        return {
            "home_group": team_group.get(home), "away_group": team_group.get(away),
            "scenario_home": sh, "scenario_away": sa, "mult_home": mh, "mult_away": ma,
            "nontrivial": int(bool(nt)), **cp,
            "logged_at_utc": _now_iso(), "pred_policy": "last_preko", "pred_lead_min": lead,
        }

    new_rows, n_upd = [], 0
    for _, r in cards.iterrows():
        if pd.isna(r.get("fixture_id")) or pd.isna(r.get("our_home")):
            continue
        fid = int(r["fixture_id"])
        ko = _parse_ko(r.get("kickoff_utc"))
        pre_ko = ko is not None and now < (ko - KO_BUFFER)   # LOCK-AT-KO: only strictly pre-KO
        if fid in idx_by_fid:
            i = idx_by_fid[fid]
            settled = int(log.at[i, "settled"]) if not pd.isna(log.at[i, "settled"]) else 0
            if pre_ko and settled == 0:
                snap = snapshot(r, ko)
                if snap:
                    for col, val in snap.items():
                        log.at[i, col] = val
                    n_upd += 1
            continue  # at/after KO or settled -> FROZEN (anti-hindsight)
        if not pre_ko:
            continue  # never first-log a fixture whose KO already passed
        snap = snapshot(r, ko)
        if snap is None:
            continue
        new_rows.append({
            "fixture_id": fid, "kickoff_utc": r.get("kickoff_utc"),
            "home": r.get("home"), "away": r.get("away"), "round": r.get("round"),
            "result_ft_gh": np.nan, "result_ft_ga": np.nan, "result_1x2": np.nan,
            "result_status": np.nan, "settled": 0, "settled_at_utc": np.nan, **snap,
        })
        idx_by_fid[fid] = len(log) + len(new_rows) - 1

    if new_rows:
        log = pd.concat([log, pd.DataFrame(new_rows)], ignore_index=True)[LOG_COLUMNS]
    log.to_csv(LOG, index=False)
    nt_total = int(pd.to_numeric(log["nontrivial"], errors="coerce").fillna(0).astype(int).sum()) if len(log) else 0
    print(f"context_shadow predict: +{len(new_rows)} new, {n_upd} updated (pre-KO) | "
          f"non-trivial rows={nt_total} | total={len(log)} -> {LOG.name}")


# --------------------------------------------------------------- settle
def cmd_settle():
    log = _read_log()
    if log.empty:
        print("context_shadow settle: empty log."); return
    client = _client()
    idx = _fixture_status_index(client)
    for col in ("result_1x2", "result_status", "settled_at_utc"):
        log[col] = log[col].astype(object)
    newly = 0
    for i, r in log.iterrows():
        if int(r.get("settled") or 0) == 1:
            continue
        info = idx.get(int(r["fixture_id"]))
        if not info or info["status"] not in FINISHED:
            continue
        gh, ga = info["gh"], info["ga"]
        if gh is None or ga is None:
            continue
        res = "H" if gh > ga else ("D" if gh == ga else "A")
        log.at[i, "result_ft_gh"] = gh; log.at[i, "result_ft_ga"] = ga
        log.at[i, "result_1x2"] = res; log.at[i, "result_status"] = info["status"]
        log.at[i, "settled"] = 1; log.at[i, "settled_at_utc"] = _now_iso()
        newly += 1
    log.to_csv(LOG, index=False)
    nset = int((log["settled"].fillna(0).astype(int) == 1).sum())
    print(f"context_shadow settle: +{newly} newly settled, {nset} total -> {LOG.name}")


# --------------------------------------------------------------- scorecard
def _logloss_multi(P, Y):
    Pc = np.clip(P, EPS, 1.0); Pc = Pc / Pc.sum(1, keepdims=True)
    return float(-np.mean(np.sum(Y * np.log(Pc), axis=1)))


def _brier_multi(P, Y):
    Pc = np.clip(P, EPS, 1.0); Pc = Pc / Pc.sum(1, keepdims=True)
    return float(np.mean(np.sum((Pc - Y) ** 2, axis=1)))


def _acc_multi(P, Y):
    return float(np.mean(P.argmax(1) == Y.argmax(1)))


def _bin_logloss(p, y):
    p = np.clip(np.asarray(p, float), EPS, 1 - EPS); y = np.asarray(y, float)
    return float(-np.mean(y * np.log(p) + (1 - y) * np.log(1 - p)))


def _bin_brier(p, y):
    return float(np.mean((np.asarray(p, float) - np.asarray(y, float)) ** 2))


GRADUATION_NOTE = (
    "# CRITERIO DE GRADUACIÓN (definido ANTES de ver datos; no post-hoc): el ajuste por CONTEXTO\n"
    "# pasa de SOMBRA a producción SOLO si, sobre N>=20 PARTIDOS de escenario NO TRIVIAL, BATE al\n"
    "# L3 puro en logloss Y brier (1X2). Si no, se queda en sombra.\n"
    "# NOTA HONESTA: en un solo torneo la muestra de escenarios no triviales será probablemente\n"
    "# <20 -> se quedará en sombra (resultado VÁLIDO, no un fallo). Los multiplicadores son\n"
    "# HIPÓTESIS explícitas (signo ambiguo), no verdades; el scorecard es el único juez.\n"
)


def cmd_scorecard():
    log = _read_log()
    lines = [GRADUATION_NOTE, "=" * 78,
             "CONTEXT-ADJUSTMENT — context-adjusted VS pure L3 (SOMBRA · heurístico · NO validado)",
             "=" * 78, f"generated_at_utc: {_now_iso()}"]
    settled = log[log["settled"].fillna(0).astype(int) == 1].copy() if len(log) else log
    settled = settled[settled["result_1x2"].isin(["H", "D", "A"])].copy() if len(settled) else settled
    # ONLY non-trivial scenarios (where the adjustment actually changes the prediction)
    nt = settled[pd.to_numeric(settled["nontrivial"], errors="coerce").fillna(0).astype(int) == 1] \
        if len(settled) else settled
    n = len(nt)
    n_triv = len(settled) - n
    lines.append(f"partidos liquidados (total)={len(settled)} | con escenario NO trivial={n} | "
                 f"triviales (sin cambio, excluidos)={n_triv} | umbral graduación N>={SMALL_N}")
    if n < SMALL_N:
        lines.append(f"MUESTRA INSUFICIENTE para graduar (N<{SMALL_N}). Métricas orientativas; sigue en SOMBRA.")
    lines.append("")
    if n == 0:
        lines.append("Aún sin partidos de escenario no trivial liquidados; el scorecard se llenará tras los FT.")
        # scenario breakdown of what's been logged so far (even unsettled) for visibility
        if len(log):
            br = pd.to_numeric(log["nontrivial"], errors="coerce").fillna(0).astype(int)
            lines.append(f"(log: {len(log)} filas, {int(br.sum())} no triviales pendientes de resolver)")
        SCORECARD.write_text("\n".join(lines), encoding="utf-8")
        print(f"context_shadow scorecard: non-trivial settled=0 -> {SCORECARD.name}")
        return

    res_idx = {"H": 0, "D": 1, "A": 2}
    y = nt["result_1x2"].map(res_idx).to_numpy(int)
    Y = np.eye(3)[y]
    L3 = nt[["l3_home", "l3_draw", "l3_away"]].to_numpy(float)
    CX = nt[["ctx_home", "ctx_draw", "ctx_away"]].to_numpy(float)
    ok = ~(np.isnan(L3).any(1) | np.isnan(CX).any(1))
    L3, CX, Y = L3[ok], CX[ok], Y[ok]
    nn = len(Y)

    ll_l3, ll_cx = _logloss_multi(L3, Y), _logloss_multi(CX, Y)
    br_l3, br_cx = _brier_multi(L3, Y), _brier_multi(CX, Y)
    ac_l3, ac_cx = _acc_multi(L3, Y), _acc_multi(CX, Y)

    lines.append("--- 1X2 (multiclase H/D/A) sobre escenarios NO triviales ---")
    hdr = f"  {'modelo':16} {'n':>4} {'logloss':>8} {'brier':>7} {'acc%':>6}"
    lines.append(hdr); lines.append("  " + "-" * (len(hdr) - 2))
    lines.append(f"  {'L3 puro':16} {nn:>4} {ll_l3:>8.4f} {br_l3:>7.4f} {ac_l3*100:>6.1f}")
    lines.append(f"  {'context-adj':16} {nn:>4} {ll_cx:>8.4f} {br_cx:>7.4f} {ac_cx*100:>6.1f}")
    beats = (ll_cx < ll_l3) and (br_cx < br_l3)
    lines.append(f"  Δ(L3 − ctx): logloss {ll_l3-ll_cx:+.4f} · brier {br_l3-br_cx:+.4f} "
                 f"-> ctx {'BATE' if beats else 'NO bate'} a L3 (1X2)")
    lines.append("")

    # OU 2.5 (binary) — derived Poisson bet
    gh = nt["result_ft_gh"].to_numpy(float)[ok]; ga = nt["result_ft_ga"].to_numpy(float)[ok]
    real_over = ((gh + ga) >= 3).astype(int)
    o_l3 = nt["l3_over25"].to_numpy(float)[ok]; o_cx = nt["ctx_over25"].to_numpy(float)[ok]
    om = ~(np.isnan(o_l3) | np.isnan(o_cx))
    lines.append("--- Over 2.5 (binario, Poisson xG) sobre escenarios NO triviales ---")
    if om.sum():
        lines.append(f"  real Over={real_over[om].mean()*100:.0f}% (n={int(om.sum())})")
        lines.append(f"  {'L3 puro':16} logloss {_bin_logloss(o_l3[om], real_over[om]):.4f} · "
                     f"brier {_bin_brier(o_l3[om], real_over[om]):.4f}")
        lines.append(f"  {'context-adj':16} logloss {_bin_logloss(o_cx[om], real_over[om]):.4f} · "
                     f"brier {_bin_brier(o_cx[om], real_over[om]):.4f}")
    else:
        lines.append("  sin Over2.5 utilizable.")
    lines.append("")

    # scenario breakdown (counts) so we see WHERE the non-trivial sample comes from
    lines.append("--- recuento por escenario (filas no triviales liquidadas) ---")
    tags = pd.concat([nt["scenario_home"], nt["scenario_away"]]).value_counts()
    for tag, cnt in tags.items():
        if MULT.get(str(tag), 1.0) != 1.0:
            lines.append(f"  {str(tag):16} {int(cnt)}")
    lines.append("")

    verdict = ("GRADÚA (cumple criterio)" if (beats and nn >= SMALL_N)
               else f"SIGUE EN SOMBRA (no cumple: {'N<20' if nn < SMALL_N else 'no bate L3'})")
    lines.append(f"VEREDICTO: {verdict}.")
    lines.append("  (NO se aplica nada automáticamente; los multiplicadores son hipótesis, muestra pequeña.)")
    SCORECARD.write_text("\n".join(lines), encoding="utf-8")
    print(f"context_shadow scorecard: non-trivial settled={nn} | ctx beats L3={beats} -> {SCORECARD.name}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="World Cup qualification-context adjustment (SHADOW).")
    ap.add_argument("cmd", choices=["predict", "settle", "scorecard"])
    a = ap.parse_args()
    {"predict": cmd_predict, "settle": cmd_settle, "scorecard": cmd_scorecard}[a.cmd]()
