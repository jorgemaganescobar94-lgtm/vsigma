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
BACKUP_MATCHES = ROOT / "data" / "raw" / "matches_before_odds_context_v2_backup.csv"

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


def parse_match_winner(payload: dict) -> dict:
    best = {
        "odds_1_home_v2": np.nan,
        "odds_1_draw_v2": np.nan,
        "odds_1_away_v2": np.nan,
    }

    for item in payload.get("response", []):
        for bookmaker in item.get("bookmakers", []):
            for bet in bookmaker.get("bets", []):
                for value in bet.get("values", []):
                    name = normalize_text(value.get("value"))
                    odd = value.get("odd")

                    if name == "home":
                        update_best(best, "odds_1_home_v2", odd)
                    elif name == "draw":
                        update_best(best, "odds_1_draw_v2", odd)
                    elif name == "away":
                        update_best(best, "odds_1_away_v2", odd)

    return best


def parse_btts(payload: dict) -> dict:
    best = {
        "odds_btts_yes_v2": np.nan,
        "odds_btts_no_v2": np.nan,
    }

    for item in payload.get("response", []):
        for bookmaker in item.get("bookmakers", []):
            for bet in bookmaker.get("bets", []):
                for value in bet.get("values", []):
                    name = normalize_text(value.get("value"))
                    odd = value.get("odd")

                    if name == "yes":
                        update_best(best, "odds_btts_yes_v2", odd)
                    elif name == "no":
                        update_best(best, "odds_btts_no_v2", odd)

    return best


def parse_goals_ou(payload: dict) -> dict:
    best = {
        "odds_over_1_5_v2": np.nan,
        "odds_under_1_5_v2": np.nan,
        "odds_over_2_5_v2": np.nan,
        "odds_under_2_5_v2": np.nan,
        "odds_over_3_5_v2": np.nan,
        "odds_under_3_5_v2": np.nan,
    }

    for item in payload.get("response", []):
        for bookmaker in item.get("bookmakers", []):
            for bet in bookmaker.get("bets", []):
                for value in bet.get("values", []):
                    name = normalize_text(value.get("value"))
                    odd = value.get("odd")

                    mapping = {
                        "over 1.5": "odds_over_1_5_v2",
                        "under 1.5": "odds_under_1_5_v2",
                        "over 2.5": "odds_over_2_5_v2",
                        "under 2.5": "odds_under_2_5_v2",
                        "over 3.5": "odds_over_3_5_v2",
                        "under 3.5": "odds_under_3_5_v2",
                    }

                    key = mapping.get(name)
                    if key:
                        update_best(best, key, odd)

    return best


def parse_double_chance(payload: dict) -> dict:
    best = {
        "odds_dc_1x_v2": np.nan,
        "odds_dc_x2_v2": np.nan,
        "odds_dc_12_v2": np.nan,
    }

    for item in payload.get("response", []):
        for bookmaker in item.get("bookmakers", []):
            for bet in bookmaker.get("bets", []):
                for value in bet.get("values", []):
                    name = normalize_text(value.get("value"))
                    odd = value.get("odd")

                    if name == "1x":
                        update_best(best, "odds_dc_1x_v2", odd)
                    elif name == "x2":
                        update_best(best, "odds_dc_x2_v2", odd)
                    elif name == "12":
                        update_best(best, "odds_dc_12_v2", odd)

    return best


def parse_no_bet(payload: dict, side: str) -> dict:
    key = "odds_home_dnb_v2" if side == "home" else "odds_away_dnb_v2"
    best = {key: np.nan}

    for item in payload.get("response", []):
        for bookmaker in item.get("bookmakers", []):
            for bet in bookmaker.get("bets", []):
                for value in bet.get("values", []):
                    odd = value.get("odd")
                    update_best(best, key, odd)

    return best


def merge_dicts(*dicts) -> dict:
    out = {}
    for d in dicts:
        out.update(d)
    return out


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

    print("\n=== ENRIQUECIMIENTO ODDS CONTEXT v2 ===")
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
            payload_match = client.odds(fixture=fixture_id, bet=BET_MATCH_WINNER, ttl_hours=1)
            payload_goals = client.odds(fixture=fixture_id, bet=BET_GOALS_OU, ttl_hours=1)
            payload_btts = client.odds(fixture=fixture_id, bet=BET_BTTS, ttl_hours=1)
            payload_dc = client.odds(fixture=fixture_id, bet=BET_DOUBLE_CHANCE, ttl_hours=1)
            payload_home_dnb = client.odds(fixture=fixture_id, bet=BET_HOME_NO_BET, ttl_hours=1)
            payload_away_dnb = client.odds(fixture=fixture_id, bet=BET_AWAY_NO_BET, ttl_hours=1)

            parsed = merge_dicts(
                parse_match_winner(payload_match),
                parse_goals_ou(payload_goals),
                parse_btts(payload_btts),
                parse_double_chance(payload_dc),
                parse_no_bet(payload_home_dnb, "home"),
                parse_no_bet(payload_away_dnb, "away"),
            )

            found_any = False
            for col, val in parsed.items():
                raw.loc[raw_idx, col] = val
                if not pd.isna(val):
                    found_any = True

            # implied probs
            for col in [
                "odds_1_home_v2", "odds_1_draw_v2", "odds_1_away_v2",
                "odds_btts_yes_v2", "odds_btts_no_v2",
                "odds_over_1_5_v2", "odds_under_1_5_v2",
                "odds_over_2_5_v2", "odds_under_2_5_v2",
                "odds_over_3_5_v2", "odds_under_3_5_v2",
                "odds_dc_1x_v2", "odds_dc_x2_v2", "odds_dc_12_v2",
                "odds_home_dnb_v2", "odds_away_dnb_v2",
            ]:
                raw.loc[raw_idx, f"imp_{col.replace('odds_', '').replace('_v2', '')}"] = implied_prob(parsed.get(col))

            raw.loc[raw_idx, "odds_context_v2_updated_at"] = datetime.now(timezone.utc).isoformat()

            if found_any:
                raw.loc[raw_idx, "odds_context_v2_status"] = "OK"
                ok += 1
                print(f"OK fixture={fixture_id} {match['home_team']} vs {match['away_team']}")
            else:
                raw.loc[raw_idx, "odds_context_v2_status"] = "NO_ODDS_FOUND"
                no_data += 1
                print(f"NO_ODDS fixture={fixture_id} {match['home_team']} vs {match['away_team']}")

        except APIFootballError as e:
            raw.loc[raw_idx, "odds_context_v2_status"] = "API_ERROR"
            raw.loc[raw_idx, "odds_context_v2_error"] = str(e)
            errors += 1
            print(f"API_ERROR fixture={fixture_id} {match['home_team']} vs {match['away_team']} -> {e}")

        except Exception as e:
            raw.loc[raw_idx, "odds_context_v2_status"] = "ERROR"
            raw.loc[raw_idx, "odds_context_v2_error"] = str(e)
            errors += 1
            print(f"ERROR fixture={fixture_id} {match['home_team']} vs {match['away_team']} -> {e}")

    raw.to_csv(RAW_MATCHES, index=False)

    print("\n=== ODDS CONTEXT v2 COMPLETADO ===")
    print(f"OK: {ok}")
    print(f"NO_ODDS_FOUND: {no_data}")
    print(f"ERRORS: {errors}")
    print(f"CSV actualizado: {RAW_MATCHES}")
    print(f"Backup: {BACKUP_MATCHES}")

    preview_cols = [
        "date", "country", "league", "home_team", "away_team",
        "odds_1_home_v2", "odds_1_draw_v2", "odds_1_away_v2",
        "odds_dc_1x_v2", "odds_dc_x2_v2",
        "odds_home_dnb_v2", "odds_away_dnb_v2",
        "odds_btts_yes_v2", "odds_btts_no_v2",
        "odds_over_1_5_v2", "odds_over_2_5_v2", "odds_under_3_5_v2",
        "odds_context_v2_status",
    ]
    existing = [c for c in preview_cols if c in raw.columns]

    preview = raw[raw["fixture_id"].isin(targets["fixture_id"])].copy()

    print("\nVista previa odds v2:")
    if not preview.empty:
        print(preview[existing].head(20).to_string(index=False))
    else:
        print("Vacío")


if __name__ == "__main__":
    main()