from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

CLASS_ORDER = ["HOME", "DRAW", "AWAY"]
MARKET_COLS = ["feat_market_home_prob", "feat_market_draw_prob", "feat_market_away_prob"]


def softmax(logits: np.ndarray) -> np.ndarray:
    z = logits - np.max(logits, axis=1, keepdims=True)
    exp = np.exp(z)
    return exp / np.sum(exp, axis=1, keepdims=True)


def add_bias(x: np.ndarray) -> np.ndarray:
    return np.c_[np.ones((x.shape[0], 1)), x]


def log_loss(probs: np.ndarray, y: np.ndarray) -> float:
    p = np.clip(probs[np.arange(len(y)), y], 1e-12, 1.0)
    return float(-np.mean(np.log(p)))


def brier(probs: np.ndarray, y: np.ndarray) -> float:
    yy = np.eye(len(CLASS_ORDER))[y]
    return float(np.mean(np.sum((probs - yy) ** 2, axis=1)))


def accuracy(probs: np.ndarray, y: np.ndarray) -> float:
    return float(np.mean(np.argmax(probs, axis=1) == y))


def normalize_probs(probs: np.ndarray) -> np.ndarray:
    probs = np.clip(probs.astype(float), 1e-12, None)
    totals = probs.sum(axis=1, keepdims=True)
    return probs / totals


def load_model_probs(model: dict, df: pd.DataFrame) -> np.ndarray:
    feature_cols = model["feature_cols"]
    missing = [col for col in feature_cols if col not in df.columns]
    if missing:
        raise RuntimeError(f"Dataset missing model feature columns: {missing[:20]}")
    scaler = model["scaler"]
    med = pd.Series(scaler["median"])
    mean = pd.Series(scaler["mean"])
    std = pd.Series(scaler["std"]).replace(0, 1.0)
    x = df[feature_cols].copy()
    for col in feature_cols:
        x[col] = pd.to_numeric(x[col], errors="coerce").fillna(float(med.get(col, 0.0)))
    x_std = ((x - mean[feature_cols]) / std[feature_cols]).to_numpy(dtype=float)
    weights = np.array(model["result_model"]["weights"], dtype=float)
    temp = float(model["result_model"].get("temperature", 1.0))
    return softmax((add_bias(x_std) @ weights) / temp)


def eval_block(name: str, probs: np.ndarray, y: np.ndarray) -> dict[str, float]:
    return {
        "accuracy": accuracy(probs, y),
        "log_loss": log_loss(probs, y),
        "brier": brier(probs, y),
    }


def confidence_buckets(df_valid: pd.DataFrame, probs: np.ndarray, y: np.ndarray) -> list[dict[str, object]]:
    conf = probs.max(axis=1)
    pred = probs.argmax(axis=1)
    buckets = [(0.0, 0.45), (0.45, 0.50), (0.50, 0.55), (0.55, 0.60), (0.60, 0.70), (0.70, 1.01)]
    out: list[dict[str, object]] = []
    for lo, hi in buckets:
        mask = (conf >= lo) & (conf < hi)
        n = int(mask.sum())
        if not n:
            continue
        out.append({
            "range": f"[{lo:.2f},{hi:.2f})",
            "rows": n,
            "accuracy": float(np.mean(pred[mask] == y[mask])),
            "avg_confidence": float(np.mean(conf[mask])),
            "home_rate": float(np.mean(pred[mask] == 0)),
            "draw_rate": float(np.mean(pred[mask] == 1)),
            "away_rate": float(np.mean(pred[mask] == 2)),
        })
    return out


def build_divergence_csv(df_valid: pd.DataFrame, model_probs: np.ndarray, market_probs: np.ndarray, y: np.ndarray, out_path: Path, top_n: int) -> None:
    diff = np.abs(model_probs - market_probs).sum(axis=1)
    rows = []
    for idx in np.argsort(-diff)[:top_n]:
        rows.append({
            "fixture_date": df_valid.iloc[idx].get("fixture_date", ""),
            "league_name": df_valid.iloc[idx].get("league_name", ""),
            "home_team": df_valid.iloc[idx].get("home_team", ""),
            "away_team": df_valid.iloc[idx].get("away_team", ""),
            "actual": CLASS_ORDER[int(y[idx])],
            "market_pick": CLASS_ORDER[int(np.argmax(market_probs[idx]))],
            "model_pick": CLASS_ORDER[int(np.argmax(model_probs[idx]))],
            "market_home": round(float(market_probs[idx, 0]), 5),
            "market_draw": round(float(market_probs[idx, 1]), 5),
            "market_away": round(float(market_probs[idx, 2]), 5),
            "model_home": round(float(model_probs[idx, 0]), 5),
            "model_draw": round(float(model_probs[idx, 1]), 5),
            "model_away": round(float(model_probs[idx, 2]), 5),
            "l1_diff": round(float(diff[idx]), 5),
            "market_correct": int(np.argmax(market_probs[idx]) == y[idx]),
            "model_correct": int(np.argmax(model_probs[idx]) == y[idx]),
        })
    out_path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(out_path, index=False, encoding="utf-8")


def evaluate(dataset: Path, model_path: Path, metrics_out: Path, divergences_out: Path, top_n: int) -> None:
    df = pd.read_csv(dataset)
    if "fixture_date" in df.columns:
        df = df.sort_values("fixture_date")
    df = df[df["target_result_class"].isin(CLASS_ORDER)].copy()
    df["class_idx"] = df["target_result_class"].map({c: i for i, c in enumerate(CLASS_ORDER)})
    split = max(1, int(len(df) * 0.8))
    df_valid = df.iloc[split:].copy()
    if df_valid.empty:
        raise RuntimeError("Validation split is empty")
    with model_path.open("r", encoding="utf-8") as handle:
        model = json.load(handle)
    y = df_valid["class_idx"].to_numpy(dtype=int)
    model_probs = normalize_probs(load_model_probs(model, df_valid))
    market_probs = normalize_probs(df_valid[MARKET_COLS].fillna(0.0).astype(float).to_numpy())

    base_metrics = {
        "rows_valid": int(len(df_valid)),
        "market": eval_block("market", market_probs, y),
        "model": eval_block("model", model_probs, y),
    }

    blend_grid = []
    best = None
    for model_weight in [i / 100 for i in range(0, 101, 5)]:
        blend = normalize_probs((model_weight * model_probs) + ((1 - model_weight) * market_probs))
        item = {
            "model_weight": round(model_weight, 2),
            "market_weight": round(1 - model_weight, 2),
            **eval_block("blend", blend, y),
        }
        blend_grid.append(item)
        if best is None or item["log_loss"] < best["log_loss"]:
            best = item

    market_loss = base_metrics["market"]["log_loss"]
    model_loss = base_metrics["model"]["log_loss"]
    best_loss = best["log_loss"] if best else 999.0
    if best and best_loss < market_loss - 0.002:
        verdict = "BLEND_CANDIDATE_BEATS_MARKET"
    elif model_loss < market_loss - 0.002:
        verdict = "MODEL_CANDIDATE_BEATS_MARKET"
    else:
        verdict = "MARKET_DOMINANT_KEEP_ML_SHADOW"

    out = {
        **base_metrics,
        "best_blend_by_log_loss": best,
        "blend_grid": blend_grid,
        "market_confidence_buckets": confidence_buckets(df_valid, market_probs, y),
        "model_confidence_buckets": confidence_buckets(df_valid, model_probs, y),
        "verdict": verdict,
        "notes": [
            "If verdict is MARKET_DOMINANT_KEEP_ML_SHADOW, use ML for disagreement alerts and stat regressions, not as a 1X2 replacement.",
            "Blend model_weight is the share of ML probabilities in the blended 1X2 probability.",
        ],
    }
    metrics_out.parent.mkdir(parents=True, exist_ok=True)
    metrics_out.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    build_divergence_csv(df_valid, model_probs, market_probs, y, divergences_out, top_n)
    print(f"Market/model blend evaluation verdict={verdict}")
    print(f"metrics={metrics_out}")
    print(f"divergences={divergences_out}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=Path, default=Path("data/modeling/vsigma_football_data_uk_top5.csv"))
    parser.add_argument("--model", type=Path, default=Path("data/modeling/models/vsigma_stat_model_football_data_uk_top5.json"))
    parser.add_argument("--metrics-out", type=Path, default=Path("data/modeling/models/vsigma_market_blend_football_data_uk_top5_metrics.json"))
    parser.add_argument("--divergences-out", type=Path, default=Path("data/modeling/models/vsigma_market_blend_football_data_uk_top5_divergences.csv"))
    parser.add_argument("--top-n", type=int, default=100)
    args = parser.parse_args()
    evaluate(args.dataset, args.model, args.metrics_out, args.divergences_out, args.top_n)
