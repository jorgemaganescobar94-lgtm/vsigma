"""
Offline tests for the Fase-4L team shots-on-target (SOT) scorecard. Read-only, no network, no model,
no API, no market/odds/betting. Cover:
  * real SOT extracted from a /fixtures/statistics mock JSON ('Shots on Goal');
  * predicted SOT = sum of per-player lam_shot_on;
  * MAE / RMSE / bias over the evaluable rows;
  * a fixture with no real SOT -> not evaluable (no fabrication);
  * a fixture with no predicted SOT but a real SOT -> actual-only, not evaluable;
  * Fase 4J marks 'Team stats: SOT' ACTIVO when the scorecard has enough rows;
  * Fase 4J keeps it NO_EVALUABLE when the scorecard is absent;
  * the report carries no betting language;
  * the module touches no market/API endpoint.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import build_worldcup_team_sot_scorecard as sot  # noqa: E402
import evaluate_worldcup_prediction_accuracy as pa  # noqa: E402


# ------------------------------------------------------------------ builders for mock inputs
def _player(fid, tid, team, pid, lam, act, is_xi=1, settled=1, ko="2026-06-26 19:00"):
    return {"fixture_id": fid, "kickoff_utc": ko, "team_id": tid, "team": team,
            "player_id": pid, "is_xi": is_xi, "lam_shot_on": lam, "act_shots_on": act,
            "settled": settled}


def _props(rows):
    return pd.DataFrame(rows)


def _enrichment_dir(tmp_path, fid, home_id, home, away_id, away, sog_home, sog_away):
    d = tmp_path / "enrich"
    d.mkdir(exist_ok=True)
    payload = {
        "fixture_id": fid, "home": home, "away": away, "home_id": home_id, "away_id": away_id,
        "postft": {"statistics": [
            {"team": {"id": home_id, "name": home},
             "statistics": [{"type": "Shots on Goal", "value": sog_home},
                            {"type": "Total Shots", "value": sog_home + 5}]},
            {"team": {"id": away_id, "name": away},
             "statistics": [{"type": "Shots on Goal", "value": sog_away},
                            {"type": "Total Shots", "value": sog_away + 5}]},
        ]},
    }
    (d / f"{fid}.json").write_text(json.dumps(payload), encoding="utf-8")
    return d


# ------------------------------------------------------------------ real SOT from fixture statistics
def test_real_sot_from_fixture_statistics_mock(tmp_path):
    d = _enrichment_dir(tmp_path, 900, 10, "England", 1504, "Ghana", 3, 1)
    fs = sot.load_fixture_statistics_sot(d)
    assert fs[(900, 10)]["sot"] == 3.0
    assert fs[(900, 1504)]["sot"] == 1.0
    # opponent + side resolved from within the same fixture / home-away ids
    assert fs[(900, 10)]["opponent_id"] == 1504 and fs[(900, 10)]["side"] == "home"
    assert fs[(900, 1504)]["side"] == "away"


def test_fixture_statistics_skips_missing_sot(tmp_path):
    d = tmp_path / "enrich"; d.mkdir()
    # a team with no 'Shots on Goal' entry must NOT be fabricated (absent from the map)
    payload = {"fixture_id": 901, "home_id": 1, "away_id": 2,
               "postft": {"statistics": [
                   {"team": {"id": 1, "name": "A"}, "statistics": [{"type": "Total Shots", "value": 9}]},
                   {"team": {"id": 2, "name": "B"}, "statistics": [{"type": "Shots on Goal", "value": 4}]},
               ]}}
    (d / "901.json").write_text(json.dumps(payload), encoding="utf-8")
    fs = sot.load_fixture_statistics_sot(d)
    assert (901, 1) not in fs and fs[(901, 2)]["sot"] == 4.0


# ------------------------------------------------------------------ predicted SOT = sum of players
def test_predicted_sot_is_player_lambda_sum():
    rows = [_player(1, 10, "A", 101, 1.2, 1), _player(1, 10, "A", 102, 0.8, 0),
            _player(1, 10, "A", 103, 0.5, 2)]
    agg = sot.aggregate_player_sot(_props(rows))
    assert agg[(1, 10)]["pred_sot"] == pytest.approx(2.5)
    assert agg[(1, 10)]["act_player_sum"] == pytest.approx(3.0)
    assert agg[(1, 10)]["n_players"] == 3 and agg[(1, 10)]["n_xi"] == 3


def test_unsettled_rows_excluded():
    rows = [_player(1, 10, "A", 101, 1.2, 1, settled=1),
            _player(1, 10, "A", 102, 5.0, 9, settled=0)]   # not settled -> ignored
    agg = sot.aggregate_player_sot(_props(rows))
    assert agg[(1, 10)]["pred_sot"] == pytest.approx(1.2)
    assert agg[(1, 10)]["n_players"] == 1


# ------------------------------------------------------------------ metrics MAE/RMSE/bias
def test_metrics_mae_rmse_bias():
    # two teams: pred 3.0 vs real 1.0 (err +2), pred 1.0 vs real 2.0 (err -1)
    rows = [_player(1, 10, "A", 101, 3.0, 1.0, ko=""), _player(1, 20, "B", 201, 1.0, 2.0, ko="")]
    rows_out = sot.build_rows(_props(rows), None, None, {})
    summary, _ = sot.compute_summary(rows_out)
    assert summary["n_team_rows"] == 2
    assert summary["mae"] == pytest.approx((2 + 1) / 2)
    assert summary["bias"] == pytest.approx((2 - 1) / 2)
    assert summary["rmse"] == pytest.approx(np.sqrt((4 + 1) / 2), abs=1e-3)
    assert summary["overprediction_rows"] == 1 and summary["underprediction_rows"] == 1
    assert summary["status"] == "INSUFFICIENT_SAMPLE"   # n=2 < SMALL_N


def test_rmse_ge_mae_on_live_csv():
    """Sanity vs the committed live scorecard (robust to growth)."""
    df = pa._read_csv(sot.OUT_CSV)
    if df is None:
        pytest.skip("no live SOT scorecard yet")
    ev = df.dropna(subset=["predicted_sot", "actual_sot"])
    if not len(ev):
        pytest.skip("no evaluable rows yet")
    err = ev["predicted_sot"].astype(float) - ev["actual_sot"].astype(float)
    assert err.abs().mean() >= 0
    assert np.sqrt((err ** 2).mean()) >= err.abs().mean() - 1e-9


# ------------------------------------------------------------------ fixture statistics preferred as actual
def test_actual_prefers_fixture_statistics_over_player_sum(tmp_path):
    rows = [_player(900, 10, "England", 101, 2.0, 5.0, ko="")]   # player-sum real would be 5.0
    fs = sot.load_fixture_statistics_sot(
        _enrichment_dir(tmp_path, 900, 10, "England", 1504, "Ghana", 3, 1))
    out = {r["team_id"]: r for r in sot.build_rows(_props(rows), None, None, fs)}
    r = out[10]
    assert r["source_actual"] == "fixture_statistics" and float(r["actual_sot"]) == 3.0
    assert r["data_quality"].startswith("evaluable")


# ------------------------------------------------------------------ missing actual / missing prediction
def test_fixture_without_actual_is_not_evaluable():
    rows = [_player(1, 10, "A", 101, 2.0, np.nan, ko="")]   # no real SOT
    out = sot.build_rows(_props(rows), None, None, {})
    r = out[0]
    assert r["actual_sot"] == "" and r["data_quality"] == "prediction_only_no_actual"
    summary, _ = sot.compute_summary(out)
    assert summary["n_team_rows"] == 0


def test_fixture_without_prediction_is_actual_only(tmp_path):
    # store has real SOT for a fixture with NO logged props -> actual-only, never paired
    fs = sot.load_fixture_statistics_sot(
        _enrichment_dir(tmp_path, 902, 7, "X", 8, "Y", 2, 4))
    out = {r["team_id"]: r for r in sot.build_rows(None, None, None, fs)}
    assert out[7]["predicted_sot"] == "" and out[7]["data_quality"] == "actual_only_no_prediction"
    assert float(out[7]["actual_sot"]) == 2.0
    summary, _ = sot.compute_summary(list(out.values()))
    assert summary["n_team_rows"] == 0 and summary["n_actual_only"] == 2


# ------------------------------------------------------------------ Fase 4J integration
def test_phase4j_marks_sot_activo_with_scorecard(tmp_path):
    rows = [{"fixture_id": i, "predicted_sot": 3.0, "actual_sot": 2.0} for i in range(pa.MIN_SAMPLE + 5)]
    p = tmp_path / "sot.csv"; pd.DataFrame(rows).to_csv(p, index=False)
    m = pa.evaluate_team_sot(p)
    assert m["module"] == "Team stats: SOT" and m["status"] == "ACTIVO"
    assert m["n"] == pa.MIN_SAMPLE + 5 and m["primary_value"] == pytest.approx(1.0)


def test_phase4j_insufficient_sample_small_scorecard(tmp_path):
    rows = [{"fixture_id": i, "predicted_sot": 3.0, "actual_sot": 2.0} for i in range(5)]
    p = tmp_path / "sot.csv"; pd.DataFrame(rows).to_csv(p, index=False)
    assert pa.evaluate_team_sot(p)["status"] == "INSUFFICIENT_SAMPLE"


def test_phase4j_keeps_no_evaluable_when_scorecard_missing(tmp_path):
    m = pa.evaluate_team_sot(tmp_path / "does_not_exist.csv")
    assert m["status"] == "NO_EVALUABLE" and m["n"] == 0


def test_phase4j_no_evaluable_when_no_paired_rows(tmp_path):
    rows = [{"fixture_id": 1, "predicted_sot": 3.0, "actual_sot": ""},
            {"fixture_id": 2, "predicted_sot": "", "actual_sot": 2.0}]
    p = tmp_path / "sot.csv"; pd.DataFrame(rows).to_csv(p, index=False)
    assert pa.evaluate_team_sot(p)["status"] == "NO_EVALUABLE"


def test_team_stats_no_longer_injects_sot_placeholder():
    """evaluate_team_stats must NOT add a 'Team stats: SOT' placeholder anymore (Fase 4L owns it)."""
    sc = pd.DataFrame([{"stat": "shots", "n": 39, "mae": 7.4, "rmse": 8.9, "bias": -6.0,
                        "mean_pred": 18.3, "mean_real": 24.3, "line_acc": None}])
    names = {m["module"] for m in pa.evaluate_team_stats(sc)}
    assert "Team stats: tiros" in names and "Team stats: SOT" not in names


# ------------------------------------------------------------------ report honesty + isolation
def test_report_has_no_betting_language():
    rows = [_player(1, 10, "A", 101, 3.0, 1.0, ko=""), _player(1, 20, "B", 201, 1.0, 2.0, ko="")]
    out = sot.build_rows(_props(rows), None, None, {})
    summary, _ = sot.compute_summary(out)
    text = sot.render_txt(out, summary).lower()
    for bad in ["apuesta", "cuota", "stake", "odds", "edge", "pick", "roi", "bet", "mercado de"]:
        assert bad not in text


def test_empty_inputs_soft():
    out = sot.build_rows(None, None, None, {})
    summary, _ = sot.compute_summary(out)
    assert summary["n_team_rows"] == 0
    assert "aún sin equipos-partido" in sot.render_txt(out, summary)


def test_no_market_or_api_calls_in_module():
    src = (HERE / "build_worldcup_team_sot_scorecard.py").read_text(encoding="utf-8")
    for bad in ('request("/odds"', "request('/odds'", 'request("/predictions"',
                "request('/predictions'", ".odds(", ".predictions(", "APIFootballClient",
                "requests.get", "http://", "https://"):
        assert bad not in src
