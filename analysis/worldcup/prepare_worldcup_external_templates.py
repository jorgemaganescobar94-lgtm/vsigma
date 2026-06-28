"""
WORLD CUP 2026 — EXTERNAL-DATA TEMPLATE PREPARER (Fase 4A). READ-ONLY inputs · NO API · NO scraping ·
NO market/odds · NO betting · NO fabrication.

Bootstraps the optional data/external/*.csv contracts the player-events module (Fase 3) consumes, so
Jorge can fill them by hand. It:
  * CREATES each CSV with the exact documented header IF it does not exist yet;
  * PRE-POPULATES *only* fields derivable from REAL data already in the repo:
      - set_piece_takers.csv   -> PENALTY takers from REAL World Cup /fixtures/events (penalty goals +
                                  missed penalties); free-kick/corner takers are NOT inferable -> left out
      - player_positional_profiles.csv -> the player POSITION from cached /fixtures/players (G/D/M/F);
                                  roles / threats / zones are scouting fields -> left EMPTY (no invention)
      - weather_by_fixture.csv -> fixture_id + kickoff_time only (no temperature/wind/rain measured)
  * NEVER overwrites a file that already exists (preserves manual edits) — create-if-missing only;
  * leaves an honest source / data_quality / confidence on every pre-populated row;
  * does NOT treat internal proxies as real xG/xA (player_xg_xa.csv stays an EMPTY template);
  * does NOT invent referees / coaches / weather (those stay EMPTY templates).

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

# templates that are pre-populated from real repo data vs. left empty for manual entry
DERIVED = {"set_piece_takers.csv", "player_positional_profiles.csv", "weather_by_fixture.csv"}
EMPTY_ONLY = {"player_xg_xa.csv", "coach_tactical_profiles.csv", "referee_profiles.csv",
              "fixture_referees.csv"}

# map the single-letter /fixtures/players position to a readable label (NOT a finer position)
_POS_LABEL = {"G": "GK", "D": "DEF", "M": "MID", "F": "FWD"}


# ============================================================ pure derivations (testable, no I/O)
def derive_set_piece_takers(events_df) -> list:
    """PENALTY takers from REAL events. attempts = penalties taken (scored+missed); rank by attempts
    desc within team; last_taken_date = latest. Free-kick/corner roles are NOT inferable -> not emitted.
    NEVER fabricates. Returns rows matching COLUMNS['set_piece_takers.csv']."""
    if events_df is None or len(events_df) == 0:
        return []
    df = events_df.copy()
    for c in ("is_penalty_goal", "is_penalty_miss"):
        if c not in df.columns:
            df[c] = 0
    df["pen"] = df["is_penalty_goal"].fillna(0).astype(int) + df["is_penalty_miss"].fillna(0).astype(int)
    pens = df[df["pen"] > 0]
    rows = []
    agg = {}
    for _, r in pens.iterrows():
        try:
            tid = int(r["team_id"]); pid = int(r["player_id"])
        except Exception:
            continue
        key = (tid, pid)
        d = agg.setdefault(key, {"team_id": tid, "team_name": r.get("team_name"),
                                 "player_id": pid, "player_name": r.get("player_name"),
                                 "attempts": 0, "last_taken_date": None})
        d["attempts"] += int(r["pen"])
        date = str(r.get("date") or "")[:10]
        if date and (d["last_taken_date"] is None or date > d["last_taken_date"]):
            d["last_taken_date"] = date
    # rank within team by attempts desc
    by_team = {}
    for (tid, pid), d in agg.items():
        by_team.setdefault(tid, []).append(d)
    for tid, lst in by_team.items():
        lst.sort(key=lambda x: x["attempts"], reverse=True)
        for i, d in enumerate(lst, 1):
            n = d["attempts"]
            dq = "alta" if n >= 3 else ("media" if n == 2 else "baja")
            conf = "media" if n >= 2 else "baja"
            rows.append({
                "team_id": d["team_id"], "team_name": d["team_name"],
                "player_id": d["player_id"], "player_name": d["player_name"],
                "role": "penalty", "rank": i, "attempts": n,
                "last_taken_date": d["last_taken_date"],
                "source": "worldcup_events", "data_quality": dq, "confidence": conf,
            })
    return rows


def derive_positional_profiles(store_records) -> list:
    """Player POSITION (G/D/M/F -> GK/DEF/MID/FWD label) from cached /fixtures/players. Only player_id,
    player_name, team_id and position are real; scouting fields stay EMPTY (no fabrication). Dedup by
    player_id (keep first seen with a position). store_records: iterable of store dicts."""
    seen = {}
    for store in store_records or []:
        players = ((store or {}).get("postft") or {}).get("players") or []
        for block in players:
            team = (block or {}).get("team") or {}
            tid = team.get("id")
            for p in (block.get("players") or []):
                pl = (p or {}).get("player") or {}
                pid = pl.get("id")
                if pid is None or pid in seen:
                    continue
                stats = (p.get("statistics") or [{}])
                games = (stats[0] or {}).get("games") or {} if stats else {}
                pos = games.get("position")
                if not pos:
                    continue
                seen[pid] = {
                    "player_id": pid, "player_name": pl.get("name"), "team_id": tid,
                    "position": _POS_LABEL.get(str(pos).strip().upper(), str(pos).strip()),
                    "role": None, "preferred_zone": None,
                    "attacking_weight": None, "defensive_weight": None, "aerial_threat": None,
                    "pace_threat": None, "1v1_threat": None, "crossing_threat": None,
                    "card_risk_role": None,
                    "source": "api_football_lineup_position",
                    "data_quality": "media", "confidence": "baja",
                }
    return list(seen.values())


def derive_weather_template(cards_df) -> list:
    """fixture_id + kickoff_time from the card (real). venue/measurements are NOT available here ->
    left EMPTY (weather_context degrades to 'pendiente de rellenar', never implies normal weather)."""
    if cards_df is None or len(cards_df) == 0 or "fixture_id" not in cards_df.columns:
        return []
    rows = []
    for _, c in cards_df.iterrows():
        fid = c.get("fixture_id")
        if pd.isna(fid):
            continue
        rows.append({
            "fixture_id": int(fid), "venue": None,
            "kickoff_time": c.get("kickoff_utc"),
            "temperature": None, "humidity": None, "wind_speed": None,
            "rain_probability": None, "pitch_condition": None,
            "source": "plantilla_kickoff", "data_quality": "pendiente", "confidence": "pendiente",
        })
    return rows


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
    """Create-if-missing: write header (+ any pre-populated rows) ONLY when the file does not exist.
    NEVER overwrites an existing file (preserves manual edits) unless overwrite=True (not used by main).
    Returns (action, n_rows) where action in {created, exists, overwritten}."""
    path = Path(path)
    rows = rows or []
    if path.exists() and not overwrite:
        return "exists", None
    df = pd.DataFrame(rows, columns=columns)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    return ("overwritten" if path.exists() and overwrite else "created"), len(df)


# ============================================================ orchestration
def prepare(ext_dir=EXT_DIR, events_df=None, cards_df=None, store_records=None, overwrite=False):
    """Build every template (create-if-missing). Returns a summary dict per file. Pure-ish: callers
    (tests) can inject events_df/cards_df/store_records; main() loads them from the real repo files."""
    ext_dir = Path(ext_dir)
    events_df = _load_events() if events_df is None else events_df
    cards_df = _load_cards() if cards_df is None else cards_df
    store_records = _load_store_records() if store_records is None else store_records

    derived_rows = {
        "set_piece_takers.csv": derive_set_piece_takers(events_df),
        "player_positional_profiles.csv": derive_positional_profiles(store_records),
        "weather_by_fixture.csv": derive_weather_template(cards_df),
    }

    summary = {}
    for fname, cols in COLUMNS.items():
        rows = derived_rows.get(fname, [])
        action, n = write_template(ext_dir / fname, cols, rows, overwrite=overwrite)
        # which columns are still empty/pending across the written rows
        pending = []
        if action == "created" and rows:
            present = pd.DataFrame(rows)
            for col in cols:
                if col not in present.columns or present[col].isna().all():
                    pending.append(col)
        elif action == "created":
            pending = list(cols)   # empty template -> everything pending
        summary[fname] = {"action": action, "rows": n, "prepopulated": len(rows),
                          "pending_columns": pending, "kind": "derived" if fname in DERIVED else "empty"}
    return summary


def main():
    ap = argparse.ArgumentParser(description="World Cup external-data template preparer (read-only, "
                                             "no API, no scraping, no fabrication).")
    ap.add_argument("--overwrite", action="store_true",
                    help="DANGEROUS: overwrite existing templates (default create-if-missing). Off by default.")
    a = ap.parse_args()
    summary = prepare(overwrite=a.overwrite)
    print("=== external-data templates (data/external/) ===")
    for fname, s in summary.items():
        tag = s["action"].upper()
        extra = ""
        if s["action"] == "created":
            extra = f" | pre-poblado {s['prepopulated']} fila(s)"
            if s["pending_columns"]:
                shown = ", ".join(s["pending_columns"][:6]) + ("…" if len(s["pending_columns"]) > 6 else "")
                extra += f" | pendientes: {shown}"
        print(f"  {fname:34s} [{tag:11s}] {extra}")
    created = sum(1 for s in summary.values() if s["action"] == "created")
    prepop = sum(s["prepopulated"] for s in summary.values())
    print(f"--- {created} plantilla(s) creada(s), {prepop} fila(s) pre-pobladas desde datos reales; "
          f"el resto queda para relleno manual (sin inventar). ---")
    return summary


if __name__ == "__main__":
    main()
