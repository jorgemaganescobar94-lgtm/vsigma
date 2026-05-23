from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROCESSED = Path("data/processed")
FIELDS = [
    "target_date", "generated_at", "rank", "factory_experiment_id", "registry_experiment_id",
    "pattern_key", "factory_status", "registry_status", "sync_status", "sync_reason",
    "recommended_next_step", "auto_apply", "production_change", "guardrail_status"
]


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


def source(processed: Path, target_date: str, filename: str) -> Path:
    p = processed / "today" / target_date / filename
    return p if p.exists() else processed / "governance" / filename


def key(row: dict[str, str]) -> str:
    return up(row.get("pattern_key") or row.get("source_pattern_key"))


def registry_index(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    for row in rows:
        k = key(row)
        if k and k not in out:
            out[k] = row
    return out


def classify(factory: dict[str, str], registry: dict[str, str] | None) -> tuple[str, str, str, str]:
    fstatus = up(factory.get("shadow_status"))
    if registry:
        rstatus = up(registry.get("shadow_status")) or "REGISTERED"
        return "ALREADY_REGISTERED", f"Pattern already exists in registry with status {rstatus}.", "CONTINUE_FORWARD_TEST", rstatus
    if fstatus == "CREATE_SHADOW_ONLY":
        return "REGISTRY_CREATE_NEEDED", "Factory created a shadow candidate that is not in registry yet.", "CREATE_REGISTRY_ENTRY_REVIEW_ONLY", "MISSING"
    if fstatus == "CONTINUE_SHADOW_ONLY":
        return "REGISTRY_MISSING_FOR_CONTINUE", "Factory expects continuation but no registry entry was found.", "CREATE_OR_REPAIR_REGISTRY_ENTRY", "MISSING"
    return "MONITOR_ONLY", "Factory row does not request registry action.", "KEEP_MONITORING", "N/A"


def build(target_date: str, timezone: str, processed: Path) -> list[dict[str, object]]:
    generated_at = datetime.now(ZoneInfo(timezone)).isoformat(timespec="seconds")
    factory_rows = read_rows(source(processed, target_date, "vsigma_shadow_experiment_factory.csv"))
    registry_rows = read_rows(processed / "governance" / "vsigma_shadow_experiments.csv")
    idx = registry_index(registry_rows)
    rows: list[dict[str, object]] = []
    for n, f in enumerate(factory_rows, start=1):
        k = key(f)
        reg = idx.get(k)
        sync, reason, step, rstatus = classify(f, reg)
        rows.append({
            "target_date": target_date,
            "generated_at": generated_at,
            "rank": n,
            "factory_experiment_id": norm(f.get("experiment_id")),
            "registry_experiment_id": norm((reg or {}).get("experiment_id")),
            "pattern_key": k,
            "factory_status": up(f.get("shadow_status")),
            "registry_status": rstatus,
            "sync_status": sync,
            "sync_reason": reason,
            "recommended_next_step": step,
            "auto_apply": "NO",
            "production_change": "NO",
            "guardrail_status": "SHADOW_REGISTRY_SYNC_REPORT_ONLY",
        })
    return rows


def counts(rows: list[dict[str, object]], field: str) -> str:
    c = Counter(str(r.get(field) or "UNKNOWN") for r in rows)
    return "; ".join(f"{k}={v}" for k, v in c.most_common()) if c else "none"


def md(target_date: str, rows: list[dict[str, object]]) -> str:
    lines = [
        f"# vSIGMA Shadow Registry Sync - {target_date}", "",
        "## Summary",
        f"- factory_rows: {len(rows)}",
        f"- sync_status_counts: {counts(rows, 'sync_status')}",
        "- auto_apply: NO",
        "- production_change: NO", "",
        "## Registry Sync Rows",
    ]
    if not rows:
        lines.append("- none")
    for r in rows:
        lines.append(f"- #{r['rank']} | {r['sync_status']} | pattern={r['pattern_key']} | factory={r['factory_status']} | registry={r['registry_status']} | next={r['recommended_next_step']}")
    lines += ["", "## Guardrails", "- This report does not create or modify registry entries automatically.", "- Registry changes require separate review.", "- Production picks remain unchanged."]
    return "\n".join(lines) + "\n"


def run(target_date: str, timezone: str, processed: Path) -> None:
    target_date = date.fromisoformat(target_date).isoformat()
    rows = build(target_date, timezone, processed)
    for base in [processed / "today" / target_date, processed / "governance"]:
        write_rows(base / "vsigma_shadow_registry_sync.csv", rows)
        (base / "vsigma_shadow_registry_sync.md").write_text(md(target_date, rows), encoding="utf-8")
    print("=== VSIGMA SHADOW REGISTRY SYNC ===")
    print(f"factory_rows={len(rows)}")
    print(f"sync_status_counts={counts(rows, 'sync_status')}")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--date", required=True)
    p.add_argument("--timezone", default="Atlantic/Canary")
    p.add_argument("--processed-dir", type=Path, default=PROCESSED)
    a = p.parse_args()
    run(a.date, a.timezone, a.processed_dir)


if __name__ == "__main__":
    main()
