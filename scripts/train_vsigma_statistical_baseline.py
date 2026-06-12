from __future__ import annotations

import argparse
import csv
import glob
import json
import math
from pathlib import Path
from statistics import mean

BASE = Path("data/modeling")
FEATURES = [
    "home_recent_matches","away_recent_matches",
    "home_gf_avg","home_ga_avg","away_gf_avg","away_ga_avg",
    "home_shots_for_avg","home_shots_against_avg","away_shots_for_avg","away_shots_against_avg",
    "home_sot_for_avg","home_sot_against_avg","away_sot_for_avg","away_sot_against_avg",
    "home_corners_for_avg","home_corners_against_avg","away_corners_for_avg","away_corners_against_avg",
    "home_possession_avg","away_possession_avg","home_yellows_avg","away_yellows_avg",
]
REGRESSION_TARGETS = [
    "home_goals","away_goals","home_actual_shots","away_actual_shots","home_actual_sot","away_actual_sot",
    "home_actual_corners","away_actual_corners","home_actual_possession","away_actual_possession","home_actual_yellows","away_actual_yellows",
]
CLASSES = ["H", "D", "A"]


def fnum(v, default=0.0) -> float:
    try:
        return float(str(v).strip())
    except Exception:
        return default


def read_rows(patterns: list[str]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for pattern in patterns:
        for path in sorted(glob.glob(pattern)):
            with open(path, "r", encoding="utf-8-sig", newline="") as handle:
                rows.extend(dict(row) for row in csv.DictReader(handle))
    rows = [r for r in rows if r.get("result_class") in CLASSES]
    rows.sort(key=lambda r: r.get("date", ""))
    return rows


def matrix(rows: list[dict[str, str]], feature_means=None, feature_stds=None):
    raw = [[fnum(r.get(f)) for f in FEATURES] for r in rows]
    if feature_means is None:
        feature_means = [mean([x[i] for x in raw]) if raw else 0.0 for i in range(len(FEATURES))]
    if feature_stds is None:
        feature_stds = []
        for i in range(len(FEATURES)):
            vals = [x[i] for x in raw]
            mu = feature_means[i]
            var = sum((v - mu) ** 2 for v in vals) / max(1, len(vals))
            feature_stds.append(math.sqrt(var) or 1.0)
    x = [[1.0] + [(row[i] - feature_means[i]) / feature_stds[i] for i in range(len(FEATURES))] for row in raw]
    return x, feature_means, feature_stds


def dot(a,b): return sum(x*y for x,y in zip(a,b))

def train_linear(x, y, epochs=1400, lr=0.025, l2=0.001):
    if not x: return []
    w = [0.0 for _ in x[0]]
    for _ in range(epochs):
        grad = [0.0 for _ in w]
        for xi, yi in zip(x, y):
            pred = dot(w, xi)
            err = pred - yi
            for j, val in enumerate(xi):
                grad[j] += err * val
        n = max(1, len(x))
        for j in range(len(w)):
            penalty = l2 * w[j] if j > 0 else 0.0
            w[j] -= lr * ((grad[j] / n) + penalty)
    return [round(v, 8) for v in w]


def softmax(logits):
    m = max(logits)
    ex = [math.exp(v-m) for v in logits]
    total = sum(ex) or 1.0
    return [v/total for v in ex]


def train_softmax(x, labels, epochs=1800, lr=0.035, l2=0.001):
    if not x: return []
    k = len(CLASSES)
    w = [[0.0 for _ in x[0]] for _ in range(k)]
    label_idx = [CLASSES.index(y) for y in labels]
    for _ in range(epochs):
        grad = [[0.0 for _ in x[0]] for _ in range(k)]
        for xi, yi in zip(x, label_idx):
            probs = softmax([dot(w[c], xi) for c in range(k)])
            for c in range(k):
                diff = probs[c] - (1.0 if c == yi else 0.0)
                for j, val in enumerate(xi):
                    grad[c][j] += diff * val
        n = max(1, len(x))
        for c in range(k):
            for j in range(len(w[c])):
                penalty = l2*w[c][j] if j > 0 else 0.0
                w[c][j] -= lr*((grad[c][j]/n)+penalty)
    return [[round(v,8) for v in row] for row in w]


def predict_linear(w, x): return [dot(w, xi) for xi in x]

def predict_softmax(w, x): return [softmax([dot(w[c], xi) for c in range(len(CLASSES))]) for xi in x]

def mae(y, pred):
    if not y: return 0.0
    return round(sum(abs(a-b) for a,b in zip(y,pred))/len(y), 4)

def accuracy(labels, probs):
    if not labels: return 0.0
    hits = 0
    for label, pr in zip(labels, probs):
        pred = CLASSES[max(range(len(CLASSES)), key=lambda i: pr[i])]
        hits += int(pred == label)
    return round(hits / len(labels), 4)

def brier(labels, probs):
    if not labels: return 0.0
    total = 0.0
    for label, pr in zip(labels, probs):
        y = [1.0 if c == label else 0.0 for c in CLASSES]
        total += sum((p-t)**2 for p,t in zip(pr,y)) / len(CLASSES)
    return round(total/len(labels), 5)

def train(rows: list[dict[str,str]], holdout_pct: float):
    split = max(1, int(len(rows) * (1.0 - holdout_pct)))
    train_rows = rows[:split]
    test_rows = rows[split:] if split < len(rows) else rows[:]
    x_train, means, stds = matrix(train_rows)
    x_test, _, _ = matrix(test_rows, means, stds)
    result_w = train_softmax(x_train, [r["result_class"] for r in train_rows])
    result_probs = predict_softmax(result_w, x_test)
    regressions = {}
    regression_metrics = {}
    for target in REGRESSION_TARGETS:
        y_train = [fnum(r.get(target)) for r in train_rows]
        y_test = [fnum(r.get(target)) for r in test_rows]
        w = train_linear(x_train, y_train)
        pred = predict_linear(w, x_test)
        regressions[target] = w
        regression_metrics[target + "_mae"] = mae(y_test, pred)
    metrics = {
        "rows_total": len(rows),
        "rows_train": len(train_rows),
        "rows_test": len(test_rows),
        "result_accuracy": accuracy([r["result_class"] for r in test_rows], result_probs),
        "result_brier": brier([r["result_class"] for r in test_rows], result_probs),
        **regression_metrics,
    }
    model = {
        "model_type": "vSIGMA_STAT_BASELINE_STD_LIB_V1",
        "features": FEATURES,
        "classes": CLASSES,
        "feature_means": means,
        "feature_stds": stds,
        "result_softmax_weights": result_w,
        "regression_weights": regressions,
        "metrics": metrics,
        "promotion_status": "SHADOW_ONLY",
        "note": "Interpretable statistical baseline. Do not replace vSIGMA rules until shadow metrics beat current system.",
    }
    return model


def write_outputs(model: dict, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "vsigma_statistical_baseline_model.json").write_text(json.dumps(model, indent=2, ensure_ascii=False), encoding="utf-8")
    metrics = model["metrics"]
    with (out_dir / "vsigma_statistical_baseline_metrics.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(metrics.keys()))
        writer.writeheader(); writer.writerow(metrics)
    lines = ["# vSIGMA Statistical Baseline Metrics", "", f"- model_type: {model['model_type']}", f"- promotion_status: {model['promotion_status']}", "", "## Metrics"]
    for k,v in metrics.items():
        lines.append(f"- {k}: {v}")
    lines += ["", "## Features", *[f"- {f}" for f in model["features"]], "", "## Note", f"- {model['note']}"]
    (out_dir / "vsigma_statistical_baseline_metrics.md").write_text("\n".join(lines)+"\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-glob", action="append", default=[])
    parser.add_argument("--holdout-pct", type=float, default=0.20)
    parser.add_argument("--out-dir", type=Path, default=BASE)
    args = parser.parse_args()
    patterns = args.input_glob or [str(BASE / "api_historical_features_*.csv")]
    rows = read_rows(patterns)
    if len(rows) < 30:
        raise SystemExit(f"Need at least 30 rows to train; got {len(rows)}")
    model = train(rows, args.holdout_pct)
    write_outputs(model, args.out_dir)
    print(json.dumps(model["metrics"], indent=2))

if __name__ == "__main__":
    main()
