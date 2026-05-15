from __future__ import annotations

import argparse
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

try:
    from api_football_client import APIFootballClient, APIFootballError, CACHE_DB_PATH, build_params_key
except ModuleNotFoundError:
    from scripts.api_football_client import APIFootballClient, APIFootballError, CACHE_DB_PATH, build_params_key


ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = ROOT / "data" / "processed"
DEFAULT_INPUT = PROCESSED_DIR / "vsigma_today_candidate_v2_competition_shortlist.csv"
DEFAULT_OUTPUT = PROCESSED_DIR / "vsigma_today_candidate_v6_predictions_benchmark_enriched.csv"
DEFAULT_REPORT = PROCESSED_DIR / "api_predictions_benchmark_report.csv"

PREDICTION_NUMERIC_COLUMNS = [
    "api_prediction_available_flag",
    "api_prediction_home_prob",
    "api_prediction_draw_prob",
    "api_prediction_away_prob",
    "api_prediction_disagreement_flag",
    "api_prediction_confidence_adjustment",
]

PREDICTION_TEXT_COLUMNS = [
    "api_prediction_quality_flag",
    "api_prediction_winner",
    "api_prediction_advice",
    "api_prediction_over_under_hint",
    "api_prediction_goal_hint",
    "api_prediction_btts_hint",
    "api_prediction_alignment_flag",
    "api_prediction_benchmark_reason",
]

PREDICTION_COLUMNS = [*PREDICTION_NUMERIC_COLUMNS, *PREDICTION_TEXT_COLUMNS]

UNKNOWN_FEATURES = {
    "api_prediction_available_flag": 0,
    "api_prediction_quality_flag": "UNKNOWN",
    "api_prediction_winner": "UNKNOWN",
    "api_prediction_advice": "",
    "api_prediction_home_prob": np.nan,
    "api_prediction_draw_prob": np.nan,
    "api_prediction_away_prob": np.nan,
    "api_prediction_over_under_hint": "UNKNOWN",
    "api_prediction_goal_hint": "UNKNOWN",
    "api_prediction_btts_hint": "UNKNOWN",
    "api_prediction_alignment_flag": "UNKNOWN",
    "api_prediction_disagreement_flag": 0,
    "api_prediction_confidence_adjustment": 0.0,
    "api_prediction_benchmark_reason": "API predictions unavailable; benchmark neutral.",
}


def norm_text(value: object) -> str:
    if pd.isna(value):
        return ""
    return str(value).strip()


def norm_upper(value: object) -> str:
    return norm_text(value).upper()


def safe_int(value: object) -> int | None:
    try:
        if pd.isna(value):
            return None
        return int(float(value))
    except Exception:
        return None


def safe_float(value: object, default: float = 0.0) -> float:
    try:
        if pd.isna(value):
            return default
        return float(value)
    except Exception:
        return default


def parse_percent(value: object) -> float:
    text = norm_text(value).replace("%", "")
    if not text:
        return np.nan
    try:
        num = float(text)
    except Exception:
        return np.nan
    if num > 1.5:
        num /= 100.0
    return round(max(0.0, min(1.0, num)), 6)


def norm_name(value: object) -> str:
    return " ".join(norm_text(value).lower().split())


def infer_winner_side(winner: dict[str, Any], row: pd.Series) -> str:
    name = norm_name(winner.get("name"))
    winner_id = safe_int(winner.get("id"))
    home_id = safe_int(row.get("home_team_id"))
    away_id = safe_int(row.get("away_team_id"))
    home_name = norm_name(row.get("home_team"))
    away_name = norm_name(row.get("away_team"))
    if winner_id is not None and home_id is not None and winner_id == home_id:
        return "HOME"
    if winner_id is not None and away_id is not None and winner_id == away_id:
        return "AWAY"
    if name and home_name and name == home_name:
        return "HOME"
    if name and away_name and name == away_name:
        return "AWAY"
    if "draw" in name:
        return "DRAW"
    return "UNKNOWN"


def parse_over_under_hint(value: object, advice: str = "") -> str:
    text = f"{norm_text(value)} {advice}".lower()
    if "over" in text and ("2.5" in text or "2,5" in text):
        return "OVER_2_5"
    if "under" in text and ("2.5" in text or "2,5" in text):
        return "UNDER_2_5"
    if "over" in text and ("1.5" in text or "1,5" in text):
        return "OVER_1_5"
    if "under" in text and ("3.5" in text or "3,5" in text):
        return "UNDER_3_5"
    if "over" in text:
        return "OVER"
    if "under" in text:
        return "UNDER"
    return "UNKNOWN"


def parse_goal_hint(predictions: dict[str, Any], advice: str, over_under_hint: str) -> str:
    if over_under_hint in {"OVER_2_5", "OVER"}:
        return "HIGH_GOALS"
    if over_under_hint == "OVER_1_5":
        return "MILD_GOALS"
    if over_under_hint in {"UNDER_2_5", "UNDER"}:
        return "LOW_GOALS"
    goals = predictions.get("goals") or {}
    blob = f"{advice} {json.dumps(goals, ensure_ascii=False)} {over_under_hint}".lower()
    if any(token in blob for token in ["under", "low", "-2.5", "0-0", "1-0"]):
        return "LOW_GOALS"
    if any(token in blob for token in ["over_2_5", "over 2.5", "+2.5", "goals", "score"]):
        return "HIGH_GOALS"
    if over_under_hint in {"OVER_1_5", "OVER"}:
        return "MILD_GOALS"
    return "UNKNOWN"


def parse_btts_hint(advice: str) -> str:
    text = advice.lower()
    if "both teams" in text and ("yes" in text or "score" in text):
        return "BTTS_YES"
    if "btts yes" in text:
        return "BTTS_YES"
    if "btts no" in text or ("both teams" in text and "no" in text):
        return "BTTS_NO"
    return "UNKNOWN"


def highest_prob_side(home_prob: float, draw_prob: float, away_prob: float) -> str:
    values = {"HOME": home_prob, "DRAW": draw_prob, "AWAY": away_prob}
    known = {key: value for key, value in values.items() if not pd.isna(value)}
    if not known:
        return "UNKNOWN"
    return max(known, key=known.get)


def parse_prediction_payload(payload: dict[str, Any], row: pd.Series) -> dict[str, Any]:
    response = payload.get("response", []) if isinstance(payload, dict) else []
    if not response:
        return UNKNOWN_FEATURES.copy()

    item = response[0] or {}
    predictions = item.get("predictions") or {}
    percent = predictions.get("percent") or {}
    advice = norm_text(predictions.get("advice"))
    home_prob = parse_percent(percent.get("home"))
    draw_prob = parse_percent(percent.get("draw"))
    away_prob = parse_percent(percent.get("away"))
    winner = infer_winner_side(predictions.get("winner") or {}, row)
    if winner == "UNKNOWN":
        winner = highest_prob_side(home_prob, draw_prob, away_prob)
    over_under_hint = parse_over_under_hint(predictions.get("under_over"), advice)
    goal_hint = parse_goal_hint(predictions, advice, over_under_hint)
    btts_hint = parse_btts_hint(advice)

    known_signal_count = sum(
        [
            winner != "UNKNOWN",
            not pd.isna(home_prob) or not pd.isna(draw_prob) or not pd.isna(away_prob),
            over_under_hint != "UNKNOWN",
            goal_hint != "UNKNOWN",
            btts_hint != "UNKNOWN",
            bool(advice),
        ]
    )
    quality = "FULL" if known_signal_count >= 3 else ("PARTIAL" if known_signal_count >= 1 else "UNKNOWN")
    features = {
        "api_prediction_available_flag": 1 if quality != "UNKNOWN" else 0,
        "api_prediction_quality_flag": quality,
        "api_prediction_winner": winner,
        "api_prediction_advice": advice,
        "api_prediction_home_prob": home_prob,
        "api_prediction_draw_prob": draw_prob,
        "api_prediction_away_prob": away_prob,
        "api_prediction_over_under_hint": over_under_hint,
        "api_prediction_goal_hint": goal_hint,
        "api_prediction_btts_hint": btts_hint,
    }
    features.update(alignment_features(row, features))
    return features


def alignment_features(row: pd.Series, features: dict[str, Any]) -> dict[str, Any]:
    if features.get("api_prediction_quality_flag") == "UNKNOWN":
        return {
            "api_prediction_alignment_flag": "UNKNOWN",
            "api_prediction_disagreement_flag": 0,
            "api_prediction_confidence_adjustment": 0.0,
            "api_prediction_benchmark_reason": "API predictions unavailable; benchmark neutral.",
        }

    market = norm_upper(row.get("market_primary"))
    winner = norm_upper(features.get("api_prediction_winner"))
    over_under = norm_upper(features.get("api_prediction_over_under_hint"))
    goal_hint = norm_upper(features.get("api_prediction_goal_hint"))
    btts_hint = norm_upper(features.get("api_prediction_btts_hint"))
    home_prob = safe_float(features.get("api_prediction_home_prob"), np.nan)
    draw_prob = safe_float(features.get("api_prediction_draw_prob"), np.nan)
    away_prob = safe_float(features.get("api_prediction_away_prob"), np.nan)

    aligned = False
    disagreement = False
    reason = "API prediction benchmark neutral."

    if market == "OVER_2_5":
        aligned = over_under in {"OVER_2_5", "OVER"} or goal_hint == "HIGH_GOALS"
        disagreement = over_under in {"UNDER_2_5", "UNDER"} or goal_hint == "LOW_GOALS"
        reason = "API benchmark compared goals/over signal against vSIGMA OVER_2_5."
    elif market == "OVER_1_5":
        aligned = over_under in {"OVER_2_5", "OVER_1_5", "OVER"} or goal_hint in {"HIGH_GOALS", "MILD_GOALS"}
        disagreement = over_under in {"UNDER_2_5", "UNDER"} and goal_hint == "LOW_GOALS"
        reason = "API benchmark compared mild goals support against vSIGMA OVER_1_5."
    elif market == "UNDER_3_5":
        aligned = over_under in {"UNDER_2_5", "UNDER", "UNDER_3_5"} or goal_hint == "LOW_GOALS"
        disagreement = over_under in {"OVER_2_5", "OVER"} and goal_hint == "HIGH_GOALS"
        reason = "API benchmark compared low-goals support against vSIGMA UNDER_3_5."
    elif market == "BTTS_YES":
        aligned = btts_hint == "BTTS_YES" or goal_hint == "HIGH_GOALS"
        disagreement = btts_hint == "BTTS_NO" or goal_hint == "LOW_GOALS"
        reason = "API benchmark compared both-teams-scoring support against vSIGMA BTTS_YES."
    elif market in {"HOME_WIN", "HOME_DNB"}:
        aligned = winner == "HOME" or (
            not pd.isna(home_prob)
            and not pd.isna(away_prob)
            and home_prob >= away_prob + 0.08
            and (pd.isna(draw_prob) or home_prob >= draw_prob + 0.04)
        )
        disagreement = winner in {"AWAY", "DRAW"} or (
            not pd.isna(home_prob)
            and max(away_prob if not pd.isna(away_prob) else 0.0, draw_prob if not pd.isna(draw_prob) else 0.0) >= home_prob + 0.08
        )
        reason = "API benchmark compared side winner/percent against vSIGMA home side."
    elif market in {"AWAY_WIN", "AWAY_DNB"}:
        aligned = winner == "AWAY" or (
            not pd.isna(away_prob)
            and not pd.isna(home_prob)
            and away_prob >= home_prob + 0.08
            and (pd.isna(draw_prob) or away_prob >= draw_prob + 0.04)
        )
        disagreement = winner in {"HOME", "DRAW"} or (
            not pd.isna(away_prob)
            and max(home_prob if not pd.isna(home_prob) else 0.0, draw_prob if not pd.isna(draw_prob) else 0.0) >= away_prob + 0.08
        )
        reason = "API benchmark compared side winner/percent against vSIGMA away side."

    if aligned and not disagreement:
        return {
            "api_prediction_alignment_flag": "ALIGNED",
            "api_prediction_disagreement_flag": 0,
            "api_prediction_confidence_adjustment": 1.5,
            "api_prediction_benchmark_reason": reason + " External signal aligned; modest confidence support only.",
        }
    if disagreement and not aligned:
        return {
            "api_prediction_alignment_flag": "DISAGREEMENT",
            "api_prediction_disagreement_flag": 1,
            "api_prediction_confidence_adjustment": -3.0,
            "api_prediction_benchmark_reason": reason + " External signal disagreed; modest confidence caution only.",
        }
    return {
        "api_prediction_alignment_flag": "NEUTRAL",
        "api_prediction_disagreement_flag": 0,
        "api_prediction_confidence_adjustment": 0.0,
        "api_prediction_benchmark_reason": reason,
    }


def cached_prediction_payload(fixture_id: int, cache_db_path: Path = CACHE_DB_PATH) -> dict[str, Any] | None:
    if not cache_db_path.exists():
        return None
    params_key = build_params_key("/predictions", {"fixture": fixture_id})
    with sqlite3.connect(cache_db_path) as conn:
        row = conn.execute(
            "SELECT response_json, expires_at_utc FROM api_cache WHERE params_key = ?",
            (params_key,),
        ).fetchone()
    if not row:
        return None
    response_json, expires_at_utc = row
    try:
        expires_at = datetime.fromisoformat(expires_at_utc)
        if datetime.now(timezone.utc) > expires_at:
            return None
        return json.loads(response_json)
    except Exception:
        return None


def fetch_prediction_payload(
    fixture_id: int,
    client: APIFootballClient | None,
    counters: dict[str, int],
    *,
    use_api: bool,
    force_refresh: bool = False,
) -> dict[str, Any] | None:
    cached = cached_prediction_payload(fixture_id)
    if cached is not None and not force_refresh:
        counters["cache_hits"] += 1
        return cached
    if not use_api or client is None:
        counters["cache_misses"] += 1
        return None

    counters["api_calls_made"] += 1
    try:
        return client.predictions(fixture_id, use_cache=True, force_refresh=force_refresh)
    except APIFootballError as exc:
        counters["api_errors"] += 1
        if exc.is_plan_limit:
            counters["plan_limit_errors"] += 1
        return None
    except Exception:
        counters["api_errors"] += 1
        return None


def add_api_prediction_benchmark_fields(
    df: pd.DataFrame,
    *,
    use_api: bool = False,
    force_refresh: bool = False,
    payload_by_fixture: dict[int, dict[str, Any]] | None = None,
) -> tuple[pd.DataFrame, dict[str, int]]:
    out = df.copy()
    counters = {
        "rows_processed": int(len(out)),
        "cache_hits": 0,
        "cache_misses": 0,
        "api_calls_made": 0,
        "api_errors": 0,
        "plan_limit_errors": 0,
        "available_rows": 0,
        "aligned_rows": 0,
        "disagreement_rows": 0,
    }
    if out.empty:
        for col in PREDICTION_NUMERIC_COLUMNS:
            if col not in out.columns:
                out[col] = pd.Series(dtype=float)
        for col in PREDICTION_TEXT_COLUMNS:
            if col not in out.columns:
                out[col] = pd.Series(dtype=object)
        return out, counters

    client: APIFootballClient | None = None
    if use_api:
        try:
            client = APIFootballClient()
        except Exception:
            counters["api_errors"] += 1
            client = None

    rows: list[dict[str, Any]] = []
    for _, row in out.iterrows():
        fixture_id = safe_int(row.get("fixture_id"))
        payload = payload_by_fixture.get(fixture_id) if payload_by_fixture and fixture_id is not None else None
        if payload is None and fixture_id is not None:
            payload = fetch_prediction_payload(
                fixture_id,
                client,
                counters,
                use_api=use_api,
                force_refresh=force_refresh,
            )
        features = parse_prediction_payload(payload or {"response": []}, row)
        rows.append(features)

    features_df = pd.DataFrame(rows, index=out.index)
    out = out.drop(columns=[col for col in PREDICTION_COLUMNS if col in out.columns], errors="ignore")
    out = pd.concat([out, features_df], axis=1)
    counters["available_rows"] = int(pd.to_numeric(out["api_prediction_available_flag"], errors="coerce").fillna(0).eq(1).sum())
    counters["aligned_rows"] = int(out["api_prediction_alignment_flag"].map(norm_upper).eq("ALIGNED").sum())
    counters["disagreement_rows"] = int(out["api_prediction_alignment_flag"].map(norm_upper).eq("DISAGREEMENT").sum())
    return out, counters


def build_report(counters: dict[str, int], enriched: pd.DataFrame) -> pd.DataFrame:
    quality = enriched.get("api_prediction_quality_flag", pd.Series(dtype=object)).map(norm_upper)
    alignment = enriched.get("api_prediction_alignment_flag", pd.Series(dtype=object)).map(norm_upper)
    return pd.DataFrame(
        [
            {
                **counters,
                "full_rows": int(quality.eq("FULL").sum()),
                "partial_rows": int(quality.eq("PARTIAL").sum()),
                "unknown_rows": int(quality.eq("UNKNOWN").sum()),
                "neutral_rows": int(alignment.eq("NEUTRAL").sum()),
                "generated_at_utc": datetime.now(timezone.utc).isoformat(),
            }
        ]
    )


def enrich_file(
    input_path: Path = DEFAULT_INPUT,
    output_path: Path = DEFAULT_OUTPUT,
    report_path: Path = DEFAULT_REPORT,
    *,
    use_api: bool = False,
    force_refresh: bool = False,
) -> tuple[pd.DataFrame, dict[str, int]]:
    if not input_path.exists():
        raise FileNotFoundError(f"Missing API predictions benchmark input: {input_path}")
    source = pd.read_csv(input_path)
    enriched, counters = add_api_prediction_benchmark_fields(source, use_api=use_api, force_refresh=force_refresh)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    enriched.to_csv(output_path, index=False)
    build_report(counters, enriched).to_csv(report_path, index=False)
    return enriched, counters


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Add API Predictions benchmark fields to candidate rows.")
    parser.add_argument("--input", default=str(DEFAULT_INPUT))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--report", default=str(DEFAULT_REPORT))
    parser.add_argument("--use-api", action="store_true", help="Fetch missing predictions from the API.")
    parser.add_argument("--force-refresh", action="store_true", help="Force-refresh prediction cache.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    enriched, counters = enrich_file(
        Path(args.input),
        Path(args.output),
        Path(args.report),
        use_api=args.use_api,
        force_refresh=args.force_refresh,
    )
    print("\n=== API PREDICTIONS BENCHMARK ENRICHMENT COMPLETADO ===")
    print(f"Rows processed: {len(enriched)}")
    print(f"Available rows: {counters['available_rows']}")
    print(f"Aligned: {counters['aligned_rows']} | disagreement: {counters['disagreement_rows']}")
    print(f"API calls: {counters['api_calls_made']} | cache hits: {counters['cache_hits']} | errors: {counters['api_errors']}")
    print(f"Output: {Path(args.output)}")
    print(f"Report: {Path(args.report)}")


if __name__ == "__main__":
    main()
