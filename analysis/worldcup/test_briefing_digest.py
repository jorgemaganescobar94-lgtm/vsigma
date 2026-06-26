"""
Offline tests for the DISPLAY-ONLY briefing digest in build_worldcup_full_card:
  * day_summary_line: clearest favourite (highest single-team prob) + most balanced match.
  * firmest_predictions_block: top-3 ordered by model confidence (winning-class prob), honest label.
  * no matches -> no lines; honest wording (NO 'value'/'apuesta'/'bet').
Pure rendering from the already-stored predictions; NO model recompute, NO API, NO network.

Run:  python analysis/worldcup/test_briefing_digest.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_worldcup_full_card as F  # noqa: E402


def _row(home, away, ph, pdrw, pa, xgh=1.5, xga=1.0, **kw):
    base = {"home": home, "away": away, "kickoff_utc": "2026-06-26 20:00",
            "round": "Group Stage - 3", "home_group": "Group H",
            "our_home": ph, "our_draw": pdrw, "our_away": pa,
            "our_xg_home": xgh, "our_xg_away": xga}
    base.update(kw)
    return base


def _df(rows):
    return pd.DataFrame(rows)


# Netherlands huge favourite (0.84); Colombia-Portugal near-even (0.34 max).
SLATE = _df([
    _row("Netherlands", "Qatar", 0.84, 0.10, 0.06, xgh=2.6, xga=0.4),
    _row("Colombia", "Portugal", 0.33, 0.34, 0.33, xgh=1.1, xga=1.2),
    _row("Spain", "Uruguay", 0.65, 0.19, 0.16, xgh=1.9, xga=0.7),
    _row("Brazil", "Haiti", 0.78, 0.14, 0.08, xgh=2.3, xga=0.5),
])


def test_day_summary_picks_clearest_favourite_and_most_even():
    line = F.day_summary_line(SLATE)
    assert line is not None
    assert "4 partidos hoy" in line
    # clearest favourite = Netherlands 84% (es_name -> Países Bajos), NOT Brazil 78%
    assert "favorito más claro: Países Bajos (84%)" in line, line
    # most balanced = Colombia-Portugal (max class prob 0.34, lowest of the slate)
    assert "más parejo: Colombia–Portugal" in line, line


def test_day_summary_uses_away_team_when_away_is_favourite():
    df = _df([_row("Qatar", "Netherlands", 0.06, 0.10, 0.84, xgh=0.4, xga=2.6),
              _row("A", "B", 0.4, 0.3, 0.3)])
    line = F.day_summary_line(df)
    assert "favorito más claro: Países Bajos (84%)" in line, line


def test_day_summary_uses_ctx_when_present():
    # ctx_* overrides our_* (the displayed prediction). Favourite must read ctx.
    df = _df([_row("Spain", "Uruguay", 0.65, 0.19, 0.16,
                   ctx_home=0.90, ctx_draw=0.06, ctx_away=0.04,
                   ctx_xg_home=2.8, ctx_xg_away=0.3, context_note="ajustado por contexto de grupo"),
              _row("A", "B", 0.5, 0.3, 0.2)])
    line = F.day_summary_line(df)
    assert "favorito más claro: España (90%)" in line, line


def test_firmest_orders_by_confidence_top3():
    block = F.firmest_predictions_block(SLATE, top_n=3)
    assert block, "expected a firmest block"
    assert block[0] == F.FIRMEST_LABEL
    body = block[1:]
    assert len(body) == 3, body
    # order by confidence: Netherlands 84% > Brazil 78% > Spain 65% (Colombia 34% excluded)
    assert "Países Bajos vs Catar — Países Bajos 84%" in body[0], body[0]
    assert "Brasil" in body[1] and "78%" in body[1], body[1]
    assert "España" in body[2] and "65%" in body[2], body[2]
    assert "Colombia" not in " ".join(body)
    # xG is shown
    assert "xG 2.6-0.4" in body[0], body[0]


def test_firmest_label_is_honest_no_betting_words():
    txt = " ".join(F.firmest_predictions_block(SLATE)).lower()
    for forbidden in ("value", "apuesta", "apostar", "bet", "mejores apuestas", "pick"):
        assert forbidden not in txt, f"label must not contain '{forbidden}': {txt}"
    assert "firmes" in txt and "confianza" in txt


def test_empty_slate_yields_no_digest_lines():
    empty = pd.DataFrame(columns=["home", "away", "our_home", "our_draw", "our_away"])
    assert F.day_summary_line(empty) is None
    assert F.firmest_predictions_block(empty) == []


def test_single_match_no_most_even_and_no_firmest_ranking():
    df = _df([_row("Netherlands", "Qatar", 0.84, 0.10, 0.06)])
    line = F.day_summary_line(df)
    assert "1 partido hoy" in line and "favorito más claro" in line
    assert "más parejo" not in line          # needs >=2 matches
    assert F.firmest_predictions_block(df) == []   # a 'top' needs a ranking (>=2)


def test_missing_probs_row_is_skipped_softfail():
    df = _df([_row("Netherlands", "Qatar", 0.84, 0.10, 0.06),
              {"home": "X", "away": "Y", "kickoff_utc": "2026-06-26 21:00",
               "round": "Group Stage - 3", "home_group": "Group A"}])  # no probs
    line = F.day_summary_line(df)
    assert line is not None and "2 partidos hoy" in line   # counts the fixture, skips its prob
    block = F.firmest_predictions_block(df)
    assert block == []   # only 1 usable prediction -> no ranking


if __name__ == "__main__":
    import traceback
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    failed = 0
    for fn in fns:
        try:
            fn(); print(f"  ok  {fn.__name__}")
        except Exception:
            failed += 1; print(f" FAIL {fn.__name__}"); traceback.print_exc()
    print(f"\n{len(fns) - failed}/{len(fns)} passed")
    sys.exit(1 if failed else 0)
