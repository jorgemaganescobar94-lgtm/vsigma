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
BACKUP_MATCHES = ROOT / "data" / "raw" / "matches_before_odds_context_v3_backup.csv"

MAX_TIER_RANK_TO_ENRICH = 2

BET_MATCH_WINNER = 1
BET_GOALS_OU = 5
BET_BTTS = 8
BET_DOUBLE_CHANCE = 12
BET_HOME_NO_BET = 206
BET_AWAY_NO_BET = 207


def safe_float(value):
    try:
        return float(str(value).replace(",", "."))
    except Exception:
        return np.nan


def implied_prob(odd):
    odd = safe_float(odd)
    if pd.isna(odd) or odd <= 0:
        return np.nan
    return round(1.0 / odd, 4)


def normalize_text(value) -> str:
    if value is None:
        return ""
    return str(value).strip().lower()


def update_best(best: dict, key: str, odd_value):
    odd = safe_float(odd_value)
    if pd.isna(odd):
        return

    current = best.get(key, np.nan)
    if pd.isna(current) or odd > current:
        best[key] = odd


def parse_odds_payload_by_bet_id(payload: dict) -> dict:
    best = {
        "odds_1_home_v3": np.nan,
        "odds_1_draw_v3": np.nan,
        "odds_1_away_v3": np.nan,
        "odds_btts_yes_v3": np.nan,
        "odds_btts_no_v3": np.nan,
        "odds_over_1_5_v3": np.nan,
        "odds_under_1_5_v3": np.nan,
        "odds_over_2_5_v3": np.nan,
        "odds_under_2_5_v3": np.nan,
        "odds_over_3_5_v3": np.nan,
        "odds_under_3_5_v3": np.nan,
        "odds_dc_1x_v3": np.nan,
        "odds_dc_x2_v3": np.nan,
        "odds_dc_12_v3": np.nan,
        "odds_home_dnb_v3": np.nan,
        "odds_away_dnb_v3": np.nan,
        "odds_bookmakers_count_v3": 0,
        "odds_market_count_v3": 0,
        "odds_values_count_v3": 0,
    }

    market_ids_seen = set()
    bookmakers_count = 0
    values_count = 0

    for item in payload.get("response", []):
        bookmakers = item.get("bookmakers", [])
        bookmakers_count += len(bookmakers)

        for bookmaker in bookmakers:
            for bet in bookmaker.get("bets", []):
                bet_id = bet.get("id")
                market_ids_seen.add(bet_id)

                for value in bet.get("values", []):
                    values_count += 1
                    val_name = normalize_text(value.get("value"))
                    odd = value.get("odd")

                    if bet_id == BET_MATCH_WINNER:
                        if val_name == "home":
                            update_best(best, "odds_1_home_v3", odd)
                        elif val_name == "draw":
                            update_best(best, "odds_1_draw_v3", odd)
                        elif val_name == "away":
                            update_best(best, "odds_1_away_v3", odd)

                    elif bet_id == BET_BTTS:
                        if val_name == "yes":
                            update_best(best, "odds_btts_yes_v3", odd)
                        elif val_name == "no":
                            update_best(best, "odds_btts_no_v3", odd)

                    elif bet_id == BET_GOALS_OU:
                        mapping = {
                            "over 1.5": "odds_over_1_5_v3",
                            "under 1.5": "odds_under_1_5_v3",
                            "over 2.5": "odds_over_2_5_v3",
                            "under 2.5": "odds_under_2_5_v3",
                            "over 3.5": "odds_over_3_5_v3",
                            "under 3.5": "odds_under_3_5_v3",
                        }
                        key = mapping.get(val_name)
                        if key:
                            update_best(best, key, odd)

                    elif bet_id == BET_DOUBLE_CHANCE:
                        if val_name == "1x":
                            update_best(best, "odds_dc_1x_v3", odd)
                        elif val_name == "x2":
                            update_best(best, "odds_dc_x2_v3", odd)
                        elif val_name == "12":
                            update_best(best, "odds_dc_12_v3", odd)

                    elif bet_id == BET_HOME_NO_BET:
                        update_best(best, "odds_home_dnb_v3", odd)

                    elif bet_id == BET_AWAY_NO_BET:
                        update_best(best, "odds_away_dnb_v3", odd)

    best["odds_bookmakers_count_v3"] = bookmakers_count
    best["odds_market_count_v3"] = len(market_ids_seen)
    best["odds_values_count_v3"] = values_count

    return best


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

    print("\n=== ENRIQUECIMIENTO ODDS CONTEXT v3 ===")
    print(f"Partidos objetivo TIER_1/TIER_2: {len(targets)}")

    ok = 0
    no_data = 0
    errors = 0

    for _, match in targets.iterrows():
        fixture_id = match["fixture_id"]

        raw_idx_list = raw.index[raw["fixture_id"] == fixture_id].tolist()
        if not raw_idx_list:
            continue
        raw_idx = raw_idx_list[0]

        try:
            payload = client.odds(fixture=fixture_id)
            parsed = parse_odds_payload_by_bet_id(payload)

            found_any = False
            for col, val in parsed.items():
                raw.loc[raw_idx, col] = val
                if col.startswith("odds_") and not pd.isna(val) and "count" not in col:
                    found_any = True

            prob_cols = [
                "odds_1_home_v3", "odds_1_draw_v3", "odds_1_away_v3",
                "odds_btts_yes_v3", "odds_btts_no_v3",
                "odds_over_1_5_v3", "odds_under_1_5_v3",
                "odds_over_2_5_v3", "odds_under_2_5_v3",
                "odds_over_3_5_v3", "odds_under_3_5_v3",
                "odds_dc_1x_v3", "odds_dc_x2_v3", "odds_dc_12_v3",
                "odds_home_dnb_v3", "odds_away_dnb_v3",
            ]

            for col in prob_cols:
                raw.loc[raw_idx, f"imp_{col.replace('odds_', '').replace('_v3', '')}"] = implied_prob(parsed.get(col))

            raw.loc[raw_idx, "odds_context_v3_updated_at"] = datetime.now(timezone.utc).isoformat()

            if found_any:
                raw.loc[raw_idx, "odds_context_v3_status"] = "OK"
                ok += 1
                print(f"OK fixture={fixture_id} {match['home_team']} vs {match['away_team']}")
            else:
                raw.loc[raw_idx, "odds_context_v3_status"] = "NO_ODDS_FOUND"
                no_data += 1
                print(f"NO_ODDS fixture={fixture_id} {match['home_team']} vs {match['away_team']}")

        except APIFootballError as e:
            raw.loc[raw_idx, "odds_context_v3_status"] = "API_ERROR"
            raw.loc[raw_idx, "odds_context_v3_error"] = str(e)
            errors += 1
            print(f"API_ERROR fixture={fixture_id} {match['home_team']} vs {match['away_team']} -> {e}")

        except Exception as e:
            raw.loc[raw_idx, "odds_context_v3_status"] = "ERROR"
            raw.loc[raw_idx, "odds_context_v3_error"] = str(e)
            errors += 1
            print(f"ERROR fixture={fixture_id} {match['home_team']} vs {match['away_team']} -> {e}")

    raw.to_csv(RAW_MATCHES, index=False)

    print("\n=== ODDS CONTEXT v3 COMPLETADO ===")
    print(f"OK: {ok}")
    print(f"NO_ODDS_FOUND: {no_data}")
    print(f"ERRORS: {errors}")
    print(f"CSV actualizado: {RAW_MATCHES}")
    print(f"Backup: {BACKUP_MATCHES}")

    preview_cols = [
        "date", "country", "league", "home_team", "away_team",
        "odds_1_home_v3", "odds_1_draw_v3", "odds_1_away_v3",
        "odds_dc_1x_v3", "odds_dc_x2_v3",
        "odds_home_dnb_v3", "odds_away_dnb_v3",
        "odds_btts_yes_v3", "odds_btts_no_v3",
        "odds_over_1_5_v3", "odds_over_2_5_v3", "odds_under_3_5_v3",
        "odds_context_v3_status",
    ]
    existing = [c for c in preview_cols if c in raw.columns]

    preview = raw[raw["fixture_id"].isin(targets["fixture_id"])].copy()

    print("\nVista previa odds v3:")
    if not preview.empty:
        print(preview[existing].head(20).to_string(index=False))
    else:
        print("Vacío")


if __name__ == "__main__":
    main()