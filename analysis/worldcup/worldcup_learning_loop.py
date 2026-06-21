"""
WORLD CUP 2026 - LEARNING LOOP (ISOLATED, analysis/worldcup/ only).

Closes the feedback loop for the shadow World Cup product. Three offline-friendly
subcommands, run once per pipeline pass:

PURIFIED: evaluation is L3 (and v2) against REAL results + a naive base-rate baseline.
ZERO market/odds anywhere.

  log       Append today's per-match predictions (L3 / v2 / xG / top score) to
            worldcup_predictions_log.csv, DEDUP by fixture_id (keeps the FIRST = locks
            the pre-match prediction, no hindsight). Source: worldcup_cards.csv
            (+ worldcup_our_model_v2_predictions.csv for v2). NO API. NO odds.

  settle    For FINISHED fixtures only, attach the real result to the log. Reuses the
            SAME cached /fixtures(league=1,season=2026) call the card builder already
            made (6h TTL) -> ~0 marginal API. No per-fixture calls. 1X2 settled on the
            90' score (score.fulltime).

  scorecard Over RESOLVED fixtures, score our models (L3, v2) against REAL results and
            a base-rate baseline: log-loss, Brier, Brier-skill vs base-rate, 1X2 hit%,
            ECE, per-bet Over2.5/BTTS, reliability, xG goal error, L3-vs-base head-to-
            head -> worldcup_scorecard.txt (first lines = compact Telegram block).
            Includes a base-rate shrinkage PROPOSAL but NEVER applies it. NO market.

NOT production (WC league id 1 is rejected by the production allowlist). No .env edits,
no betting logic, no auto-execution.
"""
from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

OUT_DIR = Path(__file__).resolve().parent
CARDS = OUT_DIR / "worldcup_cards.csv"
V2 = OUT_DIR / "worldcup_our_model_v2_predictions.csv"
LOG = OUT_DIR / "worldcup_predictions_log.csv"
SCORECARD = OUT_DIR / "worldcup_scorecard.txt"
GAPS = OUT_DIR / "worldcup_gaps.txt"   # finished-before-logged coverage gaps (dedup by fixture)
KMAX = 10
EPS = 1e-15
FINISHED = {"FT", "AET", "PEN"}

LOG_COLUMNS = [
    "fixture_id", "kickoff_utc", "home", "away", "round",
    "l3_home", "l3_draw", "l3_away", "l3_xg_home", "l3_xg_away", "l3_top_score",
    "v2_home", "v2_draw", "v2_away",
    "st_corners_total", "st_corners_over", "st_corners_line", "st_cards_total", "st_shots_total",
    "logged_at_utc",
    "result_ft_gh", "result_ft_ga", "result_final_gh", "result_final_ga",
    "result_corners", "result_cards", "result_shots",
    "result_1x2", "result_status", "settled", "settled_at_utc",
]

# /fixtures/statistics type -> stat key (for settling real corners/cards/shots)
STAT_TYPE_MAP = {"Corner Kicks": "corners", "Yellow Cards": "yellow", "Red Cards": "red",
                 "Total Shots": "shots"}
SMALL_N = 30  # below this, metrics are flagged "muestra pequeña, orientativo"

# National-team confederation (public fact, not invented data) for the WC-2026 48 teams.
# Used only for the cross-confederation breakdown of the L3-vs-base-rate head-to-head.
CONF_BY_TEAM = {
    # UEFA
    "Austria": "UEFA", "Belgium": "UEFA", "Bosnia & Herzegovina": "UEFA", "Croatia": "UEFA",
    "Czechia": "UEFA", "England": "UEFA", "France": "UEFA", "Germany": "UEFA",
    "Netherlands": "UEFA", "Norway": "UEFA", "Portugal": "UEFA", "Scotland": "UEFA",
    "Spain": "UEFA", "Sweden": "UEFA", "Switzerland": "UEFA", "Türkiye": "UEFA",
    # CONMEBOL
    "Argentina": "CONMEBOL", "Brazil": "CONMEBOL", "Colombia": "CONMEBOL", "Ecuador": "CONMEBOL",
    "Paraguay": "CONMEBOL", "Uruguay": "CONMEBOL",
    # CONCACAF
    "Canada": "CONCACAF", "Curaçao": "CONCACAF", "Haiti": "CONCACAF", "Mexico": "CONCACAF",
    "Panama": "CONCACAF", "USA": "CONCACAF",
    # CAF
    "Algeria": "CAF", "Cape Verde Islands": "CAF", "Congo DR": "CAF", "Egypt": "CAF",
    "Ghana": "CAF", "Ivory Coast": "CAF", "Morocco": "CAF", "Senegal": "CAF",
    "South Africa": "CAF", "Tunisia": "CAF",
    # AFC
    "Australia": "AFC", "Iran": "AFC", "Iraq": "AFC", "Japan": "AFC", "Jordan": "AFC",
    "Qatar": "AFC", "Saudi Arabia": "AFC", "South Korea": "AFC", "Uzbekistan": "AFC",
    # OFC
    "New Zealand": "OFC",
}


def now_iso():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _parse_ko(s):
    """Parse kickoff_utc 'YYYY-MM-DD HH:MM' (treated as UTC). None if unparseable/NaN."""
    if s is None or (isinstance(s, float) and pd.isna(s)):
        return None
    try:
        return datetime.strptime(str(s).strip()[:16], "%Y-%m-%d %H:%M").replace(tzinfo=timezone.utc)
    except Exception:
        return None


def _record_gaps(gap_rows):
    """Dedup-append coverage gaps to worldcup_gaps.txt. Idempotent by fixture_id (lock-first,
    like the log). NO API, NO Telegram -- just a human-readable record of fixtures that
    finished before they were ever logged. NEVER backfilled with a known result."""
    if not gap_rows:
        return 0
    cols = ["fixture_id", "kickoff_utc", "home", "away", "round", "detected_at_utc", "reason"]
    prev = pd.read_csv(GAPS) if GAPS.exists() else pd.DataFrame(columns=cols)
    known = set(prev["fixture_id"].dropna().astype(int)) if len(prev) else set()
    fresh = [g for g in gap_rows if int(g["fixture_id"]) not in known]
    if not fresh:
        return 0
    out = pd.concat([prev, pd.DataFrame(fresh)], ignore_index=True)[cols]
    out.to_csv(GAPS, index=False)
    return len(fresh)


def pmf(lam, k=KMAX):
    ks = np.arange(k + 1)
    logf = np.concatenate([[0.0], np.cumsum(np.log(np.arange(1, k + 1)))])
    return np.exp(ks * np.log(max(lam, 1e-9)) - lam - logf)


def top_scoreline(xgh, xga):
    if pd.isna(xgh) or pd.isna(xga):
        return ""
    M = np.outer(pmf(float(xgh)), pmf(float(xga)))
    M /= M.sum()
    i, j = np.unravel_index(int(M.argmax()), M.shape)
    return f"{i}-{j}"


def _empty_log():
    return pd.DataFrame(columns=LOG_COLUMNS)


def _read_log():
    if LOG.exists():
        df = pd.read_csv(LOG)
        for c in LOG_COLUMNS:
            if c not in df.columns:
                df[c] = np.nan
        return df[LOG_COLUMNS]
    return _empty_log()


# ----------------------------------------------------------------- log
def cmd_log():
    if not CARDS.exists():
        print(f"learning_loop log: missing {CARDS}; nothing to log.")
        return
    cards = pd.read_csv(CARDS)
    v2map = {}
    if V2.exists():
        for _, r in pd.read_csv(V2).iterrows():
            v2map[int(r["fixture_id"])] = r

    log = _read_log()
    known = set(log["fixture_id"].dropna().astype(int)) if len(log) else set()

    new_rows = []
    gap_rows = []
    for _, r in cards.iterrows():
        if pd.isna(r.get("fixture_id")):
            continue
        fid = int(r["fixture_id"])
        if fid in known:
            continue  # lock-first: never overwrite a pre-match prediction
        # only log fixtures that actually carry our L3 forecast
        if pd.isna(r.get("our_home")):
            continue
        # anti-hindsight guard: never log a fixture whose kickoff already passed (it would
        # capture the prediction with the match underway, breaking the pre-match guarantee).
        # If it was also never logged pre-KO, that is a genuine coverage gap -> record it.
        ko = _parse_ko(r.get("kickoff_utc"))
        if ko is not None and ko < datetime.now(timezone.utc):
            gap_rows.append({
                "fixture_id": fid, "kickoff_utc": r.get("kickoff_utc"),
                "home": r.get("home"), "away": r.get("away"), "round": r.get("round"),
                "detected_at_utc": now_iso(),
                "reason": "kickoff_passed_before_first_log",
            })
            continue
        v2 = v2map.get(fid)
        row = {
            "fixture_id": fid, "kickoff_utc": r.get("kickoff_utc"),
            "home": r.get("home"), "away": r.get("away"), "round": r.get("round"),
            "l3_home": r.get("our_home"), "l3_draw": r.get("our_draw"),
            "l3_away": r.get("our_away"), "l3_xg_home": r.get("our_xg_home"),
            "l3_xg_away": r.get("our_xg_away"),
            "l3_top_score": top_scoreline(r.get("our_xg_home"), r.get("our_xg_away")),
            "v2_home": (v2["v2_home"] if v2 is not None else np.nan),
            "v2_draw": (v2["v2_draw"] if v2 is not None else np.nan),
            "v2_away": (v2["v2_away"] if v2 is not None else np.nan),
            "st_corners_total": r.get("st_corners_total"), "st_corners_over": r.get("st_corners_over"),
            "st_corners_line": r.get("st_corners_line"), "st_cards_total": r.get("st_cards_total"),
            "st_shots_total": r.get("st_shots_total"),
            "logged_at_utc": now_iso(),
            "result_ft_gh": np.nan, "result_ft_ga": np.nan,
            "result_final_gh": np.nan, "result_final_ga": np.nan,
            "result_1x2": np.nan, "result_status": np.nan,
            "settled": 0, "settled_at_utc": np.nan,
        }
        new_rows.append(row)
        known.add(fid)

    if new_rows:
        log = pd.concat([log, pd.DataFrame(new_rows)], ignore_index=True)[LOG_COLUMNS]
    log.to_csv(LOG, index=False)
    n_gaps = _record_gaps(gap_rows)
    print(f"learning_loop log: +{len(new_rows)} new, {len(log)} total -> {LOG}"
          + (f" | {n_gaps} gap(s) flagged -> {GAPS}" if n_gaps else ""))


# ----------------------------------------------------------------- settle
def cmd_settle():
    log = _read_log()
    if not len(log):
        print("learning_loop settle: empty log; nothing to settle.")
        return

    ROOT = OUT_DIR.parents[1]
    sys.path.insert(0, str(ROOT / "scripts"))
    from api_football_client import APIFootballClient, APIFootballError  # noqa: E402

    c = APIFootballClient()

    def quota():
        try:
            return ((c.request("/status", None, ttl_hours=0, force_refresh=True)
                     .get("response", {}) or {}).get("requests") or {}).get("current")
        except Exception:
            return None

    def stat_totals(fid):
        """Real corners/cards/shots TOTALS (home+away) via /fixtures/statistics. None if n/a."""
        try:
            resp = c.fixture_statistics(fid).get("response", []) or []
        except Exception:
            return None
        tot = {"corners": 0.0, "cards": 0.0, "shots": 0.0}
        seen = False
        for t in resp:
            d = {}
            for s in t.get("statistics", []) or []:
                col = STAT_TYPE_MAP.get(s.get("type"))
                if col:
                    v = s.get("value")
                    if isinstance(v, str):
                        v = v.strip().rstrip("%") or None
                    try:
                        d[col] = float(v) if v is not None else None
                    except Exception:
                        d[col] = None
            if d:
                seen = True
                tot["corners"] += d.get("corners") or 0
                tot["cards"] += (d.get("yellow") or 0) + (d.get("red") or 0)
                tot["shots"] += d.get("shots") or 0
        return tot if seen else None

    q0 = quota()
    try:
        # SAME cached call the card builder makes (6h TTL) -> ~0 marginal cost.
        fx = c.fixtures(league=1, season=2026).get("response", []) or []
    except APIFootballError as e:
        print(f"learning_loop settle: fixtures error ({e}); skipping (fail-soft).")
        return

    results = {}
    for f in fx:
        st = (f.get("fixture", {}).get("status") or {}).get("short")
        if st not in FINISHED:
            continue
        fid = f.get("fixture", {}).get("id")
        goals = f.get("goals") or {}
        score = f.get("score") or {}
        ft = score.get("fulltime") or {}
        gh90 = ft.get("home") if ft.get("home") is not None else goals.get("home")
        ga90 = ft.get("away") if ft.get("away") is not None else goals.get("away")
        if gh90 is None or ga90 is None:
            continue
        res = "H" if gh90 > ga90 else ("D" if gh90 == ga90 else "A")
        results[int(fid)] = {
            "result_ft_gh": gh90, "result_ft_ga": ga90,
            "result_final_gh": goals.get("home"), "result_final_ga": goals.get("away"),
            "result_1x2": res, "result_status": st,
        }

    # columns that hold strings must be object dtype (empty cols load as float64)
    for col in ("result_1x2", "result_status", "settled_at_utc"):
        log[col] = log[col].astype(object)

    newly = stats_got = 0
    for idx, r in log.iterrows():
        fid = int(r["fixture_id"])
        if int(r.get("settled") or 0) == 1:
            continue
        if fid in results:
            for k, v in results[fid].items():
                log.at[idx, k] = v
            # settle REAL corners/cards/shots totals (1 bounded /fixtures/statistics call)
            stt = stat_totals(fid)
            if stt:
                log.at[idx, "result_corners"] = stt["corners"]
                log.at[idx, "result_cards"] = stt["cards"]
                log.at[idx, "result_shots"] = stt["shots"]
                stats_got += 1
            log.at[idx, "settled"] = 1
            log.at[idx, "settled_at_utc"] = now_iso()
            newly += 1

    log.to_csv(LOG, index=False)
    q1 = quota()
    spend = (q1 - q0) if (q0 is not None and q1 is not None) else "n/a"
    nset = int((log["settled"].fillna(0).astype(int) == 1).sum())
    print(f"learning_loop settle: +{newly} newly settled ({stats_got} w/ real stats), {nset} total. "
          f"API spend this step: {spend} (fixtures cached + {newly} stat calls). quota now: {q1}")


# ----------------------------------------------------------------- scorecard
def _probs(df, prefix):
    cols = [f"{prefix}_home", f"{prefix}_draw", f"{prefix}_away"]
    if not all(c in df.columns for c in cols):
        return None
    P = df[cols].to_numpy(float)
    return P


def _metrics(P, Y):
    Pc = np.clip(P, EPS, 1.0)
    Pc = Pc / Pc.sum(1, keepdims=True)
    ll = float(-np.mean(np.sum(Y * np.log(Pc), axis=1)))
    brier = float(np.mean(np.sum((Pc - Y) ** 2, axis=1)))
    acc = float(np.mean(Pc.argmax(1) == Y.argmax(1)))
    # ECE on the max-prob (confidence) reliability
    conf = Pc.max(1)
    correct = (Pc.argmax(1) == Y.argmax(1)).astype(float)
    edges = np.linspace(0, 1, 11)
    ece = 0.0
    for i in range(10):
        m = (conf > edges[i]) & (conf <= edges[i + 1])
        if m.sum():
            ece += m.sum() / len(Pc) * abs(conf[m].mean() - correct[m].mean())
    return {"logloss": ll, "brier": brier, "acc": acc, "ece": float(ece)}


def _binary_metrics(p, y):
    """acc / Brier / log-loss for a binary probability p vs outcome y in {0,1}."""
    p = np.clip(np.asarray(p, float), EPS, 1 - EPS)
    y = np.asarray(y, float)
    acc = float(np.mean((p >= 0.5).astype(int) == y))
    brier = float(np.mean((p - y) ** 2))
    ll = float(-np.mean(y * np.log(p) + (1 - y) * np.log(1 - p)))
    return acc, brier, ll


def _pois_over25(lh, la):
    """P(total goals > 2.5) for independent Poisson xG; total ~ Poisson(lh+la)."""
    lam = max(float(lh) + float(la), 1e-9)
    p012 = np.exp(-lam) * (1.0 + lam + lam * lam / 2.0)
    return float(1.0 - p012)


def _pois_btts(lh, la):
    """P(both teams score) = (1-P(home=0))*(1-P(away=0)) for independent Poisson."""
    return float((1.0 - np.exp(-max(float(lh), 1e-9))) * (1.0 - np.exp(-max(float(la), 1e-9))))


def _small(n):
    return "  (muestra pequeña, orientativo)" if n < SMALL_N else ""


def _reliability(p, y, label):
    """Reliability table: bin flattened probs into bands, predicted vs observed freq."""
    p = np.asarray(p, float)
    y = np.asarray(y, float)
    m = ~np.isnan(p)
    p, y = p[m], y[m]
    lines = [f"  {label} (1X2 aplanado H/D/A, n_pred={len(p)}){_small(len(p) / 3)}:"]
    lines.append(f"    {'banda':>8} {'n':>4} {'predicho':>9} {'real':>6}")
    for lo, hi in [(0.0, 0.2), (0.2, 0.4), (0.4, 0.6), (0.6, 0.8), (0.8, 1.0001)]:
        mm = (p >= lo) & (p < hi)
        if mm.sum() == 0:
            continue
        hi_lbl = min(hi, 1.0)
        lines.append(f"    {int(lo*100):>3}-{int(hi_lbl*100):<3}% {int(mm.sum()):>4} "
                     f"{p[mm].mean()*100:>8.0f}% {y[mm].mean()*100:>5.0f}%")
    return lines


def cmd_scorecard():
    log = _read_log()
    settled = log[log["settled"].fillna(0).astype(int) == 1].copy() if len(log) else log
    settled = settled[settled["result_1x2"].isin(["H", "D", "A"])].copy()

    lines = []

    def out(s=""):
        lines.append(s)

    n = len(settled)
    date_tag = now_iso()[:10]
    if n == 0:
        out(f"📊 Track record Mundial: aún sin partidos resueltos ({date_tag}).")
        out("")
        out("===== detalle =====")
        out("0 partidos liquidados todavía; el scorecard se llenará tras los primeros resultados.")
        SCORECARD.write_text("\n".join(lines), encoding="utf-8")
        print(f"learning_loop scorecard: 0 resolved -> {SCORECARD}")
        return

    res_idx = {"H": 0, "D": 1, "A": 2}
    y = settled["result_1x2"].map(res_idx).to_numpy(int)
    Y = np.eye(3)[y]

    # NAIVE BASELINE: base-rate = empirical H/D/A frequencies of the resolved set.
    base = np.bincount(y, minlength=3) / n
    Pbase = np.tile(base, (n, 1))
    base_m = _metrics(Pbase, Y)

    predictors = [("L3", "l3"), ("v2", "v2")]   # own models only — NO market
    metrics = {}
    for label, pref in predictors:
        P = _probs(settled, pref)
        if P is None:
            continue
        mask = ~np.isnan(P).any(axis=1)
        if mask.sum() == 0:
            continue
        metrics[label] = {"m": _metrics(P[mask], Y[mask]), "n": int(mask.sum()),
                          "P": P, "mask": mask}

    # Brier-skill vs the NAIVE BASE-RATE (positive = better than base-rate). No market.
    skill = {}
    for label in metrics:
        common = metrics[label]["mask"]
        bb = _metrics(Pbase[common], Y[common])["brier"]
        bx = _metrics(metrics[label]["P"][common], Y[common])["brier"]
        skill[label] = (1.0 - bx / bb) if bb > 0 else 0.0

    # ---- compact Telegram block (first lines, ≤3) ----
    acc_bits = " · ".join(f"{lab} {metrics[lab]['m']['acc']*100:.0f}%"
                          for lab, _ in predictors if lab in metrics)
    out(f"📊 Track record ({n} resueltos · {date_tag})")
    out(f"Acierto 1X2: {acc_bits}" if acc_bits else "Acierto 1X2: (sin predicciones)")
    sk_bits = " · ".join(f"{lab} {skill[lab]*100:+.0f}%" for lab, _ in predictors if lab in skill)
    if sk_bits:
        out(f"Brier-skill vs base-rate: {sk_bits}")
    out("")
    out("===== detalle =====")
    out(f"resueltos={n} | 1X2 a 90' (score.fulltime) | métricas vs RESULTADOS REALES, sin mercado")
    hdr = f"{'predictor':10} {'n':>3} {'logloss':>8} {'brier':>7} {'acc%':>6} {'ECE':>6} {'Skill_base%':>11}"
    out(hdr)
    out("-" * len(hdr))
    out(f"{'base-rate':10} {n:>3} {base_m['logloss']:>8.4f} {base_m['brier']:>7.4f} "
        f"{base_m['acc']*100:>6.1f} {base_m['ece']:>6.3f} {'0.0':>11}")
    for label, _ in predictors:
        if label not in metrics:
            out(f"{label:10} {'-':>3}  (sin predicciones)")
            continue
        m = metrics[label]["m"]
        sk = skill.get(label)
        sk_s = f"{sk*100:+.1f}" if sk is not None else "n/a"
        out(f"{label:10} {metrics[label]['n']:>3} {m['logloss']:>8.4f} {m['brier']:>7.4f} "
            f"{m['acc']*100:>6.1f} {m['ece']:>6.3f} {sk_s:>11}")
    out(f"  (1X2 multiclase H/D/A; baseline ingenuo = base-rate.{_small(n)})")

    # real binary outcomes derived from the 90' score
    gh = settled["result_ft_gh"].to_numpy(float)
    ga = settled["result_ft_ga"].to_numpy(float)
    total = gh + ga
    real_over = (total >= 3).astype(int)                 # Over 2.5
    real_btts = ((gh >= 1) & (ga >= 1)).astype(int)      # both teams score
    lxh = settled["l3_xg_home"].to_numpy(float)
    lxa = settled["l3_xg_away"].to_numpy(float)
    xg_ok = ~(np.isnan(lxh) | np.isnan(lxa))
    l3_over = np.array([_pois_over25(lxh[i], lxa[i]) if xg_ok[i] else np.nan for i in range(n)])
    l3_btts = np.array([_pois_btts(lxh[i], lxa[i]) if xg_ok[i] else np.nan for i in range(n)])

    def mrow(lbl, p, yv):
        p = np.asarray(p, float)
        mk = ~np.isnan(p)
        if mk.sum() == 0:
            return f"    {lbl:18} n/d"
        a, b, l = _binary_metrics(p[mk], np.asarray(yv, float)[mk])
        return f"    {lbl:18} n={int(mk.sum()):>3}  acc {a*100:4.0f}%  Brier {b:.3f}  logloss {l:.3f}"

    # ---- (1) derived binary bets: L3 (Poisson xG) vs base-rate — Over2.5 & BTTS. NO odds ----
    base_over = np.full(n, float(real_over.mean()))
    base_btts = np.full(n, float(real_btts.mean()))
    out("")
    out("--- (1) APUESTAS DERIVADAS — L3 (Poisson xG) vs base-rate (Over2.5, BTTS) ---")
    out(f"  Over 2.5  (real Over={real_over.mean()*100:.0f}%):")
    out(mrow("L3 (Poisson xG)", l3_over, real_over))
    out(mrow("base-rate", base_over, real_over))
    out(f"  BTTS      (real Yes={real_btts.mean()*100:.0f}%):")
    out(mrow("L3 (Poisson xG)", l3_btts, real_btts))
    out(mrow("base-rate", base_btts, real_btts))

    # ---- (2) calibration / reliability (L3, v2) ----
    out("")
    out("--- (2) CALIBRACIÓN / reliability (predicho vs frecuencia real por banda) ---")
    for lab in ("L3", "v2"):
        if lab in metrics:
            for ln in _reliability(metrics[lab]["P"], Y, lab):
                out(ln)

    # ---- (3) goal error: L3 xG MAE vs tournament-mean baseline ----
    out("")
    out("--- (3) ERROR DE GOLES — L3 xG vs goles reales (MAE; baseline = media torneo) ---")
    if xg_ok.sum():
        nh = int(xg_ok.sum())
        bh, ba, bt = gh[xg_ok].mean(), ga[xg_ok].mean(), total[xg_ok].mean()
        out(f"  n={nh}{_small(nh)}  baseline = media torneo (home {bh:.2f}, away {ba:.2f}, total {bt:.2f})")
        out(f"    {'':6} {'L3 MAE':>8} {'base MAE':>9} {'mejora':>8}")
        for nm, l3v, base_v in [("home", lxh[xg_ok], bh), ("away", lxa[xg_ok], ba),
                                ("total", (lxh + lxa)[xg_ok], bt)]:
            real = {"home": gh, "away": ga, "total": total}[nm][xg_ok]
            l3mae = float(np.mean(np.abs(l3v - real)))
            bmae = float(np.mean(np.abs(base_v - real)))
            imp = (bmae - l3mae) / bmae * 100 if bmae > 0 else 0.0
            out(f"    {nm:6} {l3mae:>8.2f} {bmae:>9.2f} {imp:>+7.0f}%")
    else:
        out("  sin xG de L3 en los resueltos.")

    # ---- (4) L3 vs base-rate head-to-head: who gave more prob to the actual result ----
    out("")
    out("--- (4) L3 vs base-rate cara a cara (prob asignada al resultado real) ---")
    if "L3" in metrics:
        cm = metrics["L3"]["mask"]
        idx = np.arange(n)
        pbl = Pbase[idx, y]
        pl3 = metrics["L3"]["P"][idx, y]

        def tally(sel):
            d = (pl3 - pbl)[sel]
            l3w = int(np.sum(d > 0.01))
            bw = int(np.sum(d < -0.01))
            return l3w, bw, int(np.sum(sel) - l3w - bw), int(np.sum(sel))

        l3w, bw, tie, tot = tally(cm)
        out(f"  global n={tot}{_small(tot)}: L3 mejor {l3w} · base-rate mejor {bw} · empate {tie}")
        maxl3 = metrics["L3"]["P"].max(1)
        for nm, sel in [("L3 marca favorito (máx≥50%)", cm & (maxl3 >= 0.50)),
                        ("L3 lo ve igualado (máx<50%)", cm & (maxl3 < 0.50))]:
            if sel.sum():
                a, b, t, tt = tally(sel)
                out(f"    {nm:28} n={tt:>3}: L3 {a} · base {b} · empate {t}")
        conf_pairs = [(CONF_BY_TEAM.get(str(h)), CONF_BY_TEAM.get(str(a)))
                      for h, a in zip(settled["home"], settled["away"])]
        cross = np.array([hc is not None and ac is not None and hc != ac for hc, ac in conf_pairs])
        intra = np.array([hc is not None and ac is not None and hc == ac for hc, ac in conf_pairs])
        for nm, sel in [("cruce de confederación", cm & cross), ("misma confederación", cm & intra)]:
            if sel.sum():
                a, b, t, tt = tally(sel)
                out(f"    {nm:28} n={tt:>3}: L3 {a} · base {b} · empate {t}")
    else:
        out("  faltan predicciones L3 resueltas.")

    # ---- (5) STATS: corners/cards/shots data-model totals vs REAL totals + base-rate ----
    out("")
    out("--- (5) STATS córners/tarjetas/tiros — modelo de datos vs reales + base-rate ---")
    any_stat = False
    for nm, pcol, rcol in [("córners", "st_corners_total", "result_corners"),
                           ("tarjetas", "st_cards_total", "result_cards"),
                           ("tiros", "st_shots_total", "result_shots")]:
        if pcol not in settled.columns or rcol not in settled.columns:
            continue
        p = settled[pcol].to_numpy(float)
        rr = settled[rcol].to_numpy(float)
        m = ~(np.isnan(p) | np.isnan(rr))
        if m.sum() == 0:
            continue
        any_stat = True
        pm, rm = p[m], rr[m]
        base = float(rm.mean())
        mae_model = float(np.mean(np.abs(pm - rm)))
        mae_base = float(np.mean(np.abs(base - rm)))
        lift = (mae_base - mae_model) / mae_base * 100 if mae_base > 0 else 0.0
        out(f"  {nm:9} n={int(m.sum()):>3}{_small(int(m.sum()))} real μ={base:.1f} | "
            f"MAE modelo {mae_model:.2f} vs base {mae_base:.2f} ({lift:+.0f}%)")
    if {"st_corners_over", "result_corners", "st_corners_line"} <= set(settled.columns):
        sub = settled.dropna(subset=["st_corners_over", "result_corners", "st_corners_line"])
        if len(sub):
            po = sub["st_corners_over"].to_numpy(float)
            line = sub["st_corners_line"].to_numpy(float)
            ro = (sub["result_corners"].to_numpy(float) > line).astype(int)
            acc, brier, _ = _binary_metrics(po, ro)
            out(f"  córners O/U (línea~{np.median(line):g}) n={len(sub)}: "
                f"acc {acc*100:.0f}% · Brier {brier:.3f} · real Over={ro.mean()*100:.0f}%")
            any_stat = True
    if not any_stat:
        out("  aún sin stats reales liquidadas (settle trae córners/tarjetas/tiros al terminar el partido).")

    # ---- recalibration PROPOSAL: shrink L3 toward base-rate (calibration check, not applied) ----
    out("")
    out("PROPUESTA de recalibración (calibración, informativa, NO aplicada):")
    if "L3" in metrics and metrics["L3"]["mask"].sum() >= 5:
        common = metrics["L3"]["mask"]
        Pl3 = metrics["L3"]["P"][common]
        Pb = Pbase[common]
        Yc = Y[common]
        base_ll = _metrics(Pl3, Yc)["logloss"]
        best_lam, best_ll = 0.0, base_ll
        for lam in np.linspace(0, 1, 21):
            blend = (1 - lam) * Pl3 + lam * Pb
            ll = _metrics(blend, Yc)["logloss"]
            if ll < best_ll - 1e-9:
                best_ll, best_lam = ll, lam
        if best_lam > 0:
            out(f"  Encoger L3 hacia base-rate lambda={best_lam:.2f} bajaría log-loss "
                f"{base_ll:.4f}->{best_ll:.4f} ({(base_ll-best_ll)/base_ll*100:+.1f}%) sobre {int(common.sum())} casos")
            out("  (= L3 sobreconfiado; revisar manualmente. NO se aplica solo, muestra pequeña.)")
        else:
            out(f"  Ningún encogimiento hacia base-rate mejora el log-loss ({base_ll:.4f}); L3 bien calibrado.")
    else:
        out("  Muestra insuficiente (>=5) o sin L3 resuelto.")

    out("")
    out(f"generated_at_utc: {now_iso()}")
    SCORECARD.write_text("\n".join(lines), encoding="utf-8")
    print(f"learning_loop scorecard: {n} resolved -> {SCORECARD}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="World Cup learning loop (isolated, shadow).")
    ap.add_argument("cmd", choices=["log", "settle", "scorecard"])
    a = ap.parse_args()
    {"log": cmd_log, "settle": cmd_settle, "scorecard": cmd_scorecard}[a.cmd]()
