from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import build_candidate_provenance_ledger
import apply_candidate_provenance_ceiling

PROCESSED = Path("data/processed")
FIELDS = [
    "target_date", "generated_at", "rank", "fixture_id", "home_team", "away_team",
    "forecast_confidence", "forecast_warning", "portfolio_status", "context_level", "market_hint",
    "stat_profile", "primary_stat_market", "secondary_stat_market", "execution_permission",
    "stake_band", "translation_score", "translation_reason", "kill_switch", "source_guard",
    "auto_apply", "production_change",
]
GUARD_FIELDS = [
    "target_date", "generated_at", "fixture_id", "home_team", "away_team", "market_hint",
    "before_primary", "after_primary", "before_permission", "after_permission", "guard_action",
    "reason", "auto_apply", "production_change",
]


def norm(v: object) -> str:
    return "" if v is None else str(v).strip()


def up(v: object) -> str:
    return norm(v).upper()


def num(v: object, default: float = 0.0) -> float:
    try:
        text = norm(v)
        if not text or text.lower() == "nan":
            return default
        return float(text)
    except ValueError:
        return default


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return [dict(r) for r in csv.DictReader(f)]


def write_rows(path: Path, rows: list[dict[str, object]], fields: list[str] = FIELDS) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def dated(base: Path, day: str, name: str) -> Path:
    return base / "today" / day / name


def row_day(row: dict[str, str]) -> str:
    for field in ("target_date", "date"):
        value = norm(row.get(field))[:10]
        if value:
            return value
    return ""


def same_day(rows: list[dict[str, str]], day: str) -> list[dict[str, str]]:
    return [r for r in rows if row_day(r) in {"", day}]


def fixture_id(row: dict[str, str]) -> str:
    return norm(row.get("fixture_id")).replace(".0", "")


def index_by_fixture(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    for r in rows:
        fid = fixture_id(r)
        if fid and fid not in out:
            out[fid] = r
    return out


def level_score(confidence: str) -> int:
    return {"HIGH": 18, "MEDIUM": 10, "LOW": -12}.get(up(confidence), 0)


def warning_penalty(warning: str) -> int:
    w = up(warning)
    score = 0
    if "LINEUPS_INACTIVE" in w:
        score -= 12
    if "AVAILABILITY_RISK" in w:
        score -= 8
    if "LOW_CONVERSION" in w:
        score -= 10
    if "PARTIAL_RECENT_STATS" in w:
        score -= 8
    if "SHOT_SAMPLE_WEAK" in w:
        score -= 6
    if "CORNER_SAMPLE_WEAK" in w:
        score -= 4
    if "CARD_SAMPLE_WEAK" in w:
        score -= 4
    return score


def market_candidates(f: dict[str, str]) -> tuple[str, str, str, int]:
    total_goals_mid = num(f.get("total_goals_mid"))
    total_goals_low = num(f.get("total_goals_low"))
    total_sot_mid = num(f.get("total_sot_mid"))
    total_sot_low = num(f.get("total_sot_low"))
    total_corners_mid = num(f.get("total_corners_mid"))
    total_corners_low = num(f.get("total_corners_low"))
    total_cards_mid = num(f.get("total_cards_mid"))
    total_cards_low = num(f.get("total_cards_low"))
    tempo = up(f.get("tempo_projection"))
    threat = up(f.get("both_teams_threat_level"))
    shot_level = up(f.get("shot_volume_level"))
    corner_level = up(f.get("corner_volume_level"))
    card_level = up(f.get("card_risk_level"))

    reasons: list[str] = []
    score = 0
    primary = "NO_CLEAR_STAT_MARKET"
    secondary = "NONE"

    if total_goals_low >= 2.05 and total_sot_low >= 5 and total_goals_mid >= 2.75:
        primary = "OVER_1_5_SUPPORTED"
        secondary = "OVER_2_5_REVIEW" if total_goals_mid >= 3.05 and total_sot_mid >= 7 else "BTTS_OR_OVER_1_5_REVIEW"
        score += 28
        reasons.append("goals floor and SoT floor support broad goals market")
    elif total_goals_mid >= 2.85 and total_sot_mid >= 7:
        primary = "OVER_2_5_REVIEW"
        secondary = "OVER_1_5_SAFER"
        score += 20
        reasons.append("midline goals/SoT support over profile but floor is not strong enough")
    elif total_goals_mid <= 2.45 and total_sot_mid <= 7:
        primary = "UNDER_3_5_REVIEW"
        secondary = "NO_GOALS_AGGRESSION"
        score += 12
        reasons.append("goals and SoT profile lean controlled")

    if threat == "BOTH_TEAMS_THREAT" and total_sot_mid >= 7:
        if primary == "NO_CLEAR_STAT_MARKET":
            primary = "BTTS_YES_REVIEW"
            secondary = "OVER_1_5_REVIEW"
            score += 16
        else:
            secondary = secondary if secondary != "NONE" else "BTTS_YES_REVIEW"
            score += 5
        reasons.append("both teams carry shot-on-target threat")

    if total_corners_low >= 8 and total_corners_mid >= 10.0 and corner_level == "HIGH_CORNER_VOLUME":
        if primary == "NO_CLEAR_STAT_MARKET":
            primary = "CORNERS_OVER_8_5_REVIEW"
            secondary = "CORNERS_OVER_9_5_AGGRESSIVE"
        elif secondary in {"NONE", "NO_GOALS_AGGRESSION"}:
            secondary = "CORNERS_OVER_8_5_REVIEW"
        score += 11
        reasons.append("corner projection has playable volume")

    if total_cards_low >= 3 and total_cards_mid >= 4.4 and card_level == "HIGH_CARD_RISK":
        if primary == "NO_CLEAR_STAT_MARKET":
            primary = "CARDS_OVER_3_5_REVIEW"
            secondary = "CARDS_OVER_4_5_AGGRESSIVE"
        elif secondary == "NONE":
            secondary = "CARDS_OVER_3_5_REVIEW"
        score += 8
        reasons.append("card projection elevated")

    if tempo == "HIGH_TEMPO":
        score += 6
        reasons.append("high tempo projection")
    if shot_level == "HIGH_SHOT_VOLUME":
        score += 5
        reasons.append("high shot-volume projection")

    profile_parts = [tempo, shot_level, corner_level, card_level, threat]
    return primary, secondary, " | ".join(profile_parts), score if reasons else 0


def portfolio_gate(portfolio: dict[str, str] | None) -> tuple[str, str, int]:
    if not portfolio:
        return "NO_PORTFOLIO_CONTEXT", "WATCH_ONLY", -8
    status = up(portfolio.get("final_portfolio_status"))
    level = up(portfolio.get("context_level"))
    if status in {"CONTEXT_SUPPORTED_CANDIDATE", "CONTEXT_OK_CANDIDATE"} and level in {"L1_LOCK", "L2_SUPPORT", "L3_OK", "L4_CAUTION"}:
        return status, "LOW_IF_PRICE_OK", 10
    if status == "REVIEW_ONLY" or level == "L6_REVIEW":
        return status or level, "LOW_IF_CONFIRMED", -2
    if status == "LIVE_ONLY_OR_SYMBOLIC" or level == "L7_SOFT_DOWN":
        return status or level, "SYMBOLIC_OR_LIVE_ONLY", -14
    if level in {"L8_HARD_DOWN", "L9_MAX_BLOCK"}:
        return status or level, "NO_STAKE", -30
    return status or level or "UNKNOWN", "LOW_OR_NONE", -6


def permission(score: int, primary: str, warning: str, portfolio_status: str, confidence: str) -> tuple[str, str, str]:
    w = up(warning)
    p = up(portfolio_status)
    c = up(confidence)
    if primary == "NO_CLEAR_STAT_MARKET":
        return "NO_BET", "NO_STAKE", "no stat market has enough support"
    if c == "LOW":
        return "NO_BET_OR_WATCH", "NO_STAKE_OR_SYMBOLIC", "low forecast confidence blocks execution; watch only"
    if score < 0:
        return "NO_BET_OR_WATCH", "NO_STAKE_OR_SYMBOLIC", "negative translation score after guards"
    if p in {"L8_HARD_DOWN", "L9_MAX_BLOCK", "NO_ACTION_CONTEXT"}:
        return "NO_BET", "NO_STAKE", "context matrix blocks execution"
    if p == "NO_PORTFOLIO_CONTEXT":
        if score >= 28:
            return "STAT_WATCH_ONLY", "NO_STAKE_OR_SYMBOLIC", "statistical watch only; no portfolio/context confirmation"
        return "NO_BET_OR_WATCH", "NO_STAKE_OR_SYMBOLIC", "no portfolio/context confirmation and score not strong enough"
    if "LINEUPS_INACTIVE" in w or p == "LIVE_ONLY_OR_SYMBOLIC":
        return "LIVE_ONLY", "SYMBOLIC_ONLY", "lineups/context require live or prelock confirmation"
    if score >= 32:
        return "REVIEW_LOW_STAKE", "LOW_IF_CONFIRMED", "stat forecast supports market but no automatic execution"
    if score >= 18:
        return "REVIEW_ONLY", "LOW_OR_SYMBOLIC", "stat forecast is supportive but fragile"
    return "NO_BET_OR_WATCH", "NO_STAKE_OR_SYMBOLIC", "insufficient post-guard score"


def proxy_fixtures(base: Path, day: str) -> set[str]:
    rows = same_day(read_rows(dated(base, day, "vsigma_today_execution_shortlist.csv")), day)
    out: set[str] = set()
    for row in rows:
        marker = up(row.get("bridge_source")) + " " + up(row.get("guardrail_status"))
        if "VSIGMA_REAL_OBJECTIVE_CONTEXT_GATE" in marker or "BASE_PROXY_FROM_OBJECTIVE_GATE" in marker:
            fid = fixture_id(row)
            if fid:
                out.add(fid)
    return out


def proxy_inversion_guard(row: dict[str, object], proxy_ids: set[str]) -> tuple[dict[str, object], dict[str, str]]:
    fid = norm(row.get("fixture_id")).replace(".0", "")
    before_primary = up(row.get("primary_stat_market"))
    before_permission = up(row.get("execution_permission"))
    hint = up(row.get("market_hint"))
    is_proxy = fid in proxy_ids
    hint_is_tempo_or_over = hint.startswith("OVER") or hint.startswith("BTTS") or "TEMPO" in hint
    inversion = before_primary.startswith("UNDER") or up(row.get("secondary_stat_market")) == "NO_GOALS_AGGRESSION"
    if is_proxy and hint_is_tempo_or_over and inversion:
        row["primary_stat_market"] = "NO_CLEAR_STAT_MARKET"
        row["secondary_stat_market"] = "NONE"
        row["execution_permission"] = "NO_BET"
        row["stake_band"] = "NO_STAKE"
        row["translation_score"] = min(int(row.get("translation_score") or -34), -34)
        row["kill_switch"] = "PROXY_BRIDGE_INVERSION_BLOCK"
        row["translation_reason"] = (
            norm(row.get("translation_reason"))
            + "; proxy_bridge_calibration_guard=blocked inversion from tempo/over proxy into under/no-goals market"
        ).strip("; ")
        row["source_guard"] = (up(row.get("source_guard")) + "; PROXY_BRIDGE_CALIBRATION_GUARD").strip("; ")
        action = "BLOCKED_INVERSION"
        reason = "proxy objective-context tempo/over source cannot be inverted into under/no-goals market"
    else:
        action = "NO_CHANGE"
        reason = "not a proxy inversion"
    return row, {
        "target_date": norm(row.get("target_date")),
        "generated_at": norm(row.get("generated_at")),
        "fixture_id": fid,
        "home_team": norm(row.get("home_team")),
        "away_team": norm(row.get("away_team")),
        "market_hint": hint,
        "before_primary": before_primary,
        "after_primary": up(row.get("primary_stat_market")),
        "before_permission": before_permission,
        "after_permission": up(row.get("execution_permission")),
        "guard_action": action,
        "reason": reason,
        "auto_apply": "NO",
        "production_change": "NO",
    }


def build_row(f: dict[str, str], portfolio: dict[str, str] | None, target_date: str, generated_at: str, rank: int) -> dict[str, object]:
    primary, secondary, stat_profile, stat_score = market_candidates(f)
    port_status, default_stake, port_score = portfolio_gate(portfolio)
    confidence = f.get("forecast_confidence", "")
    score = stat_score + level_score(confidence) + warning_penalty(f.get("forecast_warning", "")) + port_score
    exec_permission, stake, reason_tail = permission(score, primary, f.get("forecast_warning", ""), port_status, confidence)
    kill = "NONE"
    if up(confidence) == "LOW":
        kill = "LOW_FORECAST_CONFIDENCE"
    if score < 0 and kill == "NONE":
        kill = "NEGATIVE_TRANSLATION_SCORE"
    if port_status == "NO_PORTFOLIO_CONTEXT" and kill == "NONE":
        kill = "NO_PORTFOLIO_CONTEXT"
    if "LOW_CONVERSION" in up(f.get("forecast_warning")) and primary == "OVER_2_5_REVIEW":
        kill = "LOW_CONVERSION_OVER25_FRAGILITY"
        primary = "OVER_1_5_SAFER_OR_LIVE"
    reason = f"stat_score={stat_score}; confidence={f.get('forecast_confidence')} {f.get('forecast_confidence_score')}; portfolio={port_status}; {reason_tail}"
    return {
        "target_date": target_date,
        "generated_at": generated_at,
        "rank": rank,
        "fixture_id": norm(f.get("fixture_id")),
        "home_team": norm(f.get("home_team")),
        "away_team": norm(f.get("away_team")),
        "forecast_confidence": norm(f.get("forecast_confidence")),
        "forecast_warning": norm(f.get("forecast_warning")),
        "portfolio_status": port_status,
        "context_level": up((portfolio or {}).get("context_level")),
        "market_hint": up(f.get("market_hint")),
        "stat_profile": stat_profile,
        "primary_stat_market": primary,
        "secondary_stat_market": secondary,
        "execution_permission": exec_permission,
        "stake_band": stake or default_stake,
        "translation_score": score,
        "translation_reason": reason,
        "kill_switch": kill,
        "source_guard": "DATED_INPUT_ONLY",
        "auto_apply": "NO",
        "production_change": "NO",
    }


def build(day: str, tz: str, base: Path) -> tuple[list[dict[str, object]], list[dict[str, str]]]:
    generated_at = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    forecast_path = dated(base, day, "vsigma_match_stat_forecasts.csv")
    portfolio_path = dated(base, day, "vsigma_context_matrix_portfolio_v2_details.csv")
    forecasts = same_day(read_rows(forecast_path), day)
    portfolio = index_by_fixture(same_day(read_rows(portfolio_path), day))
    proxy_ids = proxy_fixtures(base, day)
    rows: list[dict[str, object]] = []
    guard_rows: list[dict[str, str]] = []
    for i, f in enumerate(forecasts, start=1):
        fid = fixture_id(f)
        row = build_row(f, portfolio.get(fid), day, generated_at, i)
        row, guard = proxy_inversion_guard(row, proxy_ids)
        rows.append(row)
        guard_rows.append(guard)
    rows.sort(key=lambda r: (-int(r["translation_score"]), str(r["execution_permission"]), int(r["rank"])))
    for i, r in enumerate(rows, start=1):
        r["rank"] = i
    return rows, guard_rows


def counts(rows: list[dict[str, object]] | list[dict[str, str]], field: str) -> str:
    c = Counter(str(r.get(field) or "UNKNOWN") for r in rows)
    return "; ".join(f"{k}={v}" for k, v in c.most_common()) if c else "none"


def md(day: str, rows: list[dict[str, object]]) -> str:
    lines = [
        f"# vSIGMA Forecast-to-Market Translator - {day}",
        "",
        "## Summary",
        f"- rows_translated: {len(rows)}",
        f"- execution_permission_counts: {counts(rows, 'execution_permission')}",
        f"- primary_market_counts: {counts(rows, 'primary_stat_market')}",
        "- calibration_note: v68.1 blocks proxy-bridge inversion from tempo/over source into under/no-goals market; v68.2 emits provenance ledger and enforces ceilings.",
        "- source_guard: DATED_INPUT_ONLY",
        "- auto_apply: NO",
        "- production_change: NO",
        "",
        "## Translated Rows",
    ]
    if not rows:
        lines.append("- none. Need dated match stat forecasts first.")
    for r in rows:
        lines.append(
            f"- #{r['rank']} | {r['execution_permission']} | {r['home_team']} vs {r['away_team']} | "
            f"primary={r['primary_stat_market']} | secondary={r['secondary_stat_market']} | "
            f"score={r['translation_score']} | stake={r['stake_band']} | kill={r['kill_switch']} | reason={r['translation_reason']}"
        )
    lines += [
        "",
        "## Guardrails",
        "- This translator does not execute bets.",
        "- Proxy bridge rows can support diagnostics only; they cannot invert tempo/over thesis into under/no-goals markets.",
        "- Candidate provenance ceiling can only downgrade or preserve permissions.",
        "- Final execution still requires price/prelock/live confirmation.",
    ]
    return "\n".join(lines) + "\n"


def guard_md(day: str, rows: list[dict[str, str]]) -> str:
    lines = [
        f"# vSIGMA Proxy Bridge Calibration Guard - {day}",
        "",
        "## Summary",
        f"- rows_reviewed: {len(rows)}",
        f"- guard_action_counts: {counts(rows, 'guard_action')}",
        "- auto_apply: NO",
        "- production_change: NO",
        "",
        "## Guard Rows",
    ]
    if not rows:
        lines.append("- none. No translator rows reviewed.")
    for r in rows:
        lines.append(
            f"- {r['home_team']} vs {r['away_team']} | action={r['guard_action']} | market_hint={r['market_hint']} | "
            f"before={r['before_primary']} -> after={r['after_primary']} | permission={r['before_permission']} -> {r['after_permission']} | reason={r['reason']}"
        )
    lines += [
        "",
        "## Guardrails",
        "- Diagnostic/post-processing only; no stake permission is added.",
        "- The guard can only downgrade or preserve rows, never upgrade them.",
        "- It specifically blocks under/no-goals inversion created from objective-context proxy tempo/over rows.",
    ]
    return "\n".join(lines) + "\n"


def run(day: str, tz: str, base: Path) -> None:
    day = date.fromisoformat(day).isoformat()
    rows, guard_rows = build(day, tz, base)
    for out_base in [base / "today" / day, base / "governance"]:
        write_rows(out_base / "vsigma_forecast_market_translator.csv", rows, FIELDS)
        (out_base / "vsigma_forecast_market_translator.md").write_text(md(day, rows), encoding="utf-8")
        write_rows(out_base / "vsigma_proxy_bridge_calibration_guard.csv", guard_rows, GUARD_FIELDS)
        (out_base / "vsigma_proxy_bridge_calibration_guard.md").write_text(guard_md(day, guard_rows), encoding="utf-8")
    build_candidate_provenance_ledger.run(day, tz, base)
    apply_candidate_provenance_ceiling.run(day, tz, base)
    print("=== VSIGMA FORECAST MARKET TRANSLATOR ===")
    print(f"rows_translated={len(rows)}")
    print(f"execution_permission_counts={counts(rows, 'execution_permission')}")
    print(f"proxy_bridge_guard_counts={counts(guard_rows, 'guard_action')}")
    print("provenance_ledger=BUILT")
    print("provenance_ceiling=APPLIED")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True)
    parser.add_argument("--timezone", default="Atlantic/Canary")
    parser.add_argument("--processed-dir", type=Path, default=PROCESSED)
    args = parser.parse_args()
    run(args.date, args.timezone, args.processed_dir)


if __name__ == "__main__":
    main()
