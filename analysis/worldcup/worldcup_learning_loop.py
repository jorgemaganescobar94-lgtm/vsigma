"""
WORLD CUP 2026 - LEARNING LOOP (ISOLATED, analysis/worldcup/ only).

Closes the feedback loop for the shadow World Cup product. Three offline-friendly
subcommands, run once per pipeline pass:

  log       Append today's per-match predictions (MARKET / L3 / v2 / xG / top score)
            to worldcup_predictions_log.csv, DEDUP by fixture_id (keeps the FIRST =
            locks the pre-match prediction, no hindsight). Source: worldcup_cards.csv
            (+ worldcup_our_model_v2_predictions.csv for v2). NO API.

  settle    For FINISHED fixtures only, attach the real result to the log. Reuses the
            SAME cached /fixtures(league=1,season=2026) call the card builder already
            made (6h TTL) -> ~0 marginal API. No per-fixture calls. 1X2 settled on the
            90' score (score.fulltime) to match the de-vigged 90' market we logged.

  scorecard Over RESOLVED fixtures, score each predictor (MARKET vs L3 vs v2):
            log-loss, Brier, Brier-skill vs market, 1X2 hit%, ECE (calibration) ->
            worldcup_scorecard.txt. First lines = compact Telegram block. Includes a
            recalibration PROPOSAL (best L3->market shrink lambda) but NEVER applies it.

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
KMAX = 10
EPS = 1e-15
FINISHED = {"FT", "AET", "PEN"}

LOG_COLUMNS = [
    "fixture_id", "kickoff_utc", "home", "away", "round",
    "mkt_home", "mkt_draw", "mkt_away", "mkt_over25", "mkt_btts_yes",
    "l3_home", "l3_draw", "l3_away", "l3_xg_home", "l3_xg_away", "l3_top_score",
    "v2_home", "v2_draw", "v2_away",
    "logged_at_utc",
    "result_ft_gh", "result_ft_ga", "result_final_gh", "result_final_ga",
    "result_1x2", "result_status", "settled", "settled_at_utc",
]


def now_iso():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


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
    for _, r in cards.iterrows():
        if pd.isna(r.get("fixture_id")):
            continue
        fid = int(r["fixture_id"])
        if fid in known:
            continue  # lock-first: never overwrite a pre-match prediction
        # only log fixtures that actually carry a forecast
        if pd.isna(r.get("mkt_home")) and pd.isna(r.get("our_home")):
            continue
        v2 = v2map.get(fid)
        row = {
            "fixture_id": fid, "kickoff_utc": r.get("kickoff_utc"),
            "home": r.get("home"), "away": r.get("away"), "round": r.get("round"),
            "mkt_home": r.get("mkt_home"), "mkt_draw": r.get("mkt_draw"),
            "mkt_away": r.get("mkt_away"), "mkt_over25": r.get("mkt_over25"),
            "mkt_btts_yes": r.get("mkt_btts_yes"),
            "l3_home": r.get("our_home"), "l3_draw": r.get("our_draw"),
            "l3_away": r.get("our_away"), "l3_xg_home": r.get("our_xg_home"),
            "l3_xg_away": r.get("our_xg_away"),
            "l3_top_score": top_scoreline(r.get("our_xg_home"), r.get("our_xg_away")),
            "v2_home": (v2["v2_home"] if v2 is not None else np.nan),
            "v2_draw": (v2["v2_draw"] if v2 is not None else np.nan),
            "v2_away": (v2["v2_away"] if v2 is not None else np.nan),
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
    print(f"learning_loop log: +{len(new_rows)} new, {len(log)} total -> {LOG}")


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

    newly = 0
    for idx, r in log.iterrows():
        fid = int(r["fixture_id"])
        if int(r.get("settled") or 0) == 1:
            continue
        if fid in results:
            for k, v in results[fid].items():
                log.at[idx, k] = v
            log.at[idx, "settled"] = 1
            log.at[idx, "settled_at_utc"] = now_iso()
            newly += 1

    log.to_csv(LOG, index=False)
    q1 = quota()
    spend = (q1 - q0) if (q0 is not None and q1 is not None) else "n/a"
    nset = int((log["settled"].fillna(0).astype(int) == 1).sum())
    print(f"learning_loop settle: +{newly} newly settled, {nset} total settled. "
          f"API spend this step: {spend} (fixtures cached). quota now: {q1}")


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

    predictors = [("MERCADO", "mkt"), ("L3", "l3"), ("v2", "v2")]
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

    # Brier-skill vs market, computed on the COMMON resolved+predicted set
    skill = {}
    if "MERCADO" in metrics:
        for label in metrics:
            if label == "MERCADO":
                skill[label] = 0.0
                continue
            common = metrics["MERCADO"]["mask"] & metrics[label]["mask"]
            if common.sum() == 0:
                continue
            bm = _metrics(metrics["MERCADO"]["P"][common], Y[common])["brier"]
            bx = _metrics(metrics[label]["P"][common], Y[common])["brier"]
            skill[label] = (1.0 - bx / bm) if bm > 0 else 0.0

    # ---- compact Telegram block (first lines) ----
    acc_bits = " · ".join(f"{lab} {metrics[lab]['m']['acc']*100:.0f}%"
                          for lab, _ in predictors if lab in metrics)
    out(f"📊 Track record ({n} resueltos · {date_tag})")
    out(f"Acierto 1X2: {acc_bits}")
    sk_bits = " · ".join(f"{lab} {skill[lab]*100:+.0f}%" for lab in skill if lab != "MERCADO")
    if sk_bits:
        out(f"Brier-skill vs Mkt: {sk_bits}")
    out("")
    out("===== detalle =====")
    out(f"resueltos={n} | 1X2 liquidado a 90' (score.fulltime) | métricas multiclase H/D/A")
    hdr = f"{'predictor':9} {'n':>3} {'logloss':>8} {'brier':>7} {'acc%':>6} {'ECE':>6} {'BrierSkill%':>11}"
    out(hdr)
    out("-" * len(hdr))
    for label, _ in predictors:
        if label not in metrics:
            out(f"{label:9} {'-':>3} {'(sin predicciones)':>8}")
            continue
        m = metrics[label]["m"]
        sk = skill.get(label)
        sk_s = f"{sk*100:+.1f}" if sk is not None else "n/a"
        out(f"{label:9} {metrics[label]['n']:>3} {m['logloss']:>8.4f} {m['brier']:>7.4f} "
            f"{m['acc']*100:>6.1f} {m['ece']:>6.3f} {sk_s:>11}")

    # ---- recalibration PROPOSAL (not applied) ----
    out("")
    out("PROPUESTA de recalibración (informativa, NO aplicada):")
    if "L3" in metrics and "MERCADO" in metrics:
        common = metrics["MERCADO"]["mask"] & metrics["L3"]["mask"]
        if common.sum() >= 5:
            Pl3 = metrics["L3"]["P"][common]
            Pmk = metrics["MERCADO"]["P"][common]
            Yc = Y[common]
            base_ll = _metrics(Pl3, Yc)["logloss"]
            best_lam, best_ll = 0.0, base_ll
            for lam in np.linspace(0, 1, 21):
                blend = (1 - lam) * Pl3 + lam * Pmk
                ll = _metrics(blend, Yc)["logloss"]
                if ll < best_ll - 1e-9:
                    best_ll, best_lam = ll, lam
            if best_lam > 0:
                out(f"  Mezcla L3->mercado lambda={best_lam:.2f} bajaría log-loss "
                    f"{base_ll:.4f}->{best_ll:.4f} ({(base_ll-best_ll)/base_ll*100:+.1f}%) sobre {int(common.sum())} casos.")
                out("  -> revisar manualmente; NO se aplica automáticamente (muestra pequeña).")
            else:
                out(f"  Ninguna mezcla L3->mercado mejora el log-loss ({base_ll:.4f}); L3 se mantiene.")
        else:
            out(f"  Muestra insuficiente ({int(common.sum())} casos); se necesitan >=5 para proponer.")
    else:
        out("  Faltan predicciones L3 y/o mercado resueltas para proponer.")

    out("")
    out(f"generated_at_utc: {now_iso()}")
    SCORECARD.write_text("\n".join(lines), encoding="utf-8")
    print(f"learning_loop scorecard: {n} resolved -> {SCORECARD}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="World Cup learning loop (isolated, shadow).")
    ap.add_argument("cmd", choices=["log", "settle", "scorecard"])
    a = ap.parse_args()
    {"log": cmd_log, "settle": cmd_settle, "scorecard": cmd_scorecard}[a.cmd]()
