"""
AUTO-REFIT — SHADOW mode (continuous-learning Phase 1b).  OFFLINE · NO API · NO leakage.

Each run it: (1) appends the newly-SETTLED World Cup results found in the predictions
log to a copy of the training data (in MEMORY — the on-disk dataset is NOT modified),
(2) re-fits candidate L3 ratings with the exact production ridge-Massey math, (3) runs
an ANTI-CORRUPTION gate, and (4) writes a SHADOW REPORT. It NEVER writes the production
ratings — swapping them is Phase 1c, enabled only after the shadow is trusted.

The gate is a corruption/fit-bug guard, NOT a generalization test: appending matches at
the temporal tail leaves the held-out OOS window identical by construction (walk-forward
fits on past only), so the active guards are finite ratings, non-decreasing team count,
a bounded max rating move vs the committed ratings, and a reproduction check.

Calibration is invariant (burn-in <2024 only) -> never rebuilt here.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DISPATCHER = ROOT / "scripts" / "dispatch_telegram_alert.py"
sys.path.insert(0, str(HERE))
import national_elo_layer3 as L3  # noqa: E402  (module import does NOT hit the API)

DEF_BASE = HERE / "international_results.csv"
DEF_LOG = HERE / "worldcup_predictions_log.csv"
DEF_COMMITTED = HERE / "national_elo_layer3_ratings.csv"
DEF_REPORT = HERE / "auto_refit_shadow_report.txt"
MOVE_CAP = 0.60
REPRO_TOL = 0.05


# --------------------------------------------------------------------- data
def build_enriched(base: pd.DataFrame, log: pd.DataFrame):
    """base + settled WC rows from the log not already present. In-memory only.

    Returns (enriched_df, new_rows:list, unmapped:list)."""
    name2id = {}
    for _, r in base.iterrows():
        name2id[str(r["home"])] = int(r["home_id"]); name2id[str(r["away"])] = int(r["away_id"])
    existing = set(base["fixture_id"].dropna().astype(int))
    settled = log[(log["settled"].fillna(0).astype(int) == 1)
                  & log["result_ft_gh"].notna() & log["result_ft_ga"].notna()]
    rows, unmapped = [], []
    for _, r in settled.iterrows():
        fid = int(r["fixture_id"])
        if fid in existing:
            continue
        h, a = str(r["home"]), str(r["away"])
        if h not in name2id or a not in name2id:
            unmapped.append((h, a)); continue
        rows.append({
            "fixture_id": fid,
            "date": str(r["kickoff_utc"]).strip().replace(" ", "T") + ":00+00:00",
            "league_id": 1, "league_tag": "WC", "season": 2026, "neutral": 1,
            "home_id": name2id[h], "home": h, "away_id": name2id[a], "away": a,
            "gh": int(float(r["result_ft_gh"])), "ga": int(float(r["result_ft_ga"])),
            "venue_city": "",
        })
        existing.add(fid)  # guard against dupes within the same log
    enriched = pd.concat([base, pd.DataFrame(rows)], ignore_index=True) if rows else base.copy()
    return enriched, rows, unmapped


# ------------------------------------------------------------------ fit/oos
def run(df: pd.DataFrame):
    """Walk-forward + final fit — faithful to national_elo_layer3.main() math, no API."""
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"], utc=True, errors="coerce").dt.tz_localize(None)
    df = df.dropna(subset=["date", "home_id", "away_id", "gh", "ga"]).sort_values("date").reset_index(drop=True)
    df["home_id"] = df["home_id"].astype(int); df["away_id"] = df["away_id"].astype(int)
    n = len(df)
    votes = {}
    for _, r in df.iterrows():
        cf = L3.TAG2CONF.get(r["league_tag"])
        if cf:
            for tid in (r["home_id"], r["away_id"]):
                votes.setdefault(tid, Counter())[cf] += 1
    conf = {tid: cc.most_common(1)[0][0] for tid, cc in votes.items()}
    hid = df["home_id"].to_numpy(); aid = df["away_id"].to_numpy()
    gh = df["gh"].to_numpy(float); ga = df["ga"].to_numpy(float)
    neutral = df["neutral"].to_numpy(int); tags = df["league_tag"].to_numpy()
    dates = df["date"].to_numpy()
    days = (dates - dates.min()) / np.timedelta64(1, "D")
    margin = np.clip(gh - ga, -L3.MARGIN_CAP, L3.MARGIN_CAP)
    imp = np.array([L3.IMP_BY_TAG.get(t, 0.8) for t in tags])
    xconf = np.array([L3.XCONF_MULT if (conf.get(hid[i]) and conf.get(aid[i]) and conf[hid[i]] != conf[aid[i]])
                      else 1.0 for i in range(n)])
    base_w = imp * xconf
    is_oos = dates >= np.datetime64(L3.OOS_CUTOFF); burn = ~is_oos
    res = np.where(gh > ga, 0, np.where(gh == ga, 1, 2)); Y = np.eye(3)[res]
    sup_pre = np.full(n, np.nan); last_fit_day = None; cur_s, cur_h = None, 0.0
    for i in range(n):
        if cur_s is None or (days[i] - last_fit_day) >= L3.REFIT_DAYS:
            pm = days < days[i]
            if pm.sum() >= L3.MIN_PAST:
                w = base_w[pm] * np.exp(-np.log(2) * (days[i] - days[pm]) / L3.HL_DAYS)
                cur_s, cur_h = L3.fit_rating(hid[pm], aid[pm], neutral[pm], margin[pm], w)
                last_fit_day = days[i]
        if cur_s is not None:
            sup_pre[i] = (cur_s.get(hid[i], 0.0) - cur_s.get(aid[i], 0.0)) + (cur_h if neutral[i] == 0 else 0.0)
    ok = np.isfinite(sup_pre); bturn = burn & ok
    A = np.c_[np.ones(bturn.sum()), sup_pre[bturn]]
    coef, *_ = np.linalg.lstsq(A, (gh - ga)[bturn], rcond=None)
    a0, a1 = float(coef[0]), float(coef[1]); total_mean = float(np.mean((gh + ga)[bturn]))

    def probs(sup):
        s = a0 + a1 * sup
        return L3.wdl(max(0.05, (total_mean + s) / 2.0), max(0.05, (total_mean - s) / 2.0))

    P3 = np.zeros((n, 3))
    for i in range(n):
        if ok[i]:
            P3[i] = probs(sup_pre[i])
    P3[~ok] = np.array([0.45, 0.27, 0.28]); P3 /= P3.sum(1, keepdims=True)
    isos = [L3.Isotonic().fit(P3[bturn, k], Y[bturn, k]) for k in range(3)]
    P3c = np.c_[isos[0].predict(P3[:, 0]), isos[1].predict(P3[:, 1]), isos[2].predict(P3[:, 2])]
    P3c = np.clip(P3c, 1e-6, None); P3c /= P3c.sum(1, keepdims=True)
    pm = days < days.max() + 1
    w = base_w[pm] * np.exp(-np.log(2) * (days.max() - days[pm]) / L3.HL_DAYS)
    s_final, h_final = L3.fit_rating(hid[pm], aid[pm], neutral[pm], margin[pm], w)
    name_by_id = {}
    for _, r in df.iterrows():
        name_by_id[int(r["home_id"])] = r["home"]; name_by_id[int(r["away_id"])] = r["away"]
    return dict(dates=dates, is_oos=is_oos, ok=ok, Y=Y, P3c=P3c, s_final=s_final,
                h_final=h_final, name_by_id=name_by_id)


def oos(r, upper_excl):
    sel = r["is_oos"] & r["ok"] & (r["dates"] < upper_excl)
    P, Y = r["P3c"][sel], r["Y"][sel]
    if sel.sum() == 0:
        return dict(n=0, logloss=float("nan"), ECE=float("nan"), acc=float("nan"))
    return dict(n=int(sel.sum()), logloss=L3.logloss_mc(P, Y),
                acc=L3.acc_mc(P, Y), ECE=L3.ece_mc(P, Y))


# --------------------------------------------------------------------- gate
def check_finite(ratings: dict) -> bool:
    return all(np.isfinite(v) for v in ratings.values()) and len(ratings) > 0


def team_count_ok(candidate: dict, committed: dict) -> bool:
    return len(candidate) >= len(committed)


def max_move(candidate: dict, committed: dict):
    """Largest |Δ| over teams present in BOTH (returns (max_abs, team, old, new))."""
    worst = (0.0, None, None, None)
    for tid, sn in candidate.items():
        so = committed.get(tid)
        if so is None:
            continue
        d = abs(sn - so)
        if d > worst[0]:
            worst = (d, tid, so, sn)
    return worst


def oos_not_worse(mo, mn, tol=1e-6) -> bool:
    if mo["n"] == 0 or mn["n"] == 0:
        return True
    ll_ok = (mn["logloss"] - mo["logloss"]) <= tol
    ece_ok = (mn["ECE"] - mo["ECE"]) <= tol
    return bool(ll_ok and ece_ok)


def send_alert(title: str, body: str) -> None:
    """Reuse the shared dispatcher (TELEGRAM_* from env; fail-soft; no secrets printed)."""
    try:
        subprocess.run(
            [sys.executable, str(DISPATCHER), "--title", title,
             "--date", datetime.now(timezone.utc).strftime("%Y-%m-%d"), "--summary", body],
            cwd=str(ROOT), timeout=30,
        )
    except Exception as exc:  # noqa: BLE001
        print(f"[auto-refit] alerta no fatal: {type(exc).__name__}")


def write_ratings(path, s_final, name_by_id):
    pd.DataFrame([{"team_id": k, "team": name_by_id.get(k, k), "strength": round(v, 3)}
                  for k, v in sorted(s_final.items(), key=lambda kv: -kv[1])]).to_csv(path, index=False)


def evaluate_gate(candidate, committed, repro, mo, mn, move_cap=MOVE_CAP, repro_tol=REPRO_TOL):
    mv, mv_tid, mv_old, mv_new = max_move(candidate, committed)
    checks = {
        "finite": check_finite(candidate),
        "team_count_non_decreasing": team_count_ok(candidate, committed),
        "max_move<=cap": mv <= move_cap,
        "oos_not_worse": oos_not_worse(mo, mn),
        "repro<tol": repro <= repro_tol,
    }
    return dict(ok=all(checks.values()), checks=checks,
                max_move=mv, move_team=mv_tid, move_old=mv_old, move_new=mv_new)


# --------------------------------------------------------------------- main
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Auto-refit L3 — gate + optional SWAP.")
    ap.add_argument("--base", default=str(DEF_BASE))
    ap.add_argument("--log", default=str(DEF_LOG))
    ap.add_argument("--committed", default=str(DEF_COMMITTED))
    ap.add_argument("--report", default=str(DEF_REPORT))
    ap.add_argument("--move-cap", type=float, default=MOVE_CAP)
    ap.add_argument("--apply", action="store_true",
                    help="Fase 1c: si GATE PASS, ESCRIBIR ratings+dataset de producción "
                         "(si FALLA, mantener viejos + alerta Telegram). Default: shadow.")
    a = ap.parse_args(argv)
    mode = "APPLY (swap)" if a.apply else "SHADOW (no swap)"

    rep = []
    def out(s=""):
        print(s); rep.append(s)

    base = pd.read_csv(a.base)
    log = pd.read_csv(a.log) if Path(a.log).exists() else pd.DataFrame(
        columns=["fixture_id", "kickoff_utc", "home", "away", "round", "settled",
                 "result_ft_gh", "result_ft_ga"])
    committed_df = pd.read_csv(a.committed)
    committed = {int(r.team_id): float(r.strength) for r in committed_df.itertuples()}

    enriched, new_rows, unmapped = build_enriched(base, log)
    drng = (min(x["date"][:10] for x in new_rows), max(x["date"][:10] for x in new_rows)) if new_rows else ("-", "-")

    out("=" * 88)
    out(f"AUTO-REFIT L3 — mode={mode}")
    out("=" * 88)
    out(f"generated_at_utc: {datetime.now(timezone.utc).isoformat(timespec='seconds')}")
    out(f"base rows={len(base)} | settled-in-log={int((log.get('settled', pd.Series(dtype=int)).fillna(0).astype(int)==1).sum())} "
        f"| NEW rows={len(new_rows)} ({drng[0]}..{drng[1]}) | unmapped={len(unmapped)} | enriched={len(enriched)}")

    if not new_rows:
        out("")
        out("NO hay partidos liquidados nuevos fuera del dataset -> refit NO-OP.")
        out("(El dataset ya está al día con el log; nada que aprender hasta nuevos FT.)")
        out("GATE: N/A (sin cambios) -> ratings de producción intactos.")
        Path(a.report).write_text("\n".join(rep), encoding="utf-8")
        print(f"\nReport -> {a.report}")
        return 0

    old = run(base)
    new = run(enriched)
    cut = np.datetime64(drng[0])
    mo, mn = oos(old, cut), oos(new, cut)

    # repro: refit on the base must reproduce the committed ratings (fit-code sanity)
    repro = max((abs(old["s_final"][t] - committed[t]) for t in old["s_final"] if t in committed), default=0.0)

    g = evaluate_gate(new["s_final"], committed, repro, mo, mn, move_cap=a.move_cap)

    out("")
    out(f"OOS 1X2 — ventana común [2024-01-01 .. {str(cut)[:10]})  (leakage-safe)")
    out(f"  base     n={mo['n']}  ll={mo['logloss']:.5f}  ECE={mo['ECE']:.4f}  acc={mo['acc']*100:.1f}%")
    out(f"  enriched n={mn['n']}  ll={mn['logloss']:.5f}  ECE={mn['ECE']:.4f}  acc={mn['acc']*100:.1f}%")
    out(f"repro (refit base vs committed): max|Δ|={repro:.4f}")

    # rating movements among the newly added teams
    wc_ids = {x["home_id"] for x in new_rows} | {x["away_id"] for x in new_rows}
    moves = sorted(((new["name_by_id"].get(t, t), committed.get(t), new["s_final"][t],
                     new["s_final"][t] - committed.get(t, new["s_final"][t]))
                    for t in wc_ids if t in committed and t in new["s_final"]),
                   key=lambda z: -abs(z[3]))
    out("")
    out(f"MOVIMIENTOS DE RATING destacados (candidato vs commiteado; cap {a.move_cap}):")
    for nm, so, sn, d in moves[:10]:
        out(f"    {nm:24s} {so:+.2f} -> {sn:+.2f}  ({d:+.2f})")

    out("")
    out("GATE (anti-corrupción):")
    for k, v in g["checks"].items():
        out(f"    {'PASS' if v else 'FAIL'}  {k}")
    out(f"  max|Δ| = {g['max_move']:.3f} ({new['name_by_id'].get(g['move_team'], g['move_team'])}: "
        f"{g['move_old']:+.2f}->{g['move_new']:+.2f})")
    out(f"  -> GATE: {'PASS' if g['ok'] else 'FAIL'}")
    fails = [k for k, v in g["checks"].items() if not v]
    out("")
    if not a.apply:
        if not g["ok"]:
            out(f"  NOTA: gate FALLÓ ({', '.join(fails)}) -> en producción se MANTENDRÍAN los viejos + alerta.")
        out("SHADOW: ratings de producción NO escritos. El swap requiere --apply (Fase 1c).")
    else:
        if g["ok"]:
            # SWAP: write new ratings + persist the enriched dataset so (data, ratings) stay
            # consistent for the next run's repro check. Calibration is invariant -> not rebuilt.
            write_ratings(a.committed, new["s_final"], new["name_by_id"])
            enriched.to_csv(a.base, index=False)
            out(f"SWAP APLICADO ✅  ratings -> {Path(a.committed).name} | dataset -> {Path(a.base).name} "
                f"(+{len(new_rows)} FT). Calibración intacta (invariante).")
        else:
            out(f"SWAP RECHAZADO por gate ({', '.join(fails)}) -> ratings de producción SIN tocar.")
            send_alert("🚨 auto-refit RECHAZADO por gate",
                       f"El auto-refit del L3 NO se adoptó: gate FALLÓ ({', '.join(fails)}). "
                       f"Se mantienen los ratings previos. max|Δ|={g['max_move']:.3f}. Revisa el reporte.")

    Path(a.report).write_text("\n".join(rep), encoding="utf-8")
    print(f"\nReport -> {a.report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
