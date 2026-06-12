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
RULE_PATH = Path("data/modeling/models/vsigma_under35_shadow_gate_v1.json")

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

def train_under35_model(dataset_path: Path):
    df = pd.read_csv(dataset_path).sort_values("fixture_date").copy()
    feature_cols = sorted([c for c in df.columns if c.startswith("feat_")])
    y = pd.to_numeric(df["target_under35"], errors="coerce").fillna(0).to_numpy(float)
    x_train, _, scaler = standardize(df, df, feature_cols)
    weights = train_logistic(x_train, y)
    return feature_cols, scaler, weights

def build_live_vector(feature_cols, scaler, forecast, day, base, slug, market_under25_prob, market_over25_prob):
    values: dict[str, float] = {}

    values["feat_market_home_prob"] = fnum(forecast.get("raw_home_prob") or forecast.get("home_prob"))
    values["feat_market_draw_prob"] = fnum(forecast.get("raw_draw_prob") or forecast.get("draw_prob"))
    values["feat_market_away_prob"] = fnum(forecast.get("raw_away_prob") or forecast.get("away_prob"))

    if market_under25_prob is not None:
        values["feat_market_under25_prob"] = market_under25_prob
    else:
        values["feat_market_under25_prob"] = fnum(
            forecast.get("market_under25_prob")
            or forecast.get("under25_prob")
            or forecast.get("under_25_prob"),
            0.0,
        )

    if market_over25_prob is not None:
        values["feat_market_over25_prob"] = market_over25_prob
    else:
        values["feat_market_over25_prob"] = fnum(
            forecast.get("market_over25_prob")
            or forecast.get("over25_prob")
            or forecast.get("over_25_prob"),
            0.0,
        )

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

def classify_gate(p_under35: float, market_under25: float, league_code: str) -> tuple[str, str, str]:
    if not league_code:
        return "OUT_OF_SCOPE_NOT_TOP5", "NO", "NO"

    if p_under35 >= 0.85 and market_under25 >= 0.55:
        return "ELITE", "YES", "YES"

    if p_under35 >= 0.80 and market_under25 >= 0.60:
        return "STRONG_CLEAN", "YES", "YES"

    if p_under35 >= 0.80 and market_under25 >= 0.55:
        return "STRONG", "YES", "YES"

    if p_under35 >= 0.75 and market_under25 >= 0.60:
        return "SUPPORT", "YES_SECONDARY", "YES_WEAK"

    if 0.70 <= p_under35 < 0.75:
        return "NO_PREMIUM_ZONE", "NO", "NO"

    return "NONE", "NO", "NO"

def md(row: dict) -> str:
    return "\n".join([
        f"# vSIGMA U35 Shadow Gate - {row.get('target_date')}",
        "",
        f"- fixture: {row.get('home_team')} vs {row.get('away_team')}",
        f"- gate_label: {row.get('u35_gate_label')}",
        f"- model_under35_prob: {row.get('model_under35_prob')}",
        f"- market_under25_prob: {row.get('market_under25_prob')}",
        f"- market_over25_prob: {row.get('market_over25_prob')}",
        f"- league_code: {row.get('league_code')}",
        f"- can_validate_under35: {row.get('can_validate_under35')}",
        f"- can_veto_over_btts_builder: {row.get('can_veto_over_btts_builder')}",
        "",
        "## Governance",
        "- auto_bet: NO",
        "- production_change: NO",
        "- use: robustness gate only when vSIGMA tactical read agrees.",
        "- veto: can flag overstretched Over/BTTS/builders when gate is STRONG or ELITE.",
        "",
        "## Feature diagnostics",
        f"- feature_coverage: {row.get('feature_coverage_pct')}% explicit",
        f"- missing: {row.get('feature_missing_count')}",
    ]) + "\n"

def run(day, home, away, processed_dir, dataset_path, rule_path, market_under25_prob, market_over25_prob):
    slug = clean(f"{home}_vs_{away}")
    forecast_path = processed_dir / "today" / day / f"vsigma_adhoc_match_stat_forecast_{slug}.csv"
    rows = read_csv(forecast_path)
    if not rows:
        raise RuntimeError(f"Missing forecast file: {forecast_path}")

    forecast = rows[0]
    feature_cols, scaler, weights = train_under35_model(dataset_path)
    x, raw_features, diag = build_live_vector(
        feature_cols,
        scaler,
        forecast,
        day,
        processed_dir,
        slug,
        market_under25_prob,
        market_over25_prob,
    )

    xb = np.r_[1.0, x]
    p_under35 = float(sigmoid(xb @ weights))
    market_u25 = fnum(raw_features.get("feat_market_under25_prob"))
    market_o25 = fnum(raw_features.get("feat_market_over25_prob"))

    label, validate, veto = classify_gate(p_under35, market_u25, diag["league_code"])
    rule = json.loads(rule_path.read_text(encoding="utf-8-sig")) if rule_path.exists() else {}

    out = {
        "target_date": day,
        "home_team": forecast.get("home_team", home),
        "away_team": forecast.get("away_team", away),
        "rule_id": rule.get("rule_id", "U35_SHADOW_GATE_V1"),
        "rule_status": rule.get("status", "PROMOTED_AS_SHADOW_GATE_NOT_AUTO_BET"),
        "league_code": diag["league_code"],
        "model_under35_prob": round(p_under35, 5),
        "market_under25_prob": round(market_u25, 5),
        "market_over25_prob": round(market_o25, 5),
        "u35_gate_label": label,
        "can_validate_under35": validate,
        "can_veto_over_btts_builder": veto,
        "auto_bet": "NO",
        "production_change": "NO",
        **diag,
    }

    fields = list(out.keys())
    for folder in [processed_dir / "today" / day, processed_dir / "governance"]:
        write_csv(folder / f"vsigma_under35_shadow_gate_{slug}.csv", [out], fields)
        (folder / f"vsigma_under35_shadow_gate_{slug}.md").write_text(md(out), encoding="utf-8")

    print(f"U35 shadow gate built for {home} vs {away}: {label} p={p_under35:.5f}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True)
    parser.add_argument("--home", required=True)
    parser.add_argument("--away", required=True)
    parser.add_argument("--processed-dir", type=Path, default=BASE_PROCESSED)
    parser.add_argument("--dataset", type=Path, default=DATASET_PATH)
    parser.add_argument("--rule", type=Path, default=RULE_PATH)
    parser.add_argument("--market-under25-prob", type=float, default=None)
    parser.add_argument("--market-over25-prob", type=float, default=None)
    args = parser.parse_args()

    run(
        args.date,
        args.home,
        args.away,
        args.processed_dir,
        args.dataset,
        args.rule,
        args.market_under25_prob,
        args.market_over25_prob,
    )
