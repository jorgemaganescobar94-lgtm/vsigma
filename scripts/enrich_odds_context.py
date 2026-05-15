from __future__ import annotations

from pathlib import Path
from datetime import datetime, timezone
import shutil
import pandas as pd
import numpy as np

from api_football_client import APIFootballClient, APIFootballError


ROOT = Path(__file__).resolve().parents[1]

RAW_MATCHES = ROOT / "data" / "raw" / "matches.csv"
FILTERED_MATCHES = ROOT / "data" / "processed" / "matches_league_filtered.csv"
BACKUP_MATCHES = ROOT / "data" / "raw" / "matches_before_odds_context_backup.csv"

MAX_TIER_RANK_TO_ENRICH = 2


ODDS_COLS = [
    "odds_1_home",
    "odds_1_draw",
    "odds_1_away",
    "odds_btts_yes",
    "odds_btts_no",
    "odds_over_1_5",
    "odds_under_1_5",
    "odds_over_2_5",
    "odds_under_2_5",
    "odds_over_3_5",
    "odds_under_3_5",
    "odds_bookmakers_count",
    "odds_values_count",
    "odds_market_count",
]


def safe_float(value):
    try:
        return float(str(value).replace(",", "."))
    except Exception:
        return np.nan


def update_best(store: dict, key: str, odd_value) -> None:
    odd = safe_float(odd_value)
    if pd.isna(odd):
        return

    current = store.get(key, np.nan)
    if pd.isna(current) or odd > current:
        store[key] = odd


def normalize_text(s) -> str:
    if s is None:
        return ""
    return str(s).strip().lower()


def extract_key_from_bet(bet_name: str, value_name: str) -> str | None:
    bet = normalize_text(bet_name)
    value = normalize_text(value_name)

    # Match Winner / 1X2
    if bet in {"match winner", "winner", "1x2"}:
        if value == "home":
            return "odds_1_home"
        if value == "draw":
            return "odds_1_draw"
        if value == "away":
            return "odds_1_away"

    # BTTS
    if bet in {"both teams to score", "both teams score"}:
        if value == "yes":
            return "odds_btts_yes"
        if value == "no":
            return "odds_btts_no"

    # Over/Under
    if "over/under" in bet or "goals over/under" in bet:
        if value == "over 1.5":
            return "odds_over_1_5"
        if value == "under 1.5":
            return "odds_under_1_5"
        if value == "over 2.5":
            return "odds_over_2_5"
        if value == "under 2.5":
            return "odds_under_2_5"
        if value == "over 3.5":
            return "odds_over_3_5"
        if value == "under 3.5":
            return "odds_under_3_5"

    return None


def parse_odds_payload(payload: dict) -> dict:
    best = {col: np.nan for col in ODDS_COLS}

    response = payload.get("response", [])
    market_names = set()
    bookmakers_seen = 0
    values_seen = 0

    for item in response:
        bookmakers = item.get("bookmakers", [])
        bookmakers_seen += len(bookmakers)

        for bookmaker in bookmakers:
            bets = bookmaker.get("bets", [])

            for bet in bets:
                bet_name = bet.get("name")
                if bet_name:
                    market_names.add(str(bet_name))

                for value in bet.get("values", []):
                    values_seen += 1

                    value_name = value.get("value")
                    odd_value = value.get("odd")

                    key = extract_key_from_bet(bet_name, value_name)
                    if key:
                        update_best(best, key, odd_value)

    best["odds_bookmakers_count"] = bookmakers_seen
    best["odds_values_count"] = values_seen
    best["odds_market_count"] = len(market_names)

    return best


def implied_prob(odd):
    odd = safe_float(odd)
    if pd.isna(odd) or odd <= 0:
        return np.nan
    return round(1.0 / odd, 4)


def main() -> None:
    if not RAW_MATCHES.exists():
        raise FileNotFoundError(f"No existe: {RAW_MATCHES}")

    if not FILTERED_MATCHES.exists():
        raise FileNotFoundError(f"No existe: {FILTERED_MATCHES}")

    raw = pd.read_csv(RAW_MATCHES)
    filtered = pd.read_csv(FILTERED_MATCHES)

    if not BACKUP_MATCHES.exists():
        shutil.copy2(RAW_MATCHES, BACKUP_MATCHES)

    client = APIFootballClient()

    targets = filtered[
        pd.to_numeric(filtered["league_tier_rank"], errors="coerce") <= MAX_TIER_RANK_TO_ENRICH
    ].copy()

    print("\n=== ENRIQUECIMIENTO ODDS CONTEXT ===")
    print(f"Partidos objetivo TIER_1/TIER_2: {len(targets)}")

    ok = 0
    no_data = 0
    errors = 0

    for _, match in targets.iterrows():
        fixture_id = match["fixture_id"]
        date_value = str(match.get("date", ""))

        raw_idx_list = raw.index[raw["fixture_id"] == fixture_id].tolist()
        if not raw_idx_list:
            continue
        raw_idx = raw_idx_list[0]

        try:
            payload = client.odds(fixture=fixture_id)
            parsed = parse_odds_payload(payload)

            found_any = False
            for col, val in parsed.items():
                raw.loc[raw_idx, col] = val
                if col.startswith("odds_") and not pd.isna(val) and col not in {
                    "odds_bookmakers_count", "odds_values_count", "odds_market_count"
                }:
                    found_any = True

            # implied probabilities
            raw.loc[raw_idx, "imp_1_home"] = implied_prob(parsed.get("odds_1_home"))
            raw.loc[raw_idx, "imp_1_draw"] = implied_prob(parsed.get("odds_1_draw"))
            raw.loc[raw_idx, "imp_1_away"] = implied_prob(parsed.get("odds_1_away"))
            raw.loc[raw_idx, "imp_btts_yes"] = implied_prob(parsed.get("odds_btts_yes"))
            raw.loc[raw_idx, "imp_btts_no"] = implied_prob(parsed.get("odds_btts_no"))
            raw.loc[raw_idx, "imp_over_1_5"] = implied_prob(parsed.get("odds_over_1_5"))
            raw.loc[raw_idx, "imp_over_2_5"] = implied_prob(parsed.get("odds_over_2_5"))
            raw.loc[raw_idx, "imp_over_3_5"] = implied_prob(parsed.get("odds_over_3_5"))
            raw.loc[raw_idx, "imp_under_3_5"] = implied_prob(parsed.get("odds_under_3_5"))

            raw.loc[raw_idx, "odds_context_updated_at"] = datetime.now(timezone.utc).isoformat()

            if found_any:
                raw.loc[raw_idx, "odds_context_status"] = "OK"
                ok += 1
                print(f"OK fixture={fixture_id} {match['home_team']} vs {match['away_team']}")
            else:
                raw.loc[raw_idx, "odds_context_status"] = "NO_ODDS_FOUND"
                no_data += 1
                print(f"NO_ODDS fixture={fixture_id} {match['home_team']} vs {match['away_team']} | date={date_value}")

        except APIFootballError as e:
            raw.loc[raw_idx, "odds_context_status"] = "API_ERROR"
            raw.loc[raw_idx, "odds_context_error"] = str(e)
            errors += 1
            print(f"API_ERROR fixture={fixture_id} {match['home_team']} vs {match['away_team']} -> {e}")

        except Exception as e:
            raw.loc[raw_idx, "odds_context_status"] = "ERROR"
            raw.loc[raw_idx, "odds_context_error"] = str(e)
            errors += 1
            print(f"ERROR fixture={fixture_id} {match['home_team']} vs {match['away_team']} -> {e}")

    raw.to_csv(RAW_MATCHES, index=False)

    print("\n=== ODDS CONTEXT COMPLETADO ===")
    print(f"OK: {ok}")
    print(f"NO_ODDS_FOUND: {no_data}")
    print(f"ERRORS: {errors}")
    print(f"CSV actualizado: {RAW_MATCHES}")
    print(f"Backup: {BACKUP_MATCHES}")

    preview_cols = [
        "date", "country", "league", "home_team", "away_team",
        "odds_1_home", "odds_1_draw", "odds_1_away",
        "odds_btts_yes", "odds_btts_no",
        "odds_over_1_5", "odds_over_2_5", "odds_under_3_5",
        "odds_context_status",
    ]
    existing = [c for c in preview_cols if c in raw.columns]

    preview = raw[raw["fixture_id"].isin(targets["fixture_id"])].copy()

    print("\nVista previa odds:")
    if not preview.empty:
        print(preview[existing].head(20).to_string(index=False))
    else:
        print("Vacío")


if __name__ == "__main__":
    main()