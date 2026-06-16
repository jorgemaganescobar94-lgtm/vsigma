"""
WORLD CUP 2026 - FULL per-match card, mobile-concise (Telegram-ready). OFFLINE, NO API.
Reads only analysis/worldcup/worldcup_cards.csv (market + L3 already saved). No production.

Per match: 1X2 (market + L3) + double chance; goals (market O2.5 + BTTS, our Poisson O1.5/2.5/3.5
+ BTTS + per-team xG); top exact scorelines (our Poisson); stats (corners/cards/shots) = tournament
baseline, clearly LOW-CONFIDENCE (no validated national-team stats model).
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

OUT_DIR = Path(__file__).resolve().parent
CARDS = OUT_DIR / "worldcup_cards.csv"
KMAX = 10

# tournament per-team baselines (low confidence; no validated NT stats model)
BASE_CORNERS, BASE_SHOTS, BASE_YEL = 5.0, 12.5, 2.0


def pmf(lam, k=KMAX):
    ks = np.arange(k + 1)
    logf = np.concatenate([[0.0], np.cumsum(np.log(np.arange(1, k + 1)))])
    return np.exp(ks * np.log(max(lam, 1e-9)) - lam - logf)


def score_matrix(lh, la):
    M = np.outer(pmf(lh), pmf(la))
    return M / M.sum()


def main(date_from, date_to, limit, compact=False):
    df = pd.read_csv(CARDS)
    df = df[df["kickoff_utc"].notna()].copy()
    df["d"] = df["kickoff_utc"].str[:10]
    df = df[(df["d"] >= date_from) & (df["d"] <= date_to)].sort_values("kickoff_utc").head(limit)

    lines = []

    def out(s=""):
        print(s); lines.append(s)

    if compact:
        # COMPACT (Telegram): <=2 lines/match so it fits the 25-line dispatcher cap.
        out(f"🏆 MUNDIAL 2026 — {date_from}→{date_to} (Mkt=mercado · L3=modelo propio)")
        for _, r in df.iterrows():
            mh, md, ma = r.get("mkt_home"), r.get("mkt_draw"), r.get("mkt_away")
            lh3, ld3, la3 = r.get("our_home"), r.get("our_draw"), r.get("our_away")
            xgh, xga = r.get("our_xg_home"), r.get("our_xg_away")
            o25, btts = r.get("mkt_over25"), r.get("mkt_btts_yes")
            ko = str(r["kickoff_utc"])[5:16].replace("T", " ")  # MM-DD HH:MM
            grp = str(r.get("home_group") or "?").replace("Group ", "G")
            top = ""
            if pd.notna(xgh):
                M = score_matrix(xgh, xga)
                flat = sorted(((i, j, M[i, j]) for i in range(KMAX + 1) for j in range(KMAX + 1)),
                              key=lambda t: -t[2])[:2]
                top = " · ".join(f"{i}-{j}" for i, j, _ in flat)
            out(f"⚽ {r['home']} v {r['away']} · {grp} · {ko}Z")
            seg = []
            if pd.notna(mh):
                seg.append(f"1X2 M{mh*100:.0f}/{md*100:.0f}/{ma*100:.0f}")
            if pd.notna(lh3):
                seg.append(f"L3 {lh3*100:.0f}/{ld3*100:.0f}/{la3*100:.0f}")
            if pd.notna(o25):
                seg.append(f"O2.5 {o25*100:.0f}")
            if pd.notna(btts):
                seg.append(f"BTTS {btts*100:.0f}")
            if pd.notna(xgh):
                seg.append(f"xG {xgh:.1f}-{xga:.1f}")
            if top:
                seg.append(top)
            out("   " + " · ".join(seg))
        out("stats córners/tarj/tiros: baseline torneo (BAJA CONF). Mercado=mejor pronóstico.")
        (OUT_DIR / "worldcup_full_cards.txt").write_text("\n".join(lines), encoding="utf-8")
        print(f"\nWritten: {OUT_DIR/'worldcup_full_cards.txt'} ({len(lines)} lines)")
        return

    out(f"WORLD CUP 2026 — FULL CARDS  {date_from}..{date_to}  ({len(df)} matches)")
    out("Mkt = de-vigged market (best) · L3 = our rating model · * = LOW CONF baseline (no NT stats model)")
    out("=" * 60)

    for _, r in df.iterrows():
        h, a = r["home"], r["away"]
        ko = str(r["kickoff_utc"]).replace("T", " ")[:16]
        grp = str(r.get("home_group") or "").replace("Group ", "Gr.")
        mh, md, ma = r.get("mkt_home"), r.get("mkt_draw"), r.get("mkt_away")
        lh3, ld3, la3 = r.get("our_home"), r.get("our_draw"), r.get("our_away")
        xgh, xga = r.get("our_xg_home"), r.get("our_xg_away")
        o25, btts = r.get("mkt_over25"), r.get("mkt_btts_yes")

        out("")
        out(f"🏆 {h} vs {a}")
        out(f"   {ko} · {grp}")
        # 1X2
        if pd.notna(mh):
            out(f"1X2  Mkt {mh*100:.0f}/{md*100:.0f}/{ma*100:.0f}"
                + (f"  ·  L3 {lh3*100:.0f}/{ld3*100:.0f}/{la3*100:.0f}" if pd.notna(lh3) else ""))
            # double chance (market)
            out(f"DC   1X {(mh+md)*100:.0f}% · 12 {(mh+ma)*100:.0f}% · X2 {(md+ma)*100:.0f}%")
        # goals
        if pd.notna(xgh):
            M = score_matrix(xgh, xga)
            gh = np.arange(KMAX + 1)[:, None]; ga = np.arange(KMAX + 1)[None, :]
            tot = gh + ga
            o15 = M[tot >= 2].sum(); o25p = M[tot >= 3].sum(); o35 = M[tot >= 4].sum()
            bts = M[(gh >= 1) & (ga >= 1)].sum()
            gline = "Goals "
            if pd.notna(o25):
                gline += f"Mkt O2.5 {o25*100:.0f}%"
            if pd.notna(btts):
                gline += f" · BTTS {btts*100:.0f}%"
            out(gline)
            out(f"     Poisson O1.5 {o15*100:.0f} · O2.5 {o25p*100:.0f} · O3.5 {o35*100:.0f} · BTTS {bts*100:.0f}")
            out(f"     xG {h[:14]} {xgh:.1f} – {xga:.1f} {a[:14]}")
            # top exact scores
            flat = [((i, j), M[i, j]) for i in range(KMAX + 1) for j in range(KMAX + 1)]
            flat.sort(key=lambda kv: -kv[1])
            tops = " · ".join(f"{i}-{j} {p*100:.0f}%" for (i, j), p in flat[:4])
            out(f"     Marcadores {tops}")
        elif pd.notna(o25):
            out(f"Goals  Mkt O2.5 {o25*100:.0f}%" + (f" · BTTS {btts*100:.0f}%" if pd.notna(btts) else ""))
        # stats baseline (low conf)
        out(f"Stats* córners ~{BASE_CORNERS:.0f}-{BASE_CORNERS:.0f} · tiros ~{BASE_SHOTS:.0f}-{BASE_SHOTS:.0f} · "
            f"tarj ~{BASE_YEL:.0f}-{BASE_YEL:.0f}  (baseline torneo)")

    out("")
    out("* córners/tarjetas/tiros: media de torneo, BAJA CONFIANZA (no hay modelo validado de selecciones).")
    out("El mercado es el mejor pronóstico; L3/Poisson = opinión propia independiente.")

    (OUT_DIR / "worldcup_full_cards.txt").write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWritten: {OUT_DIR/'worldcup_full_cards.txt'}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--from", dest="dfrom", default="2026-06-16")
    ap.add_argument("--to", dest="dto", default="2026-06-18")
    ap.add_argument("--limit", type=int, default=4)
    ap.add_argument("--compact", action="store_true", help="dense <=2 lines/match for Telegram")
    a = ap.parse_args()
    main(a.dfrom, a.dto, a.limit, a.compact)
