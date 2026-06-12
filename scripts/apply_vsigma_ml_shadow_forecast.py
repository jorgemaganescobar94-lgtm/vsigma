from __future__ import annotations

import argparse
import csv
import json
import re
import unicodedata
from pathlib import Path

import numpy as np

BASE = Path("data/processed")
MODEL_PATH = Path("data/modeling/models/vsigma_stat_model.json")


def clean(v: object) -> str:
    t = unicodedata.normalize("NFKD", str(v or "")).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "_", t).strip("_")


def fnum(v: object, default: float = 0.0) -> float:
    try:
        return float(str(v).replace("%", "").strip())
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
    return exp / np.sum(exp)


def add_feature(features: dict[str, float], name: str, value: object) -> None:
    features[name] = fnum(value)


def style_features(day: str, base: Path, slug: str) -> dict[str, float]:
    rows = read_csv(base / "today" / day / f"vsigma_adhoc_team_style_{slug}.csv")
    out: dict[str, float] = {}
    for row in rows:
        side = str(row.get("team_side", "")).strip().lower()
        if side not in {"home", "away"}:
            continue
        out[f"feat_{side}_last5_gf"] = fnum(row.get("avg_goals_for"))
        out[f"feat_{side}_last5_ga"] = fnum(row.get("avg_goals_against"))
        out[f"feat_{side}_last5_shots_for"] = fnum(row.get("avg_shots"))
        out[f"feat_{side}_last5_sot_for"] = fnum(row.get("avg_sot"))
        out[f"feat_{side}_last5_corners_for"] = fnum(row.get("avg_corners"))
        out[f"feat_{side}_last5_possession"] = fnum(row.get("avg_possession"))
    return out


def build_feature_vector(model: dict, forecast: dict, day: str, base: Path, slug: str) -> tuple[np.ndarray, dict[str, float]]:
    feature_cols = model["feature_cols"]
    scaler = model["scaler"]
    values: dict[str, float] = {}
    add_feature(values, "feat_market_home_prob", forecast.get("raw_home_prob") or forecast.get("home_prob"))
    add_feature(values, "feat_market_draw_prob", forecast.get("raw_draw_prob") or forecast.get("draw_prob"))
    add_feature(values, "feat_market_away_prob", forecast.get("raw_away_prob") or forecast.get("away_prob"))
    values["feat_home_advantage"] = 1.0
    values.update(style_features(day, base, slug))
    vec = []
    for col in feature_cols:
        median = fnum(scaler["median"].get(col, 0.0))
        mean = fnum(scaler["mean"].get(col, 0.0))
        std = fnum(scaler["std"].get(col, 1.0), 1.0) or 1.0
        raw = values.get(col, median)
        vec.append((raw - mean) / std)
    return np.array(vec, dtype=float), values


def predict(model: dict, x: np.ndarray) -> dict[str, object]:
    xb = np.r_[1.0, x]
    weights = np.array(model["result_model"]["weights"], dtype=float)
    temp = fnum(model["result_model"].get("temperature", 1.0), 1.0) or 1.0
    probs = softmax((xb @ weights) / temp)
    out: dict[str, object] = {
        "ml_home_prob": round(float(probs[0]), 5),
        "ml_draw_prob": round(float(probs[1]), 5),
        "ml_away_prob": round(float(probs[2]), 5),
        "ml_result_forecast": model["class_order"][int(np.argmax(probs))],
    }
    for target, reg in (model.get("regressors") or {}).items():
        coef = np.array(reg["coef"], dtype=float)
        value = float(xb @ coef)
        out["ml_" + target.replace("target_", "")] = round(max(0.0, value), 3)
    return out


def md(row: dict) -> str:
    lines = [
        f"# vSIGMA ML Shadow Forecast - {row.get('target_date')}",
        "",
        f"- fixture: {row.get('home_team')} vs {row.get('away_team')}",
        f"- model_type: {row.get('model_type')}",
        f"- promotion_status: {row.get('promotion_status')}",
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
        if key.startswith("ml_") and key not in {"ml_home_prob", "ml_draw_prob", "ml_away_prob", "ml_result_forecast"}:
            lines.append(f"- {key}: {row[key]}")
    lines += ["", "## Note", "- Shadow only. It does not replace vSIGMA forecast until model metrics beat current baseline."]
    return "\n".join(lines) + "\n"


def run(day: str, home: str, away: str, model_path: Path, base: Path) -> None:
    slug = clean(f"{home}_vs_{away}")
    forecast_path = base / "today" / day / f"vsigma_adhoc_match_stat_forecast_{slug}.csv"
    rows = read_csv(forecast_path)
    if not rows:
        raise RuntimeError(f"Missing forecast file: {forecast_path}")
    model = json.loads(model_path.read_text(encoding="utf-8"))
    forecast = rows[0]
    x, raw_features = build_feature_vector(model, forecast, day, base, slug)
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
