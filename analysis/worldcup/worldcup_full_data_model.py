"""
WORLD CUP 2026 - FULL-DATA MODEL (1X2 + goles), ISOLATED analysis/worldcup/. NO market/odds.

Jorge's EXPLICIT, CONSCIOUS decision (2026-07-01): ship a model that INGESTS EVERY available
point-in-time feature into the shown 1X2/goals prediction, wired LIVE but fully REVERSIBLE.
It is KNOWN AND EXPECTED TO MEASURE WORSE than the L3/ensemble baseline (offline backtests
proved team-stat and player-rating features are null/redundant for national-team 1X2 — see
MEMORY: offline-predictive-core-analysis, and the 2026-07-01 new-fields backtest). This module
exists to (a) honour "use all the data" as a product stance, (b) provide an honest live A/B,
and (c) give a formula-audit anchor. It makes NO precision claim.

DESIGN
  * Estimator = STRONGLY REGULARIZED multinomial logit (1X2) + two Poisson GLMs (home/away
    goals). Strong L2 so ~26 features do not overfit. Temperature-calibrated + eps-floor.
  * ANTI-LEAKAGE: every feature is a team's time-decayed mean over its OWN PRIOR matches only
    (strictly date < kickoff). The match's own post-match value is NEVER used. Strength comes
    from the L3 model output (production-calibrated live; recipe-reconstructed in training).
  * IMPUTE-NEUTRAL: a missing feature (no coverage) -> the training mean (z=0) and n_missing++.
    The live predictor is pure-numpy over a JSON artifact and is wrapped so it NEVER crashes:
    any error -> returns None -> the caller reverts EXACTLY to the ensemble (delta = 0).

The live wire lives in build_worldcup_cards.py behind FULL_DATA_LIVE. our_/mx_/ens_ are ALWAYS
preserved in parallel (shadow + rollback). This module NEVER touches odds/predictions endpoints.
"""
from __future__ import annotations

import json
import math
import sqlite3
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "scripts"))

# ---- master flag: True -> shown 1X2/goals = full-data model; False -> EXACT revert to ensemble.
FULL_DATA_LIVE = True

# ---- CLUB_FORM_FEATURE: add `club_form_diff` (national strength from players' 2025 CLUB form,
# league-tier normalized) as a 27th feature. REVERSIBLE via a SEPARATE artifact: True -> the model
# uses worldcup_full_data_artifact_clubform.json (27 feats); False -> the base 26-feat artifact,
# EXACTLY as before this feature. Honest: NO precision claim until the live A/B validates it (offline
# it can only be an INDICATIVE test — see train(): we hold a single 2025 club snapshot).
CLUB_FORM_FEATURE = True

ARTIFACT = HERE / "worldcup_full_data_artifact.json"                 # base (26 feats)
ARTIFACT_CF = HERE / "worldcup_full_data_artifact_clubform.json"     # +club_form (27 feats)
ARTIFACT_EXTRA = HERE / "worldcup_full_data_artifact_extra.json"     # +intl-player-agg (31 feats)
CLUB_FORM_CSV = HERE / "worldcup_club_form.csv"                      # single-season 2025 club_form
CLUB_FORM_MULTI_CSV = HERE / "worldcup_club_form_multiseason.csv"    # 2025/2024/2023 recency-weighted
INTL_AGG_CSV = HERE / "worldcup_intl_player_agg.csv"                # per-team-match player aggregates
CLUB_FORM_DIFF = "club_form_diff"

# ---- CLUB_FORM_MULTISEASON: club_form_diff uses the MULTI-season (2025/2024/2023, recency-weighted)
# table instead of the single 2025 snapshot. 2023 falls in burn-in (<2024) -> the feature is now
# TRAINABLE (unlike the inert player aggregates). Data-source flag: shipped True; flip to False (single
# season) requires a retrain to be exact. The EXACT runtime revert of the whole feature stays
# CLUB_FORM_FEATURE (off -> 26-feat base, delta 0).
CLUB_FORM_MULTISEASON = True

# ---- EXTRA_PLAYER_AGG: Jorge's maximalist decision — ingest the per-match international player
# aggregates (duels/dribbles/tackles/interceptions rolled to team level) as extra features, NO gate.
# HONEST: these have ZERO burn-in (<2024) coverage in the cache, so the model cannot learn a weight
# for them (they enter ~inert, weight ~0). Kept anyway by explicit decision. REVERSIBLE via a third
# artifact: True -> 31-feat artifact; False -> falls back to the club_form/base set EXACTLY (delta 0).
EXTRA_PLAYER_AGG = True
EXTRA_FIELDS = ["duels_won", "dribbles_success", "tackles_total", "interceptions"]

# ---- FULL_DATA_REG: regularization of the 1X2 logit. A burn-in-CV sweep (2026-07-01) showed the
# shipped L2 C=0.30 UNDER-regularized (null features added noise -> ~1% worse than the ensemble).
# STRONG L1 (C=0.1, saga) zeroes the ~21 null features and recovers ~91% of the gap (OOS 1X2 logloss
# 0.9281 -> 0.9187 ~= ensemble/L3), keeping all 31 features. ADOPTED by explicit decision. Does NOT
# beat the ensemble (ceiling); NO precision claim. REVERSIBLE: "l2c0.3" retrains the EXACT old model
# (lbfgs L2 C=0.30) -> delta 0. Poisson alpha stays 1.0 (the sweep showed Over/BTTS unchanged).
FULL_DATA_REG = "l1c0.1"


def _reg_config(name):
    """Sklearn LogisticRegression kwargs for the chosen regularization. 'l2c0.3' reproduces the
    pre-adoption model EXACTLY (default lbfgs, multinomial)."""
    if name == "l1c0.1":
        return {"penalty": "l1", "C": 0.10, "solver": "saga", "max_iter": 8000, "tol": 1e-3}
    return {"penalty": "l2", "C": 0.30, "max_iter": 2000}   # l2c0.3: exact revert (lbfgs default)
CACHE = ROOT / "data" / "cache" / "api_football_cache.sqlite3"
IR = HERE / "international_results.csv"
PM = HERE / "national_elo_layer3_permatch.csv"
STATS_RAW = HERE / "worldcup_stats_raw.csv"
SQUAD = HERE / "squad_quality_raw_48.csv"

FORM_HL = 540.0        # form/stat time-decay half-life (days) — matches feature_study_stats
FORM_N = 10            # recent-form window for EWMA gf/ga/ppg
MIN_PRIOR = 3          # need >=3 prior matches with a stat to define a team's past-mean
EPS = 1e-4             # probability floor

# every non-betting /fixtures/statistics type we roll into a feature
STAT_TYPES = {
    "Shots on Goal": "sot", "Total Shots": "shots",
    "Shots insidebox": "shots_inbox", "Shots outsidebox": "shots_outbox",
    "Blocked Shots": "shots_blocked", "Goalkeeper Saves": "gk_saves",
    "Total passes": "passes_total", "Passes accurate": "passes_acc", "Passes %": "passes_pct",
    "Offsides": "offsides", "Fouls": "fouls", "Ball Possession": "possession",
    "Corner Kicks": "corners",
}
STAT_FIELDS = ["sot", "shots", "shots_inbox", "shots_outbox", "shots_blocked", "gk_saves",
               "passes_total", "passes_acc", "passes_pct", "offsides", "fouls", "possession",
               "corners"]

# ORDERED feature list (this IS the audit list — every feature the model ingests). "diff" = the
# home team's point-in-time value minus the away team's (signed towards home).
FEATURES = (
    ["l3_logit_h", "l3_logit_a", "l3_xg_h", "l3_xg_a", "neutral"]          # strength (from L3)
    + ["form_gf_diff", "form_ga_diff", "form_ppg_diff", "form_streak_diff"]  # recent form EWMA
    + ["rest_diff", "h2h_gd", "squad_diff", "team_rating_diff"]              # rest / h2h / squad / ratings
    + [f"{s}_diff" for s in STAT_FIELDS]                                     # 13 rolling real stats
)
# club_form_diff is the OPTIONAL 27th feature (behind CLUB_FORM_FEATURE). Its own artifact is trained
# on FEATURES + [CLUB_FORM_DIFF]; when the flag is off the model uses the base 26-feature artifact.
FEATURES_CF = FEATURES + [CLUB_FORM_DIFF]
# +4 international per-match player aggregates (behind EXTRA_PLAYER_AGG). Reversible via a 3rd artifact.
FEATURES_EXTRA = FEATURES_CF + [f"{x}_diff" for x in EXTRA_FIELDS]


def active_features():
    if EXTRA_PLAYER_AGG:
        return list(FEATURES_EXTRA)
    return FEATURES_CF if CLUB_FORM_FEATURE else list(FEATURES)


def active_artifact_path():
    """Most-inclusive ENABLED artifact that exists on disk; falls back down so predict never breaks."""
    if EXTRA_PLAYER_AGG and ARTIFACT_EXTRA.exists():
        return ARTIFACT_EXTRA
    if CLUB_FORM_FEATURE and ARTIFACT_CF.exists():
        return ARTIFACT_CF
    return ARTIFACT


def _num(v):
    if v is None:
        return None
    if isinstance(v, str):
        v = v.strip().rstrip("%")
        if v == "":
            return None
    try:
        f = float(v)
        return f if math.isfinite(f) else None
    except Exception:
        return None


def _softmax(z):
    z = z - np.max(z)
    e = np.exp(z)
    return e / e.sum()


# ============================================================ data sources (loaded once)
class Sources:
    """Loads every historical store ONCE and exposes point-in-time lookups. Pure/offline."""

    def __init__(self):
        import pandas as pd
        ir = pd.read_csv(IR)
        ir["date"] = pd.to_datetime(ir["date"], utc=True, errors="coerce").dt.tz_localize(None)
        ir = ir.dropna(subset=["date", "home_id", "away_id", "gh", "ga"]).copy()
        ir["home_id"] = ir["home_id"].astype(int); ir["away_id"] = ir["away_id"].astype(int)
        ir["neutral"] = ir["neutral"].fillna(0).astype(int)
        ir = ir.sort_values("date").reset_index(drop=True)
        self.ir = ir
        self.date_by_fid = {int(r.fixture_id): np.datetime64(r.date) for r in ir.itertuples(index=False)}

        # form + rest + h2h event lists (leak-free: built by scanning in date order)
        self.form = defaultdict(list)     # tid -> [(date, gf, ga, pts)]
        self.last_date = {}               # tid -> last match date (for rest)
        self.h2h = defaultdict(list)      # frozenset(ids) -> [(date, gd_home_persp, home_id)]
        # NOTE: these are consumed via point-in-time helpers that only read entries with date<when.
        for r in ir.itertuples(index=False):
            d = np.datetime64(r.date)
            ph = 3 if r.gh > r.ga else (1 if r.gh == r.ga else 0)
            pa = 3 if r.ga > r.gh else (1 if r.gh == r.ga else 0)
            self.form[int(r.home_id)].append((d, float(r.gh), float(r.ga), ph))
            self.form[int(r.away_id)].append((d, float(r.ga), float(r.gh), pa))
            self.h2h[frozenset((int(r.home_id), int(r.away_id)))].append(
                (d, float(r.gh) - float(r.ga), int(r.home_id)))

        # rolling real stats: (fid,tid) -> {field: val}, merged cache + stats_raw
        self.stat = self._load_stats()
        # per-team stat series {field: {tid: (dates, vals)}}
        self.stat_series = self._stat_series()
        # player ratings (fid,tid) -> team_rating
        self.rating_series = self._rating_series()
        # squad quality per team_id (minutes-weighted mean player rating)
        self.squad = self._load_squad()
        # club_form per team_id (from players' 2025 club season, league-tier normalized; 0 API)
        self.club_form = self._load_club_form()
        # per-team-match international player aggregates (duels/dribbles/tackles/interc.) -> series
        self.agg_series = self._load_intl_agg()

    # -------- stats --------
    def _load_stats(self):
        import pandas as pd
        stat = {}
        if CACHE.exists():
            conn = sqlite3.connect(CACHE)
            try:
                for pj, rj in conn.execute(
                        "SELECT params_json,response_json FROM api_cache WHERE path='/fixtures/statistics'"):
                    fid = json.loads(pj).get("fixture")
                    if fid is None:
                        continue
                    for t in (json.loads(rj).get("response") or []):
                        tid = (t.get("team") or {}).get("id")
                        if tid is None:
                            continue
                        d = stat.setdefault((int(fid), int(tid)), {})
                        for s in t.get("statistics", []) or []:
                            k = STAT_TYPES.get(s.get("type"))
                            v = _num(s.get("value"))
                            if k and v is not None:
                                d.setdefault(k, v)
            finally:
                conn.close()
        if STATS_RAW.exists():   # older coverage (corners/shots/sot/fouls/possession)
            raw = pd.read_csv(STATS_RAW)
            for r in raw.itertuples(index=False):
                try:
                    key = (int(r.fixture_id), int(r.team_id))
                except Exception:
                    continue
                d = stat.setdefault(key, {})
                for col in ("corners", "shots", "sot", "fouls", "possession"):
                    v = _num(getattr(r, col, None))
                    if v is not None:
                        d.setdefault(col, v)
        return stat

    def _stat_series(self):
        series = {f: defaultdict(list) for f in STAT_FIELDS}
        for (fid, tid), d in self.stat.items():
            when = self.date_by_fid.get(fid)
            if when is None:
                continue
            for f in STAT_FIELDS:
                if f in d:
                    series[f][tid].append((when, d[f]))
        out = {}
        for f, by in series.items():
            out[f] = {}
            for tid, lst in by.items():
                lst.sort(key=lambda x: x[0])
                out[f][tid] = (np.array([x[0] for x in lst], "datetime64[ns]"),
                               np.array([x[1] for x in lst], float))
        return out

    def _rating_series(self):
        by = defaultdict(list)
        if CACHE.exists():
            conn = sqlite3.connect(CACHE)
            try:
                for pj, rj in conn.execute(
                        "SELECT params_json,response_json FROM api_cache WHERE path='/fixtures/players'"):
                    fid = json.loads(pj).get("fixture")
                    when = self.date_by_fid.get(int(fid)) if fid is not None else None
                    if when is None:
                        continue
                    for tb in (json.loads(rj).get("response") or []):
                        tid = (tb.get("team") or {}).get("id")
                        if tid is None:
                            continue
                        rs = []
                        for p in tb.get("players", []) or []:
                            g = ((p.get("statistics") or [{}])[0] or {}).get("games") or {}
                            v = _num(g.get("rating"))
                            if v is not None:
                                rs.append(v)
                        if rs:
                            by[int(tid)].append((when, sum(rs) / len(rs)))
            finally:
                conn.close()
        out = {}
        for tid, lst in by.items():
            lst.sort(key=lambda x: x[0])
            out[tid] = (np.array([x[0] for x in lst], "datetime64[ns]"),
                        np.array([x[1] for x in lst], float))
        return out

    def _load_squad(self):
        import pandas as pd
        if not SQUAD.exists():
            return {}
        sq = pd.read_csv(SQUAD)
        out = {}
        for tid, g in sq.groupby("team_id"):
            r = g["rating"].astype(float); m = g["minutes"].astype(float).clip(lower=1)
            out[int(tid)] = float(np.average(r, weights=m)) if len(r) else None
        return out

    # -------- point-in-time lookups (strictly prior) --------
    def _decayed_past_mean(self, series_by_tid, tid, when):
        rec = series_by_tid.get(int(tid))
        if rec is None:
            return None
        ds, vs = rec
        m = ds < when
        if m.sum() < MIN_PRIOR:
            return None
        age = (when - ds[m]).astype("timedelta64[D]").astype(float)
        w = np.exp(-np.log(2) * age / FORM_HL)
        return float(np.average(vs[m], weights=w))

    def form_ewma(self, tid, when):
        """(gf, ga, ppg, streak) over the last FORM_N prior matches; None if <MIN_PRIOR."""
        lst = [x for x in self.form.get(int(tid), []) if x[0] < when]
        if len(lst) < MIN_PRIOR:
            return None
        last = lst[-FORM_N:]
        gf = np.mean([x[1] for x in last]); ga = np.mean([x[2] for x in last])
        ppg = np.mean([x[3] for x in last])
        streak = np.mean([x[3] for x in last[-5:]])   # recent 5-match points rate
        return float(gf), float(ga), float(ppg), float(streak)

    def rest_days(self, tid, when):
        prior = [x[0] for x in self.form.get(int(tid), []) if x[0] < when]
        if not prior:
            return None
        gap = (when - max(prior)).astype("timedelta64[D]").astype(float)
        return float(min(max(gap, 0.0), 21.0)) / 7.0

    def h2h_gd(self, home_id, away_id, when):
        lst = [x for x in self.h2h.get(frozenset((int(home_id), int(away_id))), []) if x[0] < when]
        if not lst:
            return None
        vals, wts = [], []
        for d, gd, hid in lst:
            age = (when - d).astype("timedelta64[D]").astype(float)
            wts.append(np.exp(-np.log(2) * age / (FORM_HL * 2)))
            vals.append(gd if int(hid) == int(home_id) else -gd)   # orient to current home
        return float(np.average(vals, weights=wts))

    def stat_diff(self, field, home_id, away_id, when):
        h = self._decayed_past_mean(self.stat_series.get(field, {}), home_id, when)
        a = self._decayed_past_mean(self.stat_series.get(field, {}), away_id, when)
        return (h - a) if (h is not None and a is not None) else None

    def rating_diff(self, home_id, away_id, when):
        h = self._decayed_past_mean(self.rating_series, home_id, when)
        a = self._decayed_past_mean(self.rating_series, away_id, when)
        return (h - a) if (h is not None and a is not None) else None

    def squad_diff(self, home_id, away_id):
        h = self.squad.get(int(home_id)); a = self.squad.get(int(away_id))
        return (h - a) if (h is not None and a is not None) else None

    def _load_club_form(self):
        import pandas as pd
        # prefer the multi-season table when enabled and present; else the single 2025 snapshot
        path = CLUB_FORM_MULTI_CSV if (CLUB_FORM_MULTISEASON and CLUB_FORM_MULTI_CSV.exists()) else CLUB_FORM_CSV
        if not path.exists():
            return {}
        cf = pd.read_csv(path)
        out = {}
        for r in cf.itertuples(index=False):
            v = getattr(r, "club_form", None)
            if v is not None and str(v) != "nan":
                try:
                    out[int(r.team_id)] = float(v)
                except Exception:
                    pass
        return out

    def club_form_diff(self, home_id, away_id):
        h = self.club_form.get(int(home_id)); a = self.club_form.get(int(away_id))
        return (h - a) if (h is not None and a is not None) else None

    def _load_intl_agg(self):
        """{field: {tid: (dates, vals)}} from worldcup_intl_player_agg.csv (per team-match totals)."""
        import pandas as pd
        series = {f: defaultdict(list) for f in EXTRA_FIELDS}
        if not INTL_AGG_CSV.exists():
            return {f: {} for f in EXTRA_FIELDS}
        df = pd.read_csv(INTL_AGG_CSV)
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        for r in df.dropna(subset=["date", "team_id"]).itertuples(index=False):
            when = np.datetime64(r.date)
            for f in EXTRA_FIELDS:
                v = getattr(r, f, None)
                if v is not None and str(v) != "nan":
                    try:
                        series[f][int(r.team_id)].append((when, float(v)))
                    except Exception:
                        pass
        out = {}
        for f, by in series.items():
            out[f] = {}
            for tid, lst in by.items():
                lst.sort(key=lambda x: x[0])
                out[f][tid] = (np.array([x[0] for x in lst], "datetime64[ns]"),
                               np.array([x[1] for x in lst], float))
        return out

    def intl_agg_diff(self, field, home_id, away_id, when):
        h = self._decayed_past_mean(self.agg_series.get(field, {}), home_id, when)
        a = self._decayed_past_mean(self.agg_series.get(field, {}), away_id, when)
        return (h - a) if (h is not None and a is not None) else None


# ============================================================ feature vector (raw, pre-standardise)
def build_feature_vector(src, home_id, away_id, when, neutral,
                         l3_ph, l3_pd, l3_pa, l3_xgh, l3_xga):
    """Assemble the RAW feature dict + list of missing feature names. Strength from L3 (passed in).
    Everything else point-in-time from `src`. Missing -> None (imputed to the mean downstream)."""
    when = np.datetime64(when)
    feat = {}
    # strength (L3): logits vs draw + xg
    def logit(p, ref):
        p = min(max(float(p), 1e-6), 1 - 1e-6); ref = min(max(float(ref), 1e-6), 1 - 1e-6)
        return math.log(p / ref)
    feat["l3_logit_h"] = logit(l3_ph, l3_pd) if (l3_ph is not None and l3_pd) else None
    feat["l3_logit_a"] = logit(l3_pa, l3_pd) if (l3_pa is not None and l3_pd) else None
    feat["l3_xg_h"] = _num(l3_xgh)
    feat["l3_xg_a"] = _num(l3_xga)
    feat["neutral"] = float(neutral) if neutral is not None else None
    # form
    fh = src.form_ewma(home_id, when); fa = src.form_ewma(away_id, when)
    if fh and fa:
        feat["form_gf_diff"] = fh[0] - fa[0]
        feat["form_ga_diff"] = fh[1] - fa[1]
        feat["form_ppg_diff"] = fh[2] - fa[2]
        feat["form_streak_diff"] = fh[3] - fa[3]
    else:
        feat["form_gf_diff"] = feat["form_ga_diff"] = feat["form_ppg_diff"] = feat["form_streak_diff"] = None
    # rest / h2h / squad / rating
    rh = src.rest_days(home_id, when); ra = src.rest_days(away_id, when)
    feat["rest_diff"] = (rh - ra) if (rh is not None and ra is not None) else None
    feat["h2h_gd"] = src.h2h_gd(home_id, away_id, when)
    feat["squad_diff"] = src.squad_diff(home_id, away_id)
    feat["team_rating_diff"] = src.rating_diff(home_id, away_id, when)
    # rolling real stats
    for s in STAT_FIELDS:
        feat[f"{s}_diff"] = src.stat_diff(s, home_id, away_id, when)
    # club_form (optional 27th feature; always computed, only USED when the active artifact lists it)
    feat[CLUB_FORM_DIFF] = src.club_form_diff(home_id, away_id)
    # international per-match player aggregates (optional extra features; 0 burn-in -> ~inert)
    for x in EXTRA_FIELDS:
        feat[f"{x}_diff"] = src.intl_agg_diff(x, home_id, away_id, when)
    missing = [k for k in active_features() if feat.get(k) is None]
    return feat, missing


# ============================================================ live predictor (pure numpy over JSON)
_ARTIFACT_CACHE = {}   # path(str) -> parsed artifact


def _load_artifact(path=None):
    p = Path(path) if path is not None else active_artifact_path()
    key = str(p)
    if key not in _ARTIFACT_CACHE:
        _ARTIFACT_CACHE[key] = json.loads(p.read_text(encoding="utf-8"))
    return _ARTIFACT_CACHE[key]


_SRC_CACHE = None


def _sources():
    global _SRC_CACHE
    if _SRC_CACHE is None:
        _SRC_CACHE = Sources()
    return _SRC_CACHE


def _standardise(feat, art):
    """Standardise over the ARTIFACT'S OWN feature list (26 or 27) — the artifact is the source of
    truth for dimensionality, so predict works for either the base or the club_form model."""
    feats = art.get("features", list(FEATURES))
    mean = art["mean"]; std = art["std"]
    z = np.zeros(len(feats))
    nmiss = 0
    for i, k in enumerate(feats):
        v = feat.get(k)
        if v is None or not math.isfinite(float(v)):     # None OR non-finite -> impute-neutral (z=0)
            z[i] = 0.0; nmiss += 1
        else:
            s = std[i] if std[i] > 1e-9 else 1.0
            z[i] = (float(v) - mean[i]) / s
    return z, nmiss


def predict(home_id, away_id, when, neutral, our_home, our_draw, our_away, our_xg_home, our_xg_away):
    """LIVE full-data prediction for one fixture. Returns
    {fd_home,fd_draw,fd_away,fd_xg_home,fd_xg_away,n_features,n_missing} or None on ANY problem
    (caller then reverts to the ensemble -> delta 0). NEVER raises."""
    try:
        path = active_artifact_path()
        if not path.exists():
            return None
        art = _load_artifact(path)
        src = _sources()
        feat, _missing = build_feature_vector(src, home_id, away_id, when, neutral,
                                              our_home, our_draw, our_away, our_xg_home, our_xg_away)
        z, nmiss = _standardise(feat, art)
        # 1X2: multinomial logit + temperature
        W = np.array(art["logit_W"]); b = np.array(art["logit_b"]); T = float(art["temp"])
        logits = (z @ W + b) / max(T, 1e-6)
        p = _softmax(logits)
        p = np.clip(p, EPS, None); p = p / p.sum()
        # goals: two Poisson GLMs -> lambdas
        lh = math.exp(float(z @ np.array(art["pois_gh_w"]) + art["pois_gh_b"]))
        la = math.exp(float(z @ np.array(art["pois_ga_w"]) + art["pois_ga_b"]))
        lh = float(min(max(lh, 0.05), 6.0)); la = float(min(max(la, 0.05), 6.0))
        # final finite guard: any non-finite -> None so the caller reverts to the ensemble (delta 0)
        if not (np.all(np.isfinite(p)) and math.isfinite(lh) and math.isfinite(la)):
            return None
        return {"fd_home": round(float(p[0]), 4), "fd_draw": round(float(p[1]), 4),
                "fd_away": round(float(p[2]), 4),
                "fd_xg_home": round(lh, 2), "fd_xg_away": round(la, 2),
                "n_features": len(art.get("features", FEATURES)), "n_missing": int(nmiss)}
    except Exception:
        return None


# ============================================================ offline trainer + A/B (read-only)
def _l3_recipe(ir_frame, sup, burn):
    """Reconstruct the production-family L3 per-match probs+xg from sup_pre_l3 (same recipe as the
    bake-off champion): margin a0+a1*sup (lstsq/burn), matchup total, Poisson score matrix. Used
    ONLY to build the strength FEATURE in training; live strength comes from the shipped L3."""
    import model_bakeoff_backtest as bo
    import l3_offline
    ghf = ir_frame["gh"].to_numpy(float); gaf = ir_frame["ga"].to_numpy(float)
    Ab = np.c_[np.ones(int(burn.sum())), sup[burn]]
    a0, a1 = map(float, np.linalg.lstsq(Ab, (ghf - gaf)[burn], rcond=None)[0])
    sb = sup[burn]
    tb = np.linalg.lstsq(np.c_[np.ones(len(sb)), np.abs(sb), sb ** 2], (ghf + gaf)[burn], rcond=None)[0]
    tb0, tb1, tb2 = map(float, tb)
    TCAP = float(l3_offline.TOTAL_CAP)
    ph = np.zeros(len(sup)); pd_ = np.zeros(len(sup)); pa = np.zeros(len(sup))
    xh = np.zeros(len(sup)); xa = np.zeros(len(sup))
    for i in range(len(sup)):
        margin = a0 + a1 * sup[i]
        total = min(tb0 + tb1 * abs(sup[i]) + tb2 * sup[i] ** 2, TCAP)
        lh = max(0.05, (total + margin) / 2); la = max(0.05, (total - margin) / 2)
        P, _o, _b = bo.matrix_to_markets(bo.score_matrix(lh, la))
        ph[i], pd_[i], pa[i], xh[i], xa[i] = P[0], P[1], P[2], lh, la
    return ph, pd_, pa, xh, xa, (a0, a1, tb0, tb1, tb2, TCAP)


def train(report=True, feats=None, out_path=None, reg=None):
    """Fit the regularized full-data model on the international frame over the feature list `feats`
    (default = base 26) with regularization `reg` (default FULL_DATA_REG), save to `out_path`
    (default ARTIFACT), and print an HONEST OOS A/B vs L3. Returns OOS fd probs + metrics + coefs."""
    feats = list(feats) if feats is not None else list(FEATURES)
    out_path = out_path if out_path is not None else ARTIFACT
    reg = reg if reg is not None else FULL_DATA_REG
    import pandas as pd
    from sklearn.linear_model import LogisticRegression, PoissonRegressor
    import model_bakeoff_backtest as bo
    import national_elo_layer3 as L3

    src = _sources()
    ir = src.ir.copy()
    pm = pd.read_csv(PM)
    sup_by = {int(r.fixture_id): float(r.sup_pre_l3) for r in pm.itertuples(index=False)
              if pd.notna(r.sup_pre_l3)}
    imp = {t: L3.IMP_BY_TAG.get(t, 0.8) for t in ir["league_tag"].unique()}

    CAL_START = bo.CAL_START; OOS_LO, OOS_HI = bo.OOS_LO, bo.OOS_HI
    ir = ir[ir["date"] >= pd.Timestamp(CAL_START)].copy()
    ir = ir[ir["fixture_id"].map(lambda f: int(f) in sup_by)].reset_index(drop=True)
    sup = ir["fixture_id"].map(lambda f: sup_by[int(f)]).to_numpy(float)
    dates = ir["date"].to_numpy("datetime64[ns]")
    burn = (dates >= np.datetime64(CAL_START)) & (dates < np.datetime64(OOS_LO))
    oos = (dates >= np.datetime64(OOS_LO)) & (dates < np.datetime64(OOS_HI))
    ghf = ir["gh"].to_numpy(float); gaf = ir["ga"].to_numpy(float)
    res = np.where(ghf > gaf, 0, np.where(ghf == gaf, 1, 2))
    imparr = ir["league_tag"].map(lambda t: imp.get(t, 0.8)).to_numpy(float)

    l3ph, l3pd, l3pa, l3xh, l3xa, l3coef = _l3_recipe(ir, sup, burn)

    # build raw feature matrix over `feats`
    n = len(ir)
    raw = np.full((n, len(feats)), np.nan)
    for i in range(n):
        feat, _m = build_feature_vector(
            src, int(ir.home_id[i]), int(ir.away_id[i]), dates[i], int(ir.neutral[i]),
            l3ph[i], l3pd[i], l3pa[i], l3xh[i], l3xa[i])
        for j, k in enumerate(feats):
            v = feat.get(k)
            if v is not None:
                raw[i, j] = v
    # standardisation stats from BURN-IN only (no target leakage). For features with NO burn-in
    # coverage (e.g. the intl player aggregates, all 2024+), burn-in mean/std are degenerate; fall
    # back to FULL-SAMPLE mean/std for SCALING ONLY (keeps live z in a sane range; not target info).
    mean_b = np.nanmean(raw[burn], axis=0); std_b = np.nanstd(raw[burn], axis=0)
    mean_f = np.nanmean(raw, axis=0); std_f = np.nanstd(raw, axis=0)
    degen = ~(np.isfinite(std_b) & (std_b > 1e-9))
    mean = np.where(degen, mean_f, mean_b)
    std = np.where(degen, std_f, std_b)
    mean = np.where(np.isfinite(mean), mean, 0.0)
    std = np.where(np.isfinite(std) & (std > 1e-9), std, 1.0)
    Z = (np.where(np.isfinite(raw), raw, mean) - mean) / std   # impute-neutral then standardise

    # decayed sample weights on burn-in
    age = (np.datetime64(OOS_LO) - dates[burn]) / np.timedelta64(1, "D")
    w = imparr[burn] * np.exp(-np.log(2) * age / float(L3.HL_DAYS))

    # 1X2: multinomial logit with the SELECTED regularization (FULL_DATA_REG). L1 zeroes null feats.
    rc = _reg_config(reg)
    clf = LogisticRegression(**rc)
    clf.fit(Z[burn], res[burn], sample_weight=w)
    classes = list(clf.classes_)
    W = np.zeros((len(feats), 3)); b = np.zeros(3)
    for j, c in enumerate(classes):
        W[:, c] = clf.coef_[j]; b[c] = clf.intercept_[j]

    # temperature: 1-D search minimising burn-in logloss (mild in-sample calibration)
    base_logits = Z[burn] @ W + b
    Yb = np.eye(3)[res[burn]]
    best_T, best_ll = 1.0, 1e18
    for T in np.linspace(0.6, 2.5, 39):
        P = np.array([_softmax(row / T) for row in base_logits])
        P = np.clip(P, EPS, None); P /= P.sum(1, keepdims=True)
        ll = -np.sum(Yb * np.log(P)) / len(P)
        if ll < best_ll:
            best_ll, best_T = ll, T

    # goals: two Poisson GLMs (strong alpha)
    pgh = PoissonRegressor(alpha=1.0, max_iter=1000).fit(Z[burn], ghf[burn], sample_weight=w)
    pga = PoissonRegressor(alpha=1.0, max_iter=1000).fit(Z[burn], gaf[burn], sample_weight=w)

    art = {
        "features": feats, "mean": mean.tolist(), "std": std.tolist(),
        "logit_W": W.tolist(), "logit_b": b.tolist(), "temp": float(best_T),
        "pois_gh_w": pgh.coef_.tolist(), "pois_gh_b": float(pgh.intercept_),
        "pois_ga_w": pga.coef_.tolist(), "pois_ga_b": float(pga.intercept_),
        "l3_recipe": {"a0": l3coef[0], "a1": l3coef[1], "tb0": l3coef[2], "tb1": l3coef[3],
                      "tb2": l3coef[4], "tcap": l3coef[5]},
        "trained_on": {"n_burn": int(burn.sum()), "n_oos": int(oos.sum()),
                       "cal_start": CAL_START, "oos": [OOS_LO, OOS_HI]},
        "reg": reg, "penalty": rc.get("penalty"), "C": rc.get("C"),
        "n_zero_feats": int((np.sqrt((W ** 2).sum(1)) < 1e-6).sum()),
        "poisson_alpha": 1.0, "form_hl": FORM_HL,
        "note": "Full-data model. Matches the ensemble/L3 at best (L1 reg). NOT a precision claim.",
    }
    out_path.write_text(json.dumps(art, indent=1), encoding="utf-8")
    _ARTIFACT_CACHE.pop(str(out_path), None)   # invalidate any cached copy

    # ---- HONEST OOS A/B: this model vs L3 baseline (ensemble ~= L3 for internationals: no live mx) ----
    fd = np.array([[*(_softmax((Z[i] @ W + b) / best_T))] for i in range(n)])
    fd = np.clip(fd, EPS, None); fd = fd / fd.sum(1, keepdims=True)
    l3 = np.column_stack([l3ph, l3pd, l3pa]); l3 = np.clip(l3, EPS, None); l3 /= l3.sum(1, keepdims=True)
    Yo = np.eye(3)[res[oos]]
    ll_fd = bo.ll_multi(fd[oos], Yo); ll_l3 = bo.ll_multi(l3[oos], Yo)
    d = ll_l3 - ll_fd     # >0 would mean full-data BETTER; expected NEGATIVE
    lo, hi, p = bo.paired_boot(d)
    if report:
        print("=" * 92)
        nz = int((np.sqrt((W ** 2).sum(1)) < 1e-6).sum())
        print(f"FULL-DATA MODEL trained ({len(feats)} feats, reg={reg}, {nz} feats a peso~0). OOS A/B vs L3")
        print("=" * 92)
        print(f"features ingested: {len(feats)}  |  burn-in {int(burn.sum())}  OOS {int(oos.sum())}")
        print(f"1X2 logloss  full-data={ll_fd.mean():.4f}   L3={ll_l3.mean():.4f}")
        print(f"Delta(L3 - full-data)={d.mean():+.4f}  CI95[{lo:+.4f},{hi:+.4f}]  p(fd better)={p:.2f}")
        verdict = ("full-data WORSE (as expected)" if hi < 0 else
                   "full-data better" if lo > 0 else "no clear difference")
        print(f"VERDICT: {verdict}. NO precision claim.")
        print(f"artifact -> {out_path}")
    return {"ll_fd": float(ll_fd.mean()), "ll_l3": float(ll_l3.mean()),
            "delta": float(d.mean()), "ci": [lo, hi], "p": p, "n_oos": int(oos.sum()),
            "n_features": len(feats), "fd_oos": fd[oos], "Yo": Yo}


def train_all():
    """Train BOTH artifacts (base 26 + club_form 27) and report the honest 26-vs-27 marginal A/B.

    CAVEAT (leakage): we hold a SINGLE 2025 club-form snapshot, so applying it to 2024/2025 OOS
    internationals is mild look-ahead (a near-static per-team strength constant). This offline number
    is therefore INDICATIVE and FAVOURABLE to club_form; if it STILL fails to help, that is strong
    evidence of redundancy with L3. The real, leak-free test is the LIVE A/B on the World Cup."""
    import model_bakeoff_backtest as bo
    base = train(report=True, feats=list(FEATURES), out_path=ARTIFACT)
    cf = train(report=True, feats=list(FEATURES_CF), out_path=ARTIFACT_CF)
    ex = train(report=True, feats=list(FEATURES_EXTRA), out_path=ARTIFACT_EXTRA)

    def ab(a, b, la, lb, note):
        d = bo.ll_multi(a["fd_oos"], a["Yo"]) - bo.ll_multi(b["fd_oos"], b["Yo"])
        lo, hi, p = bo.paired_boot(d)   # >0 => model b better than a
        verdict = ("b ADDS signal (CI>0)" if lo > 0 else "b WORSE (CI<0)" if hi < 0
                   else "NULL/redundant (CI cruza 0)")
        print("\n" + "=" * 92)
        print(f"MARGINAL A/B — {note}, OOS 1X2 logloss")
        print("=" * 92)
        print(f"{la}={a['ll_fd']:.4f}   {lb}={b['ll_fd']:.4f}")
        print(f"Delta({la} - {lb})={d.mean():+.4f}  CI95[{lo:+.4f},{hi:+.4f}]  p({lb} better)={p:.2f}")
        print(f"VERDICT: {verdict}")

    ab(base, cf, "base(26)", "+club_form(27)",
       "club_form(multi-season 25/24/23) vs base (INDICATIVE: static per-team value -> mild look-ahead on OOS)")
    ab(cf, ex, "+club_form(27)", "+player-agg(31)",
       "intl player-agg vs club_form — 0 burn-in coverage so EXPECTED INERT")
    print("\nReal validation is LIVE only (worldcup_full_data_ab_scorer). NO precision claim.")


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["train", "train-clubform", "train-extra", "train-all",
                                    "features", "predict-demo"])
    a = ap.parse_args()
    if a.cmd == "train":
        train(feats=list(FEATURES), out_path=ARTIFACT)
    elif a.cmd == "train-clubform":
        train(feats=list(FEATURES_CF), out_path=ARTIFACT_CF)
    elif a.cmd == "train-extra":
        train(feats=list(FEATURES_EXTRA), out_path=ARTIFACT_EXTRA)
    elif a.cmd == "train-all":
        train_all()
    elif a.cmd == "features":
        fs = active_features()
        print("\n".join(f"{i+1:2d}. {f}" for i, f in enumerate(fs)))
        print(f"TOTAL active features (CLUB_FORM_FEATURE={CLUB_FORM_FEATURE}): {len(fs)}")
    elif a.cmd == "predict-demo":
        r = predict(10, 8, "2026-06-25", 1, 0.45, 0.28, 0.27, 1.4, 1.1)
        print(json.dumps(r, indent=1))
