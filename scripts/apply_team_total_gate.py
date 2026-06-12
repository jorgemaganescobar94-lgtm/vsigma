from __future__ import annotations

import argparse
import csv
import json
import math
import re
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd

BASE_PROCESSED = Path("data/processed")
DATASET_PATH = Path("data/modeling/vsigma_football_data_uk_top5.csv")
CONFIG_PATH = Path("config/vsigma_team_total_gate_overrides_v1.json")

TOP5_LEAGUE_IDS = {
    "39": "E0",
    "140": "SP1",
    "135": "I1",
    "78": "D1",
    "61": "F1",
}

TOP5_LEAGUE_NAMES = {
    "premier_league": "E0",
    "la_liga": "SP1",
    "serie_a": "I1",
    "bundesliga": "D1",
    "ligue_1": "F1",
}

TARGETS = {
    "HOME_TT_OVER_0_5": {"target_name": "home_over05", "goal_col": "target_home_goals", "op": ">=", "line": 1, "team_side": "home", "kind": "OVER_0_5"},
    "AWAY_TT_OVER_0_5": {"target_name": "away_over05", "goal_col": "target_away_goals", "op": ">=", "line": 1, "team_side": "away", "kind": "OVER_0_5"},
    "HOME_TT_OVER_1_5": {"target_name": "home_over15", "goal_col": "target_home_goals", "op": ">=", "line": 2, "team_side": "home", "kind": "OVER_1_5"},
    "AWAY_TT_OVER_1_5": {"target_name": "away_over15", "goal_col": "target_away_goals", "op": ">=", "line": 2, "team_side": "away", "kind": "OVER_1_5"},
    "HOME_TT_UNDER_1_5": {"target_name": "home_under15", "goal_col": "target_home_goals", "op": "<=", "line": 1, "team_side": "home", "kind": "UNDER_1_5"},
    "AWAY_TT_UNDER_1_5": {"target_name": "away_under15", "goal_col": "target_away_goals", "op": "<=", "line": 1, "team_side": "away", "kind": "UNDER_1_5"},
    "HOME_TT_UNDER_0_5": {"target_name": "home_under05", "goal_col": "target_home_goals", "op": "<=", "line": 0, "team_side": "home", "kind": "UNDER_0_5"},
    "AWAY_TT_UNDER_0_5": {"target_name": "away_under05", "goal_col": "target_away_goals", "op": "<=", "line": 0, "team_side": "away", "kind": "UNDER_0_5"},
}


def clean(v: object) -> str:
    t = unicodedata.normalize("NFKD", str(v or "")).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "_", t).strip("_")


def fnum(v: object, default: float = 0.0) -> float:
    try:
        value = float(str(v).replace("%", "").strip())
        if not math.isfinite(value):
            return default
        return value
    except Exception:
        return default


def sigmoid(z):
    return 1 / (1 + np.exp(-np.clip(z, -30, 30)))


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows([{k: row.get(k, "") for k in fields} for row in rows])


def standardize(train: pd.DataFrame, valid: pd.DataFrame, cols: list[str]):
    med = train[cols].median(numeric_only=True).fillna(0.0)
    tr = train[cols].fillna(med).astype(float)
    va = valid[cols].fillna(med).astype(float)
    mean = tr.mean()
    std = tr.std().replace(0, 1.0).fillna(1.0)
    return ((tr - mean) / std).to_numpy(float), ((va - mean) / std).to_numpy(float), {
        "median": med.to_dict(),
        "mean": mean.to_dict(),
        "std": std.to_dict(),
    }


def train_logistic(x, y, epochs=1500, lr=0.04, l2=0.001):
    xb = np.c_[np.ones((x.shape[0], 1)), x]
    w = np.zeros(xb.shape[1])
    for _ in range(epochs):
        p = sigmoid(xb @ w)
        grad = (xb.T @ (p - y)) / len(y)
        grad[1:] += l2 * w[1:]
        w -= lr * grad
    return w


def infer_league_code(forecast: dict) -> str:
    lid = str(forecast.get("league_id") or "").strip()
    if lid in TOP5_LEAGUE_IDS:
        return TOP5_LEAGUE_IDS[lid]
    lname = clean(forecast.get("league_name") or forecast.get("competition") or forecast.get("league") or "")
    for key, code in TOP5_LEAGUE_NAMES.items():
        if key in lname:
            return code
    return ""


def make_target(df: pd.DataFrame, market_family: str) -> np.ndarray:
    cfg = TARGETS[market_family]
    goals = pd.to_numeric(df[cfg["goal_col"]], errors="coerce").fillna(0).to_numpy(float)
    if cfg["op"] == ">=":
        return (goals >= float(cfg["line"])).astype(float)
    return (goals <= float(cfg["line"])).astype(float)


def style_features(day: str, base: Path, slug: str) -> dict[str, float]:
    rows = read_csv(base / "today" / day / f"vsigma_adhoc_team_style_{slug}.csv")
    out: dict[str, float] = {}
    for row in rows:
        side = str(row.get("team_side", "")).strip().lower()
        if side not in {"home", "away"}:
            continue
        out[f"feat_{side}_last5_games"] = fnum(row.get("matches_sample"))
        out[f"feat_{side}_last5_gf"] = fnum(row.get("avg_goals_for"))
        out[f"feat_{side}_last5_ga"] = fnum(row.get("avg_goals_against"))
        out[f"feat_{side}_last5_points"] = 0.0
        out[f"feat_{side}_last5_shots_for"] = fnum(row.get("avg_shots"))
        out[f"feat_{side}_last5_sot_for"] = fnum(row.get("avg_sot"))
        out[f"feat_{side}_last5_corners_for"] = fnum(row.get("avg_corners"))
    return out


def train_team_total_models(dataset_path: Path):
    df = pd.read_csv(dataset_path).sort_values("fixture_date").copy()
    feature_cols = sorted([c for c in df.columns if c.startswith("feat_")])
    if not feature_cols:
        raise RuntimeError("No feat_ columns found in dataset")
    x_train, _, scaler = standardize(df, df, feature_cols)
    weights_by_market: dict[str, np.ndarray] = {}
    for market_family in TARGETS:
        y = make_target(df, market_family)
        if float(np.mean(y)) in {0.0, 1.0}:
            continue
        weights_by_market[market_family] = train_logistic(x_train, y)
    return feature_cols, scaler, weights_by_market


def build_live_vector(feature_cols, scaler, forecast, day, base, slug):
    values: dict[str, float] = {}
    values["feat_market_home_prob"] = fnum(forecast.get("raw_home_prob") or forecast.get("home_prob"))
    values["feat_market_draw_prob"] = fnum(forecast.get("raw_draw_prob") or forecast.get("draw_prob"))
    values["feat_market_away_prob"] = fnum(forecast.get("raw_away_prob") or forecast.get("away_prob"))
    values["feat_market_over25_prob"] = fnum(forecast.get("market_over25_prob") or forecast.get("over25_prob") or forecast.get("over_25_prob"), 0.0)
    values["feat_market_under25_prob"] = fnum(forecast.get("market_under25_prob") or forecast.get("under25_prob") or forecast.get("under_25_prob"), 0.0)
    values["feat_home_advantage"] = 1.0
    values["feat_odds_available"] = 0.0
    values.update(style_features(day, base, slug))

    league_code = infer_league_code(forecast)
    for code in ["E0", "SP1", "I1", "D1", "F1"]:
        values[f"feat_league_{code}"] = 1.0 if league_code == code else 0.0

    vec = []
    explicit = 0
    missing = 0
    for col in feature_cols:
        median = fnum(scaler["median"].get(col, 0.0))
        mean = fnum(scaler["mean"].get(col, 0.0))
        std = fnum(scaler["std"].get(col, 1.0), 1.0) or 1.0
        if col in values and values[col] != 0.0:
            raw = values[col]
            explicit += 1
        else:
            raw = median
            missing += 1
        vec.append((raw - mean) / std)

    return np.array(vec, dtype=float), values, {
        "league_code": league_code,
        "feature_count": len(feature_cols),
        "feature_explicit_count": explicit,
        "feature_missing_count": missing,
        "feature_coverage_pct": round(100 * explicit / max(1, len(feature_cols)), 1),
    }


def classify_market(market_family: str, prob: float, league_code: str, config: dict) -> dict[str, object]:
    blocked = config.get("blocked_markets") or {}
    if market_family.endswith("OVER_1_5") and "TEAM_TOTAL_OVER_1_5" in blocked:
        return {
            "team_total_gate_label": "MARKET_RESEARCH_ONLY",
            "team_total_gate_status": "RESEARCH_ONLY",
            "team_total_gate_reason": blocked["TEAM_TOTAL_OVER_1_5"].get("reason", ""),
            "model_prob_min": "",
            "validation_rows": "",
            "actual_hit_rate": "",
            "can_validate_builder": "NO",
            "can_validate_standalone": "NO",
            "can_veto_overstretch": "NO",
        }
    if market_family.endswith("UNDER_0_5") and "TEAM_TOTAL_UNDER_0_5" in blocked:
        return {
            "team_total_gate_label": "MARKET_BLOCKED",
            "team_total_gate_status": "BLOCKED",
            "team_total_gate_reason": blocked["TEAM_TOTAL_UNDER_0_5"].get("reason", ""),
            "model_prob_min": "",
            "validation_rows": "",
            "actual_hit_rate": "",
            "can_validate_builder": "NO",
            "can_validate_standalone": "NO",
            "can_veto_overstretch": "NO",
        }

    if not league_code:
        return {
            "team_total_gate_label": "OUT_OF_SCOPE_NOT_TOP5",
            "team_total_gate_status": "OUT_OF_SCOPE",
            "team_total_gate_reason": "League not recognized as top-5 validated scope.",
            "model_prob_min": "",
            "validation_rows": "",
            "actual_hit_rate": "",
            "can_validate_builder": "NO",
            "can_validate_standalone": "NO",
            "can_veto_overstretch": "NO",
        }

    league_cfg = (config.get("league_overrides") or {}).get(league_code)
    fallback_enabled = bool((config.get("global_fallback") or {}).get("enabled", False))
    if not league_cfg:
        return {
            "team_total_gate_label": "NO_LEAGUE_OVERRIDE",
            "team_total_gate_status": "NO_LEAGUE_OVERRIDE",
            "team_total_gate_reason": "No league-specific team-total override exists.",
            "model_prob_min": "",
            "validation_rows": "",
            "actual_hit_rate": "",
            "can_validate_builder": "NO",
            "can_validate_standalone": "NO",
            "can_veto_overstretch": "NO",
        }

    league_status = str(league_cfg.get("status", ""))
    if league_status == "RESEARCH_ONLY" and not fallback_enabled:
        return {
            "team_total_gate_label": "LEAGUE_RESEARCH_ONLY",
            "team_total_gate_status": "RESEARCH_ONLY",
            "team_total_gate_reason": league_cfg.get("reason", ""),
            "model_prob_min": "",
            "validation_rows": "",
            "actual_hit_rate": "",
            "can_validate_builder": "NO",
            "can_validate_standalone": "NO",
            "can_veto_overstretch": "NO",
        }

    if league_status == "BLOCKED":
        return {
            "team_total_gate_label": "LEAGUE_BLOCKED",
            "team_total_gate_status": "BLOCKED",
            "team_total_gate_reason": league_cfg.get("reason", ""),
            "model_prob_min": "",
            "validation_rows": "",
            "actual_hit_rate": "",
            "can_validate_builder": "NO",
            "can_validate_standalone": "NO",
            "can_veto_overstretch": "NO",
        }

    market_cfg = (league_cfg.get("markets") or {}).get(market_family)
    if not market_cfg:
        return {
            "team_total_gate_label": "MARKET_NOT_PROMOTED",
            "team_total_gate_status": "HOLD",
            "team_total_gate_reason": "Market is not explicitly promoted for this league.",
            "model_prob_min": "",
            "validation_rows": "",
            "actual_hit_rate": "",
            "can_validate_builder": "NO",
            "can_validate_standalone": "NO",
            "can_veto_overstretch": "NO",
        }

    p_min = fnum(market_cfg.get("model_prob_min"), 999.0)
    status = str(market_cfg.get("status", ""))
    if prob < p_min:
        return {
            "team_total_gate_label": "THRESHOLD_NOT_MET",
            "team_total_gate_status": status,
            "team_total_gate_reason": "Promoted market exists, but model probability is below threshold.",
            "model_prob_min": p_min,
            "validation_rows": market_cfg.get("validation_rows", ""),
            "actual_hit_rate": market_cfg.get("actual_hit_rate", ""),
            "can_validate_builder": "NO",
            "can_validate_standalone": "NO",
            "can_veto_overstretch": "NO",
        }

    label = "TEAM_TOTAL_STRONG" if status == "PROMOTE_STRONG" else "TEAM_TOTAL_SUPPORT"
    is_under15 = market_family.endswith("UNDER_1_5")
    return {
        "team_total_gate_label": label,
        "team_total_gate_status": status,
        "team_total_gate_reason": market_cfg.get("usage", ""),
        "model_prob_min": p_min,
        "validation_rows": market_cfg.get("validation_rows", ""),
        "actual_hit_rate": market_cfg.get("actual_hit_rate", ""),
        "can_validate_builder": "YES" if status == "PROMOTE_STRONG" else "YES_SECONDARY",
        "can_validate_standalone": "NO",
        "can_veto_overstretch": "YES" if is_under15 and status == "PROMOTE_STRONG" else "NO",
    }


def md(rows: list[dict[str, object]]) -> str:
    if not rows:
        return "# vSIGMA Team Total Gate\n\nNo rows.\n"
    head = rows[0]
    validated = [r for r in rows if str(r.get("team_total_gate_label")) in {"TEAM_TOTAL_STRONG", "TEAM_TOTAL_SUPPORT"}]
    lines = [
        f"# vSIGMA Team Total Gate - {head.get('target_date')}",
        "",
        f"- fixture: {head.get('home_team')} vs {head.get('away_team')}",
        f"- league_code: {head.get('league_code')}",
        f"- rule_id: {head.get('rule_id')}",
        "- auto_bet: NO",
        "- production_change: NO",
        "",
        "## Validated / supported markets",
    ]
    if not validated:
        lines.append("- none")
    else:
        for row in validated:
            lines.append(
                f"- {row.get('market_family')}: {row.get('team_total_gate_label')} "
                f"p={row.get('model_prob')} min={row.get('model_prob_min')} "
                f"builder={row.get('can_validate_builder')} veto={row.get('can_veto_overstretch')}"
            )
    lines += [
        "",
        "## Full gate map",
    ]
    for row in rows:
        lines.append(
            f"- {row.get('market_family')}: {row.get('team_total_gate_label')} "
            f"p={row.get('model_prob')} status={row.get('team_total_gate_status')}"
        )
    lines += [
        "",
        "## Governance",
        "- Team totals validate or veto; they do not automatically create picks.",
        "- Standalone use remains disabled until price survival and tactical agreement are added.",
        "- Builder use requires vSIGMA tactical agreement and lineup confirmation.",
        "",
        "## Feature diagnostics",
        f"- feature_coverage: {head.get('feature_coverage_pct')}% explicit",
        f"- missing: {head.get('feature_missing_count')}",
    ]
    return "\n".join(lines) + "\n"


def run(day: str, home: str, away: str, processed_dir: Path, dataset_path: Path, config_path: Path) -> None:
    slug = clean(f"{home}_vs_{away}")
    forecast_path = processed_dir / "today" / day / f"vsigma_adhoc_match_stat_forecast_{slug}.csv"
    rows = read_csv(forecast_path)
    if not rows:
        raise RuntimeError(f"Missing forecast file: {forecast_path}")
    forecast = rows[0]
    config = read_json(config_path)
    feature_cols, scaler, weights_by_market = train_team_total_models(dataset_path)
    x, raw_features, diag = build_live_vector(feature_cols, scaler, forecast, day, processed_dir, slug)
    xb = np.r_[1.0, x]

    out_rows: list[dict[str, object]] = []
    for market_family, cfg in TARGETS.items():
        weights = weights_by_market.get(market_family)
        prob = float(sigmoid(xb @ weights)) if weights is not None else 0.0
        gate = classify_market(market_family, prob, diag["league_code"], config)
        out_rows.append({
            "target_date": day,
            "home_team": forecast.get("home_team", home),
            "away_team": forecast.get("away_team", away),
            "rule_id": config.get("rule_id", "TEAM_TOTAL_GATE_OVERRIDES_V1"),
            "rule_status": config.get("status", ""),
            "league_code": diag["league_code"],
            "market_family": market_family,
            "target_name": cfg["target_name"],
            "team_side": cfg["team_side"],
            "market_kind": cfg["kind"],
            "model_prob": round(prob, 5),
            **gate,
            "auto_bet": "NO",
            "production_change": "NO",
            **diag,
        })

    fields = list(out_rows[0].keys())
    for folder in [processed_dir / "today" / day, processed_dir / "governance"]:
        write_csv(folder / f"vsigma_team_total_gate_{slug}.csv", out_rows, fields)
        (folder / f"vsigma_team_total_gate_{slug}.md").write_text(md(out_rows), encoding="utf-8")

    valid = [r for r in out_rows if str(r.get("team_total_gate_label")) in {"TEAM_TOTAL_STRONG", "TEAM_TOTAL_SUPPORT"}]
    print(f"Team total gate built for {home} vs {away}: validated={len(valid)} league={diag['league_code'] or 'OUT_OF_SCOPE'}")
    for row in valid:
        print(f"- {row['market_family']} {row['team_total_gate_label']} p={row['model_prob']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True)
    parser.add_argument("--home", required=True)
    parser.add_argument("--away", required=True)
    parser.add_argument("--processed-dir", type=Path, default=BASE_PROCESSED)
    parser.add_argument("--dataset", type=Path, default=DATASET_PATH)
    parser.add_argument("--config", type=Path, default=CONFIG_PATH)
    args = parser.parse_args()
    run(args.date, args.home, args.away, args.processed_dir, args.dataset, args.config)
