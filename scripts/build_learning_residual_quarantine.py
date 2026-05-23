from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROCESSED = Path("data/processed")
FIELDS = [
    "target_date", "generated_at", "rank", "fixture_id", "home_team", "away_team",
    "market_primary", "result_status", "learning_family", "learning_status",
    "sample_key", "evidence_bucket", "quarantine_reason", "counts_for_learning",
    "blocks_model_change", "auto_fix", "production_change"
]
GOOD_RESULTS = {"WIN", "LOSS", "PUSH", "VOID"}


def norm(v: object) -> str:
    return "" if v is None else str(v).strip()


def up(v: object) -> str:
    return norm(v).upper()


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return [dict(r) for r in csv.DictReader(f)]


def write_rows(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in FIELDS})


def source_path(processed: Path, target_date: str) -> Path:
    p = processed / "today" / target_date / "vsigma_learning_ledger.csv"
    return p if p.exists() else processed / "governance" / "vsigma_learning_ledger.csv"


def classify(row: dict[str, str]) -> tuple[str, str, str, str]:
    fixture = norm(row.get("fixture_id"))
    market = up(row.get("market_primary"))
    result = up(row.get("result_status"))
    family = up(row.get("learning_family"))
    status = up(row.get("learning_status"))
    sample = up(row.get("sample_key"))

    if family == "ACTIONABLE_RESULT" and result in GOOD_RESULTS:
        return "USABLE_CLOSED_SAMPLE", "Resolved actionable sample; eligible for pattern counting.", "YES", "NO"
    if family == "EXPIRED_PRELOCK":
        return "OPERATIONAL_QUARANTINE", "Expired timing row; keep out of predictive learning.", "NO", "NO"
    if not fixture or not market or market == "UNKNOWN":
        return "IDENTITY_QUARANTINE", "Missing fixture or market identity; keep out of model readiness gates.", "NO", "NO"
    if result in {"", "UNRESOLVED", "UNKNOWN", "PENDING"}:
        return "OPEN_RESULT_QUARANTINE", "Result is not closed; monitor but do not block usable closed samples.", "NO", "NO"
    if "UNKNOWN" in sample or "NO_SIGNAL" in sample or status in {"", "PROMOTION_NOT_ALLOWED"}:
        return "LOW_INFORMATION_QUARANTINE", "Low-information row; monitor separately from usable evidence.", "NO", "NO"
    return "MONITOR_ONLY", "Row is not a closed actionable sample; keep for audit only.", "NO", "NO"


def build(target_date: str, timezone: str, processed: Path) -> list[dict[str, object]]:
    generated_at = datetime.now(ZoneInfo(timezone)).isoformat(timespec="seconds")
    rows = read_rows(source_path(processed, target_date))
    out: list[dict[str, object]] = []
    for idx, row in enumerate(rows, start=1):
        bucket, reason, counts, blocks = classify(row)
        out.append({
            "target_date": target_date,
            "generated_at": generated_at,
            "rank": idx,
            "fixture_id": norm(row.get("fixture_id")),
            "home_team": norm(row.get("home_team")),
            "away_team": norm(row.get("away_team")),
            "market_primary": up(row.get("market_primary")) or "UNKNOWN",
            "result_status": up(row.get("result_status")) or "UNKNOWN",
            "learning_family": up(row.get("learning_family")) or "UNKNOWN",
            "learning_status": up(row.get("learning_status")) or "UNKNOWN",
            "sample_key": up(row.get("sample_key")),
            "evidence_bucket": bucket,
            "quarantine_reason": reason,
            "counts_for_learning": counts,
            "blocks_model_change": blocks,
            "auto_fix": "NO",
            "production_change": "NO",
        })
    return out


def counts(rows: list[dict[str, object]], field: str) -> str:
    c = Counter(str(r.get(field) or "UNKNOWN") for r in rows)
    return "; ".join(f"{k}={v}" for k, v in c.most_common()) if c else "none"


def md(target_date: str, rows: list[dict[str, object]]) -> str:
    usable = sum(1 for r in rows if r.get("counts_for_learning") == "YES")
    blocked = sum(1 for r in rows if r.get("blocks_model_change") == "YES")
    lines = [
        f"# vSIGMA Learning Residual Quarantine - {target_date}", "",
        "## Summary",
        f"- rows_reviewed: {len(rows)}",
        f"- usable_closed_samples: {usable}",
        f"- model_blocking_rows: {blocked}",
        f"- bucket_counts: {counts(rows, 'evidence_bucket')}",
        "- auto_fix: NO",
        "- production_change: NO", "",
        "## Rows",
    ]
    for r in rows[:60]:
        lines.append(f"- #{r['rank']} | {r['evidence_bucket']} | counts={r['counts_for_learning']} | fixture={r['fixture_id'] or 'N/A'} | market={r['market_primary']} | result={r['result_status']} | reason={r['quarantine_reason']}")
    lines += ["", "## Guardrails", "- No data is deleted.", "- No model behavior changes.", "- Quarantined rows remain auditable but should not block usable closed samples."]
    return "\n".join(lines) + "\n"


def run(target_date: str, timezone: str, processed: Path) -> None:
    target_date = date.fromisoformat(target_date).isoformat()
    rows = build(target_date, timezone, processed)
    for base in [processed / "today" / target_date, processed / "governance"]:
        write_rows(base / "vsigma_learning_residual_quarantine.csv", rows)
        (base / "vsigma_learning_residual_quarantine.md").write_text(md(target_date, rows), encoding="utf-8")
    print("=== VSIGMA LEARNING RESIDUAL QUARANTINE ===")
    print(f"rows={len(rows)}")
    print(f"usable_closed_samples={sum(1 for r in rows if r.get('counts_for_learning') == 'YES')}")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--date", required=True)
    p.add_argument("--timezone", default="Atlantic/Canary")
    p.add_argument("--processed-dir", type=Path, default=PROCESSED)
    a = p.parse_args()
    run(a.date, a.timezone, a.processed_dir)


if __name__ == "__main__":
    main()
