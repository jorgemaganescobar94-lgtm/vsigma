from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import numpy as np
import pandas as pd

DATASET = Path("data/modeling/vsigma_football_data_uk_top5.csv")
U35_CONFIG = Path("config/vsigma_u35_league_gate_overrides_v1.json")
TT_CONFIG = Path("config/vsigma_team_total_gate_overrides_v1.json")
OUT_JSON = Path("data/modeling/models/vsigma_gate_stability_splits_metrics.json")
OUT_CSV = Path("data/modeling/models/vsigma_gate_stability_splits_details.csv")

LEAGUE_CODE_TO_NAME = {
    "E0": "Premier League",
    "SP1": "La Liga",
    "I1": "Serie A",
    "D1": "Bundesliga",
    "F1": "Ligue 1",
}

TT_TARGETS = {
    "HOME_TT_OVER_0_5": {"goal_col": "target_home_goals", "op": ">=", "line": 1},
    "AWAY_TT_OVER_0_5": {"goal_col": "target_away_goals", "op": ">=", "line": 1},
    "HOME_TT_OVER_1_5": {"goal_col": "target_home_goals", "op": ">=", "line": 2},
    "AWAY_TT_OVER_1_5": {"goal_col": "target_away_goals", "op": ">=", "line": 2},
    "HOME_TT_UNDER_1_5": {"goal_col": "target_home_goals", "op": "<=", "line": 1},
    "AWAY_TT_UNDER_1_5": {"goal_col": "target_away_goals", "op": "<=", "line": 1},
    "HOME_TT_UNDER_0_5": {"goal_col": "target_home_goals", "op": "<=", "line": 0},
    "AWAY_TT_UNDER_0_5": {"goal_col": "target_away_goals", "op": "<=", "line": 0},
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


def read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8-sig"))


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


def make_tt_target(df: pd.DataFrame, market_family: str) -> np.ndarray:
    cfg = TT_TARGETS[market_family]
    goals = pd.to_numeric(df[cfg["goal_col"]], errors="coerce").fillna(0).to_numpy(float)
    if cfg["op"] == ">=":
        return (goals >= float(cfg["line"])).astype(float)
    return (goals <= float(cfg["line"])).astype(float)


def target_vector(df: pd.DataFrame, gate_type: str, market_family: str) -> np.ndarray:
    if gate_type == "U35":
        return pd.to_numeric(df["target_under35"], errors="coerce").fillna(0).to_numpy(float)
    return make_tt_target(df, market_family)


def gate_plan(u35_cfg: dict, tt_cfg: dict) -> list[dict[str, object]]:
    plan: list[dict[str, object]] = []
    for league_code, league_cfg in (u35_cfg.get("league_overrides") or {}).items():
        status = str(league_cfg.get("status", ""))
        if status in {"PROMOTE_STRONG_CLEAN", "PROMOTE_STRONG"}:
            plan.append({
                "gate_id": f"U35_{league_code}",
                "gate_type": "U35",
                "league_code": league_code,
                "league_name": league_cfg.get("league_name") or LEAGUE_CODE_TO_NAME.get(league_code, league_code),
                "market_family": "UNDER_3_5",
                "status": status,
                "model_prob_min": float(league_cfg.get("model_under35_prob_min", 999.0)),
                "market_under25_prob_min": float(league_cfg.get("market_under25_prob_min", 0.0)),
                "required_hit_rate": 0.86 if status == "PROMOTE_STRONG_CLEAN" else 0.82,
                "required_uplift": 0.07,
            })

    for league_code, league_cfg in (tt_cfg.get("league_overrides") or {}).items():
        if str(league_cfg.get("status", "")) in {"RESEARCH_ONLY", "BLOCKED"}:
            continue
        for market_family, market_cfg in (league_cfg.get("markets") or {}).items():
            status = str(market_cfg.get("status", ""))
            if status not in {"PROMOTE_STRONG", "PROMOTE_SUPPORT"}:
                continue
            plan.append({
                "gate_id": f"TT_{league_code}_{market_family}",
                "gate_type": "TEAM_TOTAL",
                "league_code": league_code,
                "league_name": league_cfg.get("league_name") or LEAGUE_CODE_TO_NAME.get(league_code, league_code),
                "market_family": market_family,
                "status": status,
                "model_prob_min": float(market_cfg.get("model_prob_min", 999.0)),
                "market_under25_prob_min": 0.0,
                "required_hit_rate": 0.82 if status == "PROMOTE_STRONG" else 0.78,
                "required_uplift": 0.05 if status == "PROMOTE_STRONG" else 0.04,
            })
    return plan


def split_eval(
    league_df: pd.DataFrame,
    feature_cols: list[str],
    gate: dict[str, object],
    split: float,
    epochs: int,
    lr: float,
    l2: float,
) -> dict[str, object]:
    split_idx = int(len(league_df) * split)
    train = league_df.iloc[:split_idx].copy()
    valid = league_df.iloc[split_idx:].copy()
    if len(train) < 100 or len(valid) < 25:
        return {"split": split, "status": "INSUFFICIENT_SPLIT_ROWS", "rows_train": len(train), "rows_valid": len(valid)}

    x_train, x_valid = standardize(train, valid, feature_cols)
    y_train = target_vector(train, str(gate["gate_type"]), str(gate["market_family"]))
    y_valid = target_vector(valid, str(gate["gate_type"]), str(gate["market_family"]))
    if float(np.mean(y_train)) in {0.0, 1.0}:
        return {"split": split, "status": "DEGENERATE_TARGET", "rows_train": len(train), "rows_valid": len(valid)}

    w = train_logistic(x_train, y_train, epochs=epochs, lr=lr, l2=l2)
    p = predict(w, x_valid)
    base_p = np.full(len(valid), float(np.mean(y_train)))
    mask = p >= float(gate["model_prob_min"])
    if str(gate["gate_type"]) == "U35" and float(gate.get("market_under25_prob_min", 0.0)) > 0:
        market_u25 = pd.to_numeric(valid.get("feat_market_under25_prob", pd.Series([0.0] * len(valid))), errors="coerce").fillna(0.0).to_numpy(float)
        mask = mask & (market_u25 >= float(gate["market_under25_prob_min"]))

    n = int(mask.sum())
    base_rate = float(np.mean(y_valid))
    actual_hit = float(np.mean(y_valid[mask])) if n else 0.0
    avg_prob = float(np.mean(p[mask])) if n else 0.0
    uplift = actual_hit - base_rate if n else 0.0
    return {
        "split": split,
        "status": "OK",
        "rows_train": int(len(train)),
        "rows_valid": int(len(valid)),
        "base_actual_rate": base_rate,
        "model_accuracy": accuracy(p, y_valid),
        "model_log_loss": log_loss(p, y_valid),
        "model_brier": brier(p, y_valid),
        "base_log_loss": log_loss(base_p, y_valid),
        "base_brier": brier(base_p, y_valid),
        "threshold_rows": n,
        "actual_hit_rate": actual_hit,
        "avg_model_prob_threshold": avg_prob,
        "uplift_vs_base": uplift,
    }


def classify_stability(rows: list[dict[str, object]], min_gate_rows: int, required_hit: float, required_uplift: float) -> str:
    ok_rows = [r for r in rows if r.get("status") == "OK"]
    if not ok_rows:
        return "BLOCK_NO_VALID_SPLITS"
    pass_rows = [
        r for r in ok_rows
        if int(r.get("threshold_rows", 0)) >= min_gate_rows
        and float(r.get("actual_hit_rate", 0.0)) >= required_hit
        and float(r.get("uplift_vs_base", 0.0)) >= required_uplift
    ]
    catastrophic = [
        r for r in ok_rows
        if int(r.get("threshold_rows", 0)) >= max(10, min_gate_rows // 2)
        and float(r.get("actual_hit_rate", 0.0)) < required_hit - 0.10
    ]
    if len(pass_rows) == len(ok_rows) and len(ok_rows) >= 3:
        return "STABLE_PROMOTE"
    if len(pass_rows) >= max(2, int(np.ceil(len(ok_rows) * 0.75))) and not catastrophic:
        return "PROMOTE_BUT_MONITOR"
    if len(pass_rows) >= 2 and not catastrophic:
        return "RESEARCH_ONLY_STABLE_SUPPORT"
    if catastrophic:
        return "DEGRADE_VOLATILE"
    return "HOLD_RESEARCH_ONLY"


def evaluate(
    dataset: Path,
    u35_config: Path,
    tt_config: Path,
    out_json: Path,
    out_csv: Path,
    splits: list[float],
    min_gate_rows: int,
    epochs: int,
    lr: float,
    l2: float,
) -> None:
    df = pd.read_csv(dataset)
    if "fixture_date" in df.columns:
        df = df.sort_values("fixture_date")
    feature_cols = sorted([c for c in df.columns if c.startswith("feat_")])
    if not feature_cols:
        raise RuntimeError("No feat_ columns found")
    u35_cfg = read_json(u35_config)
    tt_cfg = read_json(tt_config)
    plan = gate_plan(u35_cfg, tt_cfg)

    detail_rows: list[dict[str, object]] = []
    summary: dict[str, object] = {}
    for gate in plan:
        league_name = str(gate["league_name"])
        league_df = df[df["league_name"] == league_name].sort_values("fixture_date").copy()
        split_rows = [split_eval(league_df, feature_cols, gate, s, epochs, lr, l2) for s in splits]
        stability = classify_stability(
            split_rows,
            min_gate_rows=min_gate_rows,
            required_hit=float(gate["required_hit_rate"]),
            required_uplift=float(gate["required_uplift"]),
        )
        pass_count = 0
        ok_count = 0
        for row in split_rows:
            if row.get("status") == "OK":
                ok_count += 1
                passed = int(row.get("threshold_rows", 0)) >= min_gate_rows and float(row.get("actual_hit_rate", 0.0)) >= float(gate["required_hit_rate"]) and float(row.get("uplift_vs_base", 0.0)) >= float(gate["required_uplift"])
                pass_count += int(passed)
            else:
                passed = False
            detail_rows.append({
                "gate_id": gate["gate_id"],
                "gate_type": gate["gate_type"],
                "league_code": gate["league_code"],
                "league_name": gate["league_name"],
                "market_family": gate["market_family"],
                "configured_status": gate["status"],
                "model_prob_min": gate["model_prob_min"],
                "market_under25_prob_min": gate.get("market_under25_prob_min", 0.0),
                "required_hit_rate": gate["required_hit_rate"],
                "required_uplift": gate["required_uplift"],
                "stability_verdict": stability,
                "split_pass": "YES" if passed else "NO",
                **row,
            })
        rates = [float(r.get("actual_hit_rate", 0.0)) for r in split_rows if r.get("status") == "OK" and int(r.get("threshold_rows", 0)) > 0]
        rows_counts = [int(r.get("threshold_rows", 0)) for r in split_rows if r.get("status") == "OK"]
        summary[str(gate["gate_id"])] = {
            **gate,
            "stability_verdict": stability,
            "ok_splits": ok_count,
            "passing_splits": pass_count,
            "min_threshold_rows_observed": min(rows_counts) if rows_counts else 0,
            "avg_threshold_rows_observed": float(np.mean(rows_counts)) if rows_counts else 0.0,
            "min_actual_hit_rate_observed": min(rates) if rates else 0.0,
            "avg_actual_hit_rate_observed": float(np.mean(rates)) if rates else 0.0,
        }

    out = {
        "dataset": str(dataset),
        "splits": splits,
        "min_gate_rows": min_gate_rows,
        "feature_count": len(feature_cols),
        "u35_config": str(u35_config),
        "team_total_config": str(tt_config),
        "gate_count": len(plan),
        "summary": summary,
        "precision_read": {
            "STABLE_PROMOTE": "eligible for active shadow gate",
            "PROMOTE_BUT_MONITOR": "keep active but monitor closely",
            "RESEARCH_ONLY_STABLE_SUPPORT": "support only; not production validation",
            "DEGRADE_VOLATILE": "remove or downgrade from active config",
            "HOLD_RESEARCH_ONLY": "keep research-only",
        },
    }
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    fields = list(detail_rows[0].keys()) if detail_rows else []
    with out_csv.open("w", encoding="utf-8", newline="") as handle:
        if fields:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            for row in detail_rows:
                writer.writerow({k: row.get(k, "") for k in fields})
    print(f"Gate stability evaluation complete gates={len(plan)}")
    print(f"json={out_json}")
    print(f"csv={out_csv}")
    for gate_id, row in summary.items():
        print(gate_id, row["stability_verdict"], f"pass={row['passing_splits']}/{row['ok_splits']}", f"min_hit={row['min_actual_hit_rate_observed']:.3f}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", type=Path, default=DATASET)
    ap.add_argument("--u35-config", type=Path, default=U35_CONFIG)
    ap.add_argument("--team-total-config", type=Path, default=TT_CONFIG)
    ap.add_argument("--out-json", type=Path, default=OUT_JSON)
    ap.add_argument("--out-csv", type=Path, default=OUT_CSV)
    ap.add_argument("--splits", default="0.70,0.75,0.80,0.85")
    ap.add_argument("--min-gate-rows", type=int, default=25)
    ap.add_argument("--epochs", type=int, default=1200)
    ap.add_argument("--lr", type=float, default=0.04)
    ap.add_argument("--l2", type=float, default=0.001)
    args = ap.parse_args()
    splits = [float(x.strip()) for x in args.splits.split(",") if x.strip()]
    evaluate(args.dataset, args.u35_config, args.team_total_config, args.out_json, args.out_csv, splits, args.min_gate_rows, args.epochs, args.lr, args.l2)
