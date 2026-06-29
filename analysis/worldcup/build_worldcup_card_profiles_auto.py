"""
WORLD CUP 2026 — AUTO CARD-DISCIPLINE PROFILES from REAL events (Fase 4F). READ-ONLY inputs · NO API ·
NO scraping · NO web · NO market/odds/betting · NO fabrication · NO secrets · NO commit. Pure football.

Derives per-PLAYER, per-TEAM and per-POSITION card (discipline) profiles using ONLY data the World Cup
product already captured:
  * analysis/worldcup/worldcup_fixture_events.csv  -> real cards per fixture/team/player (Fase 2)
  * data/external/player_positional_profiles.csv   -> player_id -> position (GK/DEF/MID/FWD)
  * data/external/fixture_referees.csv             -> (availability note only)
  * analysis/worldcup/worldcup_referee_profiles_auto.csv -> (availability note only; the referee
    dimension is combined per-fixture by card_risk_adjuster, not baked into these profiles)

NO new API calls, NO scraping, NO invented numbers. Tiny samples are flagged with low confidence and an
explicit "do not extrapolate" reason — never a hard percentage dressed up as reliable. A player WITH a
sample but WITHOUT cards is NOT assumed to be a hard zero-risk: it is marked low / insufficient sample.

Outputs (generated artifacts — NOT data/external; the manual tables stay manual & blocked):
  * analysis/worldcup/worldcup_card_profiles_auto.csv   (player-level table)
  * analysis/worldcup/worldcup_card_profiles_auto.json  ({meta, players, teams, positions})
  * analysis/worldcup/worldcup_card_profiles_auto_report.txt

Run:  python analysis/worldcup/build_worldcup_card_profiles_auto.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "analysis" / "players"))

import player_data_adapters as adapters  # noqa: E402

FIXTURE_EVENTS = HERE / "worldcup_fixture_events.csv"
FIXTURE_REFEREES = ROOT / "data" / "external" / "fixture_referees.csv"
REFEREE_AUTO = HERE / "worldcup_referee_profiles_auto.csv"
OUT_CSV = HERE / "worldcup_card_profiles_auto.csv"
OUT_JSON = HERE / "worldcup_card_profiles_auto.json"
OUT_TXT = HERE / "worldcup_card_profiles_auto_report.txt"

SOURCE = "worldcup_events_auto"

# card_type strings the Fase-2 extractor emits — never guessed.
YELLOW = "Yellow Card"
RED = "Red Card"
SECOND_YELLOW = "Second Yellow card"

# qualitative thresholds (LABELS only — never a number presented as a bet/edge). Conservative for the
# short tournament samples. Player rate = yellow cards per appearance.
PLAYER_HIGH_PG = 0.50
PLAYER_LOW_PG = 0.20
# Team rate = the team's OWN cards per match (cards_for_pg).
TEAM_HIGH_PG = 1.80
TEAM_LOW_PG = 0.90
# Position label is RELATIVE to the mean across the observed positions (avoids hard-coding a per-game
# number that depends on how many positions exist).
POS_HIGH_RATIO = 1.25
POS_LOW_RATIO = 0.75
POS_MIN_CARDS = 4          # below this a position label stays low-confidence

CSV_COLUMNS = [
    "player_id", "player_name", "team_id", "team_name", "position", "matches_sample",
    "yellow_cards_total", "red_cards_total", "second_yellow_total", "cards_total",
    "yellow_cards_pg", "red_cards_pg", "cards_pg", "card_risk_player_history",
    "data_quality", "confidence", "reason", "source",
]

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


# ============================================================ loaders (soft-failing, no fabrication)
def load_events(path=FIXTURE_EVENTS):
    """The real per-fixture events table (Fase 2). None when absent/empty."""
    p = Path(path)
    if not p.exists():
        return None
    try:
        df = pd.read_csv(p)
    except Exception:
        return None
    return df if len(df) else None


def load_positions(path=None):
    """{player_id: position} from the positional profiles (GK/DEF/MID/FWD). {} if absent."""
    pos_map, _reason = (adapters.load_positional_profiles() if path is None
                        else adapters.load_positional_profiles(path))
    out = {}
    for pid, d in (pos_map or {}).items():
        pos = (d.get("position") or "").strip().upper()
        if pos:
            try:
                out[int(pid)] = pos
            except Exception:
                continue
    return out


def _availability_note(path) -> str:
    p = Path(path)
    if not p.exists():
        return "no generado"
    try:
        df = pd.read_csv(p)
        return f"{len(df)} filas"
    except Exception:
        return "ilegible"


# ============================================================ confidence / quality ladders
def confidence_for(matches: int) -> str:
    if matches <= 0:
        return "no determinado"
    if matches == 1:
        return "baja"
    if matches <= 3:
        return "media-baja"
    if matches <= 5:
        return "media"
    return "alta"


def data_quality_for(matches: int) -> str:
    if matches <= 0:
        return "baja"
    if matches >= 6:
        return "alta"
    if matches >= 4:
        return "media"
    return "baja"


def _r(v, nd=3):
    return None if v is None else round(float(v), nd)


def classify_card_type(ctype: str):
    """Map a raw card_type string to (yellow, red, second_yellow) counts. NEVER guesses beyond the
    known strings: anything flagged as a card that is not red/second-yellow counts as a yellow."""
    c = (ctype or "").strip().lower()
    if "second yellow" in c:
        return 0, 0, 1
    if c == RED.lower() or c == "red card":
        return 0, 1, 0
    return 1, 0, 0


def card_counts(e):
    """(yellow, red, second_yellow) for an event row. ONLY is_card==1 rows count — guards against
    str(NaN)=='nan' false positives on non-card rows (goals/subs). Blank type on a card -> yellow."""
    if int(e.get("is_card") or 0) != 1:
        return 0, 0, 0
    ct = e.get("card_type")
    ct = "" if (ct is None or (isinstance(ct, float) and pd.isna(ct))) else str(ct)
    return classify_card_type(ct)


# ============================================================ player profiles (§2)
def player_history_label(matches: int, cards_total: int, cards_pg) -> str:
    """bajo / medio / alto / no determinado. A sample WITHOUT cards is 'bajo' (low confidence), never a
    hard zero (spec §2). No sample -> 'no determinado'."""
    if matches <= 0:
        return "no determinado"
    if cards_total == 0:
        return "bajo"                       # muestra sin tarjetas — NO riesgo cero fuerte
    if cards_pg is None:
        return "no determinado"
    if matches == 1:
        return "medio"                      # 1 partido con tarjeta NO es tendencia -> tope 'medio'
    if cards_pg >= PLAYER_HIGH_PG:
        return "alto"
    if cards_pg <= PLAYER_LOW_PG:
        return "bajo"
    return "medio"


def _player_reason(matches: int, cards_total: int) -> str:
    if matches <= 0:
        return "jugador sin partidos con eventos reales todavía; no extrapolar"
    if cards_total == 0:
        return f"{matches} partido(s) con eventos, sin tarjetas — muestra insuficiente, no asumir riesgo cero"
    if matches == 1:
        return "solo 1 partido con eventos, no extrapolar fuerte"
    if matches <= 3:
        return f"{matches} partidos con eventos reales — muestra reducida, orientativo"
    if matches <= 5:
        return f"{matches} partidos con eventos reales — muestra media"
    return f"{matches} partidos con eventos reales — muestra suficiente"


def derive_player_profiles(events_df, pos_map=None) -> list:
    """Per-player discipline profile from REAL events. matches_sample = distinct fixtures the player
    appears in (a floor for appearances; documented). NEVER fabricates."""
    pos_map = pos_map or {}
    if events_df is None or not len(events_df):
        return []

    # appearances (distinct fixtures with any event) + card tallies, indexed by player_id
    appear = {}            # pid -> set(fixture_id)
    meta = {}              # pid -> {player_name, team_id, team_name}
    yel = {}; red = {}; sec = {}
    for _, e in events_df.iterrows():
        try:
            pid = int(e.get("player_id"))
        except Exception:
            continue
        try:
            fid = int(e.get("fixture_id"))
        except Exception:
            fid = None
        if fid is not None:
            appear.setdefault(pid, set()).add(fid)
        m = meta.setdefault(pid, {"player_name": None, "team_id": None, "team_name": None})
        if m["player_name"] is None and isinstance(e.get("player_name"), str):
            m["player_name"] = e.get("player_name")
        if m["team_id"] is None and pd.notna(e.get("team_id")):
            try:
                m["team_id"] = int(e.get("team_id"))
            except Exception:
                pass
        if m["team_name"] is None and isinstance(e.get("team_name"), str):
            m["team_name"] = e.get("team_name")
        y, r, s = card_counts(e)
        if y or r or s:
            yel[pid] = yel.get(pid, 0) + y
            red[pid] = red.get(pid, 0) + r
            sec[pid] = sec.get(pid, 0) + s

    profiles = []
    for pid in sorted(appear):
        matches = len(appear[pid])
        y, r, s = yel.get(pid, 0), red.get(pid, 0), sec.get(pid, 0)
        cards_total = y + r + s
        cards_pg = (cards_total / matches) if matches else None
        yel_pg = (y / matches) if matches else None
        red_pg = ((r + s) / matches) if matches else None
        m = meta.get(pid, {})
        profiles.append({
            "player_id": pid,
            "player_name": m.get("player_name"),
            "team_id": m.get("team_id"),
            "team_name": m.get("team_name"),
            "position": pos_map.get(pid),
            "matches_sample": matches,
            "yellow_cards_total": y,
            "red_cards_total": r,
            "second_yellow_total": s,
            "cards_total": cards_total,
            "yellow_cards_pg": _r(yel_pg),
            "red_cards_pg": _r(red_pg),
            "cards_pg": _r(cards_pg),
            "card_risk_player_history": player_history_label(matches, cards_total, cards_pg),
            "data_quality": data_quality_for(matches),
            "confidence": confidence_for(matches),
            "reason": _player_reason(matches, cards_total),
            "source": SOURCE,
        })
    return profiles


# ============================================================ team profiles (§3)
def team_environment_label(matches: int, cards_for_pg) -> str:
    if matches <= 0 or cards_for_pg is None:
        return "no determinado"
    if cards_for_pg >= TEAM_HIGH_PG:
        return "alto"
    if cards_for_pg <= TEAM_LOW_PG:
        return "bajo"
    return "medio"


def _team_reason(matches: int) -> str:
    if matches <= 0:
        return "equipo sin partidos con eventos reales todavía; no extrapolar"
    if matches == 1:
        return "solo 1 partido con eventos, no extrapolar fuerte"
    if matches <= 3:
        return f"{matches} partidos con eventos reales — muestra reducida, orientativo"
    return f"{matches} partidos con eventos reales — muestra usable"


def derive_team_profiles(events_df) -> list:
    """Per-team discipline profile. cards_for = the team's OWN cards; cards_against = the opponent's
    cards in the same fixtures (derived from team_id vs opponent_id). NEVER fabricates."""
    if events_df is None or not len(events_df):
        return []

    fixture_teams = {}     # fid -> set(team_id)
    team_names = {}        # team_id -> name
    cards_in_fix = {}      # (fid, team_id) -> {y,r,s}
    for _, e in events_df.iterrows():
        try:
            fid = int(e.get("fixture_id"))
        except Exception:
            continue
        for id_col, nm_col in (("team_id", "team_name"), ("opponent_id", "opponent_name")):
            if pd.notna(e.get(id_col)):
                try:
                    tid = int(e.get(id_col))
                except Exception:
                    continue
                fixture_teams.setdefault(fid, set()).add(tid)
                if isinstance(e.get(nm_col), str) and tid not in team_names:
                    team_names[tid] = e.get(nm_col)
        y, r, s = card_counts(e)
        if (y or r or s) and pd.notna(e.get("team_id")):
            try:
                tid = int(e.get("team_id"))
            except Exception:
                tid = None
            if tid is not None:
                d = cards_in_fix.setdefault((fid, tid), {"y": 0, "r": 0, "s": 0})
                d["y"] += y; d["r"] += r; d["s"] += s

    team_fixtures = {}     # team_id -> set(fid)
    for fid, teams in fixture_teams.items():
        for tid in teams:
            team_fixtures.setdefault(tid, set()).add(fid)

    profiles = []
    for tid in sorted(team_fixtures):
        fixtures = sorted(team_fixtures[tid])
        matches = len(fixtures)
        y = r = s = 0
        against = 0
        for fid in fixtures:
            d = cards_in_fix.get((fid, tid))
            if d:
                y += d["y"]; r += d["r"]; s += d["s"]
            others = [t for t in fixture_teams.get(fid, set()) if t != tid]
            for ot in others:
                od = cards_in_fix.get((fid, ot))
                if od:
                    against += od["y"] + od["r"] + od["s"]
        cards_for = y + r + s
        cards_for_pg = (cards_for / matches) if matches else None
        cards_against_pg = (against / matches) if matches else None
        profiles.append({
            "team_id": tid,
            "team_name": team_names.get(tid),
            "matches_sample": matches,
            "yellow_cards_total": y,
            "red_cards_total": r + s,
            "cards_total": cards_for,
            "cards_pg": _r(cards_for_pg),
            "cards_for_pg": _r(cards_for_pg),
            "cards_against_pg": _r(cards_against_pg),
            "card_environment_team": team_environment_label(matches, cards_for_pg),
            "data_quality": data_quality_for(matches),
            "confidence": confidence_for(matches),
            "reason": _team_reason(matches),
            "source": SOURCE,
        })
    return profiles


# ============================================================ position profiles (§4)
def derive_position_profiles(events_df, pos_map) -> list:
    """Per-position card aggregation. cards_pg = cards of that position per OBSERVED fixture (same
    denominator for all positions -> comparable). Labels are RELATIVE to the cross-position mean.
    Only positions with a real mapping are produced; fine positions are never invented."""
    if events_df is None or not len(events_df) or not pos_map:
        return []
    total_fixtures = events_df["fixture_id"].nunique() if "fixture_id" in events_df.columns else 0
    cards_by_pos = {}
    for _, e in events_df.iterrows():
        y, r, s = card_counts(e)
        if not (y or r or s):
            continue
        try:
            pid = int(e.get("player_id"))
        except Exception:
            continue
        pos = pos_map.get(pid)
        if not pos:
            continue
        cards_by_pos[pos] = cards_by_pos.get(pos, 0) + y + r + s

    if not cards_by_pos or not total_fixtures:
        return []
    pg_by_pos = {p: c / total_fixtures for p, c in cards_by_pos.items()}
    # baseline = mean across positions with a usable sample only (a 1-card GK must not drag the mean).
    usable = [pg_by_pos[p] for p, c in cards_by_pos.items() if c >= POS_MIN_CARDS]
    mean_pg = (sum(usable) / len(usable)) if usable else 0.0

    profiles = []
    for pos in sorted(cards_by_pos):
        cards = cards_by_pos[pos]
        pg = pg_by_pos[pos]
        if cards < POS_MIN_CARDS:
            label, conf = "no determinado", "baja"
            reason = f"{cards} tarjeta(s) en posición {pos} — muestra insuficiente, no extrapolar"
        elif mean_pg <= 0:
            label, conf = "no determinado", "baja"
            reason = "sin base comparativa entre posiciones"
        elif pg >= POS_HIGH_RATIO * mean_pg:
            label, conf = "alto", "media"
            reason = f"{cards} tarjetas; ritmo por encima de la media de posiciones (orientativo)"
        elif pg <= POS_LOW_RATIO * mean_pg:
            label, conf = "bajo", "media"
            reason = f"{cards} tarjetas; ritmo por debajo de la media de posiciones (orientativo)"
        else:
            label, conf = "medio", "media"
            reason = f"{cards} tarjetas; en la media de posiciones (orientativo)"
        profiles.append({
            "position": pos,
            "matches_sample": int(total_fixtures),
            "cards_total": cards,
            "cards_pg": _r(pg),
            "card_risk_position": label,
            "confidence": conf,
            "reason": reason,
            "source": SOURCE,
        })
    return profiles


# ============================================================ rendering / I/O
def render_txt(players, teams, positions, notes) -> str:
    L = ["===== WORLD CUP — PERFILES AUTO DE TARJETAS (eventos reales · Fase 4F) =====", "",
         f"Jugadores con perfil: {len(players)}",
         f"Equipos con perfil:   {len(teams)}",
         f"Posiciones con perfil: {len(positions)}",
         f"Árbitros (fixture_referees): {notes.get('fixture_referees')} · "
         f"perfiles árbitro auto: {notes.get('referee_auto')}", ""]
    L.append("-- POSICIONES --")
    for p in sorted(positions, key=lambda x: (-x["cards_total"], x["position"])):
        L.append(f"  {p['position']:4s} tarjetas={p['cards_total']} cards_pg={p['cards_pg']} "
                 f"-> riesgo {p['card_risk_position']} (conf {p['confidence']})")
    L.append("")
    L.append("-- EQUIPOS (top por cards_pg) --")
    for t in sorted(teams, key=lambda x: (-(x['cards_pg'] or 0), x['team_name'] or ""))[:16]:
        L.append(f"  {str(t['team_name'])[:22]:22s} m={t['matches_sample']} "
                 f"cards_for_pg={t['cards_for_pg']} vs_pg={t['cards_against_pg']} "
                 f"-> entorno {t['card_environment_team']} (conf {t['confidence']})")
    L.append("")
    L.append("-- JUGADORES (top por cards_pg, muestra>=2) --")
    top = [p for p in players if p["matches_sample"] >= 2]
    for p in sorted(top, key=lambda x: (-(x['cards_pg'] or 0), x['player_name'] or ""))[:20]:
        L.append(f"  {str(p['player_name'])[:22]:22s} ({str(p['team_name'])[:14]:14s}) "
                 f"pos={p['position'] or '—'} m={p['matches_sample']} cards={p['cards_total']} "
                 f"cards_pg={p['cards_pg']} -> {p['card_risk_player_history']} (conf {p['confidence']})")
    L.append("")
    L.append("Predicción futbolística pura, sin terminología de juego. NO toca data/external. Muestras "
             "pequeñas -> confidence baja; un jugador sin tarjetas con muestra NO es riesgo cero.")
    return "\n".join(L)


def build(events_path=FIXTURE_EVENTS, positions_path=None, out_csv=OUT_CSV, out_json=OUT_JSON,
          out_txt=OUT_TXT, write=True):
    events = load_events(events_path)
    pos_map = load_positions(positions_path)
    players = derive_player_profiles(events, pos_map)
    teams = derive_team_profiles(events)
    positions = derive_position_profiles(events, pos_map)
    notes = {"fixture_referees": _availability_note(FIXTURE_REFEREES),
             "referee_auto": _availability_note(REFEREE_AUTO)}
    payload = {
        "meta": {"source": SOURCE, "players": len(players), "teams": len(teams),
                 "positions": len(positions),
                 "note": "matches_sample de jugador = nº de fixtures con eventos del jugador (cota "
                         "inferior de apariciones); muestras pequeñas -> confidence baja."},
        "players": players, "teams": teams, "positions": positions,
    }
    if write:
        pd.DataFrame(players, columns=CSV_COLUMNS).to_csv(out_csv, index=False)
        Path(out_json).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        Path(out_txt).write_text(render_txt(players, teams, positions, notes) + "\n", encoding="utf-8")
    return payload


def main():
    payload = build()
    m = payload["meta"]
    print(f"card profiles auto: {m['players']} jugadores · {m['teams']} equipos · "
          f"{m['positions']} posiciones -> {OUT_CSV.name} / {OUT_JSON.name}")
    for p in sorted(payload["positions"], key=lambda x: -x["cards_total"]):
        print(f"  pos {p['position']:4s} cards={p['cards_total']} pg={p['cards_pg']} "
              f"-> {p['card_risk_position']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
