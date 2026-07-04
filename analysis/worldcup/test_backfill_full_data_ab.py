"""
Offline tests for the FULL-DATA A/B backfill (no network, no API). Covers: the ensemble blend
formula, that reconstruction is leakage-free-by-construction (fd_* reproduces predict() exactly and
ens_* reproduces the frozen mx_*/l3_* blend), valid probability triples, and merge/dedup semantics
(existing live rows win over reconstruction).
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import backfill_full_data_ab_log as bf  # noqa: E402
import worldcup_full_data_model as ffdm  # noqa: E402


# ----------------------------------------------------------------- blend formula
def test_blend_is_renormalised_half_mean():
    out = bf.blend_1x2(0.6, 0.3, 0.1, 0.4, 0.2, 0.4)
    # mean = (0.5, 0.25, 0.25) already sums to 1
    assert out == pytest.approx((0.5, 0.25, 0.25))


def test_blend_renormalises_when_sum_off_one():
    out = bf.blend_1x2(0.5, 0.5, 0.5, 0.5, 0.5, 0.5)   # mean (0.5,0.5,0.5) -> /1.5
    assert out == pytest.approx((1 / 3, 1 / 3, 1 / 3))
    assert sum(out) == pytest.approx(1.0)


def test_blend_none_on_missing():
    assert bf.blend_1x2(None, 0.3, 0.1, 0.4, 0.2, 0.4) is None
    assert bf.blend_1x2(0.6, 0.3, 0.1, float("nan"), 0.2, 0.4) is None


# ----------------------------------------------------------------- reconstruction
@pytest.fixture(scope="module")
def rebuilt():
    log_df = pd.read_csv(bf.LOG)
    ir_df = pd.read_csv(bf.IR)
    return bf.reconstruct(log_df, ir_df), log_df, ir_df


def test_reconstruct_yields_rows_with_valid_triples(rebuilt):
    rows, _log, _ir = rebuilt
    assert len(rows) >= 20                     # ~22 settled fixtures with mx_+l3_
    for row in rows:
        for pref in ("fd_", "ens_"):
            tri = [row[f"{pref}home"], row[f"{pref}draw"], row[f"{pref}away"]]
            assert all(0.0 <= v <= 1.0 for v in tri)
            assert sum(tri) == pytest.approx(1.0, abs=1e-3)
        assert row["n_features"] == len(ffdm.active_features())   # 31 with current flags


def test_fd_matches_predict_exactly(rebuilt):
    """fd_* in a row must EQUAL a fresh predict() with the same point-in-time inputs -> proves the
    backfill adds no post-hoc information (leakage-free reconstruction of the live prediction)."""
    rows, log_df, ir_df = rebuilt
    idmap = bf._id_map(ir_df)
    by_fid = {int(r.fixture_id): r for r in log_df.itertuples(index=False)}
    row = rows[0]
    fid = int(row["fixture_id"])
    r = by_fid[fid]
    hid, aid = idmap[fid]
    fd = ffdm.predict(hid, aid, str(r.kickoff_utc)[:10], 1,
                      float(r.l3_home), float(r.l3_draw), float(r.l3_away),
                      float(r.l3_xg_home), float(r.l3_xg_away))
    assert (fd["fd_home"], fd["fd_draw"], fd["fd_away"]) == \
           (row["fd_home"], row["fd_draw"], row["fd_away"])


def test_ens_matches_frozen_blend(rebuilt):
    """ens_* must be the 50/50 blend of the FROZEN mx_*/l3_* in the log (read, not recomputed)."""
    rows, log_df, _ir = rebuilt
    by_fid = {int(r.fixture_id): r for r in log_df.itertuples(index=False)}
    row = rows[0]
    r = by_fid[int(row["fixture_id"])]
    ens = bf.blend_1x2(r.mx_home, r.mx_draw, r.mx_away, r.l3_home, r.l3_draw, r.l3_away)
    assert (round(ens[0], 4), round(ens[1], 4), round(ens[2], 4)) == \
           (row["ens_home"], row["ens_draw"], row["ens_away"])


def test_only_settled_fixtures(rebuilt):
    """No unsettled fixture may appear (anti-hindsight: A/B is scored only on resolved matches)."""
    rows, log_df, _ir = rebuilt
    settled_ids = set(log_df[log_df["settled"].fillna(0).astype(float).eq(1)]["fixture_id"].astype(int))
    for row in rows:
        assert int(row["fixture_id"]) in settled_ids


# ----------------------------------------------------------------- merge/dedup
def test_merge_prefers_existing_live_row(tmp_path, monkeypatch):
    """If a fixture already has a live-written row, the backfill must NOT clobber it."""
    fake = tmp_path / "worldcup_full_data_ab_log.csv"
    # a pre-existing "live" row with a sentinel fd_home we can detect
    pd.DataFrame([{
        "fixture_id": 1489420, "kickoff_utc": "2026-06-27 00:00", "home": "X", "away": "Y",
        "fd_home": 0.9999, "fd_draw": 0.00005, "fd_away": 0.00005,
        "ens_home": 0.9999, "ens_draw": 0.00005, "ens_away": 0.00005,
        "n_features": 31, "n_missing": 0}]).to_csv(fake, index=False)
    monkeypatch.setattr(bf, "AB_LOG", fake)
    bf.main(dry_run=False)
    df = pd.read_csv(fake)
    kept = df[df["fixture_id"] == 1489420].iloc[0]
    assert kept["fd_home"] == pytest.approx(0.9999)   # live row preserved, not overwritten
    assert kept["home"] == "X"


def test_dry_run_writes_nothing(tmp_path, monkeypatch):
    fake = tmp_path / "worldcup_full_data_ab_log.csv"
    monkeypatch.setattr(bf, "AB_LOG", fake)
    bf.main(dry_run=True)
    assert not fake.exists()
