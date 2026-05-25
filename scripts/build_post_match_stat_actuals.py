from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROCESSED = Path("data/processed")
FINAL_STATUS = {"FT", "AET", "PEN"}
FIELDS = [
    "target_date", "generated_at", "fixture_id", "home_team", "away_team", "status",
    "actual_home_goals", "actual_away_goals", "actual_total_goals",
    "actual_home_sot", "actual_away_sot", "actual_total_sot",
    "actual_home_shots", "actual_away_shots", "actual_total_shots",
    "actual_home_corners", "actual_away_corners", "actual_total_corners",
    "actual_home_cards", "actual_away_cards", "actual_total_cards",
    "actual_home_fouls", "actual_away_fouls", "actual_total_fouls",
    "actual_home_xg", "actual_away_xg", "actual_total_xg",
    "actual_home_big", "actual_away_big", "actual_total_big",
    "available_metrics", "actuals_verdict", "source_guard", "auto_apply", "production_change",
]


def n(v: object) -> str:
    return "" if v is None else str(v).strip()


def u(v: object) -> str:
    return n(v).upper()


def x(v: object) -> float | None:
    t = n(v)
    if not t or t.lower() == "nan":
        return None
    try:
        return float(t)
    except ValueError:
        return None


def v(vv: float | None) -> str:
    if vv is None:
        return ""
    return str(int(vv)) if abs(vv - round(vv)) < 1e-9 else f"{vv:.2f}"


def read(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return [dict(r) for r in csv.DictReader(f)]


def write(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in FIELDS})


def dated(base: Path, day: str, name: str) -> Path:
    return base / "today" / day / name


def row_day(r: dict[str, str]) -> str:
    for k in ("target_date", "date"):
        val = n(r.get(k))[:10]
        if val:
            return val
    return ""


def status(r: dict[str, str]) -> str:
    s = u(r.get("fixture_status_short") or r.get("status"))
    if s:
        return s
    if "MATCH FINISHED" in u(r.get("fixture_status_long")):
        return "FT"
    return "UNKNOWN"


def first(r: dict[str, str], names: list[str]) -> float | None:
    for name in names:
        if name in r:
            val = x(r.get(name))
            if val is not None:
                return val
    return None


def pair(r: dict[str, str], h: list[str], a: list[str]) -> tuple[float | None, float | None, float | None]:
    hv, av = first(r, h), first(r, a)
    tv = None if hv is None or av is None else hv + av
    return hv, av, tv


def same_day(rows: list[dict[str, str]], day: str) -> list[dict[str, str]]:
    return [r for r in rows if row_day(r) in {"", day}]


def build(day: str, tz: str, base: Path) -> list[dict[str, object]]:
    gen = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    rows = same_day(read(dated(base, day, "matches.csv")), day)
    out: list[dict[str, object]] = []
    for r in rows:
        st = status(r)
        if st not in FINAL_STATUS:
            continue
        hg, ag, tg = pair(r, ["goals_home", "score_fulltime_home", "actual_home_goals"], ["goals_away", "score_fulltime_away", "actual_away_goals"])
        hsot, asot, tsot = pair(r, ["actual_home_sot", "home_sot", "home_sot_for"], ["actual_away_sot", "away_sot", "away_sot_for"])
        hsh, ash, tsh = pair(r, ["actual_home_shots", "home_shots"], ["actual_away_shots", "away_shots"])
        hcor, acor, tcor = pair(r, ["actual_home_corners", "home_corners"], ["actual_away_corners", "away_corners"])
        hcard, acard, tcard = pair(r, ["actual_home_cards", "home_cards", "home_yellow_cards"], ["actual_away_cards", "away_cards", "away_yellow_cards"])
        hfoul, afoul, tfoul = pair(r, ["actual_home_fouls", "home_fouls"], ["actual_away_fouls", "away_fouls"])
        hxg, axg, txg = pair(r, ["actual_home_xg", "home_xg_for"], ["actual_away_xg", "away_xg_for"])
        hbig, abig, tbig = pair(r, ["actual_home_big", "home_big_for"], ["actual_away_big", "away_big_for"])
        if tsot == 0 and (tg or 0) > 0:
            hsot = asot = tsot = None
        metrics = []
        if tg is not None: metrics.append("goals")
        if tsot is not None: metrics.append("sot")
        if tsh is not None: metrics.append("shots")
        if tcor is not None: metrics.append("corners")
        if tcard is not None: metrics.append("cards")
        if tfoul is not None: metrics.append("fouls")
        if txg is not None: metrics.append("xg")
        if tbig is not None: metrics.append("big")
        out.append({
            "target_date": day, "generated_at": gen, "fixture_id": n(r.get("fixture_id")),
            "home_team": n(r.get("home_team")), "away_team": n(r.get("away_team")), "status": st,
            "actual_home_goals": v(hg), "actual_away_goals": v(ag), "actual_total_goals": v(tg),
            "actual_home_sot": v(hsot), "actual_away_sot": v(asot), "actual_total_sot": v(tsot),
            "actual_home_shots": v(hsh), "actual_away_shots": v(ash), "actual_total_shots": v(tsh),
            "actual_home_corners": v(hcor), "actual_away_corners": v(acor), "actual_total_corners": v(tcor),
            "actual_home_cards": v(hcard), "actual_away_cards": v(acard), "actual_total_cards": v(tcard),
            "actual_home_fouls": v(hfoul), "actual_away_fouls": v(afoul), "actual_total_fouls": v(tfoul),
            "actual_home_xg": v(hxg), "actual_away_xg": v(axg), "actual_total_xg": v(txg),
            "actual_home_big": v(hbig), "actual_away_big": v(abig), "actual_total_big": v(tbig),
            "available_metrics": "; ".join(metrics) if metrics else "none",
            "actuals_verdict": "FINAL_ACTUALS_AVAILABLE" if metrics else "FINAL_BUT_STATS_MISSING",
            "source_guard": "DATED_INPUT_ONLY", "auto_apply": "NO", "production_change": "NO",
        })
    return out


def counts(rows: list[dict[str, object]], field: str) -> str:
    c = Counter(str(r.get(field) or "UNKNOWN") for r in rows)
    return "; ".join(f"{k}={v}" for k, v in c.most_common()) if c else "none"


def md(day: str, rows: list[dict[str, object]]) -> str:
    lines = [f"# vSIGMA Post-Match Stat Actuals - {day}", "", "## Summary", f"- rows_final: {len(rows)}", f"- verdict_counts: {counts(rows, 'actuals_verdict')}", "- source_guard: DATED_INPUT_ONLY", "- auto_apply: NO", "- production_change: NO", "", "## Actual Rows"]
    if not rows:
        lines.append("- none. No final fixtures found yet in dated matches.csv.")
    for r in rows:
        lines.append(f"- {r['home_team']} vs {r['away_team']} | status={r['status']} | goals={r['actual_total_goals'] or 'NA'} | SoT={r['actual_total_sot'] or 'NA'} | corners={r['actual_total_corners'] or 'NA'} | cards={r['actual_total_cards'] or 'NA'} | metrics={r['available_metrics']}")
    lines += ["", "## Guardrails", "- This normalizer does not infer missing shots/corners/cards/fouls from recent averages.", "- It only exposes final fixture actuals that exist in dated source files."]
    return "\n".join(lines) + "\n"


def run(day: str, tz: str, base: Path) -> None:
    day = date.fromisoformat(day).isoformat()
    rows = build(day, tz, base)
    for out_base in [base / "today" / day, base / "governance"]:
        write(out_base / "vsigma_post_match_stat_actuals.csv", rows)
        (out_base / "vsigma_post_match_stat_actuals.md").write_text(md(day, rows), encoding="utf-8")
    print("=== VSIGMA POST MATCH STAT ACTUALS ===")
    print(f"rows_final={len(rows)}")
    print(f"verdict_counts={counts(rows, 'actuals_verdict')}")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--date", required=True)
    p.add_argument("--timezone", default="Atlantic/Canary")
    p.add_argument("--processed-dir", type=Path, default=PROCESSED)
    a = p.parse_args()
    run(a.date, a.timezone, a.processed_dir)


if __name__ == "__main__":
    main()
