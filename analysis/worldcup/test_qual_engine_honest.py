"""
Tests for the HONEST qualification engine (qual_engine.analyze_team / phrase_es / short_tag). NO network,
NO API, NO files: the real World Cup tables are embedded as literals (points only) from the live
standings snapshot, so the real cases (Saudi Arabia, Cape Verde, Uruguay, Spain) are deterministic.

One test per category + the four real cases the operator demanded:
  qualified · eliminated · le_vale_empate · le_vale_empate_cond · gana_y_pasa · gana_y_pasa_cond ·
  debe_ganar · vivo_mejor_tercero · gd-dependent (diferencia de goles) · alive-as-third format dependence.

Run:  .\.venv\Scripts\python.exe analysis/worldcup/test_qual_engine_honest.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import qual_engine as Q  # noqa: E402


def _tbl(rows):
    """rows: [(key, pts)] -> {key: {'pts': pts}}."""
    return {k: {"pts": float(p)} for k, p in rows}


# ----------------------------------------------------------------- real World Cup tables (points only)
# embedded from the live standings snapshot standings_2026-06-25.json (12 groups, top-2 + 8 thirds).
REAL_GROUPS = {
    "A": [("Mexico", 9), ("South Africa", 4), ("South Korea", 3), ("Czechia", 1)],
    "B": [("Switzerland", 7), ("Canada", 4), ("Bosnia & Herzegovina", 4), ("Qatar", 1)],
    "C": [("Brazil", 7), ("Morocco", 7), ("Scotland", 3), ("Haiti", 0)],
    "D": [("USA", 6), ("Australia", 3), ("Paraguay", 3), ("Türkiye", 0)],
    "E": [("Germany", 6), ("Ivory Coast", 3), ("Ecuador", 1), ("Curaçao", 1)],
    "F": [("Netherlands", 4), ("Japan", 4), ("Sweden", 3), ("Tunisia", 0)],
    "G": [("Egypt", 4), ("Iran", 2), ("Belgium", 2), ("New Zealand", 1)],
    "H": [("Spain", 4), ("Uruguay", 2), ("Cape Verde Islands", 2), ("Saudi Arabia", 1)],
    "I": [("France", 6), ("Norway", 6), ("Senegal", 0), ("Iraq", 0)],
    "J": [("Argentina", 6), ("Austria", 3), ("Algeria", 3), ("Jordan", 0)],
    "K": [("Colombia", 6), ("Portugal", 4), ("Congo DR", 1), ("Uzbekistan", 0)],
    "L": [("England", 4), ("Ghana", 4), ("Croatia", 3), ("Panama", 0)],
}
REAL_TABLES = [_tbl(rows) for rows in REAL_GROUPS.values()]
N_GROUPS = 12   # 48-team format: top-2 + 8 best thirds


def _analyze_real(group_letter, match, team):
    return Q.analyze_team(_tbl(REAL_GROUPS[group_letter]), match, team, REAL_TABLES, N_GROUPS)


# ================================================================= category tests (constructed)
def test_cat_qualified():
    # A=7 leader; even losing it stays top-2 by points in every branch -> ya clasificado.
    g = _tbl([("A", 7), ("B", 0), ("C", 1), ("D", 1)])
    sc = Q.analyze_team(g, ("A", "B"), "A", [g], 8)
    assert sc["qualified"] is True and Q.short_tag(sc) == "qualified"
    assert Q.phrase_es(sc) == "ya clasificado"


def test_cat_eliminated():
    # no-thirds format (n_groups=8): T=0 cannot reach top-2 in any branch and no best-third exists.
    g = _tbl([("A", 7), ("B", 6), ("C", 7), ("T", 0)])
    sc = Q.analyze_team(g, ("T", "C"), "T", [g], 8)
    assert sc["eliminated"] is True and Q.short_tag(sc) == "eliminated"
    assert Q.phrase_es(sc) == "eliminado"


def test_cat_le_vale_empate_uncond():
    # A=4,B=4 face each other, C=1,D=1: a draw makes A & B top-2 by points in EVERY parallel result.
    g = _tbl([("A", 4), ("B", 4), ("C", 1), ("D", 1)])
    sc = Q.analyze_team(g, ("A", "B"), "A", [g], 8)
    assert Q.short_tag(sc) == "le_vale_empate"
    assert "le vale el empate" in Q.phrase_es(sc) and sc["qualified"] is False


def test_cat_le_vale_empate_cond():
    # Cape Verde (real): a draw GUARANTEES top-2 only if Spain wins (Uruguay loses); otherwise GD/third.
    sc = _analyze_real("H", ("Cape Verde Islands", "Saudi Arabia"), "Cape Verde Islands")
    assert Q.short_tag(sc) == "le_vale_empate_cond"
    ph = Q.phrase_es(sc)
    assert "le vale el empate" in ph and "Spain gana" in ph
    assert ph != "debe ganar"          # the legacy bug


def test_cat_gana_y_pasa():
    # Uruguay (real): winning secures 2nd by points; a draw only keeps it alive (GD / best third).
    sc = _analyze_real("H", ("Uruguay", "Spain"), "Uruguay")
    assert Q.short_tag(sc) == "gana_y_pasa"
    assert "gana y pasa 2ª" in Q.phrase_es(sc) and sc["qualified"] is False


def test_cat_gana_y_pasa_cond():
    # Saudi Arabia (real): can go through 2nd DIRECTLY if it wins and Uruguay does not win.
    sc = _analyze_real("H", ("Cape Verde Islands", "Saudi Arabia"), "Saudi Arabia")
    assert Q.short_tag(sc) == "gana_y_pasa_cond"
    ph = Q.phrase_es(sc)
    assert "gana y pasa 2ª si Uruguay no gana" in ph
    assert sc["second_direct_possible"] is True


def test_cat_debe_ganar():
    # no-thirds format: only winning reaches top-2; a draw or loss is dead in every branch.
    g = _tbl([("A", 4), ("B", 4), ("C", 1), ("T", 2)])
    sc = Q.analyze_team(g, ("T", "B"), "T", [g], 8)
    assert Q.short_tag(sc) == "debe_ganar"
    assert Q.phrase_es(sc) == "debe ganar"
    assert sc["own"]["D"]["verdict"] == "dead" and sc["own"]["L"]["verdict"] == "dead"


def test_cat_vivo_mejor_tercero():
    # thirds format, low team: never guarantees top-2 but is never dead -> best-third contention only.
    g = _tbl([("A", 6), ("B", 6), ("T", 1), ("C", 1)])
    sc = Q.analyze_team(g, ("T", "C"), "T", [g], 6)
    assert Q.short_tag(sc) == "vivo_mejor_tercero"
    assert "mejor tercero" in Q.phrase_es(sc)


def test_cat_gd_dependent_phrase():
    # Paraguay (real) vs Australia, both on 3: a draw leaves 2nd to be settled on goal difference.
    sc = _analyze_real("D", ("Paraguay", "Australia"), "Paraguay")
    assert "diferencia de goles" in Q.phrase_es(sc)
    assert sc["own"]["D"]["verdict"] == "alive_if"   # draw does NOT secure -> honest


# ================================================================= the four real headline cases
def test_real_spain_not_already_qualified():
    # Spain=4 is NOT mathematically qualified: losing while Cape Verde wins drops it to 3rd.
    sc = _analyze_real("H", ("Uruguay", "Spain"), "Spain")
    assert sc["qualified"] is False
    assert Q.short_tag(sc) == "le_vale_empate"
    ph = Q.phrase_es(sc)
    assert "le vale el empate" in ph and "perdiendo" in ph


def test_real_saudi_can_go_second_direct():
    sc = _analyze_real("H", ("Cape Verde Islands", "Saudi Arabia"), "Saudi Arabia")
    # the WIN branch reaches a DIRECT (points) 2nd place in >=1 parallel result
    assert sc["own"]["W"]["verdict"] in ("secures", "secures_if")
    assert sc["own"]["W"]["yes"]          # at least one guaranteed-top-2 parallel on a win


def test_real_cape_verde_draw_can_be_enough():
    sc = _analyze_real("H", ("Cape Verde Islands", "Saudi Arabia"), "Cape Verde Islands")
    assert sc["own"]["D"]["verdict"] == "secures_if"   # a draw IS enough in some parallel (not must-win)


def test_real_uruguay_must_win_to_secure():
    sc = _analyze_real("H", ("Uruguay", "Spain"), "Uruguay")
    assert sc["own"]["W"]["verdict"] == "secures"      # only a win guarantees 2nd by points
    assert sc["own"]["D"]["verdict"] == "alive_if"     # a draw does not


# ================================================================= structural / bound tests
def test_alive_as_third_bound_is_conservative():
    # a 3rd with 3 pts is 'alive' unless >=8 OTHER groups guarantee a better third (>=3 teams above 3).
    own = _tbl([("A", 6), ("B", 6), ("C", 3), ("D", 0)])
    # 8 groups each with 3 teams on 4 pts -> guaranteed-better thirds -> NOT alive
    strong = [_tbl([("x", 4), ("y", 4), ("z", 4), ("w", 0)]) for _ in range(8)]
    assert Q.alive_as_third(3, strong + [own], own, 8) is False
    # only 7 such groups -> still alive
    assert Q.alive_as_third(3, strong[:7] + [own], own, 8) is True


def test_format_dependence_thirds():
    # a clear 3rd: alive in a thirds format (6 groups) but eliminated in a no-thirds format (8 groups).
    g = _tbl([("A", 6), ("B", 6), ("C", 1), ("D", 1)])
    sc6 = Q.analyze_team(g, ("C", "D"), "C", [g], 6)
    sc8 = Q.analyze_team(g, ("C", "D"), "C", [g], 8)
    assert any(sc6["own"][r]["maybe"] for r in ("W", "D", "L"))   # best-third route exists with thirds
    assert sc8["eliminated"] is True                              # no thirds -> dead


def test_malformed_input_returns_none():
    g = _tbl([("A", 3), ("B", 3), ("C", 0)])           # not a 4-team group
    assert Q.analyze_team(g, ("A", "B"), "A", [g], 8) is None
    g4 = _tbl([("A", 3), ("B", 3), ("C", 0), ("D", 0)])
    assert Q.analyze_team(g4, ("A", "B"), "C", [g4], 8) is None   # team not in the named match


def _run():
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in fns:
        fn()
        print(f"  PASS {fn.__name__}")
    print(f"\n{len(fns)}/{len(fns)} honest-engine tests passed (no network, no API).")


if __name__ == "__main__":
    _run()
