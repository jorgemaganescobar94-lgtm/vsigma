"""
Offline tests for CLEAN_FORMAT (the redesigned Telegram per-match card). NO network, NO API.

Covers: headline "✅ Gana X — NN%" (group) / "Favorito … (a 90')" + "Avanza" (knockout) · natural-
language "💬 Por qué" WITHOUT jargon (no 'xG'/'rating') · labelled+spaced sections (Goles/Jugadores/
Córners-tiros/Contexto) with ALL metrics present · honesty+attribution note ONCE at the end · the
number is EXACTLY pred_1x2 (unchanged) · reversibility (CLEAN_FORMAT=False -> classic "Resultado:").
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_worldcup_full_card as F  # noqa: E402
import worldcup_explain as WE  # noqa: E402


def _group_row(fid=-101, **kw):
    base = {"fixture_id": fid, "home": "England", "away": "Congo DR", "round": "Group Stage - 3",
            "home_group": "Group A", "kickoff_utc": "2026-06-25 18:00",
            "our_elo_home": 1.30, "our_elo_away": 0.47,
            "fd_home": 0.671, "fd_draw": 0.202, "fd_away": 0.127, "fd_xg_home": 1.9, "fd_xg_away": 0.8,
            "st_corners_home": 6.0, "st_corners_away": 3.0, "st_shots_home": 14.0, "st_shots_away": 7.0,
            "group_info": "Inglaterra pasa como 1ª si gana o empata"}
    base.update(kw)
    return pd.Series(base)


def _ko_row(**kw):
    base = {"fixture_id": -102, "home": "Spain", "away": "France", "round": "Semi-finals",
            "kickoff_utc": "2026-07-08 19:00", "our_elo_home": 1.6, "our_elo_away": 1.45,
            "fd_home": 0.44, "fd_draw": 0.30, "fd_away": 0.26, "fd_xg_home": 1.5, "fd_xg_away": 1.2}
    base.update(kw)
    return pd.Series(base)


def _props():
    F._props_cache = pd.DataFrame([
        {"fixture_id": -101, "player": "H. Kane", "p_goal": 0.38, "p_assist": 0.14, "p_card": 0.08,
         "exp_shots": 3.6, "is_xi": 1, "basis": "probable_xi"}])


def test_clean_group_all_sections_and_headline():
    _props()
    F.CLEAN_FORMAT = True
    r = _group_row()
    lines = F.match_block(r)
    txt = "\n".join(lines)
    # headline: favourite + pct, with the runners-up underneath
    assert "✅ Gana Inglaterra — 67%" in txt
    assert "empate 20%" in txt and "RD Congo 13%" in txt
    # every content section present with its label
    assert "💬 Por qué:" in txt
    assert "⚽ Goles: esperados 1.9–0.8" in txt and "Over 2.5" in txt and "BTTS" in txt
    assert "Marcador más probable:" in txt
    assert "👥 Jugadores" in txt and "se confirma ~1h antes" in txt
    assert "Gol: H. Kane 38%" in txt
    assert "📈 Córners/tiros —" in txt and "confianza:" in txt
    assert "📋 Contexto de grupo (información, no es la predicción):" in txt
    # honesty + attribution ONCE at the end
    assert txt.count("Modelo propio de selecciones (sin cuotas)") == 1
    assert "Atribución:" in txt and txt.rstrip().endswith("decisión de usar todo el dato)")


def test_clean_number_equals_pred_1x2_unchanged():
    F.CLEAN_FORMAT = True
    r = _group_row()
    lh, ld, la, *_ = F.pred_1x2(r)
    assert (round(lh, 3), round(ld, 3), round(la, 3)) == (0.671, 0.202, 0.127)
    txt = "\n".join(F.match_block(r))
    assert f"{lh*100:.0f}%" == "67%" and "✅ Gana Inglaterra — 67%" in txt


def test_clean_knockout_advance_and_chip():
    F.CLEAN_FORMAT = True
    txt = "\n".join(F.match_block(_ko_row()))
    assert "Semifinal" in txt.splitlines()[0]          # round chip, not a group
    assert "(a 90')" in txt and "empate→prórroga" in txt
    assert "🏅 Avanza:" in txt and "moneda al aire" in txt
    # P(advance) = win90 + draw*0.5 : Spain .44+.15=.59 ; France .26+.15=.41
    assert "España 59%" in txt and "Francia 41%" in txt


def test_clean_why_is_plain_language_no_jargon():
    # the clean "por qué" must NOT contain jargon tokens (xG / rating); it explains strength in words
    why = WE.explain_l3_clean("England", "Congo DR", 1.30, 0.47, neutral=1)
    assert "xG" not in why and "rating" not in why.lower()
    assert "plantilla histórica es más fuerte" in why and "campo neutral" in why


def test_honesty_note_not_repeated_per_line():
    F.CLEAN_FORMAT = True
    lines = F.match_block(_group_row())
    # the long "nunca certezas" honesty phrase appears on exactly one line
    assert sum(1 for ln in lines if "nunca certezas" in ln) == 1


def test_reversible_flag_off_is_classic_format():
    r = _group_row()
    try:
        F.CLEAN_FORMAT = False
        classic = "\n".join(F.match_block(r))
    finally:
        F.CLEAN_FORMAT = True
    # classic layout uses "Resultado:" and has no clean headline/footer
    assert "Resultado:" in classic and "✅ Gana" not in classic
    # SAME number in both formats (presentation only)
    assert "Inglaterra 67%" in classic
