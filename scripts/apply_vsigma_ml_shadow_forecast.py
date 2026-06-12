from __future__ import annotations

import argparse
import csv
import json
import math
import re
import unicodedata
from pathlib import Path

import numpy as np

BASE = Path("data/processed")
MODEL_PATH = Path("data/modeling/models/vsigma_stat_model.json")
STD_CLIP = 5.0
PROB_OVERCONFIDENT_THRESHOLD = 0.97
TARGET_BOUNDS = {
    "home_goals": (0.0, 5.5),
    "away_goals": (0.0, 5.5),
    "total_goals": (0.0, 8.0),
    "home_shots": (0.0, 32.0),
    "away_shots": (0.0, 32.0),
    "home_sot": (0.0, 14.0),
    "away_sot": (0.0, 14.0),
    "home_corners": (0.0, 16.0),
    "away_corners": (0.0, 16.0),
    "home_possession": (20.0, 80.0),
    "away_possession": (20.0, 80.0),
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


def softmax(logits: np.ndarray) -> np.ndarray:
    z = logits - np.max(logits)
    exp = np.exp(z)
    total = np.sum(exp)
    if not np.isfinite(total) or total <= 0:
        return np.array([1/3, 1/3, 1/3], dtype=float)
    return exp / total


def add_feature(features: dict[str, float], name: str, value: object) -> None:
    features[name] = fnum(value)


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
        out[f"feat_{side}_last5_possession"] = fnum(row.get("avg_possession"))
    return out


def build_feature_vector(model: dict, forecast: dict, day: str, base: Path, slug: str) -> tuple[np.ndarray, dict[str, float], dict[str, object]]:
    feature_cols = model["feature_cols"]
    scaler = model["scaler"]
    values: dict[str, float] = {}
    add_feature(values, "feat_market_home_prob", forecast.get("raw_home_prob") or forecast.get("home_prob"))
    add_feature(values, "feat_market_draw_prob", forecast.get("raw_draw_prob") or forecast.get("draw_prob"))
    add_feature(values, "feat_market_away_prob", forecast.get("raw_away_prob") or forecast.get("away_prob"))
    # Ad hoc forecasts usually use current market-derived or fallback probabilities, not verified historical closing odds.
    values["feat_odds_available"] = 0.0
    values["feat_home_advantage"] = 1.0
    values.update(style_features(day, base, slug))

    vec = []
    missing = 0
    clipped = 0
    explicit = 0
    for col in feature_cols:
        median = fnum(scaler["median"].get(col, 0.0))
        mean = fnum(scaler["mean"].get(col, 0.0))
        std = fnum(scaler["std"].get(col, 1.0), 1.0) or 1.0
        if col in values:
            raw = values[col]
            explicit += 1
        else:
            raw = median
            missing += 1
        z = (raw - mean) / std
        z_clipped = max(-STD_CLIP, min(STD_CLIP, z))
        if z != z_clipped:
            clipped += 1
        vec.append(z_clipped)
    diagnostics = {
        "ml_feature_count": len(feature_cols),
        "ml_feature_explicit_count": explicit,
        "ml_feature_missing_count": missing,
        "ml_feature_clip_count": clipped,
        "ml_feature_coverage_pct": round(100 * explicit / max(1, len(feature_cols)), 1),
    }
    return np.array(vec, dtype=float), values, diagnostics


def bounded_target(key: str, value: float) -> tuple[float, bool]:
    target = key.replace("target_", "")
    lo, hi = TARGET_BOUNDS.get(target, (0.0, 100.0))
    clipped_value = max(lo, min(hi, value))
    return clipped_value, clipped_value != value


def predict(model: dict, x: np.ndarray) -> dict[str, object]:
    xb = np.r_[1.0, x]
    weights = np.array(model["result_model"]["weights"], dtype=float)
    temp = fnum(model["result_model"].get("temperature", 1.0), 1.0) or 1.0
    probs = softmax((xb @ weights) / temp)
    promotion = ((model.get("metrics") or {}).get("promotion_status") or "")
    overconfident = float(np.max(probs)) >= PROB_OVERCONFIDENT_THRESHOLD and not promotion.startswith("CANDIDATE")
    out: dict[str, object] = {
        "ml_home_prob": round(float(probs[0]), 5),
        "ml_draw_prob": round(float(probs[1]), 5),
        "ml_away_prob": round(float(probs[2]), 5),
        "ml_result_forecast": model["class_order"][int(np.argmax(probs))],
        "ml_probability_sanity": "OVERCONFIDENT_SHADOW_ONLY" if overconfident else "OK",
    }
    clipped_targets = []
    for target, reg in (model.get("regressors") or {}).items():
        coef = np.array(reg["coef"], dtype=float)
        raw_value = float(xb @ coef)
        bounded, was_clipped = bounded_target(target, raw_value)
        out["ml_" + target.replace("target_", "")] = round(bounded, 3)
        if was_clipped:
            clipped_targets.append(target)
    out["ml_regression_sanity"] = "CLIPPED:" + ",".join(clipped_targets) if clipped_targets else "OK"
    return out


def md(row: dict) -> str:
    lines = [
        f"# vSIGMA ML Shadow Forecast - {row.get('target_date')}",
        "",
        f"- fixture: {row.get('home_team')} vs {row.get('away_team')}",
        f"- model_type: {row.get('model_type')}",
        f"- promotion_status: {row.get('promotion_status')}",
        f"- ml_probability_sanity: {row.get('ml_probability_sanity')}",
        f"- ml_regression_sanity: {row.get('ml_regression_sanity')}",
        f"- feature_coverage: {row.get('ml_feature_coverage_pct')}% explicit | missing={row.get('ml_feature_missing_count')} | clipped={row.get('ml_feature_clip_count')}",
        "- auto_apply: NO",
        "- production_change: NO",
        "",
        "## vSIGMA Current Forecast",
        f"- adjusted 1X2: {row.get('vsigma_home_prob')} / {row.get('vsigma_draw_prob')} / {row.get('vsigma_away_prob')}",
        f"- xG: {row.get('vsigma_home_xg')} - {row.get('vsigma_away_xg')}",
        f"- score: {row.get('vsigma_score')}",
        "",
        "## ML Shadow",
        f"- ML 1X2: {row.get('ml_home_prob')} / {row.get('ml_draw_prob')} / {row.get('ml_away_prob')}",
        f"- ML result: {row.get('ml_result_forecast')}",
    ]
    for key in sorted(row):
        if key.startswith("ml_") and key not in {"ml_home_prob", "ml_draw_prob", "ml_away_prob", "ml_result_forecast", "ml_probability_sanity", "ml_regression_sanity", "ml_feature_count", "ml_feature_explicit_count", "ml_feature_missing_count", "ml_feature_clip_count", "ml_feature_coverage_pct"}:
            lines.append(f"- {key}: {row[key]}")
    lines += [
        "",
        "## Note",
        "- Shadow only. It does not replace vSIGMA forecast until model metrics beat current baseline.",
        "- Guardrails cap out-of-range regression outputs. If sanity is CLIPPED or OVERCONFIDENT, treat ML as diagnostic only.",
    ]
    return "\n".join(lines) + "\n"


def run(day: str, home: str, away: str, model_path: Path, base: Path) -> None:
    slug = clean(f"{home}_vs_{away}")
    forecast_path = base / "today" / day / f"vsigma_adhoc_match_stat_forecast_{slug}.csv"
    rows = read_csv(forecast_path)
    if not rows:
        raise RuntimeError(f"Missing forecast file: {forecast_path}")
    model = json.loads(model_path.read_text(encoding="utf-8"))
    forecast = rows[0]
    x, raw_features, diagnostics = build_feature_vector(model, forecast, day, base, slug)
    preds = predict(model, x)
    out = {
        "target_date": day,
        "home_team": forecast.get("home_team", home),
        "away_team": forecast.get("away_team", away),
        "model_type": model.get("model_type", ""),
        "promotion_status": (model.get("metrics") or {}).get("promotion_status", ""),
        "vsigma_home_prob": forecast.get("home_prob", ""),
        "vsigma_draw_prob": forecast.get("draw_prob", ""),
        "vsigma_away_prob": forecast.get("away_prob", ""),
        "vsigma_home_xg": forecast.get("home_xg", ""),
        "vsigma_away_xg": forecast.get("away_xg", ""),
        "vsigma_score": forecast.get("ft_score_primary", ""),
        "auto_apply": "NO",
        "production_change": "NO",
        **diagnostics,
        **preds,
    }
    fields = list(out.keys())
    for folder in [base / "today" / day, base / "governance"]:
        write_csv(folder / f"vsigma_ml_shadow_forecast_{slug}.csv", [out], fields)
        (folder / f"vsigma_ml_shadow_forecast_{slug}.md").write_text(md(out), encoding="utf-8")
    print(f"ML shadow forecast built for {home} vs {away}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True)
    parser.add_argument("--home", required=True)
    parser.add_argument("--away", required=True)
    parser.add_argument("--model", type=Path, default=MODEL_PATH)
    parser.add_argument("--processed-dir", type=Path, default=BASE)
    args = parser.parse_args()
    run(args.date, args.home, args.away, args.model, args.processed_dir)
