from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Iterable
from zoneinfo import ZoneInfo

import pandas as pd

try:
    from daily_hardening import PROCESSED_DIR, format_markdown_table, read_csv_lenient, split_fresh_stale_rows
    from materialize_daily_audit_bundle import materialize_daily_audit_bundle
except ModuleNotFoundError:
    from scripts.daily_hardening import PROCESSED_DIR, format_markdown_table, read_csv_lenient, split_fresh_stale_rows
    from scripts.materialize_daily_audit_bundle import materialize_daily_audit_bundle


ROOT = Path(__file__).resolve().parents[1]

RESOLVER_CSV = "vsigma_prelock_decision_resolver.csv"
CLOUD_SUMMARY_CSV = "vsigma_cloud_decision_summary.csv"
OFFICIAL_TOP_CSV = "vsigma_today_competition_top.csv"
LEDGER_CSV = "vsigma_decision_outcome_ledger.csv"
LEDGER_JSONL = "vsigma_decision_outcome_ledger.jsonl"
REPORT_MD = "vsigma_decision_outcome_ledger_report.md"

LEDGER_COLUMNS = [
    "ledger_id",
    "target_date",
    "generated_at",
    "fixture_id",
    "league",
    "home_team",
    "away_team",
    "market_primary",
    "candidate_present",
    "official_action",
    "executable_now",
    "final_block_reason",
    "retry_allowed",
    "next_retry_time",
    "execution_family_status",
    "decision_source",
    "competition_calibrated_prob",
    "accuracy_confidence_score",
    "accuracy_primary_risk",
    "resolver_run_id",
    "cloud_summary_status",
    "is_actionable",
    "is_non_actionable",
    "is_expired",
    "is_waiting",
    "is_blocked",
    "is_technical_review",
]


@dataclass(frozen=True)
class LedgerPaths:
    csv_path: Path
    jsonl_path: Path
    report_path: Path


def norm_text(value: object) -> str:
    if value is None or pd.isna(value):
        return ""
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value).strip()


def norm_upper(value: object) -> str:
    return norm_text(value).upper()


def snapshot_dir(processed_dir: Path, target_date: str) -> Path:
    return processed_dir / "today" / target_date


def read_fresh_csv(path: Path, target_date: str) -> pd.DataFrame:
    df = read_csv_lenient(path)
    if df.empty:
        return df
    fresh, _stale = split_fresh_stale_rows(df, target_date, include_target_date=True)
    return fresh.reset_index(drop=True)


def first_available(row: pd.Series | None, columns: Iterable[str]) -> object:
    if row is None:
        return ""
    for column in columns:
        if column in row.index and norm_text(row.get(column)):
            return row.get(column)
    return ""


def key_for_row(row: pd.Series | dict[str, object]) -> tuple[str, str]:
    return (norm_text(row.get("fixture_id")), norm_upper(row.get("market_primary")))


def index_by_key(df: pd.DataFrame) -> dict[tuple[str, str], pd.Series]:
    rows: dict[tuple[str, str], pd.Series] = {}
    if df.empty:
        return rows
    for _, row in df.iterrows():
        key = key_for_row(row)
        if key[0] and key not in rows:
            rows[key] = row
    return rows


def lookup_row(index: dict[tuple[str, str], pd.Series], row: pd.Series | dict[str, object]) -> pd.Series | None:
    key = key_for_row(row)
    if key in index:
        return index[key]
    fixture_id = key[0]
    if not fixture_id:
        return None
    matches = [value for candidate_key, value in index.items() if candidate_key[0] == fixture_id]
    return matches[0] if matches else None


def ledger_id_for(target_date: str, fixture_id: object, market_primary: object, official_action: object) -> str:
    return "::".join(
        [
            pd.Timestamp(target_date).date().isoformat(),
            norm_text(fixture_id) or "NO_FIXTURE",
            norm_upper(market_primary) or "NO_MARKET",
            norm_upper(official_action) or "NO_ACTION",
        ]
    )


def cloud_summary_status(summary_row: pd.Series | None) -> str:
    if summary_row is None:
        return "MISSING"
    execution_status = norm_upper(first_available(summary_row, ["execution_family_status"]))
    final_reason = norm_upper(first_available(summary_row, ["final_block_reason"]))
    if execution_status == "EXPIRED" or final_reason == "KICKOFF_ALREADY_PASSED":
        return "EXPIRED"
    return (
        execution_status
        or norm_upper(first_available(summary_row, ["decision_state"]))
        or norm_upper(first_available(summary_row, ["official_action"]))
        or "PRESENT"
    )


def yes_no(value: bool) -> str:
    return "YES" if value else "NO"


def classify_row(official_action: str, executable_now: str, final_block_reason: str, execution_family_status: str) -> dict[str, str]:
    is_actionable = official_action == "EXECUTABLE" and executable_now == "YES"
    is_expired = final_block_reason == "KICKOFF_ALREADY_PASSED" or execution_family_status == "EXPIRED"
    is_waiting = official_action == "WAIT" or execution_family_status.startswith("WAITING")
    is_technical_review = official_action == "TECHNICAL_REVIEW" or execution_family_status == "TECHNICAL_REVIEW"
    is_blocked = (
        not is_actionable
        and not is_expired
        and not is_waiting
        and not is_technical_review
        and official_action in {"NO_BET", "WAIT"}
    )
    return {
        "is_actionable": yes_no(is_actionable),
        "is_non_actionable": yes_no(not is_actionable),
        "is_expired": yes_no(is_expired),
        "is_waiting": yes_no(is_waiting),
        "is_blocked": yes_no(is_blocked),
        "is_technical_review": yes_no(is_technical_review),
    }


def source_rows(resolver: pd.DataFrame, summary: pd.DataFrame, official_top: pd.DataFrame) -> pd.DataFrame:
    for frame in [resolver, summary, official_top]:
        if frame.empty or "fixture_id" not in frame.columns:
            continue
        current = frame[frame["fixture_id"].fillna("").astype(str).str.strip().ne("")].copy()
        if not current.empty:
            key_columns = [column for column in ["fixture_id", "market_primary"] if column in current.columns]
            return current.drop_duplicates(key_columns or None).reset_index(drop=True)
    return resolver.copy() if not resolver.empty else pd.DataFrame()


def build_ledger_rows(
    *,
    target_date: str,
    generated_at: str,
    resolver: pd.DataFrame,
    summary: pd.DataFrame,
    official_top: pd.DataFrame,
) -> pd.DataFrame:
    summary_index = index_by_key(summary)
    official_index = index_by_key(official_top)
    resolver_index = index_by_key(resolver)
    rows: list[dict[str, object]] = []

    for _, source in source_rows(resolver, summary, official_top).iterrows():
        resolver_row = lookup_row(resolver_index, source)
        summary_row = lookup_row(summary_index, source)
        candidate_row = lookup_row(official_index, source)
        decision_row = resolver_row if resolver_row is not None else summary_row
        if decision_row is None:
            decision_row = source

        official_action = norm_upper(first_available(decision_row, ["official_action"])) or "TECHNICAL_REVIEW"
        executable_now = norm_upper(first_available(decision_row, ["executable_now"])) or "NO"
        final_block_reason = norm_upper(first_available(decision_row, ["final_block_reason"])) or "TECHNICAL_REVIEW"
        execution_family_status = norm_upper(first_available(decision_row, ["execution_family_status"])) or "TECHNICAL_REVIEW"
        market_primary = norm_upper(
            first_available(decision_row, ["market_primary"])
            or first_available(source, ["market_primary"])
            or first_available(candidate_row, ["market_primary"])
        )
        fixture_id = norm_text(
            first_available(decision_row, ["fixture_id"])
            or first_available(source, ["fixture_id"])
            or first_available(candidate_row, ["fixture_id"])
        )
        classifications = classify_row(official_action, executable_now, final_block_reason, execution_family_status)
        rows.append(
            {
                "ledger_id": ledger_id_for(target_date, fixture_id, market_primary, official_action),
                "target_date": target_date,
                "generated_at": generated_at,
                "fixture_id": fixture_id,
                "league": norm_text(first_available(decision_row, ["league"]) or first_available(candidate_row, ["league"])),
                "home_team": norm_text(first_available(decision_row, ["home_team"]) or first_available(candidate_row, ["home_team"])),
                "away_team": norm_text(first_available(decision_row, ["away_team"]) or first_available(candidate_row, ["away_team"])),
                "market_primary": market_primary,
                "candidate_present": yes_no(candidate_row is not None),
                "official_action": official_action,
                "executable_now": executable_now,
                "final_block_reason": final_block_reason,
                "retry_allowed": norm_upper(first_available(decision_row, ["retry_allowed"])) or "NO",
                "next_retry_time": norm_text(first_available(decision_row, ["next_retry_time"])),
                "execution_family_status": execution_family_status,
                "decision_source": norm_text(first_available(decision_row, ["decision_source"])) or "UNKNOWN",
                "competition_calibrated_prob": first_available(summary_row, ["competition_calibrated_prob"]) or first_available(candidate_row, ["competition_calibrated_prob"]),
                "accuracy_confidence_score": first_available(summary_row, ["accuracy_confidence_score"]) or first_available(candidate_row, ["accuracy_confidence_score"]),
                "accuracy_primary_risk": norm_text(first_available(summary_row, ["accuracy_primary_risk"]) or first_available(candidate_row, ["accuracy_primary_risk"])),
                "resolver_run_id": norm_text(first_available(candidate_row, ["run_id"]) or first_available(summary_row, ["run_id"]) or first_available(resolver_row, ["generated_at"])),
                "cloud_summary_status": cloud_summary_status(summary_row),
                **classifications,
            }
        )

    if not rows:
        rows.append(
            {
                "ledger_id": ledger_id_for(target_date, "", "", "NO_BET"),
                "target_date": target_date,
                "generated_at": generated_at,
                "fixture_id": "",
                "league": "",
                "home_team": "",
                "away_team": "",
                "market_primary": "",
                "candidate_present": "NO",
                "official_action": "NO_BET",
                "executable_now": "NO",
                "final_block_reason": "NO_CANDIDATES",
                "retry_allowed": "NO",
                "next_retry_time": "",
                "execution_family_status": "NO_CANDIDATES",
                "decision_source": "NO_CANDIDATES",
                "competition_calibrated_prob": "",
                "accuracy_confidence_score": "",
                "accuracy_primary_risk": "",
                "resolver_run_id": "",
                "cloud_summary_status": "MISSING",
                **classify_row("NO_BET", "NO", "NO_CANDIDATES", "NO_CANDIDATES"),
            }
        )

    return pd.DataFrame(rows, columns=LEDGER_COLUMNS)


def upsert_ledger(existing: pd.DataFrame, new_rows: pd.DataFrame) -> pd.DataFrame:
    if existing.empty:
        combined = new_rows.copy()
    else:
        for column in LEDGER_COLUMNS:
            if column not in existing.columns:
                existing[column] = ""
        existing = existing[LEDGER_COLUMNS]
        new_ids = set(new_rows["ledger_id"].astype(str))
        combined = pd.concat(
            [existing[~existing["ledger_id"].astype(str).isin(new_ids)], new_rows],
            ignore_index=True,
            sort=False,
        )
    return combined[LEDGER_COLUMNS].drop_duplicates("ledger_id", keep="last").reset_index(drop=True)


def write_jsonl(df: pd.DataFrame, path: Path) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for record in df[LEDGER_COLUMNS].fillna("").to_dict(orient="records"):
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")


def write_report(df: pd.DataFrame, new_rows: pd.DataFrame, report_path: Path, target_date: str) -> None:
    target_rows = df[df["target_date"].astype(str).str[:10].eq(target_date)].copy()
    lines = [
        f"# vSIGMA Decision Outcome Ledger - {target_date}",
        "",
        "## Summary",
        f"- Rows total: {len(df)}",
        f"- Rows for target date: {len(target_rows)}",
        f"- Rows updated this run: {len(new_rows)}",
        f"- Actionable rows: {int(target_rows['is_actionable'].astype(str).eq('YES').sum()) if not target_rows.empty else 0}",
        f"- Non-actionable rows: {int(target_rows['is_non_actionable'].astype(str).eq('YES').sum()) if not target_rows.empty else 0}",
        f"- Expired rows: {int(target_rows['is_expired'].astype(str).eq('YES').sum()) if not target_rows.empty else 0}",
        f"- Waiting rows: {int(target_rows['is_waiting'].astype(str).eq('YES').sum()) if not target_rows.empty else 0}",
        f"- Blocked rows: {int(target_rows['is_blocked'].astype(str).eq('YES').sum()) if not target_rows.empty else 0}",
        f"- Technical review rows: {int(target_rows['is_technical_review'].astype(str).eq('YES').sum()) if not target_rows.empty else 0}",
        "",
        "## Target Date Rows",
        format_markdown_table(
            target_rows,
            [
                "fixture_id",
                "league",
                "home_team",
                "away_team",
                "market_primary",
                "official_action",
                "executable_now",
                "final_block_reason",
                "execution_family_status",
                "is_actionable",
                "is_expired",
                "is_waiting",
                "is_blocked",
                "is_technical_review",
            ],
            max_rows=100,
        ),
        "",
    ]
    report_path.write_text("\n".join(lines), encoding="utf-8")


def update_decision_outcome_ledger(
    *,
    target_date: str,
    timezone_name: str = "Atlantic/Canary",
    processed_dir: Path = PROCESSED_DIR,
    now: datetime | None = None,
) -> tuple[pd.DataFrame, LedgerPaths]:
    target_date = pd.Timestamp(target_date).date().isoformat()
    timezone = ZoneInfo(timezone_name)
    now = now.astimezone(timezone) if now is not None else datetime.now(timezone)
    generated_at = now.isoformat(timespec="seconds")
    snap = snapshot_dir(processed_dir, target_date)
    ledger_dir = processed_dir / "ledger"
    snap.mkdir(parents=True, exist_ok=True)
    ledger_dir.mkdir(parents=True, exist_ok=True)

    resolver = read_fresh_csv(snap / RESOLVER_CSV, target_date)
    summary = read_fresh_csv(snap / CLOUD_SUMMARY_CSV, target_date)
    official_top = read_fresh_csv(snap / OFFICIAL_TOP_CSV, target_date)
    new_rows = build_ledger_rows(
        target_date=target_date,
        generated_at=generated_at,
        resolver=resolver,
        summary=summary,
        official_top=official_top,
    )

    paths = LedgerPaths(
        csv_path=ledger_dir / LEDGER_CSV,
        jsonl_path=ledger_dir / LEDGER_JSONL,
        report_path=snap / REPORT_MD,
    )
    existing = read_csv_lenient(paths.csv_path, columns=LEDGER_COLUMNS)
    ledger = upsert_ledger(existing, new_rows)
    ledger.to_csv(paths.csv_path, index=False)
    write_jsonl(ledger, paths.jsonl_path)
    write_report(ledger, new_rows, paths.report_path, target_date)
    materialize_daily_audit_bundle(target_date, processed_dir)
    return ledger, paths


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Update the vSIGMA decision outcome ledger from PRELOCK resolver outputs.")
    parser.add_argument("--date", default=date.today().isoformat())
    parser.add_argument("--timezone", default="Atlantic/Canary")
    parser.add_argument("--processed-dir", type=Path, default=PROCESSED_DIR)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    ledger, paths = update_decision_outcome_ledger(
        target_date=args.date,
        timezone_name=args.timezone,
        processed_dir=args.processed_dir,
    )
    target_date = pd.Timestamp(args.date).date().isoformat()
    target_rows = ledger[ledger["target_date"].astype(str).str[:10].eq(target_date)]
    print("=== VSIGMA DECISION OUTCOME LEDGER ===")
    print(f"target_date={target_date}")
    print(f"rows_total={len(ledger)}")
    print(f"rows_target_date={len(target_rows)}")
    print(f"csv={paths.csv_path}")
    print(f"jsonl={paths.jsonl_path}")
    print(f"report={paths.report_path}")


if __name__ == "__main__":
    main()
