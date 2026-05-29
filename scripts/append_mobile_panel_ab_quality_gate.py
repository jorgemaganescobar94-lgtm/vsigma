from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

P = Path("data/processed")
PANEL_FIELDS = ["target_date", "generated_at", "card", "status", "detail", "next_action"]


def s(x):
    return "" if x is None else str(x).strip()


def read(path: Path):
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return [dict(r) for r in csv.DictReader(f)]


def write_csv(path: Path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=PANEL_FIELDS)
        w.writeheader()
        w.writerows([{k: r.get(k, "") for k in PANEL_FIELDS} for r in rows])


def read_text(path: Path):
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_text(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


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
        return "NO_DATA", "No A/B quality gate rows yet.", "Generate post-match learning chain first."
    if any(r.get("quality_gate") == "BAD_SHADOW_SIGNAL" for r in rows):
        return "BAD_SHADOW_SIGNAL", "At least one A/B shadow metric worsened.", "Block promotion and keep shadow only."
    if any(r.get("quality_gate") == "USABLE_SHADOW_SIGNAL" for r in rows):
        return "USABLE_SHADOW_SIGNAL", "At least one metric has usable A/B signal.", "Manual review only; no auto promotion."
    if any(r.get("quality_gate") == "PROMOTION_BLOCKED" for r in rows):
        return "PROMOTION_BLOCKED", "A/B improved but sample is not promotion-ready.", "Keep accumulating sample."
    if any(r.get("quality_gate") == "LOW_SAMPLE" for r in rows):
        return "LOW_SAMPLE", "A/B exists but sample is low.", "Wait for more detail rows."
    if any(r.get("quality_gate") == "NO_DATA" for r in rows):
        return "NO_DATA", "No usable A/B data.", "Do not use A/B for calibration decisions."
    return "NO_CLEAR_AB_EDGE", "No clear A/B quality edge.", "Continue monitoring."


def strip(text):
    marker = "\n## Shadow A/B Quality Gate\n"
    i = text.find(marker)
    return text.rstrip() + "\n" if i == -1 else text[:i].rstrip() + "\n"


def block(rows, src):
    st, detail, action = status(rows)
    lines = [
        "## Shadow A/B Quality Gate",
        f"- ab_quality_status: {st}",
        f"- quality_gates: {counts(rows, 'quality_gate')}",
        f"- quality_priorities: {counts(rows, 'quality_priority')}",
        f"- usable_metrics: {metrics(rows, {'USABLE_SHADOW_SIGNAL'})}",
        f"- bad_metrics: {metrics(rows, {'BAD_SHADOW_SIGNAL'})}",
        f"- blocked_metrics: {metrics(rows, {'PROMOTION_BLOCKED'})}",
        f"- ab_quality_source: {src}",
        "- auto_apply: NO",
        "- production_change: NO",
    ]
    return st, detail, action, "\n".join(lines) + "\n"


def update_panel_csv(path, day, ts, st, detail, action, rows):
    panel = [r for r in read(path) if r.get("card") != "SHADOW_AB_QUALITY"]
    panel.append({
        "target_date": day,
        "generated_at": ts,
        "card": "SHADOW_AB_QUALITY",
        "status": st,
        "detail": f"quality_gates={counts(rows, 'quality_gate')}; usable={metrics(rows, {'USABLE_SHADOW_SIGNAL'})}; bad={metrics(rows, {'BAD_SHADOW_SIGNAL'})}; {detail}",
        "next_action": action,
    })
    write_csv(path, panel)


def run(day, tz):
    day = date.fromisoformat(day).isoformat()
    ts = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    rows, src = source(day)
    st, detail, action, md_block = block(rows, src)
    for base in [P / "today" / day, P / "governance"]:
        md_path = base / "vsigma_mobile_operator_control_panel.md"
        csv_path = base / "vsigma_mobile_operator_control_panel.csv"
        write_text(md_path, strip(read_text(md_path)) + "\n" + md_block)
        update_panel_csv(csv_path, day, ts, st, detail, action, rows)
    print("=== VSIGMA MOBILE PANEL AB QUALITY GATE ===")
    print(f"ab_quality_status={st}")
    print(f"quality_gates={counts(rows, 'quality_gate')}")
    print("auto_apply=NO")
    print("production_change=NO")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--date", required=True)
    p.add_argument("--timezone", default="Atlantic/Canary")
    a = p.parse_args()
    run(a.date, a.timezone)


if __name__ == "__main__":
    main()
