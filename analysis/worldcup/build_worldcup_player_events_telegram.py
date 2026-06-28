"""
WORLD CUP 2026 — PLAYER-EVENTS Telegram report (§13). READ-ONLY · NO API · NO market/odds · NO betting.

Turns worldcup_player_events.json (built by build_worldcup_player_events.py) into a PURE FOOTBALL
prediction message per fixture: result probabilities, likely score, top scorers / shots-on-target /
assisters, set-piece takers, card risk, expected team stats, probable match script, and honest
confidence / uncertainty / data warnings. NO betting language whatsoever (asserted at build time).

Output: worldcup_player_events_msg_<i>.txt + worldcup_player_events_messages_manifest.txt (one
'path|title' per line, consumed by the shared dispatcher — NOT modified here).

Run:  python analysis/worldcup/build_worldcup_player_events_telegram.py
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
EVENTS_JSON = HERE / "worldcup_player_events.json"
MANIFEST = HERE / "worldcup_player_events_messages_manifest.txt"
COMBINED = HERE / "worldcup_player_events_full.txt"

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# words that would turn this into a betting message — must NEVER appear (spec §13)
FORBIDDEN = ["apuesta", "apostar", "cuota", "odds", "edge", "pick", "stake", "roi", "mercado",
             "value bet", "valor esperado de apuesta", "bookie", "casa de apuestas"]


def assert_no_betting_language(text: str):
    low = text.lower()
    hits = [w for w in FORBIDDEN if w in low]
    if hits:
        raise AssertionError(f"betting language leaked into player-events message: {hits}")


def _pct(x):
    return "—" if x is None else f"{float(x)*100:.0f}%"


def _f1(x):
    return "—" if x is None else f"{float(x):.1f}"


def match_script(tc):
    """Honest probable script from OUR OWN numbers (1X2 + total xG). Not external/fabricated."""
    ph, pa = tc.get("p_home"), tc.get("p_away")
    xh, xa = tc.get("xg_home"), tc.get("xg_away")
    total = (float(xh) + float(xa)) if (xh is not None and xa is not None) else None
    parts = []
    if ph is not None and pa is not None:
        if float(ph) - float(pa) >= 0.25:
            parts.append("dominio del local")
        elif float(pa) - float(ph) >= 0.25:
            parts.append("dominio del visitante")
        else:
            parts.append("partido igualado")
    if total is not None:
        parts.append("ida y vuelta (mucho gol esperado)" if total >= 2.9
                     else ("bloque bajo (poco gol esperado)" if total <= 2.1 else "ritmo intermedio"))
    return " · ".join(parts) if parts else "sin guion (datos insuficientes)"


def _set_piece_line(label, side):
    p = side.get("primary")
    if not p:
        return f"  {label}: no determinado ({side.get('confidence', 'baja')})"
    s = f" / 2º {side['secondary']}" if side.get("secondary") else ""
    extra = ""
    if side.get("primary_count"):
        extra += f" · {side['primary_count']} lanzamiento(s)"
    last = side.get("primary_last")
    if isinstance(last, dict) and last.get("date"):
        scored = last.get("scored")
        mark = "" if scored is None else (" ✓" if scored else " ✗")
        extra += f" · último {last['date']}{mark}"
    return f"  {label}: {p}{s} ({side.get('confidence')}){extra}"


# ----- Fase 3 source labels (clearly state real xG/xA vs proxy; NO betting language) -----
_REAL_TAG = "datos reales (xG/xA)"
_PROXY_TAG = "estimación (proxy del modelo)"


def _fixture_uses_real(obj):
    """True iff a SHOWN ranked player in this fixture actually used real xG/xA (player_xg_xa.csv). A
    headers-only template -> no player gets real data -> False (we never claim 'real' without it)."""
    pp = obj.get("player_predictions", {})
    for cat in ("likely_scorers", "likely_shots_on_target", "likely_assisters"):
        for it in pp.get(cat, []) or []:
            if it.get("source_used") == "real_xg_xa":
                return True
    return False


def _src_mark(it):
    """A compact per-player tag: ✓real when that player used real data, else nothing (proxy is default)."""
    return " ·real" if it.get("source_used") == "real_xg_xa" else ""


def render_fixture(obj):
    f = obj["fixture"]
    tc = obj.get("team_context", {})
    pp = obj["player_predictions"]
    L = []
    L.append(f"⚽ {f['home']} vs {f['away']}")
    L.append(f"🏆 Mundial 2026 · {f.get('round','')} · 🕒 {f.get('kickoff_utc','')} UTC")
    L.append(f"📊 Resultado: V {_pct(tc.get('p_home'))} · E {_pct(tc.get('p_draw'))} · "
             f"D {_pct(tc.get('p_away'))}")
    L.append(f"🔮 Marcador más probable: {tc.get('top_score','—')}  "
             f"(goles esp. {_f1(tc.get('xg_home'))}-{_f1(tc.get('xg_away'))})")
    L.append(f"🎯 Tiros a puerta esp.: {f['home']} {_f1(tc.get('exp_sot_home'))} · "
             f"{f['away']} {_f1(tc.get('exp_sot_away'))}")
    L.append(f"🚩 Córners esp.: {_f1(tc.get('exp_corners_total'))}  ·  "
             f"🟨 Tarjetas esp.: {_f1(tc.get('exp_cards_total'))}")
    # Fase 3 — model source (real xG/xA vs proxy)
    uses_real = _fixture_uses_real(obj)
    L.append(f"🧪 Fuente del modelo de jugador: {_REAL_TAG if uses_real else _PROXY_TAG}")
    L.append("")
    sc = pp["likely_scorers"]
    L.append("🥅 Más probables para marcar:")
    L += [f"  {i+1}. {s['player']} ({s['team']}) — {_pct(s['probability_goal'])} · "
          f"xG {s['expected_goals']}{_src_mark(s)}"
          for i, s in enumerate(sc)] or ["  — datos insuficientes —"]
    so = pp["likely_shots_on_target"]
    L.append("🎯 Más probables para tirar a puerta:")
    L += [f"  {i+1}. {s['player']} ({s['team']}) — 1+ a puerta {_pct(s['probability_1_sot'])} "
          f"(SOT esp. {s['expected_sot']}){_src_mark(s)}" for i, s in enumerate(so)] \
        or ["  — datos insuficientes —"]
    asst = pp["likely_assisters"]
    L.append("🅰️ Más probables para asistir:")
    L += [f"  {i+1}. {s['player']} ({s['team']}) — {_pct(s['probability_assist'])}{_src_mark(s)}"
          for i, s in enumerate(asst)] or ["  — datos insuficientes —"]
    L.append("")
    L.append("🎯 Balón parado:")
    spk = pp["set_piece_takers"]
    for side_label, side in (("Local", spk.get("home", {})), ("Visitante", spk.get("away", {}))):
        L.append(f" {side_label} ({f['home'] if side_label=='Local' else f['away']}):")
        pen = side.get("penalties", {})
        L.append(_set_piece_line("Penaltis", pen))
        if pen.get("primary") and pen.get("if_primary_absent"):
            L.append(f"    ↪ {pen['if_primary_absent']}")
        L.append(_set_piece_line("Faltas directas", side.get("direct_free_kicks", {})))
        L.append(_set_piece_line("Córners", side.get("corners_left", {})))
    cr = pp["card_risk"]
    if cr:
        L.append("🟨 Riesgo de tarjeta:")
        L += [f"  {c['player']} ({c['team']}) — {_pct(c['probability_card'])}" for c in cr]
    L.append("")

    # ---- Fase 3 — árbitro (§5) ----
    rc = obj.get("referee_context") or {}
    if rc.get("referee_name"):
        L.append(f"🧑‍⚖️ Árbitro: {rc['referee_name']} — entorno de tarjetas: "
                 f"{rc.get('expected_card_environment','—')} (conf. {rc.get('confidence','baja')})")
        if rc.get("possible_penalty_environment") and rc["possible_penalty_environment"] != "no determinado":
            L.append(f"   Penaltis: {rc['possible_penalty_environment']}")

    # ---- Fase 3 — clima (§6) ----
    wx = obj.get("weather_context") or {}
    if wx.get("weather_summary") and wx["weather_summary"] != "no determinado":
        L.append(f"🌦️ Clima: {wx['weather_summary']} (conf. {wx.get('confidence','baja')})")
        if wx.get("extreme"):
            impacts = [v for v in (wx.get("impact_on_tempo"), wx.get("impact_on_shots"),
                                   wx.get("impact_on_crosses"), wx.get("impact_on_fatigue"))
                       if v and v != "neutro"]
            if impacts:
                L.append("   Impacto: " + " · ".join(dict.fromkeys(impacts)))

    # ---- Fase 3 — estilo del seleccionador (§7) ----
    txc = obj.get("tactical_context") or {}
    hs, as_ = txc.get("home_style") or {}, txc.get("away_style") or {}
    if (hs.get("style") and "no determinado" not in hs["style"]) or \
       (as_.get("style") and "no determinado" not in as_["style"]):
        L.append("🧠 Estilo (perfil externo):")
        if hs.get("style"):
            L.append(f"   {f['home']}: {hs['style']}")
        if as_.get("style"):
            L.append(f"   {f['away']}: {as_['style']}")
        if txc.get("expected_match_script"):
            L.append(f"   Guion táctico: {txc['expected_match_script']}")

    # ---- Fase 3 — 3 matchups clave (§8) ----
    km = obj.get("key_matchups") or pp.get("key_matchups") or []
    real_duels = [m for m in km if not m.get("matchups_heuristic_only")
                  and m.get("player_a") and m.get("player_b")]
    if real_duels:
        L.append("⚔️ Duelos clave:")
        for m in real_duels[:3]:
            adv = m.get("advantage")
            adv_txt = f" → ventaja: {adv}" if adv and adv != "no determinado" else ""
            L.append(f"  {m['player_a']} vs {m['player_b']} ({m.get('zone','')}){adv_txt} "
                     f"[{m.get('confidence','baja')}]")

    L.append("")
    L.append(f"🎬 Guion probable: {match_script(tc)}")
    L.append(f"✅ Confianza: {obj.get('confidence','?')} · ❓ Incertidumbre/datos: {obj.get('data_quality','?')}")
    # data warnings (honest)
    warns = []
    if not uses_real:
        warns.append("sin xG/xA real por jugador (goles/tiros/asistencias = proxy del modelo)")
    if not spk.get("home", {}).get("penalties", {}).get("primary") \
            and not spk.get("away", {}).get("penalties", {}).get("primary"):
        warns.append("lanzadores de penalti no determinados (sin eventos reales ni set_piece_takers.csv)")
    if not spk.get("home", {}).get("direct_free_kicks", {}).get("primary"):
        warns.append("faltas/córners no disponibles (requiere set_piece_takers.csv · Fase 3)")
    ext = obj.get("external_data_status", {})
    if not ext.get("referee_available") or not rc.get("referee_name"):
        warns.append("sin tendencia de árbitro")
    if not ext.get("weather_available") or (wx.get("weather_summary") in (None, "no determinado")):
        warns.append("sin datos de clima")
    if not ext.get("coach_profile_available"):
        warns.append("sin perfil táctico del seleccionador")
    if not real_duels:
        warns.append("matchups solo heurísticos (faltan perfiles posicionales)")
    if warns:
        L.append("⚠️ Avisos de datos: " + " · ".join(warns))
    L.append("")
    L.append("ℹ️ Predicción futbolística pura para análisis (no es consejo de juego).")
    text = "\n".join(L)
    assert_no_betting_language(text)
    return text


def main(events_json=EVENTS_JSON):
    if not Path(events_json).exists():
        print("player-events telegram: no hay worldcup_player_events.json (soft).")
        MANIFEST.write_text("", encoding="utf-8")
        return 0
    data = json.loads(Path(events_json).read_text(encoding="utf-8"))
    # only fixtures that actually have at least one ranked player (no empty spam)
    data = [o for o in data if o["player_predictions"]["likely_scorers"]
            or o["player_predictions"]["likely_shots_on_target"]]
    # clean stale msg files
    for fp in HERE.glob("worldcup_player_events_msg_*.txt"):
        try:
            fp.unlink()
        except Exception:
            pass
    manifest, combined = [], []
    for i, obj in enumerate(data, 1):
        text = render_fixture(obj)
        fp = HERE / f"worldcup_player_events_msg_{i}.txt"
        fp.write_text(text + "\n", encoding="utf-8")
        title = f"Predicción jugadores — {obj['fixture']['home']} vs {obj['fixture']['away']}"
        manifest.append(f"{fp}|{title}")
        combined.append(f"===== {title} =====\n{text}\n")
    MANIFEST.write_text("\n".join(manifest) + ("\n" if manifest else ""), encoding="utf-8")
    COMBINED.write_text("\n".join(combined), encoding="utf-8")
    print(f"player-events telegram: {len(data)} mensajes -> {MANIFEST.name}")
    return len(data)


if __name__ == "__main__":
    argparse.ArgumentParser(description="World Cup player-events Telegram report (no betting).").parse_args()
    main()
