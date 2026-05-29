from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import date
from pathlib import Path

P = Path("data/processed")


def s(x):
    return "" if x is None else str(x).strip()


def read(path: Path):
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return [dict(r) for r in csv.DictReader(f)]


def d(day, name):
    return P / "today" / day / name


def g(name):
    return P / "governance" / name


def source(day):
    p = d(day, "vsigma_formula_patch_governance_dashboard.csv")
    rows = read(p)
    if rows:
        return rows, str(p)
    p = g("vsigma_formula_patch_governance_dashboard.csv")
    return read(p), str(p)


def counts(rows, field):
    c = Counter(s(r.get(field)) or "UNKNOWN" for r in rows)
    return "; ".join(f"{k}={v}" for k, v in c.most_common()) if c else "none"


def metrics(rows, statuses):
    out = []
    for r in rows:
        if r.get("overall_status") in statuses:
            m = s(r.get("metric")) or "UNKNOWN"
            if m not in out:
                out.append(m)
    return ",".join(out) if out else "none"


def verdict(rows):
    if not rows:
        return "NO_DASHBOARD", "No formula patch governance dashboard found.", "Run formula patch governance dashboard first."
    if any(r.get("overall_status") == "READY_FOR_MANUAL_CODE_REVIEW" for r in rows):
        return "READY_FOR_MANUAL_CODE_REVIEW", "At least one formula patch path is ready for manual code review.", "Prepare a small reviewed diff/PR with rollback plan; do not auto-apply."
    if any(r.get("overall_status") == "REJECT_PATCH_PATH" for r in rows):
        return "REJECT_PRESENT", "At least one patch path is rejected by governance.", "Do not touch rejected formulas; keep accumulating evidence elsewhere."
    if any(r.get("overall_status") == "WAIT_MORE_SAMPLE" for r in rows):
        return "WAIT_MORE_SAMPLE", "Formula patch paths need more sample.", "Keep shadow/backtest accumulation."
    if all(r.get("overall_status") in {"NO_ACTION", "DO_NOT_TOUCH", "DIFF_HELD"} for r in rows):
        return "NO_ACTION", "No formula patch is ready.", "No code action required."
    return "MIXED", "Formula patch governance is mixed or incomplete.", "Review dashboard before any formula work."


def block(day):
    rows, src = source(day)
    st, reason, action = verdict(rows)
    lines = [
        "## Formula Patch Governance",
        f"- Status: `{st}`",
        f"- Overall statuses: `{counts(rows, 'overall_status')}`",
        f"- Ready metrics: `{metrics(rows, {'READY_FOR_MANUAL_CODE_REVIEW'})}`",
        f"- Rejected metrics: `{metrics(rows, {'REJECT_PATCH_PATH'})}`",
        f"- Waiting metrics: `{metrics(rows, {'WAIT_MORE_SAMPLE'})}`",
        f"- Source: `{src}`",
        f"- Reason: {reason}",
        f"- Next action: {action}",
        "- Auto apply: `NO`",
        "- Production change: `NO`",
    ]
    return "\n".join(lines) + "\n"


def run(day, output):
    day = date.fromisoformat(day).isoformat()
    text = block(day)
    if output:
        with Path(output).open("a", encoding="utf-8") as f:
            f.write("\n")
            f.write(text)
    print(text)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--date", required=True)
    p.add_argument("--output")
    a = p.parse_args()
    run(a.date, a.output)


if __name__ == "__main__":
    main()
