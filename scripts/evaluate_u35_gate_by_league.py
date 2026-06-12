from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import numpy as np
import pandas as pd

DATASET = Path("data/modeling/vsigma_football_data_uk_top5.csv")
OUT_JSON = Path("data/modeling/models/vsigma_u35_gate_by_league_metrics.json")
OUT_CSV = Path("data/modeling/models/vsigma_u35_gate_by_league_thresholds.csv")
TARGET = "target_under35"


def sigmoid(z: np.ndarray) -> np.ndarray:
    return 1 / (1 + np.exp(-np.clip(z, -30, 30)))


def log_loss(p: np.ndarray, y: np.ndarray) -> float:
    p = np.clip(p, 1e-12, 1 - 1e-12)
    return float(-np.mean(y * np.log(p) + (1 - y) * np.log(1 - p)))


def brier(p: np.ndarray, y: np.ndarray) -> float:
    return float(np.mean((p - y) ** 2))


def accuracy(p: np.ndarray, y: np.ndarray) -> float:
    return float(np.mean((p >= 0.5) == y))


def metrics(p: np.ndarray, y: np.ndarray) -> dict[str, float]:
    return {
        "accuracy": accuracy(p, y),
        "log_loss": log_loss(p, y),
        "brier": brier(p, y),
        "avg_prediction": float(np.mean(p)),
        "actual_rate": float(np.mean(y)),
    }


def standardize(train: pd.DataFrame, valid: pd.DataFrame, cols: list[str]) -> tuple[np.ndarray, np.ndarray]:
    med = train[cols].median(numeric_only=True).fillna(0.0)
    tr = train[cols].fillna(med).astype(float)
    va = valid[cols].fillna(med).astype(float)
    mean = tr.mean()
    std = tr.std().replace(0, 1.0).fillna(1.0)
    return ((tr - mean) / std).to_numpy(float), ((va - mean) / std).to_numpy(float)


def train_logistic(x: np.ndarray, y: np.ndarray, epochs: int, lr: float, l2: float) -> np.ndarray:
    xb = np.c_[np.ones((x.shape[0], 1)), x]
    w = np.zeros(xb.shape[1])
    for _ in range(epochs):
        p = sigmoid(xb @ w)
        grad = (xb.T @ (p - y)) / len(y)
        grad[1:] += l2 * w[1:]
        w -= lr * grad
    return w


def predict(w: np.ndarray, x: np.ndarray) -> np.ndarray:
    xb = np.c_[np.ones((x.shape[0], 1)), x]
    return sigmoid(xb @ w)


def threshold_rows(valid: pd.DataFrame, p: np.ndarray, y: np.ndarray, league_name: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    market_u25 = pd.to_numeric(valid.get("feat_market_under25_prob", pd.Series([0.0] * len(valid))), errors="coerce").fillna(0.0).to_numpy(float)
    market_o25 = pd.to_numeric(valid.get("feat_market_over25_prob", pd.Series([0.0] * len(valid))), errors="coerce").fillna(0.0).to_numpy(float)
    for p_th in [0.70, 0.75, 0.80, 0.85, 0.90]:
        for mu_th in [0.50, 0.55, 0.60, 0.65]:
            mask = (p >= p_th) & (market_u25 >= mu_th)
            n = int(mask.sum())
            if n == 0:
                continue
            rows.append({
                "league_name": league_name,
                "model_under35_threshold": p_th,
                "market_under25_threshold": mu_th,
                "rows": n,
                "actual_under35_rate": float(np.mean(y[mask])),
                "avg_model_under35_prob": float(np.mean(p[mask])),
                "avg_market_under25_prob": float(np.mean(market_u25[mask])),
                "avg_market_over25_prob": float(np.mean(market_o25[mask])),
            })
    return rows


def promote_league(thresholds: list[dict[str, object]], valid_under35_rate: float) -> dict[str, object]:
    def find(p_th: float, mu_th: float) -> dict[str, object] | None:
        candidates = [r for r in thresholds if r["model_under35_threshold"] == p_th and r["market_under25_threshold"] == mu_th]
        return candidates[0] if candidates else None

    strong_clean = find(0.80, 0.60)
    strong = find(0.80, 0.55)
    elite = find(0.85, 0.55)

    if strong_clean and strong_clean["rows"] >= 50 and strong_clean["actual_under35_rate"] >= 0.84 and strong_clean["actual_under35_rate"] >= valid_under35_rate + 0.08:
        return {"league_gate_status": "PROMOTE_STRONG_CLEAN", "selected_threshold": strong_clean}
    if strong and strong["rows"] >= 50 and strong["actual_under35_rate"] >= 0.82 and strong["actual_under35_rate"] >= valid_under35_rate + 0.07:
        return {"league_gate_status": "PROMOTE_STRONG", "selected_threshold": strong}
    if elite and elite["rows"] >= 25 and elite["actual_under35_rate"] >= 0.88:
        return {"league_gate_status": "ELITE_ONLY_SMALL_SAMPLE", "selected_threshold": elite}
    return {"league_gate_status": "HOLD_GLOBAL_GATE", "selected_threshold": None}


def evaluate(dataset: Path, out_json: Path, out_csv: Path, min_rows: int, epochs: int, lr: float, l2: float) -> None:
    df = pd.read_csv(dataset)
    if "fixture_date" in df.columns:
        df = df.sort_values("fixture_date")
    if TARGET not in df.columns:
        raise RuntimeError(f"Missing target column: {TARGET}")
    feature_cols = sorted([c for c in df.columns if c.startswith("feat_")])
    if not feature_cols:
        raise RuntimeError("No feat_ columns found")

    all_thresholds: list[dict[str, object]] = []
    league_summaries: dict[str, object] = {}

    for league_name, league_df in df.groupby("league_name", sort=True):
        league_df = league_df.sort_values("fixture_date").copy()
        if len(league_df) < min_rows:
            continue
        split = int(len(league_df) * 0.8)
        train = league_df.iloc[:split].copy()
        valid = league_df.iloc[split:].copy()
        if len(valid) < 50:
            continue

        x_train, x_valid = standardize(train, valid, feature_cols)
        y_train = pd.to_numeric(train[TARGET], errors="coerce").fillna(0).to_numpy(float)
        y_valid = pd.to_numeric(valid[TARGET], errors="coerce").fillna(0).to_numpy(float)

        base_p = np.full(len(valid), float(np.mean(y_train)))
        weights = train_logistic(x_train, y_train, epochs=epochs, lr=lr, l2=l2)
        p = predict(weights, x_valid)

        league_thresholds = threshold_rows(valid, p, y_valid, str(league_name))
        all_thresholds.extend(league_thresholds)
        model_m = metrics(p, y_valid)
        base_m = metrics(base_p, y_valid)
        promotion = promote_league(league_thresholds, float(np.mean(y_valid)))
        league_summaries[str(league_name)] = {
            "rows_total": int(len(league_df)),
            "rows_train": int(len(train)),
            "rows_valid": int(len(valid)),
            "valid_under35_rate": float(np.mean(y_valid)),
            "base_rate_metrics": base_m,
            "model_metrics": model_m,
            "improvement_base_minus_model": {
                "log_loss": base_m["log_loss"] - model_m["log_loss"],
                "brier": base_m["brier"] - model_m["brier"],
                "accuracy": model_m["accuracy"] - base_m["accuracy"],
            },
            **promotion,
        }

    out = {
        "dataset": str(dataset),
        "target": TARGET,
        "min_rows_per_league": min_rows,
        "feature_count": len(feature_cols),
        "league_summaries": league_summaries,
        "priority_read": {
            "primary_goal": "precision_max_first",
            "preferred_markets": ["1X2", "team_totals", "protected_builders"],
            "builder_governance": "singles_plus_prudent_combos_with_strong_veto",
            "next_promotions_require": "out_of_sample_league_threshold_stability",
        },
    }

    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with out_csv.open("w", encoding="utf-8", newline="") as handle:
        fields = [
            "league_name", "model_under35_threshold", "market_under25_threshold", "rows",
            "actual_under35_rate", "avg_model_under35_prob", "avg_market_under25_prob", "avg_market_over25_prob",
        ]
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in all_thresholds:
            writer.writerow({k: row.get(k, "") for k in fields})

    print(f"U35 by-league evaluation complete leagues={len(league_summaries)}")
    print(f"json={out_json}")
    print(f"csv={out_csv}")
    for league, summary in league_summaries.items():
        print(league, summary["league_gate_status"], summary.get("selected_threshold"))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", type=Path, default=DATASET)
    ap.add_argument("--out-json", type=Path, default=OUT_JSON)
    ap.add_argument("--out-csv", type=Path, default=OUT_CSV)
    ap.add_argument("--min-rows", type=int, default=1000)
    ap.add_argument("--epochs", type=int, default=1500)
    ap.add_argument("--lr", type=float, default=0.04)
    ap.add_argument("--l2", type=float, default=0.001)
    args = ap.parse_args()
    evaluate(args.dataset, args.out_json, args.out_csv, args.min_rows, args.epochs, args.lr, args.l2)
