from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

MODEL_DIR = Path("data/modeling/models")
CLASS_ORDER = ["HOME", "DRAW", "AWAY"]
REGRESSION_TARGETS = [
    "target_home_goals", "target_away_goals", "target_total_goals",
    "target_home_shots", "target_away_shots", "target_home_sot", "target_away_sot",
    "target_home_corners", "target_away_corners", "target_home_possession", "target_away_possession",
]


def softmax(logits: np.ndarray) -> np.ndarray:
    z = logits - np.max(logits, axis=1, keepdims=True)
    exp = np.exp(z)
    return exp / np.sum(exp, axis=1, keepdims=True)


def log_loss(probs: np.ndarray, y: np.ndarray) -> float:
    p = np.clip(probs[np.arange(len(y)), y], 1e-12, 1.0)
    return float(-np.mean(np.log(p)))


def brier(probs: np.ndarray, y: np.ndarray, n_classes: int) -> float:
    yy = np.eye(n_classes)[y]
    return float(np.mean(np.sum((probs - yy) ** 2, axis=1)))


def standardize(train: pd.DataFrame, valid: pd.DataFrame, feature_cols: list[str]) -> tuple[np.ndarray, np.ndarray, dict]:
    med = train[feature_cols].median(numeric_only=True).fillna(0.0)
    train_filled = train[feature_cols].fillna(med).astype(float)
    valid_filled = valid[feature_cols].fillna(med).astype(float)
    mean = train_filled.mean()
    std = train_filled.std().replace(0, 1.0).fillna(1.0)
    x_train = ((train_filled - mean) / std).to_numpy(dtype=float)
    x_valid = ((valid_filled - mean) / std).to_numpy(dtype=float)
    scaler = {"median": med.to_dict(), "mean": mean.to_dict(), "std": std.to_dict()}
    return x_train, x_valid, scaler


def add_bias(x: np.ndarray) -> np.ndarray:
    return np.c_[np.ones((x.shape[0], 1)), x]


def train_softmax_regression(x: np.ndarray, y: np.ndarray, epochs: int, lr: float, l2: float) -> np.ndarray:
    xb = add_bias(x)
    n, d = xb.shape
    k = len(CLASS_ORDER)
    y_one = np.eye(k)[y]
    w = np.zeros((d, k), dtype=float)
    for _ in range(epochs):
        probs = softmax(xb @ w)
        grad = (xb.T @ (probs - y_one)) / n
        grad[1:] += l2 * w[1:]
        w -= lr * grad
    return w


def best_temperature(logits: np.ndarray, y: np.ndarray) -> tuple[float, float]:
    candidates = [0.55, 0.7, 0.85, 1.0, 1.15, 1.35, 1.6, 2.0, 2.5, 3.0]
    best_t, best_loss = 1.0, 999.0
    for t in candidates:
        loss = log_loss(softmax(logits / t), y)
        if loss < best_loss:
            best_t, best_loss = t, loss
    return best_t, best_loss


def train_ridge(x: np.ndarray, y: np.ndarray, alpha: float) -> dict:
    xb = add_bias(x)
    ident = np.eye(xb.shape[1])
    ident[0, 0] = 0.0
    beta = np.linalg.pinv(xb.T @ xb + alpha * ident) @ xb.T @ y
    return {"coef": beta.tolist()}


def predict_ridge(model: dict, x: np.ndarray) -> np.ndarray:
    beta = np.array(model["coef"], dtype=float)
    return add_bias(x) @ beta


def baseline_market_metrics(df: pd.DataFrame, y: np.ndarray) -> dict:
    needed = ["feat_market_home_prob", "feat_market_draw_prob", "feat_market_away_prob"]
    if not all(c in df.columns for c in needed):
        return {"available": False}
    probs = df[needed].fillna(0.0).astype(float).to_numpy()
    totals = probs.sum(axis=1, keepdims=True)
    probs = np.divide(probs, totals, out=np.full_like(probs, 1 / 3), where=totals > 0)
    return {"available": True, "log_loss": log_loss(probs, y), "brier": brier(probs, y, 3), "accuracy": float(np.mean(np.argmax(probs, axis=1) == y))}


def train(dataset: Path, model_out: Path, metrics_out: Path, min_rows: int, epochs: int, lr: float, l2: float, ridge_alpha: float) -> None:
    df = pd.read_csv(dataset)
    if "fixture_date" in df.columns:
        df = df.sort_values("fixture_date")
    feature_cols = sorted([c for c in df.columns if c.startswith("feat_")])
    if not feature_cols:
        raise RuntimeError("No feature columns found. Expected columns starting with feat_")
    df = df[df["target_result_class"].isin(CLASS_ORDER)].copy()
    df["class_idx"] = df["target_result_class"].map({c: i for i, c in enumerate(CLASS_ORDER)})
    n = len(df)
    if n < 50:
        raise RuntimeError(f"Not enough rows to train even shadow model: {n}")
    split = max(1, int(n * 0.8))
    train_df = df.iloc[:split].copy()
    valid_df = df.iloc[split:].copy()
    if valid_df.empty:
        valid_df = train_df.copy()
    x_train, x_valid, scaler = standardize(train_df, valid_df, feature_cols)
    y_train = train_df["class_idx"].to_numpy(dtype=int)
    y_valid = valid_df["class_idx"].to_numpy(dtype=int)

    w = train_softmax_regression(x_train, y_train, epochs=epochs, lr=lr, l2=l2)
    logits_valid = add_bias(x_valid) @ w
    temp, calibrated_loss = best_temperature(logits_valid, y_valid)
    probs_valid = softmax(logits_valid / temp)
    metrics = {
        "rows_total": int(n),
        "rows_train": int(len(train_df)),
        "rows_valid": int(len(valid_df)),
        "feature_count": len(feature_cols),
        "result_model": {
            "accuracy": float(np.mean(np.argmax(probs_valid, axis=1) == y_valid)),
            "log_loss": calibrated_loss,
            "brier": brier(probs_valid, y_valid, 3),
            "temperature": temp,
        },
        "market_baseline": baseline_market_metrics(valid_df, y_valid),
        "regression_targets": {},
    }

    regressors = {}
    for target in REGRESSION_TARGETS:
        if target not in df.columns:
            continue
        target_train = pd.to_numeric(train_df[target], errors="coerce")
        target_valid = pd.to_numeric(valid_df[target], errors="coerce")
        if "goals" not in target:
            mask_train = target_train > 0
            mask_valid = target_valid > 0
        else:
            mask_train = target_train.notna()
            mask_valid = target_valid.notna()
        if int(mask_train.sum()) < 50 or int(mask_valid.sum()) < 10:
            continue
        reg = train_ridge(x_train[mask_train.to_numpy()], target_train[mask_train].to_numpy(dtype=float), ridge_alpha)
        preds = predict_ridge(reg, x_valid[mask_valid.to_numpy()])
        actual = target_valid[mask_valid].to_numpy(dtype=float)
        mae = float(np.mean(np.abs(preds - actual)))
        regressors[target] = reg
        metrics["regression_targets"][target] = {"mae": mae, "valid_rows": int(mask_valid.sum())}

    market = metrics["market_baseline"]
    if n < min_rows:
        promotion = "SHADOW_ONLY_INSUFFICIENT_ROWS"
    elif market.get("available") and calibrated_loss < float(market.get("log_loss", 999)) - 0.01 and metrics["result_model"]["brier"] <= float(market.get("brier", 999)):
        promotion = "CANDIDATE_BEATS_MARKET_BASELINE"
    else:
        promotion = "SHADOW_ONLY_NEEDS_MORE_EDGE"
    metrics["promotion_status"] = promotion

    model = {
        "model_type": "vsigma_hybrid_statistical_v1",
        "class_order": CLASS_ORDER,
        "feature_cols": feature_cols,
        "scaler": scaler,
        "result_model": {"weights": w.tolist(), "temperature": temp},
        "regressors": regressors,
        "metrics": metrics,
    }
    model_out.parent.mkdir(parents=True, exist_ok=True)
    model_out.write_text(json.dumps(model, indent=2, ensure_ascii=False), encoding="utf-8")
    metrics_out.parent.mkdir(parents=True, exist_ok=True)
    metrics_out.write_text(json.dumps(metrics, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Trained vSIGMA statistical model rows={n} promotion={promotion}")
    print(f"model={model_out}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=Path, default=Path("data/modeling/vsigma_historical_dataset.csv"))
    parser.add_argument("--model-out", type=Path, default=MODEL_DIR / "vsigma_stat_model.json")
    parser.add_argument("--metrics-out", type=Path, default=MODEL_DIR / "vsigma_stat_model_metrics.json")
    parser.add_argument("--min-rows", type=int, default=1000)
    parser.add_argument("--epochs", type=int, default=1500)
    parser.add_argument("--lr", type=float, default=0.05)
    parser.add_argument("--l2", type=float, default=0.001)
    parser.add_argument("--ridge-alpha", type=float, default=5.0)
    args = parser.parse_args()
    train(args.dataset, args.model_out, args.metrics_out, args.min_rows, args.epochs, args.lr, args.l2, args.ridge_alpha)
