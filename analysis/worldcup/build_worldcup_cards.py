"""
WORLD CUP 2026 - per-match forecast cards (ISOLATED, analysis/worldcup/ only).

NOT production. Production's league allowlist (scripts/filter_leagues.py) REJECTS the
World Cup (no ('world','world cup') entry -> 'country_league_not_allowlisted'), so this
is a standalone shadow product. No .env edits, no git, BOUNDED API.

Per upcoming fixture builds a card combining, each with its SOURCE marked:
  * 1X2 / O/U2.5 / BTTS  -> de-vigged MARKET (consensus median across books + Pinnacle).
    The market is the best forecast; no invented edge.
  * API model prediction (/predictions) where available (some WC fixtures lack it).
  * Group context from /standings (rank, points, played, form).
  * Lineups/injuries flagged if not yet published.

API budget: 1 /fixtures (cached) + 1 /standings + per-fixture (/odds + /predictions).
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
from api_football_client import APIFootballClient, APIFootballError, build_params_key  # noqa: E402

OUT_DIR = Path(__file__).resolve().parent
WC_LEAGUE = 1
WC_SEASON = 2026


def devig(odds_by_outcome):
    """odds_by_outcome: {outcome: decimal_odd}. Return de-vigged probs summing to 1."""
    imp = {k: 1.0 / v for k, v in odds_by_outcome.items() if v and v > 1.0}
    s = sum(imp.values())
    if s <= 0:
        return {}
    return {k: v / s for k, v in imp.items()}


def parse_bet(bookmakers, bet_name):
    """Return list of {value: odd} dicts, one per bookmaker offering bet_name."""
    out = []
    for bm in bookmakers:
        for bet in bm.get("bets", []) or []:
            if str(bet.get("name", "")).strip().lower() == bet_name.lower():
                vals = {}
                for v in bet.get("values", []) or []:
                    try:
                        vals[str(v.get("value")).strip()] = float(v.get("odd"))
                    except Exception:
                        pass
                if vals:
                    out.append({"book": bm.get("name"), "vals": vals})
    return out


def consensus(books, outcomes, pinnacle_name="Pinnacle"):
    """Median de-vigged prob per outcome across books, + Pinnacle if present."""
    per_book = []
    pinn = None
    for b in books:
        od = {o: b["vals"].get(o) for o in outcomes if o in b["vals"]}
        if len(od) == len(outcomes):
            dv = devig(od)
            if dv:
                per_book.append(dv)
                if b["book"] == pinnacle_name:
                    pinn = dv
    if not per_book:
        return None, None, 0
    med = {o: float(np.median([pb[o] for pb in per_book])) for o in outcomes}
    s = sum(med.values())
    med = {o: v / s for o, v in med.items()}
    return med, pinn, len(per_book)


def ou_books(bookmakers, line="2.5"):
    out = []
    for bm in bookmakers:
        for bet in bm.get("bets", []) or []:
            if str(bet.get("name", "")).strip().lower() == "goals over/under":
                vals = {}
                for v in bet.get("values", []) or []:
                    val = str(v.get("value")).strip()
                    if val in (f"Over {line}", f"Under {line}"):
                        try:
                            vals[val.split()[0]] = float(v.get("odd"))  # Over / Under
                        except Exception:
                            pass
                if {"Over", "Under"} <= set(vals):
                    out.append({"book": bm.get("name"), "vals": vals})
    return out


def main(date_from, date_to, max_fixtures):
    c = APIFootballClient()

    def true_quota():
        try:
            return (c.request("/status", None, ttl_hours=0, force_refresh=True)
                    .get("response", {}).get("requests") or {}).get("current")
        except Exception:
            return None

    api0 = true_quota()

    fx = c.fixtures(league=WC_LEAGUE, season=WC_SEASON).get("response", []) or []
    window = []
    for f in fx:
        d = (f.get("fixture", {}).get("date") or "")[:10]
        short = (f.get("fixture", {}).get("status") or {}).get("short")
        if date_from <= d <= date_to and short == "NS":
            window.append(f)
    window.sort(key=lambda f: f.get("fixture", {}).get("date") or "")
    window = window[:max_fixtures]

    # OUR MODEL predictions (Layer-3 rating), if available
    our = {}
    our_path = OUT_DIR / "worldcup_our_model_predictions.csv"
    if our_path.exists():
        for _, r in pd.read_csv(our_path).iterrows():
            our[int(r["fixture_id"])] = r
    # OUR MODEL v2 (L3 + squad blend) — EXPERIMENTAL, not validated > L3
    ourv2 = {}
    v2_path = OUT_DIR / "worldcup_our_model_v2_predictions.csv"
    if v2_path.exists():
        for _, r in pd.read_csv(v2_path).iterrows():
            ourv2[int(r["fixture_id"])] = r

    # standings -> team context
    ctx = {}
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

    report, cards = [], []

    def out(s=""):
        print(s)
        report.append(s)

    out("=" * 96)
    out(f"WORLD CUP 2026 (league 1) - FORECAST CARDS  window {date_from}..{date_to}  ({len(window)} fixtures)")
    out("=" * 96)
    out("SOURCES: [MARKET]=de-vigged consensus odds (best forecast) | [API-PRED]=API model | "
        "[STANDINGS]=group table. No invented edge.")
    out("")

    for f in window:
        fid = f["fixture"]["id"]
        ko = (f["fixture"]["date"] or "")[:16].replace("T", " ")
        home = (f.get("teams", {}).get("home") or {}).get("name")
        away = (f.get("teams", {}).get("away") or {}).get("name")
        rnd = f.get("league", {}).get("round", "")

        rec = {"fixture_id": fid, "kickoff_utc": ko, "home": home, "away": away, "round": rnd}

        # ---- odds ----
        mk1x2 = mkou = mkbtts = None
        pin1x2 = None
        nbooks = 0
        try:
            od = c.odds(fixture=fid).get("response", []) or []
            if od:
                bms = od[0].get("bookmakers", []) or []
                nbooks = len(bms)
                mk1x2, pin1x2, n1 = consensus(parse_bet(bms, "Match Winner"), ["Home", "Draw", "Away"])
                mkou, _, _ = consensus(ou_books(bms, "2.5"), ["Over", "Under"])
                mkbtts, _, _ = consensus(parse_bet(bms, "Both Teams Score"), ["Yes", "No"])
        except APIFootballError as e:
            out(f"  odds error {fid}: {e}")

        # ---- API prediction ----
        pred = None
        try:
            pr = c.predictions(fid).get("response", []) or []
            if pr:
                p = pr[0].get("predictions", {}) or {}
                pct = p.get("percent", {}) or {}
                advice = p.get("advice")
                degenerate = (pct.get("home") == pct.get("draw") == pct.get("away")) or advice == "No predictions available"
                if not degenerate and pct:
                    pred = {"home": pct.get("home"), "draw": pct.get("draw"), "away": pct.get("away"),
                            "advice": advice, "goals_h": (p.get("goals") or {}).get("home"),
                            "goals_a": (p.get("goals") or {}).get("away")}
        except APIFootballError:
            pass

        ch, ca = ctx.get(home, {}), ctx.get(away, {})

        # ---- print card ----
        out(f"\n  {home} vs {away}   [{ko} UTC | {rnd}]")
        if mk1x2:
            line = (f"    [MARKET] 1X2 (de-vig, {nbooks} books): "
                    f"{home} {mk1x2['Home']*100:4.1f}%  Draw {mk1x2['Draw']*100:4.1f}%  {away} {mk1x2['Away']*100:4.1f}%")
            if pin1x2:
                line += f"   (Pinnacle: {pin1x2['Home']*100:.0f}/{pin1x2['Draw']*100:.0f}/{pin1x2['Away']*100:.0f})"
            out(line)
        else:
            out("    [MARKET] 1X2: not available yet")
        if mkou:
            out(f"    [MARKET] O/U 2.5: Over {mkou['Over']*100:4.1f}% / Under {mkou['Under']*100:4.1f}%")
        if mkbtts:
            out(f"    [MARKET] BTTS: Yes {mkbtts['Yes']*100:4.1f}% / No {mkbtts['No']*100:4.1f}%")
        om = our.get(int(fid))
        if om is not None:
            out(f"    [OUR MODEL] (L3 rating, NO odds): {home} {om['our_home']*100:4.1f}%  "
                f"Draw {om['our_draw']*100:4.1f}%  {away} {om['our_away']*100:4.1f}%"
                f"   | exp goals {om['our_xg_home']}-{om['our_xg_away']}"
                f"   | strength {float(om['our_elo_home']):+.2f} vs {float(om['our_elo_away']):+.2f}")
            if mk1x2:
                edge = (om['our_home'] - mk1x2['Home']) * 100
                out(f"        (our_home - market_home = {edge:+.1f} pts; informational, market is the bar)")
        else:
            out("    [OUR MODEL] no L3 rating for one of the teams")
        ov = ourv2.get(int(fid))
        if ov is not None:
            sh = "" if pd.isna(ov.get("squad_home")) else f" squad {ov['squad_home']:.2f}/{ov['squad_away']:.2f}"
            out(f"    [OUR MODEL v2] (L3+squad, EXPERIMENTAL — not validated > L3): {home} {ov['v2_home']*100:4.1f}%  "
                f"Draw {ov['v2_draw']*100:4.1f}%  {away} {ov['v2_away']*100:4.1f}%{sh}")
        if pred:
            out(f"    [API-PRED] {pred['home']}/{pred['draw']}/{pred['away']} (H/D/A) | "
                f"exp goals {pred['goals_h']}-{pred['goals_a']} | advice: {pred['advice']}")
        else:
            out("    [API-PRED] not available for this fixture")
        out(f"    [STANDINGS] {home}: grp {ch.get('group','?')} #{ch.get('rank','?')} "
            f"{ch.get('pts','?')}pts {ch.get('pld','?')}pld form {ch.get('form','-')}  ||  "
            f"{away}: grp {ca.get('group','?')} #{ca.get('rank','?')} "
            f"{ca.get('pts','?')}pts {ca.get('pld','?')}pld form {ca.get('form','-')}")
        out("    [LINEUPS/INJURIES] not yet published (refresh ~1h before kickoff)")

        if mk1x2:
            rec.update({"mkt_home": round(mk1x2["Home"], 4), "mkt_draw": round(mk1x2["Draw"], 4),
                        "mkt_away": round(mk1x2["Away"], 4), "n_books": nbooks})
        if mkou:
            rec.update({"mkt_over25": round(mkou["Over"], 4), "mkt_under25": round(mkou["Under"], 4)})
        if mkbtts:
            rec.update({"mkt_btts_yes": round(mkbtts["Yes"], 4)})
        if om is not None:
            rec.update({"our_home": round(float(om["our_home"]), 4), "our_draw": round(float(om["our_draw"]), 4),
                        "our_away": round(float(om["our_away"]), 4),
                        "our_xg_home": float(om["our_xg_home"]), "our_xg_away": float(om["our_xg_away"]),
                        "our_elo_home": int(om["our_elo_home"]), "our_elo_away": int(om["our_elo_away"])})
        if pred:
            rec.update({"apipred_home": pred["home"], "apipred_draw": pred["draw"],
                        "apipred_away": pred["away"], "apipred_advice": pred["advice"]})
        rec.update({"home_group": ch.get("group"), "home_form": ch.get("form"),
                    "away_group": ca.get("group"), "away_form": ca.get("form")})
        cards.append(rec)

    api1 = true_quota()
    spend = (api1 - api0) if (api0 is not None and api1 is not None) else "n/a"
    out("")
    out("-" * 96)
    out(f"API spend THIS run (fresh-status delta): {spend}  | true quota now: {api1}/7500")
    out("(re-runs cost ~0: odds cached 1h, predictions 6h, fixtures/standings cached.)")
    out(f"generated_at_utc: {datetime.now(timezone.utc).isoformat()}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(cards).to_csv(OUT_DIR / "worldcup_cards.csv", index=False)
    (OUT_DIR / "worldcup_cards_report.txt").write_text("\n".join(report), encoding="utf-8")
    print(f"\nWritten: {OUT_DIR/'worldcup_cards.csv'}")
    print(f"Written: {OUT_DIR/'worldcup_cards_report.txt'}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--from", dest="dfrom", default="2026-06-16")
    ap.add_argument("--to", dest="dto", default="2026-06-18")
    ap.add_argument("--max-fixtures", type=int, default=14)
    a = ap.parse_args()
    main(a.dfrom, a.dto, a.max_fixtures)
