"""World Cup evidence diagnostics: read-only, deterministic and non-predictive.

This tool evaluates frozen 1X2 predictions on common settled fixtures using the final-audit
bootstrap protocol (10,000 paired resamples, seed 20260713).  It also flags pending fixtures whose
full-data/L3 disagreement lies outside the settled historical range.  Alerts are evidence for human
review only: they never select a model, change probabilities, call an API or send Telegram.

Run without writes:
    python analysis/worldcup/worldcup_evidence_diagnostics.py
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
PRED_LOG = HERE / "worldcup_predictions_log.csv"
AB_LOG = HERE / "worldcup_full_data_ab_log.csv"

N_BOOTSTRAP = 10_000
BOOTSTRAP_SEED = 20_260_713
RESULT_INDEX = {"H": 0, "D": 1, "A": 2}

MODEL_COLUMNS = {
    "l3": ("l3_home", "l3_draw", "l3_away"),
    "mx": ("mx_home", "mx_draw", "mx_away"),
    "full_data": ("fd_home", "fd_draw", "fd_away"),
    "ensemble": ("ens_home", "ens_draw", "ens_away"),
}

COMPARISONS = (
    ("full_data", "l3"),
    ("full_data", "ensemble"),
    ("ensemble", "l3"),
    ("mx", "l3"),
)


def paired_bootstrap(delta, n_bootstrap=N_BOOTSTRAP, seed=BOOTSTRAP_SEED):
    """Return mean and percentile IC95 for paired per-fixture deltas.

    A positive delta means the candidate is better because callers pass
    ``loss_reference - loss_candidate``.  The conclusion is deliberately conservative.
    """
    d = np.asarray(delta, dtype=float)
    d = d[np.isfinite(d)]
    if not len(d):
        return {"n": 0, "mean": None, "ci95_low": None, "ci95_high": None,
                "conclusion": "NO_EVALUABLE"}
    rng = np.random.default_rng(seed)
    indices = rng.integers(0, len(d), size=(n_bootstrap, len(d)))
    samples = d[indices].mean(axis=1)
    lo, hi = np.percentile(samples, (2.5, 97.5))
    if lo > 0:
        conclusion = "CANDIDATE_FAVORED"
    elif hi < 0:
        conclusion = "REFERENCE_FAVORED"
    else:
        conclusion = "INCONCLUSIVE"
    return {"n": int(len(d)), "mean": float(d.mean()), "ci95_low": float(lo),
            "ci95_high": float(hi), "conclusion": conclusion}


def _normalise_probabilities(values):
    p = np.asarray(values, dtype=float)
    if p.ndim != 2 or p.shape[1] != 3:
        raise ValueError("expected an N x 3 probability matrix")
    if not np.isfinite(p).all() or (p < 0).any() or (p.sum(axis=1) <= 0).any():
        raise ValueError("invalid probabilities")
    p = p / p.sum(axis=1, keepdims=True)
    return np.clip(p, 1e-15, 1.0)


def loss_rows(probabilities, outcomes):
    """Per-fixture multiclass log-loss and Brier loss."""
    p = _normalise_probabilities(probabilities)
    y = np.asarray(outcomes, dtype=int)
    one_hot = np.eye(3)[y]
    return {"logloss": -np.log(p[np.arange(len(y)), y]),
            "brier": np.sum((p - one_hot) ** 2, axis=1)}


def compare_models(frame, candidate, reference):
    """Compare two models on exactly the same valid settled fixtures."""
    candidate_cols = MODEL_COLUMNS[candidate]
    reference_cols = MODEL_COLUMNS[reference]
    required = [*candidate_cols, *reference_cols, "result_1x2", "settled"]
    valid = frame["settled"].fillna(0).astype(float).eq(1)
    valid &= frame["result_1x2"].isin(RESULT_INDEX)
    for col in required[:-2]:
        valid &= pd.to_numeric(frame[col], errors="coerce").notna()
    common = frame.loc[valid, required].copy()
    if common.empty:
        return []
    outcomes = common["result_1x2"].map(RESULT_INDEX).to_numpy(int)
    candidate_loss = loss_rows(common[list(candidate_cols)].to_numpy(float), outcomes)
    reference_loss = loss_rows(common[list(reference_cols)].to_numpy(float), outcomes)
    rows = []
    for metric in ("logloss", "brier"):
        result = paired_bootstrap(reference_loss[metric] - candidate_loss[metric])
        rows.append({"candidate": candidate, "reference": reference, "metric": metric,
                     "delta_reference_minus_candidate": result["mean"], **result})
    return rows


def disagreement_diagnostics(frame):
    """Flag pending full-data/L3 total variation outside the settled comparison range."""
    needed = [*MODEL_COLUMNS["full_data"], *MODEL_COLUMNS["l3"]]
    valid = pd.Series(True, index=frame.index)
    for col in needed:
        valid &= pd.to_numeric(frame[col], errors="coerce").notna()
    data = frame.loc[valid].copy()
    if data.empty:
        return []
    full = _normalise_probabilities(data[list(MODEL_COLUMNS["full_data"])].to_numpy(float))
    l3 = _normalise_probabilities(data[list(MODEL_COLUMNS["l3"])].to_numpy(float))
    data["total_variation"] = 0.5 * np.abs(full - l3).sum(axis=1)
    historical = data[data["settled"].fillna(0).astype(float).eq(1)]["total_variation"].to_numpy(float)
    pending = data[~data["settled"].fillna(0).astype(float).eq(1)]
    historical_max = float(historical.max()) if len(historical) else None
    rows = []
    for row in pending.itertuples(index=False):
        tv = float(row.total_variation)
        outside = historical_max is not None and tv > historical_max + 1e-12
        percentile = float(100.0 * np.mean(historical <= tv)) if len(historical) else None
        rows.append({"fixture_id": int(row.fixture_id), "home": row.home, "away": row.away,
                     "total_variation": tv, "settled_historical_n": int(len(historical)),
                     "settled_historical_max": historical_max, "historical_percentile": percentile,
                     "status": "EXTREME_OUTSIDE_SETTLED_RANGE" if outside else "WITHIN_SETTLED_RANGE",
                     "action": "REVIEW_ONLY_NO_MODEL_CHANGE"})
    return rows


def load_evidence_frame(pred_path=PRED_LOG, ab_path=AB_LOG):
    pred = pd.read_csv(pred_path)
    ab = pd.read_csv(ab_path)
    keep = ["fixture_id", "fd_home", "fd_draw", "fd_away", "ens_home", "ens_draw", "ens_away"]
    return pred.merge(ab[keep], on="fixture_id", how="inner", validate="one_to_one")


def build_report(frame):
    comparisons = []
    for candidate, reference in COMPARISONS:
        comparisons.extend(compare_models(frame, candidate, reference))
    return {"protocol": {"paired_bootstrap_resamples": N_BOOTSTRAP, "seed": BOOTSTRAP_SEED,
                         "ci": "percentile_95", "positive_delta": "candidate_better"},
            "comparisons": comparisons,
            "pending_disagreement_diagnostics": disagreement_diagnostics(frame),
            "production_effect": "NONE"}


def main():
    report = build_report(load_evidence_frame())
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
