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
    p = d(day, "vsigma_shadow_ab_quality_gate.csv")
    rows = read(p)
    if rows:
        return rows, str(p)
    p = g("vsigma_shadow_ab_quality_gate.csv")
    return read(p), str(p)


def counts(rows, field):
    c = Counter(s(r.get(field)) or "UNKNOWN" for r in rows)
    return "; ".join(f"{k}={v}" for k, v in c.most_common()) if c else "none"


def metrics(rows, gates):
    out = []
    for r in rows:
        if r.get("quality_gate") in gates:
            m = s(r.get("metric")) or "UNKNOWN"
            if m not in out:
                out.append(m)
    return ",".join(out) if out else "none"


def status(rows):
    if not rows:
        return "NO_DATA", "No A/B quality gate rows available.", "Run post-match learning chain after A/B simulator."
    if any(r.get("quality_gate") == "BAD_SHADOW_SIGNAL" for r in rows):
        return "BAD_SHADOW_SIGNAL", "At least one shadow metric worsened.", "Block promotion; keep shadow only."
    if any(r.get("quality_gate") == "USABLE_SHADOW_SIGNAL" for r in rows):
        return "USABLE_SHADOW_SIGNAL", "At least one metric is usable for manual review.", "Manual review only; no auto-promotion."
    if any(r.get("quality_gate") == "PROMOTION_BLOCKED" for r in rows):
        return "PROMOTION_BLOCKED", "Signal improved but sample blocks promotion.", "Keep accumulating detail rows."
    if any(r.get("quality_gate") == "LOW_SAMPLE" for r in rows):
        return "LOW_SAMPLE", "A/B sample is too small.", "Wait for more post-match detail rows."
    if any(r.get("quality_gate") == "NO_DATA" for r in rows):
        return "NO_DATA", "No usable A/B data yet.", "Do not use A/B for calibration decisions."
    return "NO_CLEAR_AB_EDGE", "No clear A/B edge.", "Continue monitoring."


def block(day):
    rows, src = source(day)
    st, reason, action = status(rows)
    lines = [
        "## Shadow A/B Quality Gate",
        f"- Status: `{st}`",
        f"- Quality gates: `{counts(rows, 'quality_gate')}`",
        f"- Priorities: `{counts(rows, 'quality_priority')}`",
        f"- Usable metrics: `{metrics(rows, {'USABLE_SHADOW_SIGNAL'})}`",
        f"- Bad metrics: `{metrics(rows, {'BAD_SHADOW_SIGNAL'})}`",
        f"- Blocked metrics: `{metrics(rows, {'PROMOTION_BLOCKED'})}`",
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
