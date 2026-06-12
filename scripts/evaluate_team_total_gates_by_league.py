from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import numpy as np
import pandas as pd

DATASET = Path("data/modeling/vsigma_football_data_uk_top5.csv")
OUT_JSON = Path("data/modeling/models/vsigma_team_total_gates_by_league_metrics.json")
OUT_CSV = Path("data/modeling/models/vsigma_team_total_gates_by_league_thresholds.csv")

TARGETS = {
    "home_over05": {"goal_col": "target_home_goals", "op": ">=", "line": 1, "market": "HOME_TT_OVER_0_5"},
    "away_over05": {"goal_col": "target_away_goals", "op": ">=", "line": 1, "market": "AWAY_TT_OVER_0_5"},
    "home_over15": {"goal_col": "target_home_goals", "op": ">=", "line": 2, "market": "HOME_TT_OVER_1_5"},
    "away_over15": {"goal_col": "target_away_goals", "op": ">=", "line": 2, "market": "AWAY_TT_OVER_1_5"},
    "home_under15": {"goal_col": "target_home_goals", "op": "<=", "line": 1, "market": "HOME_TT_UNDER_1_5"},
    "away_under15": {"goal_col": "target_away_goals", "op": "<=", "line": 1, "market": "AWAY_TT_UNDER_1_5"},
    "home_under05": {"goal_col": "target_home_goals", "op": "<=", "line": 0, "market": "HOME_TT_UNDER_0_5"},
    "away_under05": {"goal_col": "target_away_goals", "op": "<=", "line": 0, "market": "AWAY_TT_UNDER_0_5"},
}


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


def make_target(df: pd.DataFrame, target_name: str) -> np.ndarray:
    cfg = TARGETS[target_name]
    goals = pd.to_numeric(df[cfg["goal_col"]], errors="coerce").fillna(0).to_numpy(float)
    if cfg["op"] == ">=":
        return (goals >= float(cfg["line"])).astype(float)
    return (goals <= float(cfg["line"])).astype(float)


def threshold_rows(league: str, target_name: str, p: np.ndarray, y: np.ndarray) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for threshold in [0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90]:
        mask = p >= threshold
        n = int(mask.sum())
        if n == 0:
            continue
        rows.append({
            "league_name": league,
            "target": target_name,
            "market_family": TARGETS[target_name]["market"],
            "model_threshold": threshold,
            "rows": n,
            "actual_hit_rate": float(np.mean(y[mask])),
            "avg_model_prob": float(np.mean(p[mask])),
            "gap_actual_minus_model": float(np.mean(y[mask]) - np.mean(p[mask])),
        })
    return rows


def select_candidate(thresholds: list[dict[str, object]], base_rate: float, min_rows: int) -> dict[str, object]:
    candidates = []
    for row in thresholds:
        n = int(row["rows"])
        hit = float(row["actual_hit_rate"])
        threshold = float(row["model_threshold"])
        uplift = hit - base_rate
        if n >= min_rows and hit >= max(0.72, threshold - 0.02) and uplift >= 0.07:
            candidates.append({**row, "uplift_vs_base": uplift})
    if not candidates:
        return {"gate_status": "HOLD_NO_PROMOTION", "selected_threshold": None}
    candidates.sort(key=lambda r: (float(r["actual_hit_rate"]), int(r["rows"]), float(r["model_threshold"])), reverse=True)
    selected = candidates[0]
    if float(selected["actual_hit_rate"]) >= 0.85 and int(selected["rows"]) >= min_rows:
        status = "PROMOTE_STRONG_CANDIDATE"
    else:
        status = "PROMOTE_SUPPORT_CANDIDATE"
    return {"gate_status": status, "selected_threshold": selected}


def evaluate(dataset: Path, out_json: Path, out_csv: Path, min_rows_per_league: int, min_threshold_rows: int, epochs: int, lr: float, l2: float) -> None:
    df = pd.read_csv(dataset)
    if "fixture_date" in df.columns:
        df = df.sort_values("fixture_date")
    feature_cols = sorted([c for c in df.columns if c.startswith("feat_")])
    if not feature_cols:
        raise RuntimeError("No feat_ columns found")

    all_thresholds: list[dict[str, object]] = []
    league_results: dict[str, object] = {}

    for league, league_df in df.groupby("league_name", sort=True):
        league_df = league_df.sort_values("fixture_date").copy()
        if len(league_df) < min_rows_per_league:
            continue
        split = int(len(league_df) * 0.8)
        train = league_df.iloc[:split].copy()
        valid = league_df.iloc[split:].copy()
        if len(valid) < 50:
            continue

        x_train, x_valid = standardize(train, valid, feature_cols)
        league_results[str(league)] = {
            "rows_total": int(len(league_df)),
            "rows_train": int(len(train)),
            "rows_valid": int(len(valid)),
            "targets": {},
        }

        for target_name in TARGETS:
            y_train = make_target(train, target_name)
            y_valid = make_target(valid, target_name)
            if float(np.mean(y_train)) in {0.0, 1.0}:
                continue
            base_p = np.full(len(valid), float(np.mean(y_train)))
            weights = train_logistic(x_train, y_train, epochs=epochs, lr=lr, l2=l2)
            p = predict(weights, x_valid)
            base_m = metrics(base_p, y_valid)
            model_m = metrics(p, y_valid)
            target_thresholds = threshold_rows(str(league), target_name, p, y_valid)
            all_thresholds.extend(target_thresholds)
            promotion = select_candidate(target_thresholds, float(np.mean(y_valid)), min_threshold_rows)
            league_results[str(league)]["targets"][target_name] = {
                "market_family": TARGETS[target_name]["market"],
                "valid_actual_rate": float(np.mean(y_valid)),
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
        "feature_count": len(feature_cols),
        "min_rows_per_league": min_rows_per_league,
        "min_threshold_rows": min_threshold_rows,
        "targets_evaluated": TARGETS,
        "league_results": league_results,
        "priority_read": {
            "primary_goal": "precision_max_first",
            "preferred_markets": ["1X2", "team_totals", "protected_builders"],
            "status": "research_evaluator_only_not_production_gate",
        },
    }
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    fields = ["league_name", "target", "market_family", "model_threshold", "rows", "actual_hit_rate", "avg_model_prob", "gap_actual_minus_model"]
    with out_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in all_thresholds:
            writer.writerow({k: row.get(k, "") for k in fields})

    print(f"Team total gate evaluation complete leagues={len(league_results)}")
    print(f"json={out_json}")
    print(f"csv={out_csv}")
    for league, result in league_results.items():
        promoted = []
        for target, target_result in result["targets"].items():
            if str(target_result.get("gate_status", "")).startswith("PROMOTE"):
                promoted.append(f"{target}:{target_result['gate_status']}")
        print(league, promoted or "no_promotions")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", type=Path, default=DATASET)
    ap.add_argument("--out-json", type=Path, default=OUT_JSON)
    ap.add_argument("--out-csv", type=Path, default=OUT_CSV)
    ap.add_argument("--min-rows-per-league", type=int, default=1000)
    ap.add_argument("--min-threshold-rows", type=int, default=40)
    ap.add_argument("--epochs", type=int, default=1500)
    ap.add_argument("--lr", type=float, default=0.04)
    ap.add_argument("--l2", type=float, default=0.001)
    args = ap.parse_args()
    evaluate(args.dataset, args.out_json, args.out_csv, args.min_rows_per_league, args.min_threshold_rows, args.epochs, args.lr, args.l2)
