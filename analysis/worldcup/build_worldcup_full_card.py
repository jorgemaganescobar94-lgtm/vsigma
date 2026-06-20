"""
WORLD CUP 2026 - FULL per-match card, mobile-concise (Telegram-ready). OFFLINE, NO API.
Reads only analysis/worldcup/worldcup_cards.csv (our Layer-3 model already saved). No production.

PURIFIED: shows ONLY our own L3 model — 1X2 + double chance + goals/BTTS/xG (Poisson) +
top scorelines. ZERO market/odds. Corners/cards are NOT shown (pending a data model).
"""
from __future__ import annotations

import argparse
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import numpy as np
import pandas as pd

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

sys.path.insert(0, str(Path(__file__).resolve().parent))
try:
    import stats_model  # noqa: E402  (corners/cards/shots gating from OOS validation)
    SHOW_STATS = stats_model.shown_stats()
except Exception:
    SHOW_STATS = {"corners", "cards", "shots"}

OUT_DIR = Path(__file__).resolve().parent
CARDS = OUT_DIR / "worldcup_cards.csv"
LOG = OUT_DIR / "worldcup_predictions_log.csv"
META = OUT_DIR / "worldcup_render_meta.txt"  # fixture count for the workflow anti-spam gate
KMAX = 10


def pmf(lam, k=KMAX):
    ks = np.arange(k + 1)
    logf = np.concatenate([[0.0], np.cumsum(np.log(np.arange(1, k + 1)))])
    return np.exp(ks * np.log(max(lam, 1e-9)) - lam - logf)


def score_matrix(lh, la):
    M = np.outer(pmf(lh), pmf(la))
    return M / M.sum()


def read_scorecard_block(path, max_lines=4):
    """Return the compact track-record header of worldcup_scorecard.txt (lines before
    the '=====' detail separator), capped to max_lines. [] if absent."""
    if not path:
        return []
    p = Path(path)
    if not p.exists():
        return []
    block = []
    for ln in p.read_text(encoding="utf-8").splitlines():
        if ln.strip().startswith("====="):
            break
        block.append(ln.rstrip())
    while block and not block[-1].strip():
        block.pop()
    return block[:max_lines]


def _parse_ko(s):
    """Parse a kickoff_utc cell ('2026-06-19 22:00' or ISO) -> aware UTC datetime."""
    s = str(s).strip()
    for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M", "%Y-%m-%dT%H:%M:%S"):
        try:
            return datetime.strptime(s[:len(fmt) + 2], fmt).replace(tzinfo=timezone.utc)
        except Exception:
            continue
    return None


def _pick(r, pref):
    """argmax outcome H/D/A for a predictor prefix (e.g. 'mkt','l3'), or None if missing."""
    vals = [r.get(f"{pref}_home"), r.get(f"{pref}_draw"), r.get(f"{pref}_away")]
    if any(pd.isna(v) for v in vals):
        return None
    return "HDA"[int(np.argmax([float(v) for v in vals]))]


def build_yesterday_block(log_path, now, hours=36, max_results=6):
    """'Cómo acertamos ayer': real score + L3 1X2 hit (✓/✗) for fixtures resolved in the
    last `hours`. Honest, L3 only — ZERO market. Only settled rows with a result. [] if none."""
    p = Path(log_path)
    if not p.exists():
        return []
    try:
        df = pd.read_csv(p)
    except Exception:
        return []
    need = {"settled", "result_1x2", "result_ft_gh", "result_ft_ga", "kickoff_utc"}
    if df.empty or not need <= set(df.columns):
        return []
    df = df[df["settled"].fillna(0).astype(int) == 1]
    df = df[df["result_1x2"].isin(["H", "D", "A"])]
    cutoff = now - timedelta(hours=hours)
    rows = []
    for _, r in df.iterrows():
        ko = _parse_ko(r["kickoff_utc"])
        if ko is None or not (cutoff <= ko <= now):
            continue
        rows.append((ko, r))
    rows.sort(key=lambda t: -t[0].timestamp())
    rows = rows[:max_results]
    if not rows:
        return []
    lines = ["📅 Ayer (real · acierto 1X2 L3):"]
    for _, r in rows:
        actual = r["result_1x2"]
        l3 = _pick(r, "l3")
        l3_s = ("✓" if l3 == actual else "✗") if l3 else "–"
        h, a = str(r["home"])[:11], str(r["away"])[:11]
        try:
            score = f"{int(r['result_ft_gh'])}-{int(r['result_ft_ga'])}"
        except Exception:
            score = "?-?"
        lines.append(f"{h} {score} {a} — L3{l3_s}")
    return lines


def main(date_from, date_to, limit, compact=False, scorecard=None, max_lines=24,
         show_lineups=False, within_hours=None, show_yesterday=False, log_path=None):
    try:
        df = pd.read_csv(CARDS)
    except (pd.errors.EmptyDataError, FileNotFoundError):
        df = pd.DataFrame()
    if df.empty or "kickoff_utc" not in df.columns:
        df = pd.DataFrame(columns=["kickoff_utc"])
    df = df[df["kickoff_utc"].notna()].copy()
    if len(df):
        df["d"] = df["kickoff_utc"].str[:10]
        df = df[(df["d"] >= date_from) & (df["d"] <= date_to)].sort_values("kickoff_utc").head(limit)

    lines = []

    def out(s=""):
        print(s); lines.append(s)

    if compact:
        # COMPACT (Telegram): 2 lines/match (+1 lineup line in pre-KO). The track-record
        # block goes right after the header so it ALWAYS survives the dispatcher's 25-line
        # cut; matches are truncated so header + track-record + matches + footer fit max_lines.
        sc_block = read_scorecard_block(scorecard)          # priority 1 (track record)
        yest_block = build_yesterday_block(log_path or LOG, datetime.now(timezone.utc)) \
            if show_yesterday else []                        # priority 2 (yesterday, morning only)
        _abbr = {"corners": "córn", "cards": "tarj", "shots": "tir"}
        _shown = "/".join(_abbr[s] for s in ("corners", "cards", "shots") if s in SHOW_STATS) or "stats"
        FOOTER = (f"L3 + {_shown} = modelo de datos propio (sin cuotas). "
                  "Stats: BAJA CONF (señal débil OOS).")
        per_match = 3 if show_lineups else 2
        # Budget priority: track record > yesterday results > today's matches (trim today first).
        avail = max(0, max_lines - 1 - len(sc_block) - 1)    # minus header + footer
        yest_block = yest_block[:avail]
        avail_today = max(0, avail - len(yest_block))
        max_matches = avail_today // per_match
        df = df.head(max_matches) if max_matches < len(df) else df

        # anti-spam gate: the workflow skips the Telegram send when this is 0 in pre-KO mode.
        META.write_text(str(len(df)), encoding="utf-8")

        if within_hours is not None:
            head = f"🏆 MUNDIAL 2026 — PRE-SAQUE (próximas {within_hours:g}h · L3 modelo propio)"
        else:
            head = f"🏆 MUNDIAL 2026 — {date_from}→{date_to} (L3 = modelo propio, sin cuotas)"
        out(head)
        for ln in sc_block:
            out(ln)
        for ln in yest_block:
            out(ln)
        if len(df) == 0:
            if within_hours is not None:
                out(f"⏸️ Sin partidos en las próximas {within_hours:g}h. (Vuelve en el próximo refresco.)")
            elif not yest_block:
                out("⏸️ Sin partidos en la ventana.")
            out(FOOTER)
            (OUT_DIR / "worldcup_full_cards.txt").write_text("\n".join(lines), encoding="utf-8")
            print(f"\nWritten: {OUT_DIR/'worldcup_full_cards.txt'} ({len(lines)} lines, 0 today fixtures)")
            return
        for _, r in df.iterrows():
            lh3, ld3, la3 = r.get("our_home"), r.get("our_draw"), r.get("our_away")
            xgh, xga = r.get("our_xg_home"), r.get("our_xg_away")
            ko = str(r["kickoff_utc"])[5:16].replace("T", " ")  # MM-DD HH:MM
            grp = str(r.get("home_group") or "?").replace("Group ", "G")
            top = ""
            o25 = btts = None
            if pd.notna(xgh):
                M = score_matrix(xgh, xga)               # our L3 Poisson, NO market
                gh = np.arange(KMAX + 1)[:, None]; ga = np.arange(KMAX + 1)[None, :]
                o25 = float(M[(gh + ga) >= 3].sum())
                btts = float(M[(gh >= 1) & (ga >= 1)].sum())
                flat = sorted(((i, j, M[i, j]) for i in range(KMAX + 1) for j in range(KMAX + 1)),
                              key=lambda t: -t[2])[:2]
                top = " · ".join(f"{i}-{j}" for i, j, _ in flat)
            out(f"⚽ {r['home']} v {r['away']} · {grp} · {ko}Z")
            seg = []
            if pd.notna(lh3):
                seg.append(f"L3 {lh3*100:.0f}/{ld3*100:.0f}/{la3*100:.0f}")
            if o25 is not None:
                seg.append(f"O2.5 {o25*100:.0f}")
            if btts is not None:
                seg.append(f"BTTS {btts*100:.0f}")
            if pd.notna(xgh):
                seg.append(f"xG {xgh:.1f}-{xga:.1f}")
            if top:
                seg.append(top)
            # corners/cards/shots — opponent-adjusted DATA model (low conf), no odds.
            # only stats that beat the base-rate OOS are shown (noise-gated).
            ct, yt, sht = r.get("st_corners_total"), r.get("st_cards_total"), r.get("st_shots_total")
            if "corners" in SHOW_STATS and pd.notna(ct):
                seg.append(f"córn{ct:.0f}")
            if "cards" in SHOW_STATS and pd.notna(yt):
                seg.append(f"tarj{yt:.1f}")
            if "shots" in SHOW_STATS and pd.notna(sht):
                seg.append(f"tir{sht:.0f}")
            out("   " + " · ".join(seg))
            if show_lineups:
                LU = {"conf": "conf", "prob": "prob", "pend": "pend"}
                lh, la = r.get("lineup_home"), r.get("lineup_away")
                ih = "" if pd.isna(r.get("inj_home")) else str(r.get("inj_home")).strip()
                ia = "" if pd.isna(r.get("inj_away")) else str(r.get("inj_away")).strip()
                has_lineup = pd.notna(lh) and str(lh) in LU
                parts = []
                if has_lineup:
                    parts.append(f"XI {LU[str(lh)]}/{LU.get(str(la), 'pend')}")
                if ih or ia:
                    parts.append(f"bajas H:{(ih[:22] or '—')} A:{(ia[:22] or '—')}")
                if parts:
                    out("   📋 " + " · ".join(parts))
                elif pd.notna(r.get("hours_to_ko")):
                    out("   📋 alineaciones: pendientes (≈saque)")
        out(FOOTER)
        (OUT_DIR / "worldcup_full_cards.txt").write_text("\n".join(lines), encoding="utf-8")
        print(f"\nWritten: {OUT_DIR/'worldcup_full_cards.txt'} ({len(lines)} lines)")
        return

    out(f"WORLD CUP 2026 — FULL CARDS  {date_from}..{date_to}  ({len(df)} matches)")
    out("L3 = modelo propio (rating Layer-3 + Poisson). Datos reales, SIN cuotas/mercado.")
    out("=" * 60)

    for _, r in df.iterrows():
        h, a = r["home"], r["away"]
        ko = str(r["kickoff_utc"]).replace("T", " ")[:16]
        grp = str(r.get("home_group") or "").replace("Group ", "Gr.")
        lh3, ld3, la3 = r.get("our_home"), r.get("our_draw"), r.get("our_away")
        xgh, xga = r.get("our_xg_home"), r.get("our_xg_away")

        out("")
        out(f"🏆 {h} vs {a}")
        out(f"   {ko} · {grp}")
        # 1X2 (L3 only)
        if pd.notna(lh3):
            out(f"1X2  L3 {lh3*100:.0f}/{ld3*100:.0f}/{la3*100:.0f}")
            out(f"DC   1X {(lh3+ld3)*100:.0f}% · 12 {(lh3+la3)*100:.0f}% · X2 {(ld3+la3)*100:.0f}%")
        # goals (L3 Poisson)
        if pd.notna(xgh):
            M = score_matrix(xgh, xga)
            gh = np.arange(KMAX + 1)[:, None]; ga = np.arange(KMAX + 1)[None, :]
            tot = gh + ga
            o15 = M[tot >= 2].sum(); o25p = M[tot >= 3].sum(); o35 = M[tot >= 4].sum()
            bts = M[(gh >= 1) & (ga >= 1)].sum()
            out(f"Goals L3 Poisson O1.5 {o15*100:.0f} · O2.5 {o25p*100:.0f} · O3.5 {o35*100:.0f} · BTTS {bts*100:.0f}")
            out(f"     xG {h[:14]} {xgh:.1f} – {xga:.1f} {a[:14]}")
            # top exact scores
            flat = [((i, j), M[i, j]) for i in range(KMAX + 1) for j in range(KMAX + 1)]
            flat.sort(key=lambda kv: -kv[1])
            tops = " · ".join(f"{i}-{j} {p*100:.0f}%" for (i, j), p in flat[:4])
            out(f"     Marcadores {tops}")
        # corners/cards/shots — opponent-adjusted DATA model (low confidence).
        # noise-gated: only stats that beat the base-rate OOS appear in the ficha.
        ct, co, cl = r.get("st_corners_total"), r.get("st_corners_over"), r.get("st_corners_line")
        yt, sht = r.get("st_cards_total"), r.get("st_shots_total")
        st_parts = []
        if "corners" in SHOW_STATS and pd.notna(ct):
            seg = f"córners {ct:.1f}"
            if pd.notna(co) and pd.notna(cl):
                seg += f" (O{cl:g} {co*100:.0f}%)"
            st_parts.append(seg)
        if "cards" in SHOW_STATS and pd.notna(yt):
            st_parts.append(f"tarjetas {yt:.1f}")
        if "shots" in SHOW_STATS and pd.notna(sht):
            st_parts.append(f"tiros {sht:.0f}")
        if st_parts:
            out("Stats " + " · ".join(st_parts) + "  (modelo datos, BAJA CONF)")

    out("")
    shown = [n for n, k in [("córners", "corners"), ("tarjetas", "cards"), ("tiros", "shots")]
             if k in SHOW_STATS]
    hidden = [n for n, k in [("córners", "corners"), ("tarjetas", "cards"), ("tiros", "shots")]
              if k not in SHOW_STATS]
    out(f"L3/Poisson + {('/'.join(shown)) or 'stats'} = modelo de datos propio, SIN cuotas.")
    note = "Stats: opponent-adjusted, BAJA CONFIANZA (señal OOS débil)."
    if hidden:
        note += f" Ocultos por ruido OOS (sin señal vs media): {', '.join(hidden)}."
    out(note)

    (OUT_DIR / "worldcup_full_cards.txt").write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWritten: {OUT_DIR/'worldcup_full_cards.txt'}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--from", dest="dfrom", default="2026-06-16")
    ap.add_argument("--to", dest="dto", default="2026-06-18")
    ap.add_argument("--limit", type=int, default=4)
    ap.add_argument("--compact", action="store_true", help="dense <=2 lines/match for Telegram")
    ap.add_argument("--scorecard", default=None,
                    help="path to worldcup_scorecard.txt; its compact header is embedded (compact mode)")
    ap.add_argument("--max-lines", type=int, default=24,
                    help="hard line budget for the compact message (dispatcher cuts at 25)")
    ap.add_argument("--show-lineups", action="store_true",
                    help="compact mode: add a CONTEXT line with XI status + key absences (pre-KO)")
    ap.add_argument("--within-hours", type=float, default=None,
                    help="pre-KO header/empty-message context (next N hours)")
    ap.add_argument("--show-yesterday", action="store_true",
                    help="compact mode: add 'cómo acertamos ayer' (settled results, morning briefing)")
    ap.add_argument("--log", dest="log_path", default=None,
                    help="path to worldcup_predictions_log.csv (for --show-yesterday)")
    a = ap.parse_args()
    main(a.dfrom, a.dto, a.limit, a.compact, a.scorecard, a.max_lines,
         a.show_lineups, a.within_hours, a.show_yesterday, a.log_path)
