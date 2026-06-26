"""
QUALIFICATION SCENARIO ENGINE — pure Python, NO heavy imports, NO API, NO betting endpoints.

Single source of truth for the per-team group scenario at the LAST matchday of a 4-team group.

TWO layers live here:

  (1) HONEST ENGINE (the reconstruction, the part to trust): `analyze_team()` enumerates the 9 branches
      (own W/D/L × the PARALLEL match W/D/L), computes the final points of all 4 teams, applies the FIFA
      order (points -> goal difference -> goals for -> head-to-head), and returns a CONDITIONAL scenario
      that NEVER collapses a team to one label. It separates, per own-result, the parallel results that
      qualify FOR CERTAIN (top-2 by points), that are gd/best-third DEPENDENT (maybe), and that FAIL (no).
      `phrase_es()` turns that into an honest, conditional Spanish sentence. This is the engine the
      validation and tests exercise; phase 2 will wire it into the ficha.

  (2) LEGACY shim (kept verbatim, DO NOT trust its single label): `classify_team()` + `LABEL_ES` +
      `FEATURES`. The live ficha (build_worldcup_cards.compute_group_info) still calls it. It collapses
      each team to ONE tag and is exactly the thing being replaced (it mislabels e.g. a team that can go
      through 2nd directly as merely "alive as third", and overstates a 4-pt leader as "qualified"). Left
      UNTOUCHED so production behavior does not change in this read-only phase; rewire it in phase 2.

KEY HONESTY RULE (the bug being fixed): a team is qualified FOR CERTAIN in a branch ONLY when it is top-2
by POINTS (GD-independent). A points tie at the boundary (GD decides 2nd vs 3rd) and a best-third spot
(cross-group cutoff unknown) are MAYBE, never asserted as certain — but that uncertainty is NEVER allowed
to HIDE a clear path (winning while a rival loses gives 2nd by points, no GD needed). Best thirds are
bounded conservatively across every group's current table (documented; errs toward 'still alive', never
falsely eliminates). This is INFORMATION, never the probabilistic prediction.
"""
from __future__ import annotations

THIRDS_BY_NGROUPS = {6: 4, 12: 8}   # best thirds advancing by group count (real formats; else top-2 only)
RES_PTS = {"W": (3, 0), "D": (1, 1), "L": (0, 3)}   # (points for the row team, points for its opponent)

# ============================================================================================
# (1) HONEST ENGINE — the reconstruction
# ============================================================================================


def _placement(fp, team):
    """Placement of `team` by POINTS ONLY in a final-points config `fp` (4 teams), top-2 advance:
      'direct'         -> CERTAINLY top-2, GD-independent (at most 1 other team at-or-above on points)
      'boundary2'      -> tied at the top-2 boundary: 2nd OR 3rd decided by GD (could grab a direct spot)
      'third'          -> alone in 3rd (exactly 2 strictly above): only a best-third spot can save it
      'third_boundary' -> tied for 3rd/4th: a best-third spot is possible only if it wins the GD tie
      'last'           -> certainly 4th (3 strictly above): out of this group no matter the GD."""
    p = fp[team]
    above = sum(1 for u, q in fp.items() if u != team and q > p)
    equal = sum(1 for u, q in fp.items() if u != team and q == p)
    if above + equal <= 1:
        return "direct"
    if above <= 1:
        return "boundary2"
    if above == 2:
        return "third" if equal == 0 else "third_boundary"
    return "last"


def alive_as_third(third_pts, all_tables, own_table, n_thirds):
    """CONSERVATIVE, DOCUMENTED cross-group bound: could a team finishing 3rd with `third_pts` points be
    among the `n_thirds` qualifying best thirds? It is declared 'alive' UNLESS at least `n_thirds` OTHER
    groups are GUARANTEED to produce a 3rd-place team strictly better. A group is a guaranteed-better
    third only if >=3 of its teams ALREADY have > third_pts points (then its eventual 3rd place finishes
    > third_pts no matter the remaining results, since those 3 only gain points). This NEVER falsely
    eliminates a team (it errs toward 'still alive'); the exact best-third cutoff needs every group final,
    which we do not assume."""
    if n_thirds <= 0:
        return False
    sure_better = 0
    for tb in all_tables:
        if tb is own_table:
            continue
        if sum(1 for r in tb.values() if float(r["pts"]) > third_pts) >= 3:
            sure_better += 1
    return sure_better < n_thirds


def _tri(place, alive):
    """Qualifies in this branch?  'YES' = CERTAIN (top-2 by points, GD-independent) · 'MAYBE' = depends
    on GD (boundary tie for 2nd) or on the best-third cutoff · 'NO' = out. A best-third spot is NEVER
    'YES' (the cutoff is unknown); only a points top-2 is certain."""
    if place == "direct":
        return "YES"
    if place == "boundary2":
        return "MAYBE"                                  # 2nd-or-3rd decided by GD
    if place in ("third", "third_boundary"):
        return "MAYBE" if alive else "NO"               # best-third contention only
    return "NO"                                         # 'last'


def _route(place):
    """How qualification would happen in a branch (for honest phrasing)."""
    return {"direct": "second_sure", "boundary2": "second_gd",
            "third": "third", "third_boundary": "third_gd"}.get(place, "out")


# parallel-result phrasing. `par` is read from P1's perspective: 'W'=P1 beats P2, 'L'=P2 beats P1, 'D'=draw.
def _describe_parallel(qual_set, p1, p2):
    """Spanish condition on the PARALLEL match (P1 vs P2) for the set of parallel results in `qual_set`.
    None when the set is empty (never) or full (always -> unconditional)."""
    s = frozenset(qual_set)
    if not s or s == frozenset({"W", "D", "L"}):
        return None
    return {
        frozenset({"D", "L"}): f"si {p1} no gana",
        frozenset({"W", "D"}): f"si {p2} no gana",
        frozenset({"L"}): f"si {p1} pierde",
        frozenset({"W"}): f"si {p1} gana",
        frozenset({"D"}): f"si {p1} y {p2} empatan",
        frozenset({"W", "L"}): f"si {p1} y {p2} no empatan",
    }.get(s, "")


def analyze_team(table, match, team, all_tables, n_groups):
    """HONEST conditional scenario for `team` at the last matchday of a 4-team group.

      table:      {key: {"pts": float}} for the 4 teams of THIS group (key = team_id or name).
      match:      (a, b) the two teams playing TEAM's own match (team must be a or b); the OTHER two
                  teams play the PARALLEL match.
      team:       the key to analyze.
      all_tables: list of every group's table {key: {"pts": float}} (for the best-third bound).
      n_groups:   number of groups (12 -> top-2 + 8 thirds; 6 -> top-2 + 4; else top-2 only).

    Returns a scenario dict (or None on a malformed 4-team last-matchday input). Per own-result it gives
    the parallel results that qualify FOR CERTAIN (`yes`), that are gd/best-third DEPENDENT (`maybe`), and
    that FAIL (`no`), plus a `verdict` in {secures, secures_if, alive_if, dead} and a parallel `cond`."""
    keys = list(table.keys())
    if len(table) != 4 or team not in table or team not in match:
        return None
    a, b = match
    if a not in table or b not in table or a == b:
        return None
    others = [k for k in keys if k not in (a, b)]
    if len(others) != 2:
        return None
    p1, p2 = others
    opp = b if team == a else a
    base = {k: float(table[k]["pts"]) for k in keys}
    n_thirds = THIRDS_BY_NGROUPS.get(n_groups, 0)

    own = {}
    second_direct_possible = False
    for own_res in ("W", "D", "L"):
        tp, op = RES_PTS[own_res]
        yes, maybe, no = set(), set(), set()
        routes = {}
        for par in ("W", "D", "L"):
            pp1, pp2 = RES_PTS[par]
            fp = dict(base)
            fp[team] += tp
            fp[opp] += op
            fp[p1] += pp1
            fp[p2] += pp2
            place = _placement(fp, team)
            if place in ("direct", "boundary2"):
                second_direct_possible = True
            alive = alive_as_third(fp[team], all_tables, table, n_thirds)
            tri = _tri(place, alive)
            routes[par] = _route(place)
            (yes if tri == "YES" else maybe if tri == "MAYBE" else no).add(par)

        if len(yes) == 3:
            verdict = "secures"
        elif yes:
            verdict = "secures_if"
        elif maybe:
            verdict = "alive_if"
        else:
            verdict = "dead"
        qual_set = yes | maybe
        own[own_res] = {
            "yes": yes, "maybe": maybe, "no": no, "verdict": verdict, "routes": routes,
            "cond_sure": _describe_parallel(yes, p1, p2),    # parallels where top-2 is GUARANTEED
            "cond_any": _describe_parallel(qual_set, p1, p2),  # parallels where it qualifies at all
        }

    qualified = all(own[r]["verdict"] == "secures" for r in ("W", "D", "L"))
    eliminated = all(own[r]["verdict"] == "dead" for r in ("W", "D", "L"))
    return {
        "team": team, "opp": opp, "parallel": (p1, p2), "n_thirds": n_thirds,
        "qualified": qualified, "eliminated": eliminated,
        "second_direct_possible": second_direct_possible, "own": own,
    }


# ------------------------------------------------------------------ phrasing
def _clean(s):
    """Collapse whitespace and tidy stray spaces before punctuation."""
    return " ".join(s.split()).replace(" )", ")").replace("( ", "(").strip()


def _maybe_route_txt(info):
    """Describe the contingent route(s) of the MAYBE branches: best-third and/or GD for 2nd."""
    rs = {info["routes"][p] for p in info["maybe"]}
    gd = "second_gd" in rs
    third = "third" in rs or "third_gd" in rs
    if gd and third:
        return "se jugaría la 2ª por diferencia de goles (o pasaría como mejor tercero)"
    if gd:
        return "se jugaría la 2ª por diferencia de goles"
    return "seguiría vivo como mejor tercero"


def _own_clause(own_res, info):
    """Honest clause for ONE own-result. 'le vale el empate' / 'gana y pasa' phrasing, with the explicit
    parallel condition and GD/best-third nuance. None if the result is dead."""
    v = info["verdict"]
    if v == "dead":
        return None
    head = {"W": "gana", "D": "le vale el empate", "L": "pierde"}[own_res]
    if v == "secures":
        if own_res == "D":
            return "le vale el empate"
        if own_res == "W":
            return "gana y pasa 2ª"
        return "incluso perdiendo está clasificado"
    if v == "secures_if":
        cond = info["cond_sure"] or ""
        extra = f" (en otro caso, {_maybe_route_txt(info)})" if info["maybe"] else ""
        stem = {"D": "le vale el empate", "W": "gana y pasa 2ª", "L": "perdiendo aún pasa"}[own_res]
        return _clean(f"{stem} {cond}{extra}")
    # alive_if -> only a contingent route (best-third / GD), never a guaranteed top-2
    cond = info["cond_any"] or ""
    route = _maybe_route_txt(info)
    verb = {"W": "ganando", "D": "con el empate", "L": "perdiendo"}[own_res]
    return _clean(f"{verb} {route} {cond}")


def phrase_es(scenario):
    """Honest, conditional Spanish sentence for a scenario from `analyze_team` (or '' if None)."""
    if scenario is None:
        return ""
    if scenario["qualified"]:
        return "ya clasificado"
    if scenario["eliminated"]:
        return "eliminado"
    own = scenario["own"]
    w, d, l = own["W"], own["D"], own["L"]

    # 'debe ganar' EXACT (per spec): only WINNING can qualify in ANY branch; draw AND loss are dead.
    if w["verdict"] != "dead" and d["verdict"] == "dead" and l["verdict"] == "dead":
        if w["verdict"] == "alive_if":
            return _clean(f"debe ganar (y aun así {_maybe_route_txt(w)} {w['cond_any'] or ''})")
        if w["verdict"] == "secures_if":
            return _clean(f"debe ganar {w['cond_sure'] or ''}")
        return "debe ganar"   # secures: winning guarantees top-2

    # otherwise compose surviving clauses: draw first (most decision-relevant), then win, then loss.
    clauses = [_own_clause("D", d) if d["verdict"] != "dead" else None]
    # winning clause adds info unless the draw already secures it unconditionally
    if w["verdict"] != "dead" and d["verdict"] != "secures":
        clauses.append(_own_clause("W", w))
    if l["verdict"] != "dead":
        clauses.append(_own_clause("L", l))
    seen, uniq = set(), []
    for c in clauses:
        if c and c not in seen:
            seen.add(c)
            uniq.append(c)
    return "; ".join(uniq) if uniq else "depende de otros resultados"


def short_tag(scenario):
    """Coarse category tag for audit tables / tests (the honest phrase is `phrase_es`):
      qualified · eliminated · le_vale_empate · le_vale_empate_cond · gana_y_pasa · gana_y_pasa_cond ·
      debe_ganar · vivo_mejor_tercero · depende."""
    if scenario is None:
        return "unknown"
    if scenario["qualified"]:
        return "qualified"
    if scenario["eliminated"]:
        return "eliminated"
    own = scenario["own"]
    w, d, l = own["W"], own["D"], own["L"]
    if d["verdict"] == "secures":
        return "le_vale_empate"
    if d["verdict"] == "secures_if":
        return "le_vale_empate_cond"
    # draw never guarantees top-2 from here on (verdict is alive_if or dead)
    if w["verdict"] != "dead" and d["verdict"] == "dead" and l["verdict"] == "dead":
        return "debe_ganar"
    if w["verdict"] == "secures":
        return "gana_y_pasa"
    if w["verdict"] == "secures_if":
        return "gana_y_pasa_cond"
    # no result guarantees top-2 anywhere, but it is not eliminated -> best-third contention
    if any(own[r]["maybe"] for r in ("W", "D", "L")):
        return "vivo_mejor_tercero"
    return "depende"


# ============================================================================================
# (2) LEGACY shim — kept verbatim for the live ficha (build_worldcup_cards.compute_group_info).
#     DO NOT trust its single collapsed label; it is the thing being replaced. Phase 2 removes it.
# ============================================================================================

FEATURES = ["qualified", "eliminated", "controls_destiny", "draw_enough", "must_win",
            "depends_on_others", "gd_dependent", "alive_as_third"]

# readable Spanish phrase per legacy label (INFORMATION line)
LABEL_ES = {
    "qualified": "ya clasificado", "eliminated": "eliminado",
    "draw_enough": "le vale el empate", "must_win": "debe ganar",
    "alive_as_third": "vivo como mejor tercero", "depends_on_others": "depende de otros",
    "gd_dependent": "se juega la diferencia de goles", "decisive": "se lo juega todo",
    "unknown": "",
}


def _status_in_branch(pts, team):
    """LEGACY. By POINTS only: 'in'/'tie'/'third'/'third_tie'/'out'."""
    p = pts[team]
    above = sum(1 for t, q in pts.items() if t != team and q > p)
    equal = sum(1 for t, q in pts.items() if t != team and q == p)
    if above + equal <= 1:
        return "in"
    if above <= 1:
        return "tie"
    if above == 2:
        return "third" if equal == 0 else "third_tie"
    return "out"


def classify_team(table, home_key, away_key, team_key, all_tables, n_groups):
    """LEGACY single-label classifier (collapses conditionality). Kept for the live ficha ONLY.
    Prefer `analyze_team` + `phrase_es`."""
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
