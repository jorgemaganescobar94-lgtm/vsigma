from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROCESSED = Path("data/processed")
FIELDS = ["target_date","generated_at","rank","fixture_id","home_team","away_team","market_primary","adjusted_status","objective_level","dependency_level","opponent_level","draw_level","lineup_level","availability_level","market_level","memory_level","context_level","context_score","policy","auto_apply","production_change"]
SIDE = {"HOME_WIN", "AWAY_WIN"}
GOALS = {"OVER_1_5", "OVER_2_5", "BTTS_YES"}


def n(v: object) -> str:
    return "" if v is None else str(v).strip()


def u(v: object) -> str:
    return n(v).upper()


def rows(p: Path) -> list[dict[str, str]]:
    if not p.exists():
        return []
    with p.open("r", encoding="utf-8-sig", newline="") as h:
        return [dict(r) for r in csv.DictReader(h)]


def write(p: Path, data: list[dict[str, object]]) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8", newline="") as h:
        w = csv.DictWriter(h, fieldnames=FIELDS)
        w.writeheader()
        for r in data:
            w.writerow({k: r.get(k, "") for k in FIELDS})


def dated(base: Path, day: str, name: str) -> Path:
    return base / "today" / day / name


def read_dated(base: Path, day: str, name: str) -> list[dict[str, str]]:
    path = dated(base, day, name)
    data = rows(path)
    return [r for r in data if n(r.get("target_date"))[:10] in {"", day}]


def ix(data: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    for r in data:
        k = n(r.get("fixture_id")).replace(".0", "")
        if k and k not in out:
            out[k] = r
    return out


def part(name: str, pts: int) -> tuple[str, int]:
    return name, pts


def objective(real: dict[str, str], market: str) -> tuple[str, int]:
    dec = u(real.get("context_gate_decision")); over = u(real.get("objective_override_status")); edge = u(real.get("objective_edge"))
    if over == "REAL_OVERRIDE" and dec == "CONTEXT_DOWNGRADE" and edge == "NEUTRAL":
        return part("REAL_NEUTRAL_NO_EDGE", 20 if market in SIDE else 10)
    if dec == "OBJECTIVE_SUPPORTS_PICK":
        return part("REAL_SUPPORT", -18)
    if dec == "OBJECTIVE_CONFLICT":
        return part("REAL_CONFLICT", 30)
    if dec == "TABLE_PROXY_TEMPO":
        return part("PROXY_TEMPO", 8)
    if over == "PROXY_ONLY":
        return part("PROXY_ONLY", 6)
    return part("OBJ_UNKNOWN", 8)


def dependency(real: dict[str, str]) -> tuple[str, int]:
    dec = u(real.get("context_gate_decision")); edge = u(real.get("objective_edge"))
    if dec == "OBJECTIVE_SUPPORTS_PICK":
        return part("DIRECT_UNKNOWN", -4)
    if dec == "CONTEXT_DOWNGRADE" and edge == "NEUTRAL":
        return part("NO_DIRECT_EDGE", 12)
    return part("DEPENDENCY_UNKNOWN", 6)


def opponent(real: dict[str, str]) -> tuple[str, int]:
    edge = u(real.get("objective_edge"))
    if edge == "NEUTRAL":
        return part("STAKE_NEUTRAL", 8)
    if edge in {"HOME", "AWAY"}:
        return part("STAKE_ASYMMETRY", -6)
    return part("STAKE_UNKNOWN", 5)


def draw(row: dict[str, str]) -> tuple[str, int]:
    market = u(row.get("market_primary")); fail = u(row.get("pick_failure_mode"))
    if market in SIDE and "DRAW" in fail:
        return part("DRAW_KILLS_ML", 16)
    if market in SIDE:
        return part("ML_DRAW_SENSITIVE", 10)
    return part("DRAW_NOT_KEY", 0)


def lineup(obj: dict[str, str]) -> tuple[str, int]:
    s = u(obj.get("lineup_status")); dec = u(obj.get("gate_decision"))
    if dec == "WAIT_PRELOCK" or s == "WAIT_PRELOCK":
        return part("WAIT_PRELOCK", 14)
    if s == "LINEUPS_CONFIRMED":
        return part("LINEUPS_CONFIRMED", -8)
    if s == "LINEUPS_NOT_CONFIRMED":
        return part("LINEUPS_NOT_CONFIRMED", 8)
    return part("LINEUP_UNKNOWN", 6)


def availability(obj: dict[str, str]) -> tuple[str, int]:
    s = u(obj.get("availability_status"))
    if s == "AVAILABILITY_RISK_ON_PICK_SIDE":
        return part("PICK_SIDE_RISK", 18)
    if s == "AVAILABILITY_CONFLICT":
        return part("AVAIL_CONFLICT", 22)
    if s == "AVAILABILITY_ELEVATED_BOTH":
        return part("AVAIL_ELEVATED", 12)
    if s == "AVAILABILITY_REPORTED_ADVISORY":
        return part("AVAIL_ADVISORY", 5)
    return part("AVAIL_UNKNOWN_CLEAN", 3)


def market_layer(row: dict[str, str]) -> tuple[str, int]:
    m = u(row.get("market_primary")); fail = u(row.get("pick_failure_mode"))
    if m in SIDE and "DRAW" in fail:
        return part("ML_DRAW_FRAGILE", 18)
    if m == "OVER_2_5" and "LOW_CONVERSION" in fail:
        return part("O25_LOW_CONV", 18)
    if m == "OVER_1_5" and "LOW_CONVERSION" in fail:
        return part("O15_LOW_CONV", 10)
    if m in GOALS:
        return part("GOALS_STANDARD", 6)
    return part("MARKET_STANDARD", 5)


def memory(audit: dict[str, str]) -> tuple[str, int]:
    lab = u(audit.get("calibration_label"))
    if lab == "CONTEXT_FILTER_VALIDATED_CASE":
        return part("MEM_AVOIDED_LOSS", 16)
    if lab == "SOFTEN_CONTEXT_DOWNGRADE_CANDIDATE":
        return part("MEM_MISSED_WIN", -10)
    if lab == "SHADOW_KEEP_VALIDATED_CASE":
        return part("MEM_SHADOW_WIN", -6)
    return part("MEM_NONE", 0)


def level(score: int) -> tuple[str, str]:
    if score >= 75: return "L9_MAX_BLOCK", "no action"
    if score >= 60: return "L8_HARD_DOWN", "hard downgrade"
    if score >= 45: return "L7_SOFT_DOWN", "reduced stake or live"
    if score >= 30: return "L6_REVIEW", "review only"
    if score >= 18: return "L5_EDGE_ONLY", "no context edge"
    if score >= 8: return "L4_CAUTION", "caution"
    if score >= 0: return "L3_OK", "acceptable"
    if score >= -15: return "L2_SUPPORT", "context support"
    return "L1_LOCK", "strong context support"


def build(day: str, tz: str, base: Path) -> list[dict[str, object]]:
    gen = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    adjusted_path = dated(base, day, "vsigma_context_adjusted_final_picks.csv")
    if not adjusted_path.exists():
        return []
    adjusted = read_dated(base, day, "vsigma_context_adjusted_final_picks.csv")
    real = ix(read_dated(base, day, "vsigma_real_objective_context_gate.csv"))
    obj = ix(read_dated(base, day, "vsigma_objective_availability_gate.csv"))
    aud = ix(read_dated(base, day, "vsigma_context_filter_calibration_advisor_details.csv"))
    out: list[dict[str, object]] = []
    for i, r in enumerate(adjusted, start=1):
        fid = n(r.get("fixture_id")).replace(".0", "")
        rr, oo, aa = real.get(fid, {}), obj.get(fid, {}), aud.get(fid, {})
        m = u(r.get("market_primary"))
        layers = [objective(rr, m), dependency(rr), opponent(rr), draw(r), lineup(oo), availability(oo), market_layer(r), memory(aa)]
        score = int(sum(x[1] for x in layers))
        lvl, pol = level(score)
        out.append({
            "target_date": day, "generated_at": gen, "rank": n(r.get("final_rank")) or i,
            "fixture_id": fid, "home_team": n(r.get("home_team")), "away_team": n(r.get("away_team")),
            "market_primary": m, "adjusted_status": u(r.get("adjusted_final_status")),
            "objective_level": layers[0][0], "dependency_level": layers[1][0], "opponent_level": layers[2][0],
            "draw_level": layers[3][0], "lineup_level": layers[4][0], "availability_level": layers[5][0],
            "market_level": layers[6][0], "memory_level": layers[7][0], "context_level": lvl,
            "context_score": score, "policy": pol, "auto_apply": "NO", "production_change": "NO"
        })
    return sorted(out, key=lambda x: (-int(x["context_score"]), int(x["rank"])))


def counts(data: list[dict[str, object]], field: str) -> str:
    c = Counter(str(r.get(field) or "UNKNOWN") for r in data)
    return "; ".join(f"{k}={v}" for k, v in c.most_common()) if c else "none"


def md(day: str, data: list[dict[str, object]]) -> str:
    lines = [f"# vSIGMA Context Level Matrix - {day}", "", "## Summary", f"- rows_reviewed: {len(data)}", f"- context_level_counts: {counts(data, 'context_level')}", "- auto_apply: NO", "- production_change: NO", "", "## Matrix Rows"]
    if not data:
        lines.append("- none. Missing dated vsigma_context_adjusted_final_picks.csv; stale governance fallback refused.")
    for r in data:
        lines.append(f"- #{r['rank']} | {r['context_level']} | score={r['context_score']} | {r['home_team']} vs {r['away_team']} | market={r['market_primary']} | policy={r['policy']}")
    lines += ["", "## Guardrails", "- This matrix refuses stale governance fallback.", "- Run context adjusted final picks for the same date before this matrix."]
    return "\n".join(lines) + "\n"


def run(day: str, tz: str, base: Path) -> None:
    day = date.fromisoformat(day).isoformat()
    data = build(day, tz, base)
    for b in [base / "today" / day, base / "governance"]:
        write(b / "vsigma_context_level_matrix.csv", data)
        (b / "vsigma_context_level_matrix.md").write_text(md(day, data), encoding="utf-8")
    print("=== VSIGMA CONTEXT LEVEL MATRIX ===")
    print(f"rows_reviewed={len(data)}")
    print(f"context_level_counts={counts(data, 'context_level')}")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--date", required=True)
    p.add_argument("--timezone", default="Atlantic/Canary")
    p.add_argument("--processed-dir", type=Path, default=PROCESSED)
    a = p.parse_args()
    run(a.date, a.timezone, a.processed_dir)


if __name__ == "__main__":
    main()
