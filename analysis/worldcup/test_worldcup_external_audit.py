"""
Fase 4C-2 offline tests (NO network, NO API, NO betting). Covers the external-context audit, the
prepare --dry-run mode (computes change set WITHOUT writing), and the persistence-policy doc.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))

import audit_worldcup_store_external_context as audit  # noqa: E402
import prepare_worldcup_external_templates as prep  # noqa: E402


# ============================================================ store audit
def test_audit_store_without_fixture_block():
    store = [{"fixture_id": 1, "postft": {"summary": {"n_goals": 0}, "events": [{"x": 1}],
                                          "players": [{"y": 1}]}}]
    a = audit.audit_store(store)
    t = a["totals"]
    assert t["fixtures_total"] == 1 and t["has_fixture_block"] == 0
    assert t["has_referee"] == 0 and t["has_venue_name"] == 0
    assert t["has_events"] == 1 and t["has_players"] == 1
    assert t["incomplete_old"] == 1            # postft present but no fixture block


def test_audit_store_with_fixture_block():
    store = [{"fixture_id": 7, "fixture": {"referee": "Mr Ref",
                                           "venue": {"name": "Estadio X", "city": "Ciudad"},
                                           "date": "2026-06-23T19:00"},
              "postft": {"events": [{"x": 1}], "players": [{"y": 1}], "lineups": [{"z": 1}]}}]
    t = audit.audit_store(store)["totals"]
    assert t["has_fixture_block"] == 1 and t["has_referee"] == 1
    assert t["has_venue_name"] == 1 and t["has_venue_city"] == 1 and t["has_date"] == 1
    assert t["has_lineups"] == 1 and t["incomplete_old"] == 0


def test_audit_store_empty():
    t = audit.audit_store([])["totals"]
    assert t["fixtures_total"] == 0 and t["has_referee"] == 0


# ============================================================ external-CSV audit
def _write(ext, fname, rows):
    cols = prep.COLUMNS[fname]
    pd.DataFrame(rows, columns=cols).to_csv(ext / fname, index=False)


def test_audit_csv_empty_template(tmp_path):
    for fname in prep.COLUMNS:
        _write(tmp_path, fname, [])
    res = audit.audit_external_csvs(tmp_path)
    assert res["player_xg_xa.csv"]["rows"] == 0
    assert res["player_xg_xa.csv"]["has_real_data"] is False
    assert res["player_xg_xa.csv"]["pending_columns"] == prep.COLUMNS["player_xg_xa.csv"]


def test_audit_csv_distinguishes_auto_and_manual(tmp_path):
    # positional: one auto row + one manual row
    _write(tmp_path, "player_positional_profiles.csv", [
        {"player_id": 1, "position": "DEF", "source": "api_football_lineup_position"},
        {"player_id": 2, "position": "RB", "source": "manual"},
    ])
    for fname in prep.COLUMNS:
        if fname != "player_positional_profiles.csv":
            _write(tmp_path, fname, [])
    res = audit.audit_external_csvs(tmp_path)["player_positional_profiles.csv"]
    assert res["rows"] == 2 and res["auto_rows"] == 1 and res["manual_rows"] == 1
    assert res["has_real_data"] is True
    assert "api_football_lineup_position" in res["sources"] and "manual" in res["sources"]
    assert "position" in res["completed_columns"] and "pace_threat" in res["pending_columns"]


def test_audit_run_writes_artifacts(tmp_path):
    sd = tmp_path / "store"
    sd.mkdir()
    (sd / "1.json").write_text('{"fixture_id":1,"fixture":{"referee":"R"}}', encoding="utf-8")
    ext = tmp_path / "ext"
    ext.mkdir()
    for fname in prep.COLUMNS:
        _write(ext, fname, [])
    out_txt = tmp_path / "audit.txt"
    out_csv = tmp_path / "audit.csv"
    res = audit.run(store_dir=sd, ext_dir=ext, out_txt=out_txt, out_csv=out_csv, write=True)
    assert out_txt.exists() and out_csv.exists()
    assert "STORE EXTERNAL-CONTEXT AUDIT" in res["txt"]
    assert pd.read_csv(out_csv).iloc[0]["has_referee"] == 1


# ============================================================ prepare --dry-run
def _events_one_pen():
    return pd.DataFrame([{"fixture_id": 1, "date": "2026-06-20", "team_id": 10, "team_name": "H",
                          "player_id": 100, "player_name": "PenA", "is_penalty_goal": 1,
                          "is_penalty_miss": 0}])


def _cards():
    return pd.DataFrame([{"fixture_id": 1, "kickoff_utc": "2026-06-20 18:00"}])


def test_dry_run_writes_nothing(tmp_path):
    summary = prep.prepare(ext_dir=tmp_path, events_df=_events_one_pen(), cards_df=_cards(),
                           store_records=[], dry_run=True)
    # NO files created at all
    assert not any((tmp_path / f).exists() for f in prep.COLUMNS)
    assert summary["set_piece_takers.csv"]["dry_run"] is True
    assert summary["set_piece_takers.csv"]["action"] == "would-create"


def test_dry_run_counts_new_rows_correctly(tmp_path):
    summary = prep.prepare(ext_dir=tmp_path, events_df=_events_one_pen(), cards_df=_cards(),
                           store_records=[], dry_run=True)
    assert summary["set_piece_takers.csv"]["added"] == 1      # one penalty taker WOULD be added
    assert summary["weather_by_fixture.csv"]["added"] == 1    # one fixture row WOULD be added
    assert not (tmp_path / "set_piece_takers.csv").exists()   # but nothing written


def test_dry_run_respects_manual_and_reports_protected(tmp_path):
    SP = "set_piece_takers.csv"
    cols = prep.COLUMNS[SP]
    # a manual penalty row with different attempts
    pd.DataFrame([{"team_id": 10, "team_name": "H", "player_id": 100, "player_name": "PenA",
                   "role": "penalty", "rank": 1, "attempts": 9, "last_taken_date": "2026-06-01",
                   "source": "manual", "data_quality": "alta", "confidence": "alta"}],
                 columns=cols).to_csv(tmp_path / SP, index=False)
    before = (tmp_path / SP).read_text(encoding="utf-8")
    summary = prep.prepare(ext_dir=tmp_path, events_df=_events_one_pen(), cards_df=_cards(),
                           store_records=[], dry_run=True)
    # the manual row's differing attempts would be PROTECTED, nothing added
    assert summary[SP]["protected"] >= 1 and summary[SP]["added"] == 0
    assert (tmp_path / SP).read_text(encoding="utf-8") == before   # file untouched


def test_dry_run_then_real_run_are_consistent(tmp_path):
    dry = prep.prepare(ext_dir=tmp_path, events_df=_events_one_pen(), cards_df=_cards(),
                       store_records=[], dry_run=True)
    real = prep.prepare(ext_dir=tmp_path, events_df=_events_one_pen(), cards_df=_cards(),
                        store_records=[], dry_run=False)
    # what dry-run predicted matches what the real run actually added
    assert dry["set_piece_takers.csv"]["added"] == real["set_piece_takers.csv"]["added"] == 1
    assert (tmp_path / "set_piece_takers.csv").exists()      # real run wrote it


# ============================================================ policy doc
def test_persistence_policy_doc_exists_and_recommends_B():
    doc = ROOT / "docs" / "worldcup_external_data_persistence_policy.md"
    assert doc.exists()
    text = doc.read_text(encoding="utf-8").lower()
    for token in ("### a)", "### b)", "### c)", "recomend"):
        assert token in text, f"missing {token!r} in policy doc"
    # must mark B as the recommendation and NOT yet active
    assert "opción b" in text
    assert "no se activa" in text or "no activad" in text or "pendiente" in text
