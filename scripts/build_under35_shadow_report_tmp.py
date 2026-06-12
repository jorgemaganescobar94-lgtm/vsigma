import json
from pathlib import Path
import numpy as np
import pandas as pd

DATASET = Path("data/modeling/vsigma_football_data_uk_top5.csv")
OUT_CSV = Path("data/modeling/models/vsigma_under35_shadow_candidates.csv")
OUT_JSON = Path("data/modeling/models/vsigma_under35_shadow_candidates_summary.json")

def sigmoid(z):
    return 1 / (1 + np.exp(-np.clip(z, -30, 30)))

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

def predict(w, x):
    xb = np.c_[np.ones((x.shape[0], 1)), x]
    return sigmoid(xb @ w)

df = pd.read_csv(DATASET).sort_values("fixture_date").copy()

split = int(len(df) * 0.8)
train = df.iloc[:split].copy()
valid = df.iloc[split:].copy()

feat = sorted([c for c in df.columns if c.startswith("feat_")])

x_train, x_valid = standardize(train, valid, feat)
y_train = pd.to_numeric(train["target_under35"], errors="coerce").fillna(0).to_numpy(float)
y_valid = pd.to_numeric(valid["target_under35"], errors="coerce").fillna(0).to_numpy(float)

w = train_logistic(x_train, y_train)
p = predict(w, x_valid)

report = valid[[
    "fixture_date","league_name","home_team","away_team",
    "target_home_goals","target_away_goals","target_total_goals",
    "target_under35","target_over25","target_btts",
    "feat_market_home_prob","feat_market_draw_prob","feat_market_away_prob",
    "feat_market_over25_prob","feat_market_under25_prob"
]].copy()

report["model_under35_prob"] = p
report["model_under35_pick"] = (p >= 0.5).astype(int)
report["model_under35_hit"] = ((p >= 0.5).astype(int) == y_valid).astype(int)
report["actual_under35"] = y_valid.astype(int)

report = report.sort_values("model_under35_prob", ascending=False)

buckets = []
for lo, hi in [(0,.55),(.55,.60),(.60,.65),(.65,.70),(.70,.75),(.75,.80),(.80,.85),(.85,1.01)]:
    m = (p >= lo) & (p < hi)
    if int(m.sum()) == 0:
        continue
    buckets.append({
        "range": f"[{lo:.2f},{hi:.2f})",
        "rows": int(m.sum()),
        "actual_under35_rate": float(np.mean(y_valid[m])),
        "avg_model_under35_prob": float(np.mean(p[m])),
        "gap_actual_minus_model": float(np.mean(y_valid[m]) - np.mean(p[m])),
    })

thresholds = []
for th in [0.60,0.65,0.70,0.75,0.80,0.85]:
    m = p >= th
    if int(m.sum()) == 0:
        continue
    thresholds.append({
        "threshold": th,
        "rows": int(m.sum()),
        "actual_under35_rate": float(np.mean(y_valid[m])),
        "avg_model_under35_prob": float(np.mean(p[m])),
        "gap_actual_minus_model": float(np.mean(y_valid[m]) - np.mean(p[m])),
    })

summary = {
    "rows_train": int(len(train)),
    "rows_valid": int(len(valid)),
    "overall_valid_under35_rate": float(np.mean(y_valid)),
    "overall_avg_model_under35_prob": float(np.mean(p)),
    "buckets": buckets,
    "thresholds": thresholds,
    "governance_verdict": "UNDER35_BINARY_SHADOW_CANDIDATE",
    "use_case": [
        "Validate Under 3.5 only as a robustness gate",
        "Do not auto-bet from model alone",
        "Use to support vSIGMA when tactical read and market family agree",
        "Use to veto overstretched Over/BTTS/builder legs when model_under35_prob is high"
    ]
}

OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
report.to_csv(OUT_CSV, index=False, encoding="utf-8")
OUT_JSON.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")

print("csv", OUT_CSV)
print("summary", OUT_JSON)
print(json.dumps(summary, indent=2, ensure_ascii=False))
