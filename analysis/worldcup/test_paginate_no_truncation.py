"""
Offline tests for the Telegram pagination of build_worldcup_full_card.render_paginated and for the
CONCISE group-context render (qual_engine.phrase_es_short). NO API, NO network.

FIX 1 — a match block is NEVER truncated: blocks are packed COMPLETE by a line budget (max_lines),
        so the last match of every message keeps ALL its lines (props + nota), and no message body
        exceeds the dispatcher budget.
FIX 2 — phrase_es_short leads with the team's primary need + key condition and summarises the
        contingent route ONCE (shorter than the full honest phrase_es, conditionality preserved).

Run:  python -m pytest analysis/worldcup/test_paginate_no_truncation.py -q
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build_worldcup_full_card as F  # noqa: E402
import qual_engine as Q  # noqa: E402


# A long, honest group-context line (the kind FIX 2 shortens upstream — here we just need a block
# that occupies several lines so the packer is exercised).
LONG_GI = ("Croacia le vale el empate si Ghana no gana · "
           "Ghana gana y pasa 2ª si Croacia pierde")


def _row(home, away, group="Group F", gi=LONG_GI, fid=-1, **kw):
    """A deliberately LONG group block: 1X2 + heuristic adjust (+motivo) + group-context + goals +
    top scores + per-team stats. fixture_id<0 -> never matches the shadow props log (deterministic)."""
    base = {
        "fixture_id": fid, "home": home, "away": away,
        "kickoff_utc": "2026-06-27 20:00", "round": "Group Stage - 3",
        "home_group": group, "away_group": group,
        "our_home": 0.46, "our_draw": 0.28, "our_away": 0.26,
        "our_xg_home": 1.6, "our_xg_away": 1.2,
        "our_elo_home": 1800, "our_elo_away": 1750,
        # heuristic L3 adjust -> extra 2 lines (↳ Ajuste + ⚠️ motivo)
        "adj_home": 0.50, "adj_draw": 0.27, "adj_away": 0.23,
        "adj_absent_home": "Modric", "adj_absent_away": "",
        "adj_basis": "lineups", "adj_delta_home": 0.04, "adj_delta_away": -0.03,
        # per-team stats -> "Por equipo" line
        "st_corners_home": 5, "st_corners_away": 4,
        "st_shots_home": 12, "st_shots_away": 10,
        "group_info": gi,
    }
    base.update(kw)
    return base


SLATE = pd.DataFrame([
    _row("Croatia", "Ghana", group="Group F", fid=-1),
    _row("Panama", "England", group="Group F", fid=-2),
    _row("Colombia", "Portugal", group="Group G", fid=-3),
    _row("Congo DR", "Uzbekistan", group="Group G", fid=-4),
])


def _read_messages():
    """Read the paginated message bodies back from the manifest the workflow consumes."""
    man = F.MANIFEST.read_text(encoding="utf-8").strip().splitlines()
    msgs = []
    for ln in man:
        if not ln.strip():
            continue
        path, title = ln.split("|", 1)
        body = Path(path).read_text(encoding="utf-8").splitlines()
        msgs.append((title, body))
    return msgs


def _is_contiguous_sub(block, body):
    """True if `block` (list of lines) appears as a CONTIGUOUS run inside `body` (i.e. intact)."""
    n, m = len(block), len(body)
    return any(body[i:i + n] == block for i in range(0, m - n + 1))


def test_no_match_block_is_ever_truncated():
    max_lines = 24   # real dispatcher budget: 1 clean block fits, 2 don't -> exercises the packer
    F.render_paginated(SLATE, "2026-06-27", None, None, False, None,
                       show_lineups=False, per_page=2, max_lines=max_lines)
    msgs = _read_messages()
    # every match block appears WHOLE (props/nota/last line intact) in exactly one message body
    for _, r in SLATE.iterrows():
        block = F.match_block(r, show_lineups=False)
        hits = sum(1 for _t, body in msgs if _is_contiguous_sub(block, body))
        assert hits == 1, f"block for {r['home']} vs {r['away']} not intact (hits={hits})"
    # no message body exceeds the dispatcher budget
    for title, body in msgs:
        assert len(body) <= max_lines, f"message '{title}' has {len(body)} > {max_lines} lines"


def test_each_block_alone_fits_the_budget():
    """A single match block must fit the real budget (max_lines=24, dispatcher cuts at 25) so a lone
    block's own message is never cut by the dispatcher."""
    for _, r in SLATE.iterrows():
        block = F.match_block(r, show_lineups=True)
        assert len(block) <= 24, f"block too long ({len(block)}): {r['home']} vs {r['away']}"


def test_last_block_keeps_its_final_line():
    """Direct regression on the reported bug: the LAST match of each message keeps its final line
    (previously cut after 'Asistencia')."""
    F.render_paginated(SLATE, "2026-06-27", None, None, False, None,
                       show_lineups=False, per_page=2, max_lines=12)
    msgs = _read_messages()
    page_msgs = [(t, b) for t, b in msgs if "partidos" in t]
    assert page_msgs, "expected at least one match-page message"
    for _, r in SLATE.iterrows():
        block = F.match_block(r, show_lineups=False)
        last = block[-1]
        # the block's final line is present AND immediately preceded by its penultimate line
        # in some message (i.e. the tail was not chopped)
        assert any(_is_contiguous_sub(block[-2:], b) for _t, b in page_msgs), \
            f"tail of {r['home']} vs {r['away']} block missing"


# ----------------------------------------------------------------- FIX 2: concise context render
def _real_h_scenarios():
    def tbl(rows):
        return {n: {"pts": float(p), "played": pl, "gd": gd, "gf": 0, "name": n}
                for n, p, pl, gd in rows}
    gh = tbl([("Spain", 4, 2, 4), ("Uruguay", 2, 2, 0),
              ("Cape Verde Islands", 2, 2, 0), ("Saudi Arabia", 1, 2, -4)])
    allt = [gh] + [tbl([(f"{i}a", 0, 2, 0), (f"{i}b", 0, 2, 0),
                        (f"{i}c", 0, 2, 0), (f"{i}d", 0, 2, 0)]) for i in range(11)]
    cv = Q.analyze_team(gh, ("Cape Verde Islands", "Saudi Arabia"), "Cape Verde Islands", allt, 12)
    sa = Q.analyze_team(gh, ("Cape Verde Islands", "Saudi Arabia"), "Saudi Arabia", allt, 12)
    return cv, sa


def test_phrase_es_short_is_concise_and_conditional():
    cv, sa = _real_h_scenarios()
    s_cv, s_sa = Q.phrase_es_short(cv), Q.phrase_es_short(sa)
    # leads with the primary need + the key condition (the honest conditionality is kept)
    assert s_cv == "le vale el empate si Spain gana"
    assert s_sa == "gana y pasa 2ª si Uruguay no gana"
    # and is SHORTER than the full honest phrase (no per-branch route repetition)
    assert len(s_cv) < len(Q.phrase_es(cv))
    assert len(s_sa) < len(Q.phrase_es(sa))
    # no " · " inside a single team's phrase (compute_group_info joins teams with ' · ')
    assert " · " not in s_cv and " · " not in s_sa


def test_por_equipo_shows_per_stat_confidence():
    """The 'Por equipo' line tags confidence PER STAT (tiros media / córners baja), not one global
    label. Reads the committed calibration via build_worldcup_full_card.STAT_CONF."""
    # legend helper, most-confident first
    legend = F._conf_legend(["shots", "corners"])
    assert "tiros: conf media" in legend
    assert "córners: baja conf" in legend
    assert legend.index("tiros") < legend.index("córners"), "media stat listed before baja"
    # and it actually renders in a real block (Croatia row carries st_corners/st_shots)
    r = SLATE.iloc[0]
    block = F.match_block(r, show_lineups=False)
    pe = [ln for ln in block if "Córners/tiros —" in ln]   # CLEAN_FORMAT per-team stats line
    assert pe, "expected a 'Córners/tiros' line"
    assert "tiros: conf media" in pe[0] and "córners: baja conf" in pe[0]
    assert "BAJA CONF" not in pe[0], "no stale single global label"


if __name__ == "__main__":
    test_no_match_block_is_ever_truncated()
    test_each_block_alone_fits_the_budget()
    test_last_block_keeps_its_final_line()
    test_phrase_es_short_is_concise_and_conditional()
    print("OK")
