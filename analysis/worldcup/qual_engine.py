"""
QUALIFICATION SCENARIO ENGINE (correct, FIFA tiebreakers) — pure Python, NO heavy imports, NO API.

Single source of truth for the per-team group scenario, used BOTH by the offline backtest
(scenario_feature_backtest) and LIVE as an INFORMATION line in the ficha (build_worldcup_cards).

Last matchday of a 4-team group: enumerate the 9 remaining-result combinations (the team's own match
W/D/L × the PARALLEL match W/D/L), compute final POINTS, and apply the real order (points -> goal
difference -> goals for -> head-to-head). Because GD/GF depend on UNKNOWN scorelines, a tie at the
qualification boundary is flagged 'gd_dependent' (it would be decided by GD/GF/h2h), NOT asserted.
Best thirds per format (6 groups -> top-2 + 4 thirds; 12 -> top-2 + 8; else top-2 only), conservative
cross-group bound using every group's current table.

classify_team(table, home_key, away_key, team_key, all_tables, n_groups) -> (features dict, label).
Tables are keyed by ANY hashable id (team_id or name); each value needs at least {"pts": float}.
This is INFORMATION, never the probabilistic prediction.
"""
from __future__ import annotations

THIRDS_BY_NGROUPS = {6: 4, 12: 8}   # best thirds advancing by group count (real formats; else top-2)
RES_PTS = {"W": (3, 0), "D": (1, 1), "L": (0, 3)}
FEATURES = ["qualified", "eliminated", "controls_destiny", "draw_enough", "must_win",
            "depends_on_others", "gd_dependent", "alive_as_third"]

# readable Spanish phrase per label (INFORMATION line)
LABEL_ES = {
    "qualified": "ya clasificado", "eliminated": "eliminado",
    "draw_enough": "le vale el empate", "must_win": "debe ganar",
    "alive_as_third": "vivo como mejor tercero", "depends_on_others": "depende de otros",
    "gd_dependent": "se juega la diferencia de goles", "decisive": "se lo juega todo",
    "unknown": "",
}


def _status_in_branch(pts, team):
    """By POINTS only, in this final-points config: 'in' (top-2 certain) / 'tie' (boundary tie,
    GD-dependent) / 'third' (alone 3rd) / 'third_tie' / 'out' (certain 4th)."""
    p = pts[team]
    above = sum(1 for t, q in pts.items() if t != team and q > p)
    equal = sum(1 for t, q in pts.items() if t != team and q == p)
    if above <= 1 and equal == 0:
        return "in"
    if above <= 1 and equal >= 1:
        return "tie"
    if above == 2 and equal == 0:
        return "third"
    if above == 2 and equal >= 1:
        return "third_tie"
    return "out"


def classify_team(table, home_key, away_key, team_key, all_tables, n_groups):
    """Scenario FEATURES + readable label for `team_key` at the last matchday of a 4-team group.
    table: this group's table {key: {"pts": float, ...}}. home_key/away_key: this match's two teams;
    the other two play the PARALLEL match. all_tables: every group's table (best-third bound).
    Returns ({feature: 0/1}, label). label 'unknown' if not a clean 4-team group."""
    keys = list(table.keys())
    others = [t for t in keys if t not in (home_key, away_key)]
    feat = {f: 0 for f in FEATURES}
    if len(table) != 4 or len(others) != 2 or team_key not in table:
        return feat, "unknown"
    X, Y = others
    base = {t: float(table[t]["pts"]) for t in keys}
    opp = away_key if team_key == home_key else home_key

    branches = []
    for own in ("W", "D", "L"):
        tp = 3 if own == "W" else (1 if own == "D" else 0)
        op = 0 if own == "W" else (1 if own == "D" else 3)
        for par in ("W", "D", "L"):
            px, py = RES_PTS[par]
            pts = dict(base)
            pts[team_key] += tp; pts[opp] += op; pts[X] += px; pts[Y] += py
            branches.append((own, par, pts))

    def st(own_filter):
        return [_status_in_branch(pts, team_key) for own, par, pts in branches if own in own_filter]

    win, draw, loss, allb = st({"W"}), st({"D"}), st({"L"}), st({"W", "D", "L"})
    in_certain = lambda lst: all(s == "in" for s in lst)

    feat["qualified"] = int(in_certain(allb))
    feat["draw_enough"] = int(bool(draw) and in_certain(draw) and not feat["qualified"])
    feat["must_win"] = int(bool(win) and in_certain(win) and not in_certain(draw) and not feat["qualified"])
    feat["controls_destiny"] = int(feat["qualified"] or feat["draw_enough"] or feat["must_win"])
    feat["depends_on_others"] = int(not feat["controls_destiny"] and any(s in ("in", "tie") for s in win))
    feat["gd_dependent"] = int(any(s in ("tie", "third_tie") for s in allb))

    can_third = any(s in ("third", "third_tie", "tie") for s in allb)
    n_thirds = THIRDS_BY_NGROUPS.get(n_groups, 0)
    alive_third = False
    if n_thirds > 0 and can_third:
        best_pts = base[team_key] + 3
        sure_better = 0
        for tb in all_tables:
            if tb is table:
                continue
            ordered = sorted(tb.values(), key=lambda r: -float(r["pts"]))
            if len(ordered) >= 3 and float(ordered[2]["pts"]) > best_pts:
                sure_better += 1
        alive_third = sure_better < n_thirds
    feat["alive_as_third"] = int(alive_third)
    feat["eliminated"] = int(not any(s in ("in", "tie") for s in allb) and not alive_third)

    if feat["qualified"]:
        lab = "qualified"
    elif feat["eliminated"]:
        lab = "eliminated"
    elif feat["draw_enough"]:
        lab = "draw_enough"
    elif feat["must_win"]:
        lab = "must_win"
    elif feat["alive_as_third"]:
        lab = "alive_as_third"
    elif feat["depends_on_others"]:
        lab = "depends_on_others"
    elif feat["gd_dependent"]:
        lab = "gd_dependent"
    else:
        lab = "decisive"
    return feat, lab
