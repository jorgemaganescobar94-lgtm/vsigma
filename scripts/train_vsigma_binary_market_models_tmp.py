import json
from pathlib import Path
import numpy as np
import pandas as pd

DATASET = Path("data/modeling/vsigma_football_data_uk_top5.csv")
OUT = Path("data/modeling/models/vsigma_binary_market_tmp_metrics.json")

TARGETS = ["target_over25", "target_btts", "target_under35"]

def sigmoid(z):
    return 1 / (1 + np.exp(-np.clip(z, -30, 30)))

def log_loss(p, y):
    p = np.clip(p, 1e-12, 1 - 1e-12)
    return float(-np.mean(y*np.log(p) + (1-y)*np.log(1-p)))

def brier(p, y):
    return float(np.mean((p-y)**2))

def acc(p, y):
    return float(np.mean((p >= 0.5) == y))

def metrics(p, y):
    return {
        "accuracy": acc(p, y),
        "log_loss": log_loss(p, y),
        "brier": brier(p, y),
        "avg_prediction": float(np.mean(p)),
        "actual_rate": float(np.mean(y)),
    }

def standardize(train, valid, cols):
    med = train[cols].median(numeric_only=True).fillna(0.0)
    tr = train[cols].fillna(med).astype(float)
    va = valid[cols].fillna(med).astype(float)
    mean = tr.mean()
    std = tr.std().replace(0, 1.0).fillna(1.0)
    return ((tr-mean)/std).to_numpy(float), ((va-mean)/std).to_numpy(float)

def train_logistic(x, y, epochs=1500, lr=0.04, l2=0.001):
    xb = np.c_[np.ones((x.shape[0], 1)), x]
    w = np.zeros(xb.shape[1])
    for _ in range(epochs):
        p = sigmoid(xb @ w)
        grad = (xb.T @ (p-y)) / len(y)
        grad[1:] += l2 * w[1:]
        w -= lr * grad
    return w

def predict_logistic(w, x):
    xb = np.c_[np.ones((x.shape[0], 1)), x]
    return sigmoid(xb @ w)

df = pd.read_csv(DATASET).sort_values("fixture_date").copy()

split = int(len(df) * 0.8)
train = df.iloc[:split].copy()
valid = df.iloc[split:].copy()

all_feat = sorted([c for c in df.columns if c.startswith("feat_")])
stats_feat = [c for c in all_feat if not c.startswith("feat_market_") and c != "feat_odds_available"]
market_feat = all_feat[:]

results = {
    "rows_total": int(len(df)),
    "rows_train": int(len(train)),
    "rows_valid": int(len(valid)),
    "feature_count_stats_only": len(stats_feat),
    "feature_count_with_market": len(market_feat),
    "targets": {}
}

for target in TARGETS:
    y_train = pd.to_numeric(train[target], errors="coerce").fillna(0).to_numpy(float)
    y_valid = pd.to_numeric(valid[target], errors="coerce").fillna(0).to_numpy(float)

    base_p = np.full(len(y_valid), float(np.mean(y_train)))
    target_out = {
        "base_rate": metrics(base_p, y_valid)
    }

    xs_tr, xs_va = standardize(train, valid, stats_feat)
    ws = train_logistic(xs_tr, y_train)
    ps = predict_logistic(ws, xs_va)
    target_out["ml_stats_only"] = metrics(ps, y_valid)

    xm_tr, xm_va = standardize(train, valid, market_feat)
    wm = train_logistic(xm_tr, y_train)
    pm = predict_logistic(wm, xm_va)
    target_out["ml_with_market_features"] = metrics(pm, y_valid)

    if target == "target_over25":
        market_p = pd.to_numeric(valid["feat_market_over25_prob"], errors="coerce").fillna(0.0).to_numpy(float)
        mask = market_p > 0
        target_out["market_over25"] = metrics(market_p[mask], y_valid[mask])
        best_name = min(
            ["base_rate", "ml_stats_only", "ml_with_market_features", "market_over25"],
            key=lambda k: target_out[k]["log_loss"]
        )
    else:
        best_name = min(
            ["base_rate", "ml_stats_only", "ml_with_market_features"],
            key=lambda k: target_out[k]["log_loss"]
        )

    target_out["best_by_log_loss"] = best_name
    results["targets"][target] = target_out

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")

print("out", OUT)
for target, info in results["targets"].items():
    print(target, "best=", info["best_by_log_loss"])
    for name, m in info.items():
        if isinstance(m, dict) and "log_loss" in m:
            print(" ", name, m)
