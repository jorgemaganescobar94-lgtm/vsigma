"""
BACKTEST (READ-ONLY · NO production change) of the QUALIFICATION-CONTEXT heuristic
(worldcup_context_shadow.py) over the LAST GROUP-STAGE MATCHDAY of past NATIONAL-TEAM
finals tournaments. NATIONAL TEAMS ONLY (international_results.csv is national-team data;
we filter to finals tournaments and verify 0 club matches).

It does NOT duplicate the heuristic: it imports the module's own classify_fixture + MULT +
context_predict (the SAME Poisson recompute + frozen L3 calibration). It only supplies, in a
leak-free way, the two things production gets from the API:
  * the PRE-MATCH standings (here reconstructed from the EARLIER group matchdays of the same
    group — never from the match being predicted), and
  * the L3 ratings, here recomputed WALK-FORWARD (national_elo_layer3.fit_rating on matches
    strictly BEFORE the match date, same weights), with the FROZEN committed L3 calibration.

ANTI-LEAKAGE:
  * standings: only prior group matchdays (strictly earlier date, same reconstructed group).
  * ratings: fit_rating on international matches with date < match date (importance + cross-conf
    + time-decay weights identical to national_elo_layer3). NO future match enters the fit.
  * calibration: the committed national_elo_layer3_calibration.json (a0,a1,total_mean,iso) used
    as a FROZEN transform (the task's "calibración congelada"). It is slow/calibration-only, not
    the discriminative signal; documented.
  * target: real 90' 1X2 (and Over2.5), used ONLY to score, never as a feature.
  * NO API.

SCOPE / FIDELITY:
  * Only SINGLE round-robin groups of 4 (the format classify_fixture is built for: per_team=G-1).
    A tournament-season is INCLUDED only if its first-(G-1)-per-team group graph reconstructs as
    clean, vertex-disjoint, COMPLETE K4 groups (auto-rejects polluted/mislabelled seasons and
    double-round-robin formats like Nations League / qualifiers).
  * classify_fixture is used AS-IS, incl. its WC-2026 best-third rule (rank==3 -> 'tercero_en_disputa',
    NEUTRAL/trivial). In top-2-only tournaments (e.g. WC 2018/2022) that mis-tags some genuinely
    must-win 3rd-placed teams as trivial -> they are EXCLUDED from the graded set (shrinks N, does
    not corrupt the included rows). Documented.

OUTPUT (read-only): context_shadow_backtest_report.txt + context_shadow_backtest_rows.csv
                    + context_shadow_backtest_metrics.csv
"""
from __future__ import annotations

import sys
from collections import Counter
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "scripts"))

import worldcup_context_shadow as CTX   # classify_fixture, MULT, context_predict, scoring
import national_elo_layer3 as L3         # fit_rating + weights (walk-forward ratings)
import l3_offline                        # Predictor + frozen calibration loader
import json

DATA = HERE / "international_results.csv"
CALIB = HERE / "national_elo_layer3_calibration.json"
REPORT = HERE / "context_shadow_backtest_report.txt"
ROWS_CSV = HERE / "context_shadow_backtest_rows.csv"
METRICS_CSV = HERE / "context_shadow_backtest_metrics.csv"

# national-team FINALS tournaments with league-format group stages (NOT qualifiers, NOT Nations
# League). Each season is still gated on a clean K4 reconstruction below.
FINALS_TAGS = {"WC", "Euro", "AFCON", "AsianCup", "CopaAmerica", "GoldCup", "ArabCup", "GulfCup",
               "ConfedCup"}
GSIZE = 4  # single round-robin groups of 4


# --------------------------------------------------------------- structure reconstruction
def _components(edges):
    adj = {}
    for a, b in edges:
        adj.setdefault(a, set()).add(b)
        adj.setdefault(b, set()).add(a)
    seen, comps = set(), []
    for n in adj:
        if n in seen:
            continue
        stack, comp = [n], set()
        while stack:
            x = stack.pop()
            if x in seen:
                continue
            seen.add(x)
            comp.add(x)
            stack += [y for y in adj[x] if y not in seen]
        comps.append(comp)
    return comps


def reconstruct_groups(sub):
    """Return (groups, ok). groups: list of dicts {teams:set, matches:[rows sorted by date]}.
    A group match = one within each team's first (GSIZE-1) tournament matches (knockouts are
    strictly later for both teams). ok=False if the season does NOT reconstruct as clean,
    vertex-disjoint, COMPLETE K4 groups (auto-reject polluted / wrong-format seasons)."""
    sub = sub.sort_values("date")
    seen, grows = {}, []
    for r in sub.itertuples(index=False):
        a, b = int(r.home_id), int(r.away_id)
        oa, ob = seen.get(a, 0) + 1, seen.get(b, 0) + 1
        seen[a], seen[b] = oa, ob
        if oa <= GSIZE - 1 and ob <= GSIZE - 1:
            grows.append(r)
    edges = [(int(r.home_id), int(r.away_id)) for r in grows]
    comps = _components(edges)
    played = {}
    for r in grows:
        k = frozenset((int(r.home_id), int(r.away_id)))
        played[k] = played.get(k, 0) + 1
    # gate: EVERY component must be a complete K4 (size GSIZE, all C(g,2) pairs played once)
    if not comps or any(len(c) != GSIZE for c in comps):
        return [], False
    groups = []
    for c in comps:
        pairs = list(combinations(sorted(c), 2))
        if not all(played.get(frozenset(p), 0) == 1 for p in pairs):
            return [], False
        gm = [r for r in grows if {int(r.home_id), int(r.away_id)} <= c]
        gm = sorted(gm, key=lambda r: r.date)
        if len(gm) != len(pairs):
            return [], False
        groups.append({"teams": set(c), "matches": gm})
    return groups, True


def standings_before(group, upto_date, exclude_pair):
    """Reconstruct the group table from matches strictly BEFORE upto_date (leak-free).
    Returns rows [{name, points, played, gd}] in the shape classify_fixture expects."""
    acc = {}
    name_by_id = {}
    for r in group["matches"]:
        name_by_id[int(r.home_id)] = r.home
        name_by_id[int(r.away_id)] = r.away
    for tid in {int(r.home_id) for r in group["matches"]} | {int(r.away_id) for r in group["matches"]}:
        acc[tid] = {"name": name_by_id[tid], "points": 0.0, "played": 0.0, "gd": 0.0}
    for r in group["matches"]:
        if r.date >= upto_date:
            continue
        h, a = int(r.home_id), int(r.away_id)
        gh, ga = float(r.gh), float(r.ga)
        acc[h]["played"] += 1; acc[a]["played"] += 1
        acc[h]["gd"] += gh - ga; acc[a]["gd"] += ga - gh
        if gh > ga:
            acc[h]["points"] += 3
        elif gh < ga:
            acc[a]["points"] += 3
        else:
            acc[h]["points"] += 1; acc[a]["points"] += 1
    return [acc[t] for t in acc]


# --------------------------------------------------------------- walk-forward L3 ratings
class WFRatings:
    """Leak-free L3 strengths via national_elo_layer3.fit_rating on matches with date<cutoff.
    Same importance/cross-conf/time-decay weights as production. Cached per cutoff date."""
    def __init__(self, df):
        self.df = df
        self.hid = df["home_id"].to_numpy(int)
        self.aid = df["away_id"].to_numpy(int)
        self.gh = df["gh"].to_numpy(float)
        self.ga = df["ga"].to_numpy(float)
        self.neutral = df["neutral"].to_numpy(int)
        self.tags = df["league_tag"].to_numpy()
        self.dates = df["date"].to_numpy()
        self.margin = np.clip(self.gh - self.ga, -L3.MARGIN_CAP, L3.MARGIN_CAP)
        self.imp = np.array([L3.IMP_BY_TAG.get(t, 0.8) for t in self.tags])
        # confederation membership (static; used only for cross-conf up-weight, not outcome-leaky)
        votes = {}
        for i in range(len(df)):
            cf = L3.TAG2CONF.get(self.tags[i])
            if cf:
                for tid in (self.hid[i], self.aid[i]):
                    votes.setdefault(tid, Counter())[cf] += 1
        self.conf = {tid: cc.most_common(1)[0][0] for tid, cc in votes.items()}
        self.xconf = np.array([
            L3.XCONF_MULT if (self.conf.get(self.hid[i]) and self.conf.get(self.aid[i])
                              and self.conf[self.hid[i]] != self.conf[self.aid[i]]) else 1.0
            for i in range(len(df))])
        self.base_w = self.imp * self.xconf
        self.name_by_id = {}
        for _, r in df.iterrows():
            self.name_by_id[int(r["home_id"])] = r["home"]
            self.name_by_id[int(r["away_id"])] = r["away"]
        self._cache = {}

    def strengths_by_name(self, cutoff):
        key = np.datetime64(cutoff)
        if key in self._cache:
            return self._cache[key]
        pm = self.dates < key
        if pm.sum() < L3.MIN_PAST:
            self._cache[key] = None
            return None
        days = (self.dates - self.dates.min()) / np.timedelta64(1, "D")
        cut_day = (key - self.dates.min()) / np.timedelta64(1, "D")
        w = self.base_w[pm] * np.exp(-np.log(2) * (cut_day - days[pm]) / L3.HL_DAYS)
        s_by_id, _h = L3.fit_rating(self.hid[pm], self.aid[pm], self.neutral[pm], self.margin[pm], w)
        s_by_name = {}
        for tid, s in s_by_id.items():
            nm = self.name_by_id.get(int(tid))
            if nm is not None:
                s_by_name[str(nm)] = float(s)
        self._cache[key] = s_by_name
        return s_by_name


# --------------------------------------------------------------- main
def run():
    raw = pd.read_csv(DATA)
    raw["date"] = pd.to_datetime(raw["date"], utc=True, errors="coerce").dt.tz_localize(None)
    raw = raw.dropna(subset=["date", "home_id", "away_id", "gh", "ga"]).copy()
    raw["home_id"] = raw["home_id"].astype(int)
    raw["away_id"] = raw["away_id"].astype(int)

    # club check: every row must be an international/national-team tag (no club leagues present)
    club_rows = int((~raw["league_tag"].isin(set().union(
        FINALS_TAGS, {"Friendlies", "UNL", "CONCACAF_NL", "WCQ_Europe", "WCQ_Asia", "WCQ_Africa",
                      "WCQ_CONCACAF", "WCQ_SA", "WCQ_Oceania", "WCQ_ICPlayoff", "AFCONQ", "AsianCupQ",
                      "COSAFA", "ASEAN", "SAFF", "EAFF", "GulfCup", "ArabCup", "OFC_NationsCup",
                      "BalticCup", "GoldCup"}))).sum())

    wf = WFRatings(raw.sort_values("date").reset_index(drop=True))
    calib = json.loads(CALIB.read_text(encoding="utf-8"))

    fin = raw[raw["league_tag"].isin(FINALS_TAGS)]
    included, excluded = [], []
    rows = []
    for (tag, season), sub in fin.groupby(["league_tag", "season"]):
        if len(sub) < 6:
            excluded.append((tag, int(season), len(sub), "too_few"))
            continue
        groups, ok = reconstruct_groups(sub)
        if not ok:
            excluded.append((tag, int(season), len(sub), "no_clean_K4"))
            continue
        included.append((tag, int(season), len(sub), len(groups)))
        for gi, g in enumerate(groups):
            gname = f"{tag}{int(season)}#G{gi}"
            # final matchday = each team's LAST (3rd) group match -> the matches where BOTH teams
            # have already played GSIZE-2 prior group matches in this group.
            order = {}
            for r in g["matches"]:
                for tid in (int(r.home_id), int(r.away_id)):
                    order[tid] = order.get(tid, 0) + 1
            # recompute per-team ordinal in date order
            seen = {}
            for r in g["matches"]:
                h, a = int(r.home_id), int(r.away_id)
                oh, oa = seen.get(h, 0) + 1, seen.get(a, 0) + 1
                seen[h], seen[a] = oh, oa
                if oh == GSIZE - 1 and oa == GSIZE - 1:   # both playing their final group game
                    table = standings_before(g, r.date, (h, a))
                    grp_map = {gname: table}
                    tg = {row["name"]: gname for row in table}
                    sh, sa, mh, ma, nt = CTX.classify_fixture("group stage", r.home, r.away, grp_map, tg)
                    pred = l3_offline.Predictor(wf.strengths_by_name(r.date) or {}, calib)
                    cp = CTX.context_predict(pred, r.home, r.away, mh, ma)
                    if cp is None:
                        continue
                    gh, ga = float(r.gh), float(r.ga)
                    res = "H" if gh > ga else ("D" if gh == ga else "A")
                    rows.append({
                        "tag": tag, "season": int(season), "group": gname,
                        "fixture_id": int(r.fixture_id), "date": str(r.date)[:10],
                        "home": r.home, "away": r.away,
                        "scenario_home": sh, "scenario_away": sa,
                        "mult_home": mh, "mult_away": ma, "nontrivial": int(bool(nt)),
                        "result_1x2": res, "gh": gh, "ga": ga, **cp,
                    })

    rdf = pd.DataFrame(rows)
    lines = []

    def out(s=""):
        print(s); lines.append(s)

    out("=" * 96)
    out("BACKTEST · heurística de CONTEXTO de clasificación (worldcup_context_shadow) — READ-ONLY")
    out("última jornada de fase de grupos · SELECCIONES NACIONALES · sin API · sin cambios en producción")
    out("=" * 96)
    out(f"filas de clubes en el dataset: {club_rows}  (debe ser 0: international_results.csv es de selecciones)")
    out("")
    out(f"torneos-temporada INCLUIDOS (K4 limpio): {len(included)}")
    for tag, season, nm, ng in sorted(included):
        out(f"   + {tag} {season}: {nm} partidos, {ng} grupos de 4")
    out(f"torneos-temporada EXCLUIDOS (no reconstruyen K4 limpio / formato no liga simple): {len(excluded)}")
    for tag, season, nm, why in sorted(excluded):
        out(f"   - {tag} {season}: {nm} partidos ({why})")
    out("")
    if rdf.empty:
        out("Sin filas de última jornada reconstruidas."); REPORT.write_text("\n".join(lines), encoding="utf-8"); return

    out(f"PARTIDOS de última jornada (con rating L3 walk-forward disponible): {len(rdf)}")
    out(f"  de ellos NO triviales (mult != 1.0): {int(rdf['nontrivial'].sum())}")
    out("")
    out("--- distribución por escenario (ambos equipos; mult del escenario) ---")
    tags_cnt = pd.concat([rdf["scenario_home"], rdf["scenario_away"]]).value_counts()
    for tg, cnt in tags_cnt.items():
        out(f"   {str(tg):18} {int(cnt):4}   (mult {CTX.MULT.get(str(tg), 1.0)})")
    out("")

    # ---- scoring: context vs pure L3, ONLY non-trivial rows ----
    nt = rdf[rdf["nontrivial"] == 1].copy()
    res_idx = {"H": 0, "D": 1, "A": 2}

    def score_block(sub, label):
        y = sub["result_1x2"].map(res_idx).to_numpy(int)
        Y = np.eye(3)[y]
        L = sub[["l3_home", "l3_draw", "l3_away"]].to_numpy(float)
        C = sub[["ctx_home", "ctx_draw", "ctx_away"]].to_numpy(float)
        ok = ~(np.isnan(L).any(1) | np.isnan(C).any(1))
        L, C, Y = L[ok], C[ok], Y[ok]
        if len(Y) == 0:
            return None
        ll_l, ll_c = CTX._logloss_multi(L, Y), CTX._logloss_multi(C, Y)
        br_l, br_c = CTX._brier_multi(L, Y), CTX._brier_multi(C, Y)
        ac_l, ac_c = CTX._acc_multi(L, Y), CTX._acc_multi(C, Y)
        beats = (ll_c < ll_l) and (br_c < br_l)
        return {"label": label, "n": int(len(Y)),
                "ll_l3": ll_l, "ll_ctx": ll_c, "d_ll": ll_l - ll_c,
                "br_l3": br_l, "br_ctx": br_c, "d_br": br_l - br_c,
                "acc_l3": ac_l, "acc_ctx": ac_c, "beats": beats}

    metrics = []
    glob = score_block(nt, "GLOBAL no-trivial")
    out("--- 1X2 (H/D/A) — context-adjusted VS L3 puro, SOLO escenarios no triviales ---")
    hdr = f"  {'corte':22} {'n':>4} {'ll_L3':>7} {'ll_ctx':>7} {'Δll':>7} {'br_L3':>7} {'br_ctx':>7} {'Δbr':>7} {'acc_L3':>7} {'acc_ctx':>7} {'bate?':>6}"
    out(hdr); out("  " + "-" * (len(hdr) - 2))

    def emit(m):
        if not m:
            return
        out(f"  {m['label']:22} {m['n']:>4} {m['ll_l3']:>7.4f} {m['ll_ctx']:>7.4f} {m['d_ll']:>+7.4f} "
            f"{m['br_l3']:>7.4f} {m['br_ctx']:>7.4f} {m['d_br']:>+7.4f} {m['acc_l3']*100:>6.1f}% {m['acc_ctx']*100:>6.1f}% "
            f"{('SÍ' if m['beats'] else 'no'):>6}")
        metrics.append(m)

    emit(glob)
    # per-scenario: a row is attributed to a scenario if EITHER team carries it (non-trivial side)
    for scen in ["ya_clasificado", "eliminado", "debe_ganar", "le_vale_empate", "intrascendente"]:
        if CTX.MULT.get(scen, 1.0) == 1.0:
            continue
        mask = (nt["scenario_home"] == scen) | (nt["scenario_away"] == scen)
        sub = nt[mask]
        if len(sub):
            emit(score_block(sub, scen))
    out("")
    out("  Δ = L3 − ctx (positivo = ctx mejora). 'bate?' = ctx mejora en logloss Y brier.")
    out("")

    # ---- significancia: ¿la mejora global supera el ruido? (bootstrap pareado por partido) ----
    yv = nt["result_1x2"].map(res_idx).to_numpy(int)
    Yv = np.eye(3)[yv]
    Lv = nt[["l3_home", "l3_draw", "l3_away"]].to_numpy(float)
    Cv = nt[["ctx_home", "ctx_draw", "ctx_away"]].to_numpy(float)
    okv = ~(np.isnan(Lv).any(1) | np.isnan(Cv).any(1))
    Lv, Cv, Yv = Lv[okv], Cv[okv], Yv[okv]

    def _row_ll(P, Y):
        Pc = np.clip(P, CTX.EPS, 1.0); Pc = Pc / Pc.sum(1, keepdims=True)
        return -np.sum(Y * np.log(Pc), axis=1)

    def _row_br(P, Y):
        Pc = np.clip(P, CTX.EPS, 1.0); Pc = Pc / Pc.sum(1, keepdims=True)
        return np.sum((Pc - Y) ** 2, axis=1)

    dll = _row_ll(Lv, Yv) - _row_ll(Cv, Yv)   # >0 = ctx mejor
    dbr = _row_br(Lv, Yv) - _row_br(Cv, Yv)
    nB = len(dll)
    # fixed-seed bootstrap (Date.now/Math.random no aplican; usamos numpy con semilla fija)
    rng = np.random.RandomState(12345)
    idx = rng.randint(0, nB, (20000, nB))
    bll = dll[idx].mean(1); bbr = dbr[idx].mean(1)
    ll_lo, ll_hi = np.percentile(bll, 2.5), np.percentile(bll, 97.5)
    br_lo, br_hi = np.percentile(bbr, 2.5), np.percentile(bbr, 97.5)
    out("--- ¿supera el ruido? bootstrap pareado por partido (20000 resamples, semilla fija) ---")
    out(f"  logloss: media Δ(L3-ctx)={dll.mean():+.5f} | ctx mejor en {100*(dll>0).mean():.0f}% de partidos | "
        f"mejora rel. {100*dll.mean()/_row_ll(Lv, Yv).mean():.2f}% del L3")
    out(f"  IC95% Δlogloss=[{ll_lo:+.5f},{ll_hi:+.5f}] -> {'SIGNIFICATIVO (excluye 0)' if ll_lo > 0 else 'NO significativo (incluye 0)'}"
        f"  | P(Δ>0)={100*(bll>0).mean():.0f}%")
    out(f"  IC95% Δbrier  =[{br_lo:+.5f},{br_hi:+.5f}] -> {'SIGNIFICATIVO (excluye 0)' if br_lo > 0 else 'NO significativo (incluye 0)'}"
        f"  | P(Δ>0)={100*(bbr>0).mean():.0f}%")
    out("")

    # Over 2.5 (binary) on non-trivial
    gh = nt["gh"].to_numpy(float); ga = nt["ga"].to_numpy(float)
    realov = ((gh + ga) >= 3).astype(int)
    o_l3 = nt["l3_over25"].to_numpy(float); o_cx = nt["ctx_over25"].to_numpy(float)
    om = ~(np.isnan(o_l3) | np.isnan(o_cx))
    out("--- Over 2.5 (binario) sobre no triviales ---")
    if om.sum():
        out(f"  real Over={realov[om].mean()*100:.0f}% (n={int(om.sum())})")
        out(f"  L3 puro     logloss {CTX._bin_logloss(o_l3[om], realov[om]):.4f} · brier {CTX._bin_brier(o_l3[om], realov[om]):.4f}")
        out(f"  context-adj logloss {CTX._bin_logloss(o_cx[om], realov[om]):.4f} · brier {CTX._bin_brier(o_cx[om], realov[om]):.4f}")
    out("")

    out("=" * 96)
    n_nt = int(rdf["nontrivial"].sum())
    verdict = ("INSUFICIENTE" if (glob is None or glob["n"] < CTX.SMALL_N) else
               ("MEJORA" if glob["beats"] else "EMPEORA/INDISTINGUIBLE"))
    out(f"VEREDICTO GLOBAL (no triviales, N={glob['n'] if glob else 0}, umbral={CTX.SMALL_N}): {verdict}")
    out("=" * 96)

    rdf.to_csv(ROWS_CSV, index=False)
    pd.DataFrame(metrics).to_csv(METRICS_CSV, index=False)
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWritten: {REPORT}\nWritten: {ROWS_CSV}\nWritten: {METRICS_CSV}")


if __name__ == "__main__":
    run()
