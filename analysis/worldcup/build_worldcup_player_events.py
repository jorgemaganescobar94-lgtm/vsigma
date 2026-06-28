"""
WORLD CUP 2026 — PLAYER & INDIVIDUAL-EVENTS card builder (Fase 1). READ-ONLY · NO API · NO market/odds.

Glue between the existing per-player props (worldcup_player_props_log.csv, λ's frozen at KO) + the
team-level card (worldcup_cards.csv: 1X2/xG/corners/cards) and the SHARED core
(analysis/players/player_events_core.py), producing the §11 structured player_predictions output for
each upcoming fixture: likely scorers / shots-on-target / assisters, set-piece takers, card risk,
key matchups, two-XI scenario note, with honest data_quality/confidence/reason (§12). Pluggable
external sources (xA / referee / weather) via analysis/players/player_data_adapters.py — absent ->
fields None + reason, NEVER fabricated.

Output (read-only, git-add explicit):
  * worldcup_player_events.json  (list: one object per fixture, the full §11 structure + team summary)
  * worldcup_player_events.csv   (flat: one row per ranked player entry, for quick inspection)

Set-piece takers: Fase 1 reads an OPTIONAL file data/external/set_piece_history.csv
(team_id, player_id, penalties, free_kicks, corners); absent -> "no determinado" + reason (the live
/fixtures/events extractor is Fase 2). NO fabrication.

Run:  python analysis/worldcup/build_worldcup_player_events.py
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "analysis" / "players"))

import player_events_core as core  # noqa: E402
import player_data_adapters as adapters  # noqa: E402
import player_event_history as peh  # noqa: E402  (Fase 2: real per-player history aggregator)
import build_worldcup_fixture_events as fxev  # noqa: E402  (Fase 2: real events extractor)
import worldcup_learning_loop as ll  # noqa: E402  (top_scoreline only; import has no side effects)
# Fase 3 context modules (read-only, CSV-driven, no API, no betting)
import referee_context as refctx  # noqa: E402
import weather_context as wxctx  # noqa: E402
import coach_tactical_context as coachctx  # noqa: E402
import player_matchups as pmatch  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

CARDS = HERE / "worldcup_cards.csv"
PROPS_LOG = HERE / "worldcup_player_props_log.csv"
SET_PIECE_FILE = ROOT / "data" / "external" / "set_piece_history.csv"
FIXTURE_REFEREES_FILE = ROOT / "data" / "external" / "fixture_referees.csv"  # optional fixture->referee map
OUT_JSON = HERE / "worldcup_player_events.json"
OUT_CSV = HERE / "worldcup_player_events.csv"
HISTORY_CSV = HERE / "worldcup_player_event_history.csv"

# set-piece roles surfaced from set_piece_takers.csv (Fase 3), mapped to the §11 block keys
_SP_CSV_ROLE_TO_KEY = {
    "penalty": "penalties", "direct_free_kick": "direct_free_kicks",
    "indirect_free_kick": "indirect_free_kicks",
    "corner_left": "corners_left", "corner_right": "corners_right",
}


def _load_fixture_referees(path=FIXTURE_REFEREES_FILE):
    """Optional {fixture_id: referee_name} map (data/external/fixture_referees.csv). Absent -> {}.
    Lets you LINK a referee to a WC fixture (the card CSV does not carry it). NO fabrication."""
    try:
        if not Path(path).exists():
            return {}
        df = pd.read_csv(path)
    except Exception:
        return {}
    out = {}
    for _, r in df.iterrows():
        try:
            fid = int(r["fixture_id"])
        except Exception:
            continue
        name = r.get("referee_name")
        if pd.notna(name) and str(name).strip():
            out[fid] = str(name).strip()
    return out


def _csv_role_block(csv_takers_for_team, role_key, xi_set, names_by_id):
    """Build a §11-style set-piece sub-block for one role from set_piece_takers.csv (already ranked),
    restricted to players in the probable XI. Returns None if the role has no XI taker (caller falls
    back to the next source). NEVER fabricates a taker."""
    csv_role = next((r for r, k in _SP_CSV_ROLE_TO_KEY.items() if k == role_key), None)
    lst = (csv_takers_for_team or {}).get(csv_role) or []
    avail = [e for e in lst if e["player_id"] in xi_set]
    if not avail:
        return None
    primary = avail[0]
    secondary = avail[1] if len(avail) > 1 else None
    pname = primary.get("player_name") or names_by_id.get(primary["player_id"])
    sname = (secondary.get("player_name") or names_by_id.get(secondary["player_id"])) if secondary else None
    return {
        "primary": pname, "secondary": sname,
        "confidence": primary.get("confidence") or "media",
        "reason": "lanzador declarado en set_piece_takers.csv (XI probable)"
                  + (f" · {int(primary['attempts'])} intentos" if primary.get("attempts") else ""),
        "primary_count": int(primary["attempts"]) if primary.get("attempts") else None,
        "primary_last": ({"date": primary["last_taken_date"], "scored": None}
                         if primary.get("last_taken_date") else None),
        "source_priority_used": "set_piece_takers_csv",
    }


def build_set_piece_block(core_block, csv_takers_for_team, xi_set, names_by_id):
    """Apply the §4 source priority to the per-role set-piece picture:
       1) eventos reales del Mundial  2) set_piece_takers.csv  3) historial de jugador  4) no determinado.
    Penalties prefer REAL events (the core already computed them); free-kicks/corners prefer the CSV
    (events can't give them reliably), then the player-history counts, then 'no determinado'. Tags
    source_priority_used per role + at block level. NEVER fabricates a taker."""
    block = {k: (dict(v) if isinstance(v, dict) else v) for k, v in (core_block or {}).items()}
    used = []

    # PENALTIES — real WC events first (priority 1)
    pen = block.get("penalties", {}) or {}
    if pen.get("primary"):
        pen["source_priority_used"] = "eventos_reales_mundial"
        block["penalties"] = pen
        used.append("penaltis:eventos_reales")
    else:
        csv_pen = _csv_role_block(csv_takers_for_team, "penalties", xi_set, names_by_id)
        if csv_pen:
            block["penalties"] = csv_pen
            used.append("penaltis:set_piece_takers_csv")
        else:
            pen["source_priority_used"] = "no_determinado"
            block["penalties"] = pen
            used.append("penaltis:no_determinado")

    # FREE-KICKS + CORNERS — CSV (priority 2) first, else player-history counts (3), else no determinado
    for key, label in (("direct_free_kicks", "faltas"), ("corners_left", "corner_izq"),
                       ("corners_right", "corner_der")):
        csv_b = _csv_role_block(csv_takers_for_team, key, xi_set, names_by_id)
        if csv_b:
            block[key] = csv_b
            used.append(f"{label}:set_piece_takers_csv")
        elif (block.get(key) or {}).get("primary"):
            block.setdefault(key, {})["source_priority_used"] = "historial_jugador"
            used.append(f"{label}:historial_jugador")
        else:
            block.setdefault(key, {})["source_priority_used"] = "no_determinado"
            used.append(f"{label}:no_determinado")

    # INDIRECT FREE-KICKS — only available from the CSV (new §4 role)
    csv_ind = _csv_role_block(csv_takers_for_team, "indirect_free_kicks", xi_set, names_by_id)
    if csv_ind:
        block["indirect_free_kicks"] = csv_ind
        used.append("falta_indirecta:set_piece_takers_csv")

    confs = [v.get("confidence") for v in block.values()
             if isinstance(v, dict) and v.get("primary")]
    block["source_priority_used"] = "; ".join(used)
    block["confidence"] = "media" if any(c in ("alta", "media") for c in confs) else "baja"
    block["reason"] = ("prioridad de fuentes §4: eventos reales del Mundial > set_piece_takers.csv > "
                       "historial de jugador > no determinado")
    return block


def now_iso():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _load_set_piece_history(path=SET_PIECE_FILE):
    """Optional {team_id: {'penalties':{pid:ct}, 'free_kicks':{...}, 'corners':{...}}}. Absent -> {}."""
    try:
        if not Path(path).exists():
            return {}
        df = pd.read_csv(path)
    except Exception:
        return {}
    out = {}
    for _, r in df.iterrows():
        try:
            tid = int(r["team_id"]); pid = int(r["player_id"])
        except Exception:
            continue
        d = out.setdefault(tid, {"penalties": {}, "free_kicks": {}, "corners": {}})
        for col, key in (("penalties", "penalties"), ("free_kicks", "free_kicks"), ("corners", "corners")):
            if col in df.columns and pd.notna(r.get(col)):
                try:
                    d[key][pid] = float(r[col])
                except Exception:
                    pass
    return out


def _expand_side(rows, xa_map, xg_xa_map=None):
    """Expand a team's player rows. Fase 3: if xg_xa_map (player_xg_xa.csv) has the player, pass the
    REAL xg90/xa90/shots90/sot90 to the core so they REPLACE the proxy λ (flagged source_used=real_xg_xa).
    Else fall back to the Fase 1/2 xa_map (display-only xA) — proxy regime."""
    xg_xa_map = xg_xa_map or {}
    out = []
    for _, r in rows.iterrows():
        d = r.to_dict()
        pid = d.get("player_id")
        xa = key_passes = None
        real = None
        try:
            ipid = int(pid) if pid is not None and not pd.isna(pid) else None
        except Exception:
            ipid = None
        if ipid is not None and ipid in xg_xa_map:
            real = xg_xa_map[ipid]                 # full real profile -> adjusts the λ's
        if ipid is not None:
            ent = xa_map.get(ipid)
            if ent:
                xa, key_passes = ent.get("xa90"), ent.get("key_passes90")
        out.append(core.expand_player(d, xa90=xa, key_passes90=key_passes, real=real))
    return out


def _team_summary(team, attack_xg, opp_xg, corners_for, corners_against):
    dom = None
    if corners_for is not None and corners_against is not None:
        tot = corners_for + corners_against
        dom = (corners_for / tot) if tot else None
    return {"team": team, "attack_xg": attack_xg, "def_concede_proxy": opp_xg, "corner_dominance": dom}


def build():
    if not CARDS.exists() or not PROPS_LOG.exists():
        print("player-events: faltan cards o props log; nada que construir (soft).")
        OUT_JSON.write_text("[]", encoding="utf-8")
        pd.DataFrame().to_csv(OUT_CSV, index=False)
        return []
    cards = pd.read_csv(CARDS)
    props = pd.read_csv(PROPS_LOG)
    xa_map, xa_reason = adapters.load_xa_rates()
    sp_hist = _load_set_piece_history()      # optional external file (fk/corners fallback)
    status = adapters.adapters_status()

    # Fase 3 — load every external source ONCE (each degrades to {}+reason when absent/invalid).
    xg_xa_map, xg_xa_reason = adapters.load_player_xg_xa()
    sp_takers_map, sp_takers_reason = adapters.load_set_piece_takers()
    ref_profiles, ref_profiles_reason = adapters.load_referee_profiles()
    weather_map, weather_reason = adapters.load_weather_by_fixture()
    coach_map, coach_reason = adapters.load_coach_profiles()
    pos_map, pos_reason = adapters.load_positional_profiles()
    fixture_referees = _load_fixture_referees()
    ext_status = adapters.external_data_status()

    # Fase 2 — REAL event history: penalties / last taker / cards from /fixtures/events (cached store).
    events_df = fxev.extract()[fxev.COLUMNS] if True else None
    minutes_by_player = {}
    if "player_id" in props.columns and "act_minutes" in props.columns:
        mm = props.dropna(subset=["player_id"]).groupby("player_id")["act_minutes"].sum()
        minutes_by_player = {int(k): float(v) for k, v in mm.items() if pd.notna(v)}
    agg = peh.aggregate(events_df, minutes_by_player)
    real_pen_hist = agg["penalty_history"]            # GLOBAL {pid: pens_taken} from real events
    real_last_pen = agg["last_penalty"]
    ev_names = agg["names"]
    card_hist = peh.card_risk_history(agg)
    events_source = ("eventos reales (/fixtures/events)" if real_pen_hist
                     else "sin penaltis reales en eventos liquidados todavía")
    # persist the per-player real history as an inspectable artifact (§2 deliverable)
    hist_rows = []
    for pid, d in agg["players"].items():
        hist_rows.append({"player_id": pid, "player_name": d.get("player_name"),
                          "goals": d["goals"], "assists": d["assists"], "goals_per90": d["goals_per90"],
                          "pens_taken": d["pens_taken"], "pens_scored": d["pens_scored"],
                          "pens_missed": d["pens_missed"], "yellows": d["yellows"], "reds": d["reds"],
                          "goal_involvement": d["goal_involvement"], "set_piece_goals": d["set_piece_goals"],
                          "sample_fixtures": d["sample_fixtures"], "data_quality": d["data_quality"],
                          "confidence": d["confidence"], "reason": d["reason"]})
    pd.DataFrame(hist_rows).sort_values("goal_involvement", ascending=False, ignore_index=True).to_csv(
        HISTORY_CSV, index=False) if hist_rows else pd.DataFrame().to_csv(HISTORY_CSV, index=False)

    fixtures_out, flat_rows = [], []
    for _, c in cards.iterrows():
        fid = c.get("fixture_id")
        if pd.isna(fid):
            continue
        fid = int(fid)
        sub = props[pd.to_numeric(props["fixture_id"], errors="coerce") == fid]
        home, away = str(c.get("home")), str(c.get("away"))
        h_rows = sub[sub["team"].astype(str) == home]
        a_rows = sub[sub["team"].astype(str) == away]
        h_exp = _expand_side(h_rows, xa_map, xg_xa_map)
        a_exp = _expand_side(a_rows, xa_map, xg_xa_map)

        names_by_id = dict(ev_names)     # real event names first (full names), props names fill gaps
        h_ids, a_ids = [], []
        for _, r in sub.iterrows():
            try:
                pid = int(r["player_id"]); names_by_id.setdefault(pid, r["player"])
                (h_ids if str(r["team"]) == home else a_ids).append(pid)
            except Exception:
                continue
        h_tid = int(h_rows["team_id"].iloc[0]) if len(h_rows) else None
        a_tid = int(a_rows["team_id"].iloc[0]) if len(a_rows) else None
        # penalties from REAL events (global hist; core restricts to each team's XI ids). fk/corners
        # from the optional external file (events can't give them reliably). last taker for the explainer.
        sp_home = core.set_piece_hierarchy(
            h_ids, names_by_id, penalty_history=real_pen_hist, last_taken=real_last_pen,
            full_history=real_pen_hist, fk_history=sp_hist.get(h_tid, {}).get("free_kicks"),
            corner_history=sp_hist.get(h_tid, {}).get("corners"))
        sp_away = core.set_piece_hierarchy(
            a_ids, names_by_id, penalty_history=real_pen_hist, last_taken=real_last_pen,
            full_history=real_pen_hist, fk_history=sp_hist.get(a_tid, {}).get("free_kicks"),
            corner_history=sp_hist.get(a_tid, {}).get("corners"))
        # Fase 3 §4 — overlay set_piece_takers.csv with the documented source priority + tag the source.
        h_xi_set = set(h_ids); a_xi_set = set(a_ids)
        sp_home = build_set_piece_block(sp_home, sp_takers_map.get(h_tid), h_xi_set, names_by_id)
        sp_away = build_set_piece_block(sp_away, sp_takers_map.get(a_tid), a_xi_set, names_by_id)

        hx, ax = c.get("our_xg_home"), c.get("our_xg_away")
        h_sum = _team_summary(home, hx, ax, c.get("st_corners_home"), c.get("st_corners_away"))
        a_sum = _team_summary(away, ax, hx, c.get("st_corners_away"), c.get("st_corners_home"))
        team_heuristic = core.key_matchups(h_sum, a_sum)

        # Fase 3 — contexts (§5 referee, §6 weather, §7 coach/tactical, §8 individual matchups).
        ref_name = fixture_referees.get(fid)
        referee_ctx = refctx.build_referee_context(ref_name, ref_profiles, ref_profiles_reason)
        weather_ctx = wxctx.build_weather_context(fid, weather_map, weather_reason)
        tactical_ctx = coachctx.build_tactical_context(h_tid, a_tid, home, away, coach_map, coach_reason)
        h_xi = [{"player_id": pid, "player_name": names_by_id.get(pid), "team": home} for pid in h_ids]
        a_xi = [{"player_id": pid, "player_name": names_by_id.get(pid), "team": away} for pid in a_ids]
        exp_sot_total = None
        try:
            if c.get("st_shots_home") is not None and c.get("st_shots_away") is not None:
                exp_sot_total = float(c.get("st_shots_home")) + float(c.get("st_shots_away"))
        except Exception:
            exp_sot_total = None
        key_matchups = pmatch.build_matchups(
            h_xi, a_xi, positional_map=pos_map, positional_reason=pos_reason,
            home_style=tactical_ctx.get("home_style"), away_style=tactical_ctx.get("away_style"),
            team_heuristic=team_heuristic, exp_shots_total=exp_sot_total)

        meta = {"fixture_id": fid, "kickoff_utc": c.get("kickoff_utc"), "home": home, "away": away,
                "round": c.get("round")}
        obj = core.build_player_predictions(meta, h_exp, a_exp, sp_home, sp_away, key_matchups,
                                            scenarios=core.scenario_delta(h_exp + a_exp, None))
        # team-level context for the Telegram report (1X2, score, xG, corners, cards)
        obj["team_context"] = {
            "p_home": c.get("our_home"), "p_draw": c.get("our_draw"), "p_away": c.get("our_away"),
            "xg_home": hx, "xg_away": ax,
            "top_score": ll.top_scoreline(hx, ax),
            "exp_corners_total": c.get("st_corners_total"), "exp_cards_total": c.get("st_cards_total"),
            "exp_sot_home": c.get("st_shots_home"), "exp_sot_away": c.get("st_shots_away"),
        }
        # Fase 3 — external context blocks + provenance on the fixture object (§9)
        obj["external_data_status"] = ext_status
        obj["adapters_status"] = status
        obj["xa_source"] = xa_reason
        obj["xg_xa_source"] = xg_xa_reason
        obj["set_piece_source"] = sp_takers_reason
        obj["events_source"] = events_source
        obj["referee_context"] = referee_ctx
        obj["weather_context"] = weather_ctx
        obj["tactical_context"] = tactical_ctx
        # mirror matchups at the top level too (also inside player_predictions.key_matchups)
        obj["key_matchups"] = key_matchups
        fixtures_out.append(obj)

        # flat rows
        pp = obj["player_predictions"]
        for cat, items in (("scorer", pp["likely_scorers"]), ("sot", pp["likely_shots_on_target"]),
                           ("assist", pp["likely_assisters"]), ("card_risk", pp["card_risk"])):
            for it in items:
                flat_rows.append({"fixture_id": fid, "home": home, "away": away, "category": cat, **it})

    OUT_JSON.write_text(json.dumps(fixtures_out, ensure_ascii=False, indent=2, default=str),
                        encoding="utf-8")
    pd.DataFrame(flat_rows).to_csv(OUT_CSV, index=False)
    print(f"player-events: {len(fixtures_out)} fixtures -> {OUT_JSON.name} + {OUT_CSV.name} "
          f"| adapters xA={status['xa90']} ref={status['referee_card_rates']} weather={status['weather']}")
    return fixtures_out


if __name__ == "__main__":
    argparse.ArgumentParser(description="World Cup player-events card (read-only, shadow).").parse_args()
    build()
