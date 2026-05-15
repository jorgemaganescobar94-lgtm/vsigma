from __future__ import annotations

from pathlib import Path
import pandas as pd
import numpy as np


ROOT = Path(__file__).resolve().parents[1]

RAW_MATCHES = ROOT / "data" / "raw" / "matches.csv"
SCORED_CSV = ROOT / "data" / "processed" / "matches_vsigma_scored_v3.csv"
REPORT_CSV = ROOT / "data" / "processed" / "tie_state_adjust_report.csv"


def clip(x, low, high):
    return max(low, min(high, x))


def main() -> None:
    if not RAW_MATCHES.exists():
        raise FileNotFoundError(f"No existe: {RAW_MATCHES}")
    if not SCORED_CSV.exists():
        raise FileNotFoundError(f"No existe: {SCORED_CSV}")

    raw = pd.read_csv(RAW_MATCHES)
    scored = pd.read_csv(SCORED_CSV)

    tie_cols = [
        "fixture_id",
        "is_two_leg_tie",
        "tie_context_status",
        "tie_state_label",
        "tie_home_delta",
        "tie_away_delta",
        "home_trailing_in_tie",
        "away_trailing_in_tie",
        "tie_level_before_second_leg",
    ]
    tie_cols = [c for c in tie_cols if c in raw.columns]

    scored = scored.drop(columns=[c for c in tie_cols if c in scored.columns and c != "fixture_id"], errors="ignore")
    scored = scored.merge(raw[tie_cols], on="fixture_id", how="left")

    tie_defaults = {
        "is_two_leg_tie": 0,
        "tie_context_status": "NOT_TWO_LEG_TIE",
        "tie_state_label": "",
        "tie_home_delta": np.nan,
        "tie_away_delta": np.nan,
        "home_trailing_in_tie": 0,
        "away_trailing_in_tie": 0,
        "tie_level_before_second_leg": 0,
    }
    for col, default in tie_defaults.items():
        if col not in scored.columns:
            scored[col] = default
        else:
            scored[col] = scored[col].fillna(default)

    scored["tie_adjustment_applied"] = 0
    scored["tie_adjustment_note"] = ""

    for idx, row in scored.iterrows():
        if row.get("is_two_leg_tie", 0) != 1:
            continue
        if str(row.get("tie_context_status", "")) != "OK":
            continue

        market_hint = str(row.get("market_family_hint", ""))
        label = str(row.get("tie_state_label", ""))

        vsigma_pre = float(row.get("vsigma_pre_score", 0.0))
        attack_env = float(row.get("attack_environment_score", 0.0))
        team_edge = float(row.get("team_edge_score", 0.0))
        team_edge_raw = float(row.get("team_edge_raw", 0.0))

        note_parts = []

        # If home team is trailing the tie, penalize away-side bias and boost open/home chase scenarios
        if label == "HOME_TRAILING":
            attack_env = clip(attack_env + 2.5, 0.0, 20.0)
            team_edge = clip(team_edge + 2.0, -20.0, 20.0)
            team_edge_raw = team_edge_raw + 1.5
            vsigma_pre += 4.0

            if market_hint == "AWAY_SIDE_OR_AWAY_TEAM_TOTAL_CHECK":
                market_hint = "OVER_OR_BTTS_CHECK"
                note_parts.append("home_trailing_flip_away_to_over")
            else:
                note_parts.append("home_trailing_boost")

        # If away team is trailing the tie, keep away-side logic live or nudge toward away team over / open game
        elif label == "AWAY_TRAILING":
            attack_env = clip(attack_env + 2.0, 0.0, 20.0)
            team_edge = clip(team_edge - 0.5, -20.0, 20.0)
            vsigma_pre += 2.0
            note_parts.append("away_trailing_keep_away_live")

        # If tie is level, slightly prefer open markets over very narrow side assumptions
        elif label == "LEVEL_TIE":
            attack_env = clip(attack_env + 1.0, 0.0, 20.0)
            if market_hint == "AWAY_SIDE_OR_AWAY_TEAM_TOTAL_CHECK":
                market_hint = "OVER_OR_BTTS_CHECK"
                note_parts.append("level_tie_flip_away_to_over")
            else:
                note_parts.append("level_tie_soft_opening")

        scored.at[idx, "attack_environment_score"] = round(attack_env, 2)
        scored.at[idx, "team_edge_score"] = round(team_edge, 2)
        scored.at[idx, "team_edge_raw"] = round(team_edge_raw, 2)
        scored.at[idx, "vsigma_pre_score"] = round(vsigma_pre, 2)
        scored.at[idx, "market_family_hint"] = market_hint
        scored.at[idx, "tie_adjustment_applied"] = 1
        scored.at[idx, "tie_adjustment_note"] = "|".join(note_parts)

    # Rebuild priority after adjustments
    cond_a = scored["vsigma_pre_score"] >= 66
    cond_b = (scored["vsigma_pre_score"] >= 55) & (scored["vsigma_pre_score"] < 66)
    cond_c = (scored["vsigma_pre_score"] >= 48) & (scored["vsigma_pre_score"] < 55)

    scored["vsigma_priority"] = np.select(
        [cond_a, cond_b, cond_c],
        ["A_ANALIZAR_PRIMERO", "B_ANALIZAR", "C_SOLO_SI_BLOQUE_SECO"],
        default="NO_DATA_BLOCKED",
    )

    scored.to_csv(SCORED_CSV, index=False)

    report_cols = [
        "fixture_id",
        "home_team",
        "away_team",
        "tie_state_label",
        "market_family_hint",
        "vsigma_pre_score",
        "vsigma_priority",
        "tie_adjustment_note",
    ]
    scored[report_cols].to_csv(REPORT_CSV, index=False)

    print("\n=== TIE STATE ADJUST SCORES COMPLETADO ===")
    print(f"Archivo score actualizado: {SCORED_CSV}")
    print(f"Reporte: {REPORT_CSV}")
    print("\nResumen:")
    print(scored[report_cols].to_string(index=False))


if __name__ == "__main__":
    main()
