"""
WORLD CUP 2026 — AUTO REFEREE PROFILES from REAL events (Fase 4E). READ-ONLY inputs · NO API · NO
scraping · NO web · NO market/odds/betting · NO fabrication · NO secrets · NO commit. Pure football.

Derives a per-referee profile using ONLY data the World Cup product already captured:
  * data/external/fixture_referees.csv          -> {fixture_id: referee_name} (auto-persisted, Fase 4D)
  * analysis/worldcup/worldcup_fixture_events.csv -> real cards / penalties per fixture (Fase 2)
  * data/processed/worldcup/api_enrichment/<id>.json -> home_id/away_id to split home/away cards

NO new API calls, NO scraping, NO invented numbers. A referee with a thin sample is marked with low
confidence and an explicit "do not extrapolate" reason — never a hard percentage dressed up as reliable.

Outputs (generated artifacts — NOT data/external; referee_profiles.csv stays manual & blocked):
  * analysis/worldcup/worldcup_referee_profiles_auto.csv
  * analysis/worldcup/worldcup_referee_profiles_auto.json
  * analysis/worldcup/worldcup_referee_profiles_auto_report.txt

Run:  python analysis/worldcup/build_worldcup_referee_profiles_auto.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]

FIXTURE_REFEREES = ROOT / "data" / "external" / "fixture_referees.csv"
FIXTURE_EVENTS = HERE / "worldcup_fixture_events.csv"
STORE_DIR = ROOT / "data" / "processed" / "worldcup" / "api_enrichment"
OUT_CSV = HERE / "worldcup_referee_profiles_auto.csv"
OUT_JSON = HERE / "worldcup_referee_profiles_auto.json"
OUT_TXT = HERE / "worldcup_referee_profiles_auto_report.txt"

SOURCE = "worldcup_events_auto"

# card_type strings the extractor emits (Fase 2) — never guessed
YELLOW = "Yellow Card"
RED = "Red Card"
SECOND_YELLOW = "Second Yellow card"

# qualitative ENVIRONMENT thresholds (labels only — never a number presented as a bet/edge).
# Total cards per game (yellows + reds + second yellows). Conservative for tournament football.
CARD_HIGH_PG = 5.5
CARD_LOW_PG = 3.0
# penalties are rare & noisy: only label an environment with a minimally usable sample.
PEN_MIN_MATCHES = 4
PEN_HIGH_RATE = 0.40      # share of matches with >=1 penalty
PEN_LOW_RATE = 0.10

CSV_COLUMNS = [
    "referee_name", "matches", "fixtures", "yellow_cards_total", "red_cards_total",
    "second_yellow_total", "cards_total", "yellow_cards_pg", "red_cards_pg", "cards_pg",
    "penalties_total", "penalties_pg", "matches_with_penalty", "penalty_match_rate",
    "home_cards_total", "away_cards_total", "home_cards_pg", "away_cards_pg",
    "card_environment", "penalty_environment", "data_quality", "confidence", "reason", "source",
]

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


# ============================================================ loaders (pure-ish, soft-failing)
def load_fixture_referees(path=FIXTURE_REFEREES) -> dict:
    """{fixture_id: referee_name} from the auto-persisted map. Empty when absent. NO fabrication."""
    out = {}
    p = Path(path)
    if not p.exists():
        return out
    try:
        df = pd.read_csv(p)
    except Exception:
        return out
    if "fixture_id" not in df.columns or "referee_name" not in df.columns:
        return out
    for _, r in df.iterrows():
        fid, name = r.get("fixture_id"), r.get("referee_name")
        if pd.isna(fid) or not isinstance(name, str) or not name.strip():
            continue
        out[int(fid)] = name.strip()
    return out


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


def load_home_away(store_dir=STORE_DIR) -> dict:
    """{fixture_id: (home_id, away_id)} from the cached store, to split home/away cards. {} if none."""
    out = {}
    d = Path(store_dir)
    if not d.exists():
        return out
    for fp in sorted(d.glob("*.json")):
        try:
            s = json.loads(fp.read_text(encoding="utf-8"))
        except Exception:
            continue
        fid = s.get("fixture_id")
        if fid is None:
            continue
        out[int(fid)] = (s.get("home_id"), s.get("away_id"))
    return out


# ============================================================ confidence / environment ladders
def confidence_for(matches: int) -> str:
    """Conservative ladder (spec §3). NEVER asserts a tendency on 1 match."""
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


def card_environment_for(matches: int, cards_pg) -> str:
    """One of bajo/medio/alto/no determinado (spec §2). The sample caveat lives in `reason`."""
    if matches <= 0 or cards_pg is None:
        return "no determinado"
    if cards_pg >= CARD_HIGH_PG:
        return "alto"
    if cards_pg <= CARD_LOW_PG:
        return "bajo"
    return "medio"


def penalty_environment_for(matches: int, penalty_match_rate) -> str:
    """Penalties are rare/noisy -> only labelled with a minimally usable sample, else no determinado."""
    if matches < PEN_MIN_MATCHES or penalty_match_rate is None:
        return "no determinado"
    if penalty_match_rate >= PEN_HIGH_RATE:
        return "alto"
    if penalty_match_rate <= PEN_LOW_RATE:
        return "bajo"
    return "medio"


def reason_for(matches: int) -> str:
    if matches <= 0:
        return "árbitro sin partidos con eventos reales todavía; no extrapolar"
    if matches == 1:
        return "solo 1 partido, no extrapolar fuerte"
    if matches <= 3:
        return f"{matches} partidos, muestra reducida — orientativo"
    if matches <= 5:
        return f"{matches} partidos con eventos reales — muestra media"
    return f"{matches} partidos con eventos reales — muestra suficiente"


def _r(v, nd=3):
    return None if v is None else round(float(v), nd)


# ============================================================ core derivation (pure, testable)
def derive_referee_profiles(referees_map, events_df, home_away=None) -> list:
    """Aggregate real cards/penalties per referee from the events of the fixtures they officiated.
    referees_map: {fixture_id: referee_name}. events_df: the Fase-2 events table (or None).
    home_away: {fixture_id: (home_id, away_id)} (optional). NEVER fabricates."""
    home_away = home_away or {}
    # fixtures per referee (assigned), independent of whether events exist yet
    ref_fixtures = {}
    for fid, name in (referees_map or {}).items():
        ref_fixtures.setdefault(name, set()).add(int(fid))

    # index events by fixture
    ev_by_fix = {}
    if events_df is not None and len(events_df):
        for _, e in events_df.iterrows():
            try:
                fid = int(e.get("fixture_id"))
            except Exception:
                continue
            ev_by_fix.setdefault(fid, []).append(e)

    profiles = []
    for name in sorted(ref_fixtures):
        fixtures = sorted(ref_fixtures[name])
        with_events = [f for f in fixtures if f in ev_by_fix]
        matches = len(with_events)

        yel = red = sec = 0
        home_cards = away_cards = 0
        pens_total = 0
        fixtures_with_pen = 0
        home_known = False
        for fid in with_events:
            fix_pen = 0
            for e in ev_by_fix.get(fid, []):
                ctype = str(e.get("card_type") or "").strip()
                is_card = int(e.get("is_card") or 0) == 1 or ctype in (YELLOW, RED, SECOND_YELLOW)
                if is_card:
                    if ctype == YELLOW:
                        yel += 1
                    elif ctype == RED:
                        red += 1
                    elif ctype == SECOND_YELLOW:
                        sec += 1
                    # home/away split (only when we know the home/away ids for this fixture)
                    ha = home_away.get(fid)
                    if ha and ha[0] is not None:
                        home_known = True
                        try:
                            tid = int(e.get("team_id"))
                        except Exception:
                            tid = None
                        if tid is not None:
                            if tid == ha[0]:
                                home_cards += 1
                            elif tid == ha[1]:
                                away_cards += 1
                pg = int(e.get("is_penalty_goal") or 0)
                pm = int(e.get("is_penalty_miss") or 0)
                fix_pen += pg + pm
            pens_total += fix_pen
            if fix_pen > 0:
                fixtures_with_pen += 1

        cards_total = yel + red + sec
        cards_pg = (cards_total / matches) if matches else None
        yel_pg = (yel / matches) if matches else None
        red_pg = ((red + sec) / matches) if matches else None       # dismissals incl. 2nd yellow
        pen_pg = (pens_total / matches) if matches else None
        pen_match_rate = (fixtures_with_pen / matches) if matches else None
        home_pg = (home_cards / matches) if (matches and home_known) else None
        away_pg = (away_cards / matches) if (matches and home_known) else None

        profiles.append({
            "referee_name": name,
            "matches": matches,
            "fixtures": len(fixtures),
            "yellow_cards_total": yel,
            "red_cards_total": red,
            "second_yellow_total": sec,
            "cards_total": cards_total,
            "yellow_cards_pg": _r(yel_pg),
            "red_cards_pg": _r(red_pg),
            "cards_pg": _r(cards_pg),
            "penalties_total": pens_total,
            "penalties_pg": _r(pen_pg),
            "matches_with_penalty": fixtures_with_pen,
            "penalty_match_rate": _r(pen_match_rate),
            "home_cards_total": home_cards if home_known else None,
            "away_cards_total": away_cards if home_known else None,
            "home_cards_pg": _r(home_pg),
            "away_cards_pg": _r(away_pg),
            "card_environment": card_environment_for(matches, cards_pg),
            "penalty_environment": penalty_environment_for(matches, pen_match_rate),
            "data_quality": data_quality_for(matches),
            "confidence": confidence_for(matches),
            "reason": reason_for(matches),
            "source": SOURCE,
        })
    return profiles


# ============================================================ rendering / I/O
def render_txt(profiles) -> str:
    L = ["===== WORLD CUP — PERFILES DE ÁRBITRO AUTO (eventos reales) =====", "",
         f"Árbitros con perfil: {len(profiles)}",
         f"Con muestra (>=1 partido con eventos): {sum(1 for p in profiles if p['matches'] > 0)}", ""]
    for p in sorted(profiles, key=lambda x: (-x["matches"], x["referee_name"])):
        L.append(f"  {p['referee_name']}")
        L.append(f"      partidos={p['matches']} (asignados={p['fixtures']}) | "
                 f"tarjetas={p['cards_total']} (A{p['yellow_cards_total']}/R{p['red_cards_total']}/"
                 f"2A{p['second_yellow_total']}) cards_pg={p['cards_pg']} -> entorno {p['card_environment']}")
        L.append(f"      penaltis={p['penalties_total']} (en {p['matches_with_penalty']} partidos) "
                 f"rate={p['penalty_match_rate']} -> entorno {p['penalty_environment']}")
        L.append(f"      confidence={p['confidence']} dq={p['data_quality']} · {p['reason']}")
    L.append("")
    L.append("Predicción futbolística pura, sin terminología de juego. NO toca data/external; "
             "referee_profiles.csv sigue manual/bloqueado.")
    return "\n".join(L)


def build(referees_path=FIXTURE_REFEREES, events_path=FIXTURE_EVENTS, store_dir=STORE_DIR,
          out_csv=OUT_CSV, out_json=OUT_JSON, out_txt=OUT_TXT, write=True):
    refs = load_fixture_referees(referees_path)
    events = load_events(events_path)
    home_away = load_home_away(store_dir)
    profiles = derive_referee_profiles(refs, events, home_away)
    if write:
        pd.DataFrame(profiles, columns=CSV_COLUMNS).to_csv(out_csv, index=False)
        Path(out_json).write_text(json.dumps(profiles, ensure_ascii=False, indent=2), encoding="utf-8")
        Path(out_txt).write_text(render_txt(profiles) + "\n", encoding="utf-8")
    return profiles


def main():
    profiles = build()
    with_sample = sum(1 for p in profiles if p["matches"] > 0)
    print(f"referee profiles auto: {len(profiles)} árbitros ({with_sample} con muestra) -> "
          f"{OUT_CSV.name} / {OUT_JSON.name}")
    for p in sorted(profiles, key=lambda x: -x["matches"])[:8]:
        print(f"  {p['referee_name']:32s} m={p['matches']} cards_pg={p['cards_pg']} "
              f"env={p['card_environment']} conf={p['confidence']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
