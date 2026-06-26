"""
WORLD CUP 2026 - per-match forecast cards (ISOLATED, analysis/worldcup/ only).

PURIFIED: the card shows ONLY our own Layer-3 model — real data, ZERO market/odds.
NOT production. Production's league allowlist (scripts/filter_leagues.py) REJECTS the
World Cup (no ('world','world cup') entry -> 'country_league_not_allowlisted'), so this
is a standalone shadow product. No .env edits, no git, BOUNDED API.

Per upcoming fixture builds a card combining, each with its SOURCE marked:
  * [OUR MODEL] Layer-3 rating -> 1X2, xG, goals (via worldcup_our_model_predictions.csv
    or the offline l3_offline predictor for new knockout fixtures). NO odds, NO market.
  * [OUR MODEL] stats -> corners/cards/shots from the opponent-adjusted DATA model
    (stats_model.py, real stats only, LOW confidence per OOS validation). NO odds.
  * [STANDINGS] group context from /standings (rank, points, played, form) — context.
  * [LINEUPS/INJURIES] near kickoff (~4h) from /fixtures/lineups + /injuries — context.

API budget: 1 /fixtures (cached) + 1 /standings + (near KO only) lineups/injuries.
NO /odds call. NO /predictions call.
"""
from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from api_football_client import APIFootballClient, APIFootballError  # noqa: E402

OUT_DIR = Path(__file__).resolve().parent
WC_LEAGUE = 1
WC_SEASON = 2026

# 🔴 EN VIVO: ajustar la predicción 1X2/OU MOSTRADA Y ENVIADA por el contexto de grupo
# (worldcup_context_shadow: classify_fixture + MULT + recompute Poisson con calibración congelada).
# Solo afecta a grupos con escenario NO trivial; knockout/unknown/tercero/intrascendente = 1.0 (sin
# cambio). Se guarda en columnas ctx_* (NO se toca our_* = L3 puro -> el aprendizaje del L3 queda
# intacto); la ficha muestra ctx_* cuando existen. CONTEXT_LIVE=False -> rollback instantáneo a L3
# puro (no se escriben columnas ctx_*). El A/B de sombra sigue corriendo aparte como panel de control.
CONTEXT_LIVE = True
# nota del MULTIPLICADOR (solo aparecen los escenarios que ajustan, mult != 1.0). short_tag honesto.
SCENARIO_ES = {"qualified": "ya clasificado", "eliminated": "eliminado",
               "debe_ganar": "debe ganar", "le_vale_empate": "le vale el empate"}


def lineup_status(x):
    """(code, formation) from a lineup dict. code in conf|prob|pend."""
    if not x:
        return "pend", ""
    if x.get("confirmed"):
        return "conf", (x.get("formation") or "")
    return "prob", (x.get("formation") or "")


def fetch_lineups(c, fid):
    """Fresh /fixtures/lineups for an imminent fixture. {team_name: {confirmed,formation,n}}."""
    try:
        r = c.request("/fixtures/lineups", {"fixture": fid}, ttl_hours=0.25,
                      force_refresh=True).get("response", []) or []
    except APIFootballError:
        return {}
    out = {}
    for t in r:
        nm = (t.get("team") or {}).get("name")
        xi = t.get("startXI") or []
        if nm:
            # keep the count (existing behaviour) AND add the startXI player names (for L3-adj)
            xi_names = [((p.get("player") or {}).get("name")) for p in xi]
            out[nm] = {"confirmed": len(xi) >= 11, "formation": t.get("formation"), "n": len(xi),
                       "xi_names": [n for n in xi_names if n]}
    return out


def fetch_injuries(c, fid):
    """/injuries for a fixture (cached 12h). {team_name: [(player, reason), ...]}."""
    try:
        r = c.injuries(fixture=fid).get("response", []) or []
    except APIFootballError:
        return {}
    by = {}
    for it in r:
        tn = (it.get("team") or {}).get("name")
        pl = it.get("player") or {}
        nm = pl.get("name")
        reason = pl.get("reason") or pl.get("type") or ""
        if tn and nm:
            by.setdefault(tn, []).append((nm, reason))
    return by


def compute_context_adjustment(ctxmod, l3pred, ctx_groups, ctx_team_group, rnd, home, away, om):
    """LIVE qualification-context adjustment for ONE fixture, REUSING the shadow module
    (classify_fixture + adjust_prediction). Scales the displayed L3 xG by the per-team scenario
    multiplier and recomputes 1X2/OU with the frozen calibration. Returns a dict of ctx_* fields
    (incl. 'context_note') when the scenario is NON-trivial; None when trivial/knockout/no-rating or
    on ANY error (soft-fail -> caller keeps pure L3). 'our_*' is never touched."""
    if ctxmod is None or om is None or l3pred is None:
        return None
    try:
        sc_h, sc_a, m_h, m_a, nt = ctxmod.classify_fixture(rnd, home, away, ctx_groups, ctx_team_group)
        if not nt:
            return None
        adj = ctxmod.adjust_prediction(l3pred, om["our_xg_home"], om["our_xg_away"], m_h, m_a)
        parts = []
        if m_h != 1.0:
            parts.append(f"{home} {SCENARIO_ES.get(sc_h, sc_h)}")
        if m_a != 1.0:
            parts.append(f"{away} {SCENARIO_ES.get(sc_a, sc_a)}")
        note = "ajustado por contexto de grupo: " + ", ".join(parts)
        return {"ctx_home": round(adj["home"], 4), "ctx_draw": round(adj["draw"], 4),
                "ctx_away": round(adj["away"], 4),
                "ctx_xg_home": round(adj["xg_home"], 2), "ctx_xg_away": round(adj["xg_away"], 2),
                "ctx_over25": round(adj["over25"], 4),
                "ctx_scenario_home": sc_h, "ctx_scenario_away": sc_a,
                "ctx_mult_home": m_h, "ctx_mult_away": m_a, "context_note": note}
    except Exception as e:  # noqa: BLE001  (soft-fail -> L3 puro)
        print(f"context live soft-fail (-> L3 puro): {type(e).__name__}")
        return None


def compute_group_info(ctx_groups, home, away):
    """INFORMATION line (NOT the prediction) from the HONEST qualification engine (qual_engine:
    analyze_team + phrase_es — FIFA tiebreakers, best thirds, CONDICIONAL). Returns a readable string
    for a LAST-MATCHDAY 4-team group with both teams (e.g. 'Arabia gana y pasa 2ª si Uruguay no gana'),
    else None. Soft-fail -> None. Independent of CONTEXT_LIVE (it is information). Single engine: this is
    the SAME analyze_team the multiplier path uses."""
    try:
        import qual_engine  # noqa: E402  (lightweight, pure-Python; no API)
        gh = next((g for g, rows in ctx_groups.items() if any(r.get("name") == home for r in rows)), None)
        ga = next((g for g, rows in ctx_groups.items() if any(r.get("name") == away for r in rows)), None)
        if gh is None or gh != ga:
            return None
        rows = ctx_groups[gh]
        if len(rows) != 4 or any(int(r.get("played", 0)) != 2 for r in rows):
            return None                          # only the LAST group matchday (each played 2)
        table = {r["name"]: {"pts": float(r["points"])} for r in rows}
        all_tables = [{rr["name"]: {"pts": float(rr["points"])} for rr in rws}
                      for rws in ctx_groups.values() if len(rws) == 4]
        n_groups = len(all_tables)
        # this fixture is home vs away; the OTHER two teams are the PARALLEL match (analyze_team handles it)
        sc_h = qual_engine.analyze_team(table, (home, away), home, all_tables, n_groups)
        sc_a = qual_engine.analyze_team(table, (home, away), away, all_tables, n_groups)
        parts = []
        ph, pa = qual_engine.phrase_es(sc_h), qual_engine.phrase_es(sc_a)
        if ph:
            parts.append(f"{home} {ph}")
        if pa:
            parts.append(f"{away} {pa}")
        return " · ".join(parts) if parts else None
    except Exception:
        return None


def main(date_from, date_to, max_fixtures, within_hours=None, lineups_hours=4.0):
    c = APIFootballClient()

    def true_quota():
        try:
            return (c.request("/status", None, ttl_hours=0, force_refresh=True)
                    .get("response", {}).get("requests") or {}).get("current")
        except Exception:
            return None

    api0 = true_quota()

    now = datetime.now(timezone.utc)
    fx = c.fixtures(league=WC_LEAGUE, season=WC_SEASON).get("response", []) or []
    window = []
    for f in fx:
        fxd = f.get("fixture", {})
        dstr = fxd.get("date") or ""
        d = dstr[:10]
        short = (fxd.get("status") or {}).get("short")
        if short != "NS":
            continue
        try:
            hours = (datetime.fromisoformat(dstr) - now).total_seconds() / 3600.0
        except Exception:
            hours = None
        if within_hours is not None:
            # PRE-KO mode: only fixtures kicking off within the next N hours.
            if hours is None or not (0 <= hours <= within_hours):
                continue
        else:
            # MORNING mode: full day window by date.
            if not (date_from <= d <= date_to):
                continue
        f["_hours_to_ko"] = hours
        window.append(f)
    window.sort(key=lambda f: f.get("fixture", {}).get("date") or "")
    window = window[:max_fixtures]
    mode_label = f"PRE-KO (≤{within_hours}h)" if within_hours is not None else "MORNING (día completo)"

    # OUR MODEL predictions (Layer-3 rating), if available
    our = {}
    our_path = OUT_DIR / "worldcup_our_model_predictions.csv"
    if our_path.exists():
        for _, r in pd.read_csv(our_path).iterrows():
            our[int(r["fixture_id"])] = r
    # Offline L3 predictor (saved ratings + calibration, NO API): fills L3 for any
    # fixture missing from the precomputed CSV — e.g. NEW knockout fixtures as teams
    # advance. Same method as the shipped L3, just sourced live from the ratings.
    l3pred = None
    statpred = None
    try:
        sys.path.insert(0, str(OUT_DIR))
        import l3_offline  # noqa: E402
        l3pred = l3_offline.load_predictor()
    except Exception as e:  # noqa: BLE001
        print(f"l3_offline predictor unavailable: {type(e).__name__}: {e}")
    try:
        import stats_model  # noqa: E402  (corners/cards/shots DATA model, no market)
        statpred = stats_model.load_predictor()
    except Exception as e:  # noqa: BLE001
        print(f"stats_model predictor unavailable: {type(e).__name__}: {e}")
    # L3-adj: SECONDARY heuristic live adjustment (injuries/XI -> capped L3 nudge). SOFT.
    adjmod = None
    squad_idx = {}
    try:
        import worldcup_l3_adjust as adjmod  # noqa: E402
        squad_idx = adjmod.load_squad_index()
    except Exception as e:  # noqa: BLE001
        print(f"l3_adjust unavailable: {type(e).__name__}: {e}")

    # context module — used for BOTH the multiplier adjustment (gated on CONTEXT_LIVE) and the
    # group-context INFORMATION line (always). build_status_maps is needed in both cases.
    ctx_groups, ctx_team_group = {}, {}
    try:
        import worldcup_context_shadow as ctxmod  # noqa: E402
    except Exception as e:  # noqa: BLE001
        print(f"context_shadow unavailable: {type(e).__name__}: {e}")
        ctxmod = None

    # standings -> team context
    ctx = {}
    st = []
    try:
        st = c.standings(league=WC_LEAGUE, season=WC_SEASON).get("response", []) or []
        for grp in (st[0].get("league", {}).get("standings", []) if st else []):
            for t in grp:
                name = t.get("team", {}).get("name")
                gname = str(t.get("group") or "")
                is_letter_group = gname.startswith("Group ") and len(gname.split()[-1]) == 1
                # prefer the real lettered group over the aggregate "Group Stage" table
                if name in ctx and not is_letter_group:
                    continue
                ctx[name] = {
                    "group": t.get("group"), "rank": t.get("rank"), "pts": t.get("points"),
                    "pld": (t.get("all") or {}).get("played"), "form": t.get("form"),
                    "gd": t.get("goalsDiff"),
                }
    except APIFootballError as e:
        print("standings error:", e)

    # group/standing maps for the LIVE context adjustment (same builder the shadow uses). Built
    # ONCE from the pre-match /standings; soft-fail -> empty -> no adjustment (pure L3).
    if ctxmod is not None:
        try:
            ctx_groups, ctx_team_group = ctxmod.build_status_maps(st)
        except Exception:  # noqa: BLE001
            ctx_groups, ctx_team_group = {}, {}

    report, cards = [], []
    cache_upserts = {}   # lock-at-KO: NS fixtures re-predicted live -> upsert into the L3 cache

    def out(s=""):
        print(s)
        report.append(s)

    out("=" * 96)
    out(f"WORLD CUP 2026 (league 1) - FORECAST CARDS  [{mode_label}]  window {date_from}..{date_to}  "
        f"({len(window)} fixtures)")
    out("=" * 96)
    out("SOURCES: [OUR MODEL]=Layer-3 propio (resultado/goles/xG, datos reales, SIN cuotas) | "
        "[STANDINGS]=group table (contexto) | [LINEUPS/INJURIES]=contexto cerca del saque. Cero mercado.")
    out("")

    for f in window:
        fid = f["fixture"]["id"]
        ko = (f["fixture"]["date"] or "")[:16].replace("T", " ")
        home = (f.get("teams", {}).get("home") or {}).get("name")
        away = (f.get("teams", {}).get("away") or {}).get("name")
        rnd = f.get("league", {}).get("round", "")

        hours = f.get("_hours_to_ko")
        imminent = (hours is not None and 0 <= hours <= lineups_hours)

        rec = {"fixture_id": fid, "kickoff_utc": ko, "home": home, "away": away, "round": rnd,
               "hours_to_ko": (round(hours, 2) if hours is not None else "")}

        ch, ca = ctx.get(home, {}), ctx.get(away, {})

        # ---- print card: OUR MODEL (Layer-3) ONLY — real data, ZERO odds/market ----
        out(f"\n  {home} vs {away}   [{ko} UTC | {rnd}]")
        # LOCK-AT-KO: re-predict a fixture from the CURRENT ratings only while it is NOT
        # started (status NS) AND still > 5 min before kickoff; once started/imminent we use
        # the FROZEN cache row (last pre-KO snapshot) and never recompute (anti-hindsight).
        status_short = ((f.get("fixture") or {}).get("status") or {}).get("short")
        pre_ko_pred = (status_short == "NS") and (hours is not None) and (hours > 5.0 / 60.0)
        cached = our.get(int(fid))
        om = None
        from_ratings = False
        live_ns = False
        if pre_ko_pred and l3pred is not None:
            p = l3pred.predict(home, away)
            if p:
                om = p; from_ratings = True; live_ns = True
                cache_upserts[int(fid)] = {"fixture_id": int(fid), "home": home, "away": away, **p}
            else:
                om = cached
        elif cached is not None:
            om = cached                      # frozen pre-KO snapshot (locked at/after KO)
        elif l3pred is not None:
            p = l3pred.predict(home, away)   # not cached & not pre-KO -> display only, NOT persisted
            if p:
                om = p; from_ratings = True
        if om is not None:
            tag = (" [ratings al día · NS]" if live_ns
                   else " [regen from ratings]" if from_ratings else " [congelado pre-saque]")
            out(f"    [OUR MODEL]{tag} (L3 rating — modelo propio, sin cuotas): "
                f"{home} {om['our_home']*100:4.1f}%  Draw {om['our_draw']*100:4.1f}%  {away} {om['our_away']*100:4.1f}%"
                f"   | exp goals {om['our_xg_home']}-{om['our_xg_away']}"
                f"   | strength {float(om['our_elo_home']):+.2f} vs {float(om['our_elo_away']):+.2f}")
        else:
            out("    [OUR MODEL] no L3 rating for one of the teams")

        # ---- CONTEXTO EN VIVO: ajustar la predicción mostrada/enviada por el escenario de grupo ----
        # Reutiliza la maquinaria del módulo de sombra. Solo grupos NO triviales; knockout/unknown/
        # tercero/intrascendente = 1.0 -> sin cambio. Guarda ctx_* (NO toca our_* = L3 puro). Soft-fail.
        ctx_adj = compute_context_adjustment(
            ctxmod, l3pred, ctx_groups, ctx_team_group, rnd, home, away, om) if CONTEXT_LIVE else None
        context_note = ctx_adj["context_note"] if ctx_adj else None
        if ctx_adj is not None:
            out(f"    [CONTEXTO EN VIVO] (ajuste de grupo aplicado a la ficha): "
                f"{home} {ctx_adj['ctx_home']*100:4.1f}%  Draw {ctx_adj['ctx_draw']*100:4.1f}%  "
                f"{away} {ctx_adj['ctx_away']*100:4.1f}%   | exp goals "
                f"{ctx_adj['ctx_xg_home']}-{ctx_adj['ctx_xg_away']}  — {context_note}")

        # ---- INFORMACIÓN (no es la predicción): contexto de grupo del motor de clasificación
        # correcto (qual_engine: desempates FIFA, mejores terceros). Solo grupos última jornada.
        group_info = compute_group_info(ctx_groups, home, away)
        if group_info:
            out(f"    [CONTEXTO DE GRUPO] (información, no es la predicción): {group_info}")

        # ---- OUR MODEL stats: corners/cards/shots (opponent-adjusted DATA model, no odds) ----
        sp = statpred.predict(home, away) if statpred is not None else None
        if sp:
            # only stats that beat the base-rate OOS are shown; noisy ones (e.g. cards)
            # stay out of the ficha but are still logged for the scorecard.
            show = getattr(statpred, "show", {"corners": True, "cards": True, "shots": True})
            segs = []
            if show.get("corners"):
                segs.append(f"córners {sp['corners_home']:.1f}-{sp['corners_away']:.1f} "
                            f"(tot {sp['corners_total']:.1f}, O{sp['corners_line']:g} {sp['corners_over']*100:.0f}%)")
            if show.get("cards"):
                segs.append(f"tarjetas {sp['cards_home']:.1f}-{sp['cards_away']:.1f} (tot {sp['cards_total']:.1f})")
            if show.get("shots"):
                segs.append(f"tiros {sp['shots_home']:.0f}-{sp['shots_away']:.0f} (tot {sp['shots_total']:.0f})")
            if segs:
                out("    [OUR MODEL] stats (datos, BAJA CONF): " + " · ".join(segs))
        out(f"    [STANDINGS] {home}: grp {ch.get('group','?')} #{ch.get('rank','?')} "
            f"{ch.get('pts','?')}pts {ch.get('pld','?')}pld form {ch.get('form','-')}  ||  "
            f"{away}: grp {ca.get('group','?')} #{ca.get('rank','?')} "
            f"{ca.get('pts','?')}pts {ca.get('pld','?')}pld form {ca.get('form','-')}")

        # ---- injuries (ALWAYS; matinal = canonical adj) + lineups (imminent; XI refinement) ----
        VERBOSE = {"conf": "XI confirmado", "prob": "probable/parcial", "pend": "pendiente"}
        inj = fetch_injuries(c, fid)          # cached 12h; feeds the L3-adj on every run
        lu = {}
        xi_out_home = xi_out_away = None
        if imminent:
            lu = fetch_lineups(c, fid)
            hc, hform = lineup_status(lu.get(home))
            ac, aform = lineup_status(lu.get(away))
            hi = "; ".join(n for n, _ in inj.get(home, [])[:3])
            ai = "; ".join(n for n, _ in inj.get(away, [])[:3])
            out(f"    [LINEUPS] (CONTEXTO — L3 no lo usa): "
                f"{home}: {VERBOSE[hc]} {hform}".rstrip()
                + f"  |  {away}: {VERBOSE[ac]} {aform}".rstrip())
            out(f"    [INJURIES] (CONTEXTO) {home}: {hi or '—'}  ||  {away}: {ai or '—'}")
            rec.update({"lineup_home": hc, "lineup_away": ac,
                        "lineup_home_form": hform, "lineup_away_form": aform,
                        "inj_home": hi, "inj_away": ai})
            if adjmod is not None and lu:
                xi_out_home = adjmod.key_players_out_of_xi(
                    squad_idx.get(home, {}), lu.get(home), [n for n, _ in inj.get(home, [])])
                xi_out_away = adjmod.key_players_out_of_xi(
                    squad_idx.get(away, {}), lu.get(away), [n for n, _ in inj.get(away, [])])
        else:
            out("    [LINEUPS/INJURIES] not yet published (refresh ~4h before kickoff)")

        # ---- L3-adj: SECONDARY heuristic live adjustment (labelled, capped, SOFT) ----
        # The L3 above stays the OFFICIAL line. This nudges L3 strength for today's key
        # absences (injuries always; XI when imminent). Δ==0 or no data -> nothing shown.
        if adjmod is not None and l3pred is not None and om is not None:
            try:
                a = adjmod.compute_fixture_adjustment(
                    l3pred, squad_idx, home, away,
                    inj_home=[n for n, _ in inj.get(home, [])],
                    inj_away=[n for n, _ in inj.get(away, [])],
                    xi_out_home=xi_out_home, xi_out_away=xi_out_away)
            except Exception:
                a = None
            if a:
                motivo = []
                if a["adj_absent_home"]:
                    motivo.append(f"{home} sin {a['adj_absent_home']}")
                if a["adj_absent_away"]:
                    motivo.append(f"{away} sin {a['adj_absent_away']}")
                out(f"    [AJUSTE HOY] (heurístico EN VIVO, NO validado, orientativo) "
                    f"{home} {a['adj_home']*100:.0f}% · X {a['adj_draw']*100:.0f}% · "
                    f"{away} {a['adj_away']*100:.0f}%"
                    + (f"  — {' · '.join(motivo)}" if motivo else ""))
                rec.update(a)

        if om is not None:
            rec.update({"our_home": round(float(om["our_home"]), 4), "our_draw": round(float(om["our_draw"]), 4),
                        "our_away": round(float(om["our_away"]), 4),
                        "our_xg_home": float(om["our_xg_home"]), "our_xg_away": float(om["our_xg_away"]),
                        # store REAL strength (float, 2dp) — feeds the "Por qué" explanation;
                        # the L3 calibration reads the CACHE (also float), not this cards file.
                        "our_elo_home": round(float(om["our_elo_home"]), 2),
                        "our_elo_away": round(float(om["our_elo_away"]), 2)})
            # A/B del TOTAL DE GOLES: variante con total CONSTANTE (modelo viejo), si el predictor la
            # adjunta (solo en predicciones FRESCAS NS; las filas congeladas no la llevan). Nunca se
            # muestra; alimenta el scorecard A/B (learning_loop) para vigilar matchup vs constante.
            if "our_xg_home_const" in om and pd.notna(om.get("our_xg_home_const")):
                rec.update({"our_xg_home_const": float(om["our_xg_home_const"]),
                            "our_xg_away_const": float(om["our_xg_away_const"]),
                            "our_home_const": round(float(om["our_home_const"]), 4),
                            "our_draw_const": round(float(om["our_draw_const"]), 4),
                            "our_away_const": round(float(om["our_away_const"]), 4)})
        if ctx_adj is not None:
            rec.update(ctx_adj)   # ctx_* = predicción ajustada por contexto (la ficha la mostrará)
        if group_info:
            rec["group_info"] = group_info   # línea de INFORMACIÓN (motor de clasificación correcto)
        if sp:
            rec.update({"st_corners_total": sp["corners_total"], "st_corners_over": sp["corners_over"],
                        "st_corners_line": sp["corners_line"], "st_cards_total": sp["cards_total"],
                        "st_shots_total": sp["shots_total"],
                        # per-team (home/away) for the readable ficha; totals stay for the scorecard
                        "st_corners_home": sp["corners_home"], "st_corners_away": sp["corners_away"],
                        "st_shots_home": sp["shots_home"], "st_shots_away": sp["shots_away"]})
        rec.update({"home_group": ch.get("group"), "home_form": ch.get("form"),
                    "away_group": ca.get("group"), "away_form": ca.get("form")})

        # ---- "POR QUÉ": readable explanation of THIS prediction (pure rendering, soft-fail).
        # Derived from the SAME fields just shown (om strengths/xg/probs + adj_*); NO recompute.
        # Coherent with lock-at-KO: om is the live-NS or frozen prediction actually displayed.
        if om is not None:
            try:
                import worldcup_explain
                why = worldcup_explain.explain_l3(
                    home, away, om.get("our_elo_home"), om.get("our_elo_away"), neutral=1,
                    xg_home=om.get("our_xg_home"), xg_away=om.get("our_xg_away"),
                    p_home=om.get("our_home"), p_draw=om.get("our_draw"), p_away=om.get("our_away"),
                    adj_basis=rec.get("adj_basis"),
                    adj_absent_home=rec.get("adj_absent_home"), adj_absent_away=rec.get("adj_absent_away"),
                    adj_delta_home=rec.get("adj_delta_home"), adj_delta_away=rec.get("adj_delta_away"))
            except Exception as e:  # noqa: BLE001
                why = ""
                print(f"explain soft-fail: {type(e).__name__}")
            if why:
                out(f"    [POR QUÉ] {why}")
                rec["why"] = why
        cards.append(rec)

    # ---- LOCK-AT-KO: persist the L3 cache = locked rows (frozen) + NS rows re-predicted now ----
    if cache_upserts:
        CACHE_COLS = ["fixture_id", "home", "away", "our_elo_home", "our_elo_away",
                      "our_home", "our_draw", "our_away", "our_xg_home", "our_xg_away"]
        cache_rows = {}
        if our_path.exists():
            for _, rr in pd.read_csv(our_path).iterrows():
                cache_rows[int(rr["fixture_id"])] = {col: rr.get(col) for col in CACHE_COLS}
        for cfid, crow in cache_upserts.items():
            cache_rows[cfid] = {col: crow.get(col) for col in CACHE_COLS}
        pd.DataFrame([cache_rows[k] for k in cache_rows])[CACHE_COLS].to_csv(our_path, index=False)
        out(f"L3 cache lock-at-KO: {len(cache_upserts)} NS fixture(s) re-predicted; locked rows kept "
            f"-> {our_path.name}")

    api1 = true_quota()
    spend = (api1 - api0) if (api0 is not None and api1 is not None) else "n/a"
    out("")
    out("-" * 96)
    n_imm = sum(1 for f in window if (f.get("_hours_to_ko") is not None
                                      and 0 <= f["_hours_to_ko"] <= lineups_hours))
    out(f"API spend THIS run (fresh-status delta): {spend}  | true quota now: {api1}/7500")
    out(f"(NO odds, NO predictions calls. Imminent fixtures ≤{lineups_hours}h: {n_imm} -> each adds "
        "lineups + injuries (context). fixtures/standings cached.)")
    out(f"generated_at_utc: {datetime.now(timezone.utc).isoformat()}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    # keep a stable header even when there are no fixtures (pre-KO with nothing imminent)
    cards_df = pd.DataFrame(cards) if cards else pd.DataFrame(
        columns=["fixture_id", "kickoff_utc", "home", "away", "round", "hours_to_ko"])
    cards_df.to_csv(OUT_DIR / "worldcup_cards.csv", index=False)
    (OUT_DIR / "worldcup_cards_report.txt").write_text("\n".join(report), encoding="utf-8")
    print(f"\nWritten: {OUT_DIR/'worldcup_cards.csv'}")
    print(f"Written: {OUT_DIR/'worldcup_cards_report.txt'}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--from", dest="dfrom", default="2026-06-16")
    ap.add_argument("--to", dest="dto", default="2026-06-18")
    ap.add_argument("--max-fixtures", type=int, default=14)
    ap.add_argument("--within-hours", type=float, default=None,
                    help="PRE-KO mode: only fixtures kicking off within the next N hours "
                         "(lineups context). Omit for full-day MORNING mode.")
    ap.add_argument("--lineups-hours", type=float, default=4.0,
                    help="fetch lineups/injuries (CONTEXT) for fixtures within this many hours of KO")
    a = ap.parse_args()
    main(a.dfrom, a.dto, a.max_fixtures, a.within_hours, a.lineups_hours)
