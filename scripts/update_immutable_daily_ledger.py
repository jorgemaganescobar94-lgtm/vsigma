from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

try:
    from daily_hardening import PROCESSED_DIR, TODAY_DIR, format_markdown_table, read_csv_lenient, split_fresh_stale_rows
except ModuleNotFoundError:
    from scripts.daily_hardening import PROCESSED_DIR, TODAY_DIR, format_markdown_table, read_csv_lenient, split_fresh_stale_rows


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "config" / "vsigma_experiment_registry.json"
LEDGER_DIR = PROCESSED_DIR / "ledger"
LEDGER_CSV = LEDGER_DIR / "vsigma_immutable_daily_pick_ledger.csv"
LEDGER_JSONL = LEDGER_DIR / "vsigma_immutable_daily_pick_ledger.jsonl"
DAILY_REPORT = LEDGER_DIR / "vsigma_ledger_daily_report.md"

EXPERIMENT_SOURCES = [
    {
        "experiment_id": "OFFICIAL_BASELINE",
        "candidate_version": "OFFICIAL_BASELINE",
        "top_file": "vsigma_today_competition_top.csv",
        "result_file": "vsigma_execution_shortlist_results_ledger.csv",
        "is_official_pick": 1,
        "is_shadow_pick": 0,
    },
    {
        "experiment_id": "CANDIDATE_V2_SCHEDULE_ANOMALY",
        "candidate_version": "CANDIDATE_V2",
        "top_file": "vsigma_today_candidate_v2_competition_top.csv",
        "result_file": "vsigma_today_candidate_v2_results_ledger.csv",
        "is_official_pick": 0,
        "is_shadow_pick": 1,
    },
    {
        "experiment_id": "CANDIDATE_V3_ODDS_DEPTH",
        "candidate_version": "CANDIDATE_V3",
        "top_file": "vsigma_today_candidate_v3_competition_top.csv",
        "result_file": "vsigma_today_candidate_v3_results_ledger.csv",
        "is_official_pick": 0,
        "is_shadow_pick": 1,
    },
    {
        "experiment_id": "CANDIDATE_V4_O25_FIREWALL",
        "candidate_version": "CANDIDATE_V4",
        "top_file": "vsigma_today_candidate_v4_competition_top.csv",
        "result_file": "vsigma_today_candidate_v4_results_ledger.csv",
        "is_official_pick": 0,
        "is_shadow_pick": 1,
    },
    {
        "experiment_id": "CANDIDATE_V5_PLAYER_IMPACT",
        "candidate_version": "CANDIDATE_V5",
        "top_file": "vsigma_today_candidate_v5_competition_top.csv",
        "result_file": "vsigma_today_candidate_v5_results_ledger.csv",
        "is_official_pick": 0,
        "is_shadow_pick": 1,
    },
    {
        "experiment_id": "CANDIDATE_V6_API_PREDICTIONS",
        "candidate_version": "CANDIDATE_V6",
        "top_file": "vsigma_today_candidate_v6_competition_top.csv",
        "result_file": "vsigma_today_candidate_v6_results_ledger.csv",
        "is_official_pick": 0,
        "is_shadow_pick": 1,
    },
    {
        "experiment_id": "CANDIDATE_V7_PRICE_DISCIPLINE",
        "candidate_version": "CANDIDATE_V7",
        "top_file": "vsigma_today_candidate_v7_competition_top.csv",
        "waiting_file": "vsigma_today_candidate_v7_competition_shortlist.csv",
        "result_file": "vsigma_today_candidate_v7_results_ledger.csv",
        "is_official_pick": 0,
        "is_shadow_pick": 1,
    },
]

LEDGER_COLUMNS = [
    "ledger_id",
    "target_date",
    "generated_at",
    "pipeline_stage",
    "experiment_id",
    "candidate_version",
    "is_official_pick",
    "is_shadow_pick",
    "fixture_id",
    "league",
    "home_team",
    "away_team",
    "market_primary",
    "market_alt",
    "rank",
    "calibrated_probability",
    "raw_probability",
    "confidence_score",
    "edge",
    "selection_score",
    "execution_score",
    "reason_tags",
    "risk_tags",
    "forecast_score_main",
    "forecast_score_alt",
    "forecast_home_xg_range",
    "forecast_away_xg_range",
    "forecast_pick_path",
    "forecast_pick_breaker",
    "prelock_status",
    "prelock_decision",
    "prelock_decision_reason",
    "price_discipline_decision",
    "price_discipline_min_edge_required",
    "price_discipline_actual_edge",
    "price_discipline_edge_surplus",
    "price_discipline_drift_status",
    "clv_direction",
    "clv_delta",
    "result_status",
    "result",
    "profit_units",
    "roi_contribution",
    "post_verdict",
    "source_file",
    "source_file_hash",
    "ledger_row_hash",
    "record_status",
]


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def normalize_text(value: object) -> str:
    if pd.isna(value):
        return ""
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value).strip()


def first_value(row: pd.Series | dict[str, Any], names: list[str], default: object = "") -> object:
    for name in names:
        if name in row:
            value = row[name]
            if not pd.isna(value) and normalize_text(value) != "":
                return value
    return default


def parse_float(value: object, default: float | None = None) -> float | None:
    try:
        if pd.isna(value) or normalize_text(value) == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def stable_hash(parts: list[object], length: int = 24) -> str:
    text = "|".join(normalize_text(part) for part in parts)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:length]


def file_hash(path: Path) -> str:
    if not path.exists() or not path.is_file():
        return ""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_experiment_registry(path: Path = REGISTRY_PATH) -> dict[str, dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    experiments = payload.get("experiments", [])
    return {str(item["experiment_id"]): item for item in experiments}


def read_ledger(path: Path | None = None) -> pd.DataFrame:
    path = path or LEDGER_CSV
    if not path.exists() or path.stat().st_size == 0:
        return pd.DataFrame(columns=LEDGER_COLUMNS)
    try:
        df = pd.read_csv(path, dtype=str)
    except pd.errors.EmptyDataError:
        return pd.DataFrame(columns=LEDGER_COLUMNS)
    for column in LEDGER_COLUMNS:
        if column not in df.columns:
            df[column] = ""
    return df[LEDGER_COLUMNS].copy()


def write_ledger(df: pd.DataFrame, path: Path | None = None) -> None:
    path = path or LEDGER_CSV
    path.parent.mkdir(parents=True, exist_ok=True)
    out = df.copy()
    for column in LEDGER_COLUMNS:
        if column not in out.columns:
            out[column] = ""
    out = out[LEDGER_COLUMNS].fillna("")
    out.to_csv(path, index=False)


def append_events(events: list[dict[str, object]], path: Path | None = None) -> None:
    path = path or LEDGER_JSONL
    if not events:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        for event in events:
            handle.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")


def forecast_lookup(processed_dir: Path) -> dict[tuple[str, str], dict[str, object]]:
    forecasts = read_csv_lenient(processed_dir / "vsigma_today_match_script_forecasts.csv")
    lookup: dict[tuple[str, str], dict[str, object]] = {}
    if forecasts.empty:
        return lookup
    for _, row in forecasts.iterrows():
        key = (normalize_text(row.get("fixture_id")), normalize_text(row.get("market_primary")).upper())
        lookup[key] = row.to_dict()
    return lookup


def ledger_id(target_date: str, experiment_id: str, fixture_id: object, market_primary: object) -> str:
    fixture = normalize_text(fixture_id) or "NO_FIXTURE"
    market = normalize_text(market_primary).upper() or "NO_BET"
    return stable_hash([target_date, experiment_id, fixture, market], 32)


def reason_tags(row: pd.Series) -> str:
    values = []
    for column in ["accuracy_mode_reason", "pick_main_why", "pick_confirmation_layers", "reason_1", "reason_2", "reason_3"]:
        value = normalize_text(row.get(column))
        if value:
            values.append(value)
    return "; ".join(dict.fromkeys(values))


def risk_tags(row: pd.Series) -> str:
    values = []
    for column in ["accuracy_primary_risk", "pick_primary_risk", "pick_failure_mode", "execution_fragility_reason"]:
        value = normalize_text(row.get(column))
        if value:
            values.append(value)
    return "; ".join(dict.fromkeys(values))


def make_pick_record(
    row: pd.Series,
    source: dict[str, Any],
    source_path: Path,
    target_date: str,
    generated_at: str,
    stage: str,
    forecasts: dict[tuple[str, str], dict[str, object]],
) -> dict[str, object]:
    fixture_id = first_value(row, ["fixture_id"])
    market = normalize_text(first_value(row, ["market_primary"])).upper()
    forecast = forecasts.get((normalize_text(fixture_id), market), {})
    price_decision = normalize_text(first_value(row, ["price_discipline_decision"])).upper()
    prelock_decision = "WAITING_FOR_PRELOCK" if price_decision == "PRICE_NEEDS_PRELOCK_CONFIRMATION" else ""
    record = {
        "ledger_id": ledger_id(target_date, source["experiment_id"], fixture_id, market),
        "target_date": target_date,
        "generated_at": generated_at,
        "pipeline_stage": stage,
        "experiment_id": source["experiment_id"],
        "candidate_version": source["candidate_version"],
        "is_official_pick": source["is_official_pick"],
        "is_shadow_pick": source["is_shadow_pick"],
        "fixture_id": normalize_text(fixture_id),
        "league": first_value(row, ["league"]),
        "home_team": first_value(row, ["home_team"]),
        "away_team": first_value(row, ["away_team"]),
        "market_primary": market,
        "market_alt": first_value(row, ["market_alt"]),
        "rank": first_value(row, ["accuracy_mode_rank", "competition_pick_rank", "execution_rank", "shortlist_rank"]),
        "calibrated_probability": first_value(row, ["competition_calibrated_prob", "calibrated_probability"]),
        "raw_probability": first_value(row, ["competition_raw_prob", "primary_model_prob", "raw_probability"]),
        "confidence_score": first_value(row, ["accuracy_confidence_score", "confidence_score"]),
        "edge": first_value(row, ["primary_edge", "edge"]),
        "selection_score": first_value(row, ["selection_score"]),
        "execution_score": first_value(row, ["execution_score"]),
        "reason_tags": reason_tags(row),
        "risk_tags": risk_tags(row),
        "forecast_score_main": forecast.get("predicted_score_main", ""),
        "forecast_score_alt": forecast.get("predicted_score_alt", ""),
        "forecast_home_xg_range": forecast.get("predicted_home_xg_range", ""),
        "forecast_away_xg_range": forecast.get("predicted_away_xg_range", ""),
        "forecast_pick_path": forecast.get("predicted_pick_path", ""),
        "forecast_pick_breaker": forecast.get("predicted_pick_breaker", ""),
        "prelock_status": "",
        "prelock_decision": prelock_decision,
        "prelock_decision_reason": "",
        "price_discipline_decision": price_decision or first_value(row, ["price_discipline_decision"]),
        "price_discipline_min_edge_required": first_value(row, ["price_discipline_min_edge_required"]),
        "price_discipline_actual_edge": first_value(row, ["price_discipline_actual_edge"]),
        "price_discipline_edge_surplus": first_value(row, ["price_discipline_edge_surplus"]),
        "price_discipline_drift_status": first_value(row, ["price_discipline_drift_status"]),
        "clv_direction": first_value(row, ["clv_direction"]),
        "clv_delta": first_value(row, ["clv_delta"]),
        "result_status": first_value(row, ["ledger_result_status"], "PENDING"),
        "result": first_value(row, ["actionable_result", "primary_result"], "PENDING"),
        "profit_units": first_value(row, ["actionable_profit_units", "primary_profit_units"], ""),
        "roi_contribution": "",
        "post_verdict": "",
        "source_file": source_path.name,
        "source_file_hash": file_hash(source_path),
        "record_status": "PRE_REGISTERED" if stage == "PRE" else "PENDING",
    }
    record["ledger_row_hash"] = row_hash(record)
    return record


def make_no_bet_record(source: dict[str, Any], source_path: Path, target_date: str, generated_at: str, stage: str, reason: str) -> dict[str, object]:
    record = {column: "" for column in LEDGER_COLUMNS}
    record.update(
        {
            "ledger_id": ledger_id(target_date, source["experiment_id"], "", "NO_BET"),
            "target_date": target_date,
            "generated_at": generated_at,
            "pipeline_stage": stage,
            "experiment_id": source["experiment_id"],
            "candidate_version": source["candidate_version"],
            "is_official_pick": source["is_official_pick"],
            "is_shadow_pick": source["is_shadow_pick"],
            "reason_tags": f"NO_BET; {reason}",
            "source_file": source_path.name,
            "source_file_hash": file_hash(source_path),
            "record_status": "NO_BET_RECORD",
        }
    )
    record["ledger_row_hash"] = row_hash(record)
    return record


def row_hash(record: dict[str, object]) -> str:
    keys = [
        "target_date",
        "experiment_id",
        "fixture_id",
        "market_primary",
        "calibrated_probability",
        "reason_tags",
        "risk_tags",
                "prelock_decision",
                "price_discipline_decision",
                "result",
        "profit_units",
        "record_status",
    ]
    return stable_hash([record.get(key, "") for key in keys], 32)


def upsert_records(current: pd.DataFrame, records: list[dict[str, object]], event_type: str, generated_at: str) -> tuple[pd.DataFrame, list[dict[str, object]]]:
    if current.empty:
        current = pd.DataFrame(columns=LEDGER_COLUMNS)
    by_id = {normalize_text(row["ledger_id"]): row.to_dict() for _, row in current.iterrows()}
    events: list[dict[str, object]] = []
    for record in records:
        ledger_key = normalize_text(record["ledger_id"])
        previous = by_id.get(ledger_key, {})
        merged = {column: previous.get(column, "") for column in LEDGER_COLUMNS}
        for column in LEDGER_COLUMNS:
            value = record.get(column, "")
            if normalize_text(value) != "" or column in {"pipeline_stage", "generated_at", "record_status", "source_file", "source_file_hash", "ledger_row_hash"}:
                merged[column] = value
        merged["ledger_row_hash"] = row_hash(merged)
        by_id[ledger_key] = merged
        events.append(
            {
                "event_id": stable_hash([event_type, generated_at, ledger_key, merged.get("ledger_row_hash")], 32),
                "event_type": event_type,
                "event_generated_at": generated_at,
                "ledger_id": ledger_key,
                "target_date": merged.get("target_date", ""),
                "experiment_id": merged.get("experiment_id", ""),
                "fixture_id": merged.get("fixture_id", ""),
                "market_primary": merged.get("market_primary", ""),
                "record_status": merged.get("record_status", ""),
                "ledger_row_hash": merged.get("ledger_row_hash", ""),
            }
        )
    out = pd.DataFrame(list(by_id.values()))
    for column in LEDGER_COLUMNS:
        if column not in out.columns:
            out[column] = ""
    return out[LEDGER_COLUMNS], events


def build_pre_records(processed_dir: Path, target_date: str, generated_at: str) -> list[dict[str, object]]:
    forecasts = forecast_lookup(processed_dir)
    records: list[dict[str, object]] = []
    for source in EXPERIMENT_SOURCES:
        source_path = processed_dir / source["top_file"]
        if not source_path.exists():
            records.append(make_no_bet_record(source, source_path, target_date, generated_at, "PRE", "SOURCE_FILE_MISSING_OR_NOT_AVAILABLE"))
            continue
        df = read_csv_lenient(source_path)
        if df.empty:
            waiting_path = processed_dir / source.get("waiting_file", "")
            waiting = read_csv_lenient(waiting_path) if source.get("waiting_file") else pd.DataFrame()
            waiting_status = waiting.get("candidate_v7_execution_status", pd.Series(dtype=object)).astype(str).str.upper() if not waiting.empty else pd.Series(dtype=object)
            waiting_decision = waiting.get("price_discipline_decision", pd.Series(dtype=object)).astype(str).str.upper() if not waiting.empty else pd.Series(dtype=object)
            waiting_rows = waiting[
                waiting_status.eq("V7_WAITING_FOR_PRELOCK") | waiting_decision.eq("PRICE_NEEDS_PRELOCK_CONFIRMATION")
            ].copy() if not waiting.empty else pd.DataFrame()
            if not waiting_rows.empty:
                for _, row in waiting_rows.iterrows():
                    records.append(make_pick_record(row, source, waiting_path, target_date, generated_at, "PRE", forecasts))
            else:
                records.append(make_no_bet_record(source, source_path, target_date, generated_at, "PRE", "no competition top rows"))
            continue
        for _, row in df.iterrows():
            records.append(make_pick_record(row, source, source_path, target_date, generated_at, "PRE", forecasts))
    return records


def build_prelock_records(processed_dir: Path, target_date: str, generated_at: str, current: pd.DataFrame | None = None) -> list[dict[str, object]]:
    path = processed_dir / "vsigma_today_prelock_comparison.csv"
    df = read_csv_lenient(path)
    records: list[dict[str, object]] = []
    if df.empty:
        return records
    df, _stale = split_fresh_stale_rows(df, target_date, include_target_date=True)
    if df.empty:
        return records
    current_day = current[current["target_date"].astype(str).eq(target_date)].copy() if current is not None and not current.empty else pd.DataFrame(columns=LEDGER_COLUMNS)
    for _, row in df.iterrows():
        fixture_id = normalize_text(row.get("fixture_id", ""))
        market = normalize_text(row.get("market_primary")).upper()
        matching = current_day[
            current_day.get("fixture_id", pd.Series(dtype=object)).astype(str).eq(fixture_id)
            & current_day.get("market_primary", pd.Series(dtype=object)).astype(str).str.upper().eq(market)
            & ~current_day.get("record_status", pd.Series(dtype=object)).astype(str).eq("NO_BET_RECORD")
        ].copy()
        if matching.empty:
            matching = pd.DataFrame([{"experiment_id": "OFFICIAL_BASELINE", "candidate_version": "OFFICIAL_BASELINE", "is_official_pick": 1, "is_shadow_pick": 0}])
        for _, existing in matching.iterrows():
            experiment_id = normalize_text(existing.get("experiment_id", "OFFICIAL_BASELINE"))
            source = next((item for item in EXPERIMENT_SOURCES if item["experiment_id"] == experiment_id), EXPERIMENT_SOURCES[0])
            prelock_decision = row.get("prelock_decision", "")
            price_decision = existing.get("price_discipline_decision", "")
            if normalize_text(price_decision).upper() == "PRICE_NEEDS_PRELOCK_CONFIRMATION" and normalize_text(prelock_decision).upper() in {"PRELOCK_CONFIRMED", "PRELOCK_NO_CHANGE"}:
                price_decision = "V7_PRELOCK_CONFIRMED"
            elif normalize_text(price_decision).upper() == "PRICE_NEEDS_PRELOCK_CONFIRMATION" and normalize_text(prelock_decision).upper() in {"PRELOCK_REMOVED", "PRELOCK_DOWNGRADED"}:
                price_decision = "V7_PRELOCK_REJECTED"
            elif normalize_text(price_decision).upper() == "PRICE_NEEDS_PRELOCK_CONFIRMATION" and normalize_text(prelock_decision).upper() == "PRELOCK_NOT_AVAILABLE":
                price_decision = "V7_PRELOCK_UNAVAILABLE"
            record = {
                "ledger_id": ledger_id(target_date, experiment_id, row.get("fixture_id"), row.get("market_primary")),
                "target_date": target_date,
                "generated_at": generated_at,
                "pipeline_stage": "PRELOCK",
                "experiment_id": experiment_id,
                "candidate_version": existing.get("candidate_version", source["candidate_version"]),
                "is_official_pick": existing.get("is_official_pick", source["is_official_pick"]),
                "is_shadow_pick": existing.get("is_shadow_pick", source["is_shadow_pick"]),
                "fixture_id": fixture_id,
                "market_primary": market,
                "prelock_status": row.get("prelock_status", ""),
                "prelock_decision": prelock_decision,
                "prelock_decision_reason": row.get("prelock_decision_reason", ""),
                "price_discipline_decision": price_decision,
                "source_file": path.name,
                "source_file_hash": file_hash(path),
                "record_status": "PRELOCK_UPDATED",
            }
            record["ledger_row_hash"] = row_hash(record)
            records.append(record)
    return records


def result_record_status(row: pd.Series) -> str:
    status = normalize_text(first_value(row, ["ledger_result_status"], "")).upper()
    result = normalize_text(first_value(row, ["actionable_result", "primary_result"], "")).upper()
    if result == "VOID":
        return "VOID"
    if status == "RESULT_AVAILABLE" or result in {"WIN", "LOSS", "PUSH"}:
        return "SETTLED"
    if status == "PENDING" or result == "PENDING":
        return "PENDING"
    return "PENDING"


def build_post_records(processed_dir: Path, target_date: str, generated_at: str, valid_ledger_ids: set[str]) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    for source in EXPERIMENT_SOURCES:
        result_path = processed_dir / source["result_file"]
        if not result_path.exists():
            continue
        df = read_csv_lenient(result_path)
        if df.empty:
            continue
        for _, row in df.iterrows():
            row_ledger_id = ledger_id(target_date, source["experiment_id"], row.get("fixture_id"), row.get("market_primary"))
            if row_ledger_id not in valid_ledger_ids:
                continue
            result = first_value(row, ["actionable_result", "primary_result"], "PENDING")
            profit = first_value(row, ["actionable_profit_units", "primary_profit_units"], "")
            profit_num = parse_float(profit, None)
            record = {
                "ledger_id": row_ledger_id,
                "target_date": target_date,
                "generated_at": generated_at,
                "pipeline_stage": "POST",
                "experiment_id": source["experiment_id"],
                "candidate_version": source["candidate_version"],
                "is_official_pick": source["is_official_pick"],
                "is_shadow_pick": source["is_shadow_pick"],
                "fixture_id": normalize_text(row.get("fixture_id", "")),
                "league": row.get("league", ""),
                "home_team": row.get("home_team", ""),
                "away_team": row.get("away_team", ""),
                "market_primary": normalize_text(row.get("market_primary")).upper(),
                "market_alt": "",
                "rank": "",
                "calibrated_probability": "",
                "raw_probability": "",
                "confidence_score": "",
                "edge": "",
                "selection_score": "",
                "execution_score": "",
                "price_discipline_decision": first_value(row, ["price_discipline_decision"]),
                "price_discipline_min_edge_required": first_value(row, ["price_discipline_min_edge_required"]),
                "price_discipline_actual_edge": first_value(row, ["price_discipline_actual_edge"]),
                "price_discipline_edge_surplus": first_value(row, ["price_discipline_edge_surplus"]),
                "price_discipline_drift_status": first_value(row, ["price_discipline_drift_status"]),
                "clv_direction": first_value(row, ["clv_direction"]),
                "clv_delta": first_value(row, ["clv_delta"]),
                "result_status": first_value(row, ["ledger_result_status"], "PENDING"),
                "result": result,
                "profit_units": profit,
                "roi_contribution": profit_num if profit_num is not None else "",
                "post_verdict": first_value(row, ["ledger_result_status"], "PENDING"),
                "source_file": result_path.name,
                "source_file_hash": file_hash(result_path),
                "record_status": result_record_status(row),
            }
            record["ledger_row_hash"] = row_hash(record)
            records.append(record)
    return records


def summarize_daily(df: pd.DataFrame, target_date: str) -> dict[str, object]:
    day = df[df["target_date"].astype(str).eq(target_date)].copy() if not df.empty else pd.DataFrame(columns=LEDGER_COLUMNS)
    non_no_bet = day[~day["record_status"].astype(str).eq("NO_BET_RECORD")].copy() if not day.empty else day
    profit = pd.to_numeric(non_no_bet.get("profit_units", pd.Series(dtype=object)), errors="coerce")
    settled = non_no_bet["record_status"].astype(str).isin({"SETTLED", "VOID"}) if not non_no_bet.empty else pd.Series(dtype=bool)
    pending_like = non_no_bet["record_status"].astype(str).isin({"PRE_REGISTERED", "PRELOCK_UPDATED", "PENDING"}) if not non_no_bet.empty else pd.Series(dtype=bool)
    return {
        "official_picks": int((non_no_bet.get("is_official_pick", pd.Series(dtype=object)).astype(str).eq("1")).sum()) if not non_no_bet.empty else 0,
        "shadow_picks": int((non_no_bet.get("is_shadow_pick", pd.Series(dtype=object)).astype(str).eq("1")).sum()) if not non_no_bet.empty else 0,
        "no_bet_records": int(day["record_status"].astype(str).eq("NO_BET_RECORD").sum()) if not day.empty else 0,
        "pending": int(pending_like.sum()) if not non_no_bet.empty else 0,
        "settled": int(settled.sum()) if not non_no_bet.empty else 0,
        "profit_units": round(float(profit.sum(skipna=True)), 6) if not profit.empty else 0.0,
    }


def build_daily_report(processed_dir: Path, target_date: str, ledger: pd.DataFrame) -> Path:
    LEDGER_DIR.mkdir(parents=True, exist_ok=True)
    snapshot_dir = TODAY_DIR / target_date
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    registry = load_experiment_registry()
    day = ledger[ledger["target_date"].astype(str).eq(target_date)].copy() if not ledger.empty else pd.DataFrame(columns=LEDGER_COLUMNS)
    picks = day[~day["record_status"].astype(str).eq("NO_BET_RECORD")].copy() if not day.empty else day
    no_bets = day[day["record_status"].astype(str).eq("NO_BET_RECORD")].copy() if not day.empty else day
    if not day.empty:
        summary_source = day.copy()
        status_text = summary_source["record_status"].fillna("").astype(str)
        summary_source["_is_pick"] = ~status_text.eq("NO_BET_RECORD")
        summary_source["_is_no_bet"] = status_text.eq("NO_BET_RECORD")
        summary_source["_is_pending"] = status_text.isin({"PRE_REGISTERED", "PRELOCK_UPDATED", "PENDING"})
        summary_source["_is_settled"] = status_text.isin({"SETTLED", "VOID"})
        by_experiment = (
            summary_source.groupby("experiment_id", dropna=False)
            .agg(
                records=("ledger_id", "count"),
                picks=("_is_pick", "sum"),
                no_bet_records=("_is_no_bet", "sum"),
                pending=("_is_pending", "sum"),
                settled=("_is_settled", "sum"),
                profit_units=("profit_units", lambda s: round(float(pd.to_numeric(s, errors="coerce").sum(skipna=True)), 6)),
            )
            .reset_index()
        )
    else:
        by_experiment = pd.DataFrame(columns=["experiment_id", "records", "picks", "no_bet_records", "pending", "settled", "profit_units"])
    settled_exps = by_experiment[pd.to_numeric(by_experiment.get("settled", pd.Series(dtype=object)), errors="coerce").fillna(0) > 0]
    if settled_exps.empty:
        winner = "NO_SETTLED_RESULTS"
    else:
        best = pd.to_numeric(settled_exps["profit_units"], errors="coerce").max()
        winners = settled_exps[pd.to_numeric(settled_exps["profit_units"], errors="coerce").eq(best)]["experiment_id"].tolist()
        winner = winners[0] if len(winners) == 1 else "TIE"
    freshness = read_csv_lenient(processed_dir / "vsigma_daily_freshness_report.csv")
    warnings = freshness[~freshness.get("status", pd.Series(dtype=object)).astype(str).eq("PASS")] if not freshness.empty and "status" in freshness.columns else pd.DataFrame()
    summary = summarize_daily(ledger, target_date)
    prelock_rows = day[
        day.get("prelock_decision", pd.Series(dtype=object)).fillna("").astype(str).str.strip().ne("")
    ].copy() if not day.empty else pd.DataFrame()
    lines = [
        f"# vSIGMA Immutable Ledger Daily Report - {target_date}",
        "",
        "## Ledger Update Status",
        f"- Ledger CSV: {LEDGER_CSV}",
        f"- JSONL event log: {LEDGER_JSONL}",
        f"- Official picks registered: {summary['official_picks']}",
        f"- Shadow picks registered: {summary['shadow_picks']}",
        f"- No-bet records: {summary['no_bet_records']}",
        f"- Pending records: {summary['pending']}",
        f"- Settled records: {summary['settled']}",
        f"- Daily winner: {winner}",
        "",
        "## Experiment Registry",
        format_markdown_table(pd.DataFrame(registry.values()), ["experiment_id", "status", "selection_role", "allowed_to_select_officially", "current_verdict"], max_rows=20),
        "",
        "## Daily Summary By Experiment",
        format_markdown_table(by_experiment, max_rows=20),
        "",
        "## Official Picks",
        format_markdown_table(picks[picks.get("is_official_pick", pd.Series(dtype=object)).astype(str).eq("1")], ["experiment_id", "rank", "fixture_id", "home_team", "away_team", "market_primary", "calibrated_probability", "risk_tags", "record_status"], max_rows=20),
        "",
        "## Shadow Picks",
        format_markdown_table(picks[picks.get("is_shadow_pick", pd.Series(dtype=object)).astype(str).eq("1")], ["experiment_id", "rank", "fixture_id", "home_team", "away_team", "market_primary", "calibrated_probability", "risk_tags", "record_status"], max_rows=40),
        "",
        "## No-Bet Modes",
        format_markdown_table(no_bets, ["experiment_id", "record_status", "reason_tags", "source_file"], max_rows=20),
        "",
        "## Pre-Lock Changes",
        format_markdown_table(prelock_rows, ["experiment_id", "fixture_id", "home_team", "away_team", "market_primary", "prelock_status", "prelock_decision", "prelock_decision_reason"], max_rows=20),
        "",
        "## Result State",
        format_markdown_table(picks, ["experiment_id", "fixture_id", "market_primary", "result_status", "result", "profit_units", "record_status"], max_rows=40),
        "",
        "## Freshness Warnings",
        format_markdown_table(warnings, ["file_name", "status", "detail"], max_rows=20),
        "",
    ]
    DAILY_REPORT.write_text("\n".join(lines), encoding="utf-8")
    shutil.copy2(DAILY_REPORT, snapshot_dir / DAILY_REPORT.name)
    return DAILY_REPORT


def update_immutable_ledger(
    processed_dir: Path = PROCESSED_DIR,
    target_date: str | None = None,
    stage: str = "PRE",
) -> dict[str, Path]:
    target_date = target_date or date.today().isoformat()
    stage = stage.strip().upper()
    generated_at = utc_now_iso()
    current = read_ledger()
    if stage == "PRE":
        records = build_pre_records(processed_dir, target_date, generated_at)
    elif stage == "PRELOCK":
        records = build_prelock_records(processed_dir, target_date, generated_at, current)
    elif stage == "POST":
        valid_pre_ids = {normalize_text(record["ledger_id"]) for record in build_pre_records(processed_dir, target_date, generated_at)}
        records = build_post_records(processed_dir, target_date, generated_at, valid_pre_ids)
    else:
        raise ValueError(f"Unsupported ledger stage: {stage}")
    updated, events = upsert_records(current, records, f"{stage}_LEDGER_UPDATE", generated_at)
    if stage == "PRE":
        active_experiments = {
            normalize_text(record.get("experiment_id", ""))
            for record in records
            if normalize_text(record.get("record_status", "")) != "NO_BET_RECORD"
        }
        if active_experiments:
            updated = updated[
                ~(
                    updated["target_date"].astype(str).eq(target_date)
                    & updated["experiment_id"].astype(str).isin(active_experiments)
                    & updated["record_status"].astype(str).eq("NO_BET_RECORD")
                )
            ].copy()
    if stage == "POST":
        updated = updated[
            ~(
                updated["target_date"].astype(str).eq(target_date)
                & ~updated["ledger_id"].astype(str).isin(valid_pre_ids)
            )
        ].copy()
    write_ledger(updated)
    append_events(events)
    report = build_daily_report(processed_dir, target_date, updated)
    return {"ledger_csv": LEDGER_CSV, "ledger_jsonl": LEDGER_JSONL, "daily_report": report}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Update the immutable vSIGMA daily pick ledger.")
    parser.add_argument("--date", default=date.today().isoformat())
    parser.add_argument("--processed-dir", type=Path, default=PROCESSED_DIR)
    parser.add_argument("--stage", choices=["PRE", "PRELOCK", "POST"], default="PRE")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    target_date = pd.Timestamp(args.date).date().isoformat()
    paths = update_immutable_ledger(args.processed_dir, target_date, args.stage)
    print("\n=== IMMUTABLE DAILY LEDGER UPDATED ===")
    for label, path in paths.items():
        print(f"{label}: {path}")


if __name__ == "__main__":
    main()
