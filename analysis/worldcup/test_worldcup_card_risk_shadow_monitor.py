"""
Fase 4I offline tests (NO network, NO API, NO scraping, NO betting, NO writes to data/external).
Cover the card-risk SHADOW MONITOR state machine, the strict should_adjust_weights gate, and the
internal report. Weights are never changed; the gate must stay False in the current regime.
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[1] / "analysis" / "players"))

import monitor_worldcup_card_risk_shadow as mon  # noqa: E402

FORBIDDEN = ["apuesta", "apostar", "cuota", "odds", "edge", "pick", "stake", "roi", "mercado"]


def _metrics(n=418, pos=39, dbp=-0.0001, dlp=-0.0004, frac=0.077,
             rs=0.12, rb=0.04, rn=0.10, cs=114, cb=79, cn=225, **extra):
    m = {
        "evaluated_predictions": n, "positive_cards": pos, "card_rate_real": round(pos / n, 4) if n else None,
        "brier_original": 0.093, "brier_adjusted_cumulative": 0.092, "brier_adjusted_pre_fixture": 0.0929,
        "delta_brier_cumulative": -0.001, "delta_brier_pre_fixture": dbp,
        "logloss_original": 0.33, "logloss_adjusted_cumulative": 0.328,
        "logloss_adjusted_pre_fixture": 0.3296,
        "delta_logloss_cumulative": -0.002, "delta_logloss_pre_fixture": dlp,
        "fraction_of_4g_gain_surviving": frac, "average_adjustment_size": 0.003,
        "count_subir": cs, "count_bajar": cb, "count_neutro": cn,
        "real_rate_subir": rs, "real_rate_bajar": rb, "real_rate_neutro": rn,
    }
    m.update(extra)
    return m


# ---------------------------------------------------------------- state machine
def test_state_shadow_neutral_when_negligible():
    state, mode, verdict, reason = mon.classify_state(_metrics(pos=39, dbp=-0.0001))
    assert state == "SHADOW_NEUTRAL" and mode == "SHADOW_NEUTRAL"
    assert "negligible" in reason.lower() or "ruido" in reason.lower()


def test_state_insufficient_sample_few_positives():
    state, *_ = mon.classify_state(_metrics(n=120, pos=12))
    assert state == "INSUFFICIENT_SAMPLE"


def test_state_insufficient_sample_small_n():
    state, *_ = mon.classify_state(_metrics(n=80, pos=40))
    assert state == "INSUFFICIENT_SAMPLE"


def test_state_keep_weak_small_consistent_improvement():
    # >=75 positives, improves both, not negligible, not material, no contrary direction
    state, *_ = mon.classify_state(_metrics(n=900, pos=80, dbp=-0.0010, dlp=-0.0030,
                                            rs=0.14, rb=0.06))
    assert state == "KEEP_WEAK"


def test_state_consider_recalibration_material_and_stable():
    state, *_ = mon.classify_state(_metrics(n=1200, pos=120, dbp=-0.0030, dlp=-0.0070,
                                            frac=0.7, rs=0.20, rb=0.05))
    assert state == "CONSIDER_RECALIBRATION"


def test_state_reduce_or_disable_when_worsens():
    state, *_ = mon.classify_state(_metrics(n=900, pos=90, dbp=0.0030, dlp=0.0080))
    assert state == "REDUCE_OR_DISABLE"


def test_state_reduce_or_disable_when_direction_contrary():
    # subir players get cards LESS than bajar players -> contrary signal
    state, *_ = mon.classify_state(_metrics(n=900, pos=90, dbp=-0.001, dlp=-0.003,
                                            rs=0.03, rb=0.12, cs=120, cb=120))
    assert state == "REDUCE_OR_DISABLE"


# ---------------------------------------------------------------- safety gate
def test_should_adjust_weights_false_current_state():
    assert mon.should_adjust_weights({"metrics": _metrics()}) is False


def test_should_adjust_weights_false_even_if_improves_but_few_positives():
    assert mon.should_adjust_weights({"metrics": _metrics(pos=60, dbp=-0.003, dlp=-0.007, frac=0.7,
                                                          rs=0.2, rb=0.05)}) is False


def test_should_adjust_weights_true_only_with_strict_conditions():
    strict = _metrics(n=1500, pos=150, dbp=-0.0030, dlp=-0.0070, frac=0.7, rs=0.22, rb=0.05)
    assert mon.should_adjust_weights({"metrics": strict}) is True


def test_should_adjust_weights_false_if_fraction_too_low():
    # material + many positives BUT only 8% of the gain survives -> still False
    weak = _metrics(n=1500, pos=150, dbp=-0.0030, dlp=-0.0070, frac=0.08, rs=0.22, rb=0.05)
    assert mon.should_adjust_weights({"metrics": weak}) is False


# ---------------------------------------------------------------- report wording
def test_report_no_betting_language():
    snap = {"state": "SHADOW_NEUTRAL", "reason": "mejora negligible", "action": mon._ACTION["SHADOW_NEUTRAL"],
            "should_adjust_weights": False, "confidence": "baja", "metrics": _metrics()}
    txt = mon.render_txt(snap)
    assert "Card Risk Shadow Monitor" in txt and "Estado: SHADOW_NEUTRAL" in txt
    assert not any(w in txt.lower() for w in FORBIDDEN)


# ---------------------------------------------------------------- artifact build (round-trip, real data)
def test_build_writes_artifacts(tmp_path, monkeypatch):
    monkeypatch.setattr(mon, "OUT_CSV", tmp_path / "mon.csv")
    monkeypatch.setattr(mon, "OUT_JSON", tmp_path / "mon.json")
    monkeypatch.setattr(mon, "OUT_TXT", tmp_path / "mon.txt")
    snap = mon.build(write=True)
    assert (tmp_path / "mon.csv").exists() and (tmp_path / "mon.json").exists()
    assert snap["state"] in ("SHADOW_NEUTRAL", "INSUFFICIENT_SAMPLE", "KEEP_WEAK",
                             "CONSIDER_RECALIBRATION", "REDUCE_OR_DISABLE")
    assert snap["should_adjust_weights"] in (True, False)
