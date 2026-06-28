"""
WORLD CUP 2026 — EXTERNAL-DATA TEMPLATE PREPARER (Fase 4A + 4B). READ-ONLY inputs · NO API · NO
scraping · NO market/odds · NO betting · NO fabrication · NO secrets.

Bootstraps AND incrementally maintains the optional data/external/*.csv contracts the player-events
module (Fase 3) consumes. Fase 4A created the templates; Fase 4B makes the pre-population INCREMENTAL
and SAFE:

  * SAFE MERGE (never destructive): existing rows are never deleted; a non-empty cell is never
    overwritten with a different value UNLESS the row was auto-derived (its `source` is one of the
    known auto sources) AND the column is an auto-owned fact (e.g. attempts, last_taken_date). Manual
    edits (any row whose source is not an auto source, or any manually-filled cell) are sacred.
  * APPEND new real rows: new penalty takers, players, fixtures that appear later are added; nothing
    that already exists is duplicated.
  * COMPLETE empty cells with real data when it becomes available (e.g. a venue that was blank).

Real-data derivations (only what the repo already holds — NO scraping, NO new sources):
  - set_piece_takers.csv   -> PENALTY takers from REAL /fixtures/events (goals + missed pens). attempts
                              aggregated per player; rank per team; last_taken_date = latest. Free-kick /
                              corner takers are NOT inferable from events -> never emitted.
                              source=api_football_events, data_quality=alta, confidence by sample.
  - player_positional_profiles.csv -> player POSITION from cached lineups: a FINE position (CB/LB/RB/
                              LWB/RWB/DM/CM/AM/LW/RW/ST/CF/GK) if a lineup source carries it, else the
                              coarse G/D/M/F -> GK/DEF/MID/FWD. roles/threats/zones stay EMPTY.
  - fixture_referees.csv   -> fixture_id+referee_name IF a referee appears in the store (none today).
  - weather_by_fixture.csv -> fixture_id+kickoff_time, plus venue IF it appears in the store. NO
                              measured temperature/wind/rain is ever invented.

player_xg_xa.csv / coach_tactical_profiles.csv / referee_profiles.csv stay EMPTY templates for manual
entry (no proxy-as-real, no invented coaches/referees).

Run:  python analysis/worldcup/prepare_worldcup_external_templates.py
"""
from __future__ import annotations

import argparse
import glob
import json
import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
EXT_DIR = ROOT / "data" / "external"
FIXTURE_EVENTS = HERE / "worldcup_fixture_events.csv"
CARDS = HERE / "worldcup_cards.csv"
STORE_DIR = ROOT / "data" / "processed" / "worldcup" / "api_enrichment"

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# --- exact headers (MUST match analysis/players/player_data_adapters.py + data/external/README.md) ---
COLUMNS = {
    "set_piece_takers.csv": ["team_id", "team_name", "player_id", "player_name", "role", "rank",
                             "attempts", "last_taken_date", "source", "data_quality", "confidence"],
    "player_xg_xa.csv": ["player_id", "player_name", "team_id", "team_name", "source", "season",
                         "competition", "minutes", "xg", "xa", "xg90", "xa90", "shots90", "sot90",
                         "key_passes90", "crosses90", "data_quality", "confidence"],
    "player_positional_profiles.csv": ["player_id", "player_name", "team_id", "position", "role",
                                       "preferred_zone", "attacking_weight", "defensive_weight",
                                       "aerial_threat", "pace_threat", "1v1_threat", "crossing_threat",
                                       "card_risk_role", "source", "data_quality", "confidence"],
    "coach_tactical_profiles.csv": ["team_id", "team_name", "coach_name", "base_formation",
                                    "pressing_level", "defensive_block", "build_up_style",
                                    "transition_speed", "width_usage", "set_piece_emphasis",
                                    "substitution_aggression", "knockout_risk_profile", "source",
                                    "data_quality", "confidence"],
    "referee_profiles.csv": ["referee_name", "matches", "yellow_cards_pg", "red_cards_pg", "fouls_pg",
                             "penalties_pg", "home_cards_pg", "away_cards_pg", "tournament_context",
                             "source", "data_quality", "confidence"],
    "fixture_referees.csv": ["fixture_id", "referee_name"],
    "weather_by_fixture.csv": ["fixture_id", "venue", "kickoff_time", "temperature", "humidity",
                               "wind_speed", "rain_probability", "pitch_condition", "source",
                               "data_quality", "confidence"],
}

# templates pre-populated/maintained from real repo data (incremental merge) vs. empty-only (manual)
DERIVED = {"set_piece_takers.csv", "player_positional_profiles.csv", "weather_by_fixture.csv",
           "fixture_referees.csv"}
EMPTY_ONLY = {"player_xg_xa.csv", "coach_tactical_profiles.csv", "referee_profiles.csv"}

# `source` values produced by THIS deriver -> a row with one of these is "owned" by the deriver and its
# auto-owned facts may be refreshed. ANY other (or a human-typed) source makes the row manual = sacred.
AUTO_SOURCES = {"api_football_events", "worldcup_events", "api_football_lineup_position",
                "api_football_lineup", "plantilla_kickoff", "api_football_store"}

# per-file: columns the deriver may REFRESH on an auto-owned row (everything else is complete-if-empty).
AUTO_OWNED = {
    "set_piece_takers.csv": {"attempts", "last_taken_date", "rank", "data_quality", "confidence"},
    "player_positional_profiles.csv": {"position", "data_quality"},
    "weather_by_fixture.csv": {"kickoff_time"},
    "fixture_referees.csv": set(),
}
KEY_COLS = {
    "set_piece_takers.csv": ["team_id", "player_id", "role"],
    "player_positional_profiles.csv": ["player_id"],
    "weather_by_fixture.csv": ["fixture_id"],
    "fixture_referees.csv": ["fixture_id"],
}
DEFAULT_SOURCE = {
    "set_piece_takers.csv": "api_football_events",
    "player_positional_profiles.csv": "api_football_lineup_position",
    "weather_by_fixture.csv": "plantilla_kickoff",
    "fixture_referees.csv": "api_football_store",
}

# coarse single-letter /fixtures/players position -> readable bucket (NOT a finer position)
_POS_LABEL = {"G": "GK", "D": "DEF", "M": "MID", "F": "FWD"}
# fine positions we accept verbatim from a lineup source that carries them (never inferred from a grid)
_FINE_POS = {"GK", "CB", "LB", "RB", "LWB", "RWB", "DM", "CM", "AM", "LW", "RW", "ST", "CF"}


# ============================================================ tiny value helpers
def _is_empty(v) -> bool:
    if v is None:
        return True
    if isinstance(v, float) and pd.isna(v):
        return True
    if isinstance(v, str) and v.strip() == "":
        return True
    return False


def _norm_key(v):
    """Normalise a key value so 10 == 10.0 == '10'. Falls back to a trimmed string."""
    try:
        if _is_empty(v):
            return ""
        return str(int(float(v)))
    except Exception:
        return str(v).strip()


def _confidence_for_attempts(n: int) -> str:
    return "alta" if n >= 3 else ("media" if n == 2 else "baja")


# ============================================================ pure derivations (testable, no I/O)
def derive_set_piece_takers(events_df) -> list:
    """PENALTY takers from REAL events. attempts = penalties taken (scored+missed); rank by attempts
    desc within team; last_taken_date = latest. Free-kick/corner roles are NOT inferable -> not emitted.
    NEVER fabricates. source=api_football_events, data_quality=alta, confidence by sample size."""
    if events_df is None or len(events_df) == 0:
        return []
    df = events_df.copy()
    for c in ("is_penalty_goal", "is_penalty_miss"):
        if c not in df.columns:
            df[c] = 0
    df["pen"] = df["is_penalty_goal"].fillna(0).astype(int) + df["is_penalty_miss"].fillna(0).astype(int)
    pens = df[df["pen"] > 0]
    agg = {}
    for _, r in pens.iterrows():
        try:
            tid = int(r["team_id"]); pid = int(r["player_id"])
        except Exception:
            continue
        d = agg.setdefault((tid, pid), {"team_id": tid, "team_name": r.get("team_name"),
                                        "player_id": pid, "player_name": r.get("player_name"),
                                        "attempts": 0, "last_taken_date": None})
        d["attempts"] += int(r["pen"])
        date = str(r.get("date") or "")[:10]
        if date and (d["last_taken_date"] is None or date > d["last_taken_date"]):
            d["last_taken_date"] = date
    by_team = {}
    for (tid, pid), d in agg.items():
        by_team.setdefault(tid, []).append(d)
    rows = []
    for tid, lst in by_team.items():
        lst.sort(key=lambda x: x["attempts"], reverse=True)
        for i, d in enumerate(lst, 1):
            n = d["attempts"]
            rows.append({
                "team_id": d["team_id"], "team_name": d["team_name"],
                "player_id": d["player_id"], "player_name": d["player_name"],
                "role": "penalty", "rank": i, "attempts": n,
                "last_taken_date": d["last_taken_date"],
                "source": "api_football_events", "data_quality": "alta",
                "confidence": _confidence_for_attempts(n),
            })
    return rows


def _fine_positions_from_store(store) -> dict:
    """{player_id: {'position': FINE, 'source': 'api_football_lineup'}} from a lineup source that carries
    an EXPLICIT fine position (e.g. /fixtures/lineups startXI[].player.pos == 'CB'). Grid geometry is
    NOT interpreted (that would be inference) — only verbatim fine strings are used. {} if none."""
    out = {}
    pf = (store or {}).get("postft") or {}
    lineups = pf.get("lineups") or (store or {}).get("lineups") or []
    for block in lineups:
        squad = (block or {}).get("startXI") or []
        squad = squad + ((block or {}).get("substitutes") or [])
        for slot in squad:
            pl = (slot or {}).get("player") or {}
            pid = pl.get("id")
            pos = pl.get("pos")
            if pid is None or not pos:
                continue
            up = str(pos).strip().upper()
            if up in _FINE_POS:
                out[int(pid)] = {"position": up, "source": "api_football_lineup"}
    return out


def derive_positional_profiles(store_records) -> list:
    """Player POSITION from cached lineups. Prefers a FINE position when a lineup source carries it,
    else the coarse G/D/M/F -> GK/DEF/MID/FWD. Only player_id/name/team_id/position are real; scouting
    fields stay EMPTY (no fabrication). Dedup by player_id (a fine position upgrades a coarse one)."""
    seen = {}
    for store in store_records or []:
        fine = _fine_positions_from_store(store)
        players = ((store or {}).get("postft") or {}).get("players") or []
        for block in players:
            team = (block or {}).get("team") or {}
            tid = team.get("id")
            for p in (block.get("players") or []):
                pl = (p or {}).get("player") or {}
                pid = pl.get("id")
                if pid is None:
                    continue
                stats = (p.get("statistics") or [{}])
                games = (stats[0] or {}).get("games") or {} if stats else {}
                coarse = games.get("position")
                fpos = fine.get(int(pid))
                if fpos:
                    position, source, dq = fpos["position"], fpos["source"], "alta"
                elif coarse:
                    position = _POS_LABEL.get(str(coarse).strip().upper(), str(coarse).strip())
                    source, dq = "api_football_lineup_position", "media"
                else:
                    continue
                prev = seen.get(pid)
                # a FINE position upgrades a previously-seen coarse one; otherwise first-seen wins
                if prev and prev["source"] == "api_football_lineup" and source != "api_football_lineup":
                    continue
                seen[pid] = {
                    "player_id": pid, "player_name": pl.get("name"), "team_id": tid,
                    "position": position, "role": None, "preferred_zone": None,
                    "attacking_weight": None, "defensive_weight": None, "aerial_threat": None,
                    "pace_threat": None, "1v1_threat": None, "crossing_threat": None,
                    "card_risk_role": None, "source": source,
                    "data_quality": dq, "confidence": "baja",
                }
    return list(seen.values())


def derive_weather_template(cards_df, venues=None) -> list:
    """fixture_id + kickoff_time from the card (real). venue filled IF a real venue is supplied
    (venues={fixture_id: name}); measurements are NEVER invented (left empty -> weather_context degrades
    to 'pendiente')."""
    if cards_df is None or len(cards_df) == 0 or "fixture_id" not in cards_df.columns:
        return []
    venues = venues or {}
    rows = []
    for _, c in cards_df.iterrows():
        fid = c.get("fixture_id")
        if pd.isna(fid):
            continue
        fid = int(fid)
        rows.append({
            "fixture_id": fid, "venue": venues.get(fid),
            "kickoff_time": c.get("kickoff_utc"),
            "temperature": None, "humidity": None, "wind_speed": None,
            "rain_probability": None, "pitch_condition": None,
            "source": "plantilla_kickoff", "data_quality": "pendiente", "confidence": "pendiente",
        })
    return rows


def derive_fixture_referees(referees) -> list:
    """{fixture_id: referee_name} -> rows. Empty when no referee is found in the store (no invention)."""
    return [{"fixture_id": int(fid), "referee_name": name}
            for fid, name in (referees or {}).items() if name]


# ============================================================ store detection (referee / venue)
def detect_referees(store_records) -> dict:
    """{fixture_id: referee_name} from whatever the cached store happens to carry. Scans the known
    places a referee could appear; returns {} when none (today: none cached). NEVER invents."""
    out = {}
    for s in store_records or []:
        fid = (s or {}).get("fixture_id")
        if fid is None:
            continue
        name = None
        candidates = [
            (s or {}).get("referee"),
            ((s or {}).get("fixture") or {}).get("referee"),
            (((s or {}).get("postft") or {}).get("fixture") or {}).get("referee"),
            (((s or {}).get("prematch") or {}).get("fixture") or {}).get("referee"),
        ]
        for cand in candidates:
            if isinstance(cand, str) and cand.strip():
                name = cand.strip()
                break
            if isinstance(cand, dict) and (cand.get("name") or "").strip():
                name = cand["name"].strip()
                break
        if name:
            out[int(fid)] = name
    return out


def detect_venues(store_records) -> dict:
    """{fixture_id: venue_name} from the store (prematch /venues response or a fixture.venue block).
    Returns {} when none. NEVER invents a stadium/city."""
    out = {}
    for s in store_records or []:
        fid = (s or {}).get("fixture_id")
        if fid is None:
            continue
        name = None
        pv = ((s or {}).get("prematch") or {}).get("venue")
        if isinstance(pv, list) and pv:
            name = ((pv[0] or {}).get("name") or "").strip() or None
        if not name:
            for cand in ((s or {}).get("venue"), ((s or {}).get("fixture") or {}).get("venue")):
                if isinstance(cand, dict) and (cand.get("name") or "").strip():
                    name = cand["name"].strip()
                    break
                if isinstance(cand, str) and cand.strip():
                    name = cand.strip()
                    break
        if name:
            out[int(fid)] = name
    return out


# ============================================================ the safe incremental merge engine
def safe_merge(existing_df, new_rows, columns, key_cols, auto_owned, default_source=None):
    """Merge `new_rows` (REAL data) into `existing_df` without ever destroying manual content.

    Rules:
      * a key not present in existing -> APPEND the new row;
      * an existing EMPTY cell -> COMPLETE it with the real value;
      * an existing NON-EMPTY cell -> only REFRESH it when (col in auto_owned) AND the row's `source`
        is an auto source AND the value actually differs; otherwise PROTECT (keep manual);
      * rows are never deleted; rows absent from new_rows are preserved verbatim.

    Returns (merged_df, stats) with stats = {added, completed, refreshed, protected, manual_rows}.
    """
    existing_df = existing_df.copy() if existing_df is not None else pd.DataFrame(columns=columns)
    for c in columns:
        if c not in existing_df.columns:
            existing_df[c] = pd.NA
    records = existing_df[columns].to_dict("records")

    index = {}
    for i, r in enumerate(records):
        if all(not _is_empty(r.get(k)) for k in key_cols):
            index[tuple(_norm_key(r[k]) for k in key_cols)] = i

    touched = set()
    added = completed = refreshed = protected = 0
    for nr in new_rows or []:
        if any(_is_empty(nr.get(k)) for k in key_cols):
            continue
        key = tuple(_norm_key(nr.get(k)) for k in key_cols)
        if key in index:
            i = index[key]
            row = records[i]
            touched.add(i)
            row_source = "" if _is_empty(row.get("source")) else str(row.get("source")).strip()
            is_auto = (row_source == "") or (row_source in AUTO_SOURCES)
            for col, val in nr.items():
                if col not in columns or col in key_cols or _is_empty(val):
                    continue
                cur = row.get(col)
                if _is_empty(cur):
                    row[col] = val
                    completed += 1
                elif col in auto_owned and is_auto and str(cur) != str(val):
                    row[col] = val
                    refreshed += 1
                elif str(cur) != str(val):
                    protected += 1
        else:
            nrow = {c: nr.get(c) for c in columns}
            if "source" in columns and _is_empty(nrow.get("source")) and default_source:
                nrow["source"] = default_source
            records.append(nrow)
            index[key] = len(records) - 1
            added += 1

    manual_rows = sum(1 for i, r in enumerate(records)
                      if i not in touched and i < len(existing_df)
                      and str(r.get("source") or "").strip() not in AUTO_SOURCES
                      and any(not _is_empty(r.get(c)) for c in columns))
    merged = pd.DataFrame(records, columns=columns)
    return merged, {"added": added, "completed": completed, "refreshed": refreshed,
                    "protected": protected, "manual_rows": manual_rows}


# ============================================================ I/O helpers
def _load_events(path=FIXTURE_EVENTS):
    try:
        return pd.read_csv(path) if Path(path).exists() else None
    except Exception:
        return None


def _load_cards(path=CARDS):
    try:
        return pd.read_csv(path) if Path(path).exists() else None
    except Exception:
        return None


def _load_store_records(store_dir=STORE_DIR):
    recs = []
    for fp in sorted(glob.glob(str(Path(store_dir) / "*.json"))):
        try:
            recs.append(json.load(open(fp, encoding="utf-8")))
        except Exception:
            continue
    return recs


def write_template(path, columns, rows=None, overwrite=False):
    """Create-if-missing: write header (+ any rows) ONLY when the file does not exist. NEVER overwrites
    an existing file unless overwrite=True. Returns (action, n_rows)."""
    path = Path(path)
    rows = rows or []
    if path.exists() and not overwrite:
        return "exists", None
    df = pd.DataFrame(rows, columns=columns)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    return ("overwritten" if path.exists() and overwrite else "created"), len(df)


def merge_template(path, columns, new_rows, key_cols, auto_owned, default_source=None):
    """Load (or start empty), safe-merge real rows, write back. Returns a per-file summary dict."""
    path = Path(path)
    existed = path.exists()
    if existed:
        try:
            existing = pd.read_csv(path)
        except Exception:
            existing = pd.DataFrame(columns=columns)
    else:
        existing = pd.DataFrame(columns=columns)
    before = len(existing)
    merged, stats = safe_merge(existing, new_rows, columns, key_cols, auto_owned, default_source)
    path.parent.mkdir(parents=True, exist_ok=True)
    merged[columns].to_csv(path, index=False)
    action = "created" if not existed else "merged"
    return {"action": action, "rows": len(merged), "existing_rows": before,
            "prepopulated": stats["added"], **stats}


# ============================================================ orchestration
def prepare(ext_dir=EXT_DIR, events_df=None, cards_df=None, store_records=None):
    """Build/maintain every template. DERIVED files go through the safe incremental merge; EMPTY_ONLY
    files are create-if-missing (and never touched again). Callers (tests) may inject inputs; main()
    loads them from the real repo files. Returns a per-file summary dict."""
    ext_dir = Path(ext_dir)
    events_df = _load_events() if events_df is None else events_df
    cards_df = _load_cards() if cards_df is None else cards_df
    store_records = _load_store_records() if store_records is None else store_records

    referees = detect_referees(store_records)
    venues = detect_venues(store_records)
    derived_rows = {
        "set_piece_takers.csv": derive_set_piece_takers(events_df),
        "player_positional_profiles.csv": derive_positional_profiles(store_records),
        "weather_by_fixture.csv": derive_weather_template(cards_df, venues=venues),
        "fixture_referees.csv": derive_fixture_referees(referees),
    }

    summary = {}
    for fname, cols in COLUMNS.items():
        path = ext_dir / fname
        if fname in DERIVED:
            s = merge_template(path, cols, derived_rows.get(fname, []), KEY_COLS[fname],
                               AUTO_OWNED[fname], DEFAULT_SOURCE.get(fname))
            s["kind"] = "derived"
        else:
            action, n = write_template(path, cols)
            s = {"action": action, "rows": n, "existing_rows": None, "prepopulated": 0,
                 "added": 0, "completed": 0, "refreshed": 0, "protected": 0, "manual_rows": 0,
                 "kind": "empty"}
        # pending columns = columns fully empty across the file
        pending = []
        try:
            df = pd.read_csv(path)
            for col in cols:
                if col not in df.columns or len(df) == 0 or df[col].isna().all():
                    pending.append(col)
        except Exception:
            pending = list(cols)
        s["pending_columns"] = pending
        summary[fname] = s
    return summary


def main():
    ap = argparse.ArgumentParser(description="World Cup external-data template preparer + safe "
                                             "incremental merge (read-only, no API, no scraping, "
                                             "no fabrication).")
    ap.parse_args()
    summary = prepare()
    print("=== external-data templates (data/external/) — Fase 4B incremental ===")
    for fname, s in summary.items():
        tag = s["action"].upper()
        bits = []
        if s.get("existing_rows") is not None:
            bits.append(f"existentes {s['existing_rows']}")
        if s.get("added"):
            bits.append(f"+{s['added']} nuevas")
        if s.get("completed"):
            bits.append(f"{s['completed']} celdas completadas")
        if s.get("refreshed"):
            bits.append(f"{s['refreshed']} refrescadas")
        if s.get("protected"):
            bits.append(f"{s['protected']} manuales protegidas")
        if s.get("manual_rows"):
            bits.append(f"{s['manual_rows']} filas manuales preservadas")
        extra = (" | " + ", ".join(bits)) if bits else ""
        print(f"  {fname:34s} [{tag:8s}]{extra}")
    tot_added = sum(s.get("added", 0) for s in summary.values())
    tot_done = sum(s.get("completed", 0) for s in summary.values())
    print(f"--- merge incremental: +{tot_added} fila(s) reales nuevas, {tot_done} celda(s) completadas; "
          f"datos manuales intactos; sin inventar. ---")
    # honest 'not available yet' note
    na = []
    if not summary["fixture_referees.csv"].get("added") and \
            summary["fixture_referees.csv"]["existing_rows"] in (0, None):
        na.append("árbitro (sin dato en el store)")
    if summary["weather_by_fixture.csv"]["pending_columns"]:
        if "venue" in summary["weather_by_fixture.csv"]["pending_columns"]:
            na.append("venue (sin dato en el store)")
        na.append("mediciones de clima (relleno manual)")
    if na:
        print("    no disponible aún: " + " · ".join(na))
    return summary


if __name__ == "__main__":
    main()
