"""
WORLD CUP 2026 — PRE-KICKOFF focused alert (~1h before each match, on the OFFICIAL lineup).

Goal: the moment a match's starting XI is CONFIRMED and kickoff is imminent, send ONE compact
Telegram message focused on THAT match only — so rotations (e.g. a group winner resting players)
are captured. It is NOT a re-send of the daily briefing.

HONESTY: the L3 1X2 barely moves with the lineup (it is squad strength, not who starts). The
value of this alert is (i) confirming who ACTUALLY plays and (ii) the player props now built on the
CONFIRMED XI, plus the L3-adj nudge for today's key absences. We say so; we do NOT claim the
prediction "improves" because of this.

SELECTION — a fixture is alerted iff ALL of:
  (a) it kicks off within the next WINDOW_MIN minutes (and has NOT started -> anti-hindsight),
  (b) BOTH teams' XI are CONFIRMED in the card (lineup_home==lineup_away=='conf', i.e. the
      authoritative /fixtures/lineups startXI with >=11 published),
  (c) it has NOT been alerted pre-KO before (dedup via worldcup_preko_sent.csv).
No candidate -> NOTHING is written/sent (silent run).

DEDUP is two-step: `select` writes the manifest + a PENDING list but does NOT mark anything;
`mark-sent` appends the pending fixtures to the sent-state file (called AFTER the send step), so a
run that dies before sending never marks a fixture as alerted.

SAFEGUARDS: reads only the card + the shadow props log + the sent-state file; writes only the
message files + manifest + pending/sent state. NO API, NO betting endpoints. Anti-hindsight (only
strictly pre-KO NS fixtures; never touches settled/result_*). Does NOT touch the L3 / calibration /
lock-at-KO of the daily briefing. Explicit git add (state file) in the workflow.
"""
from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

OUT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(OUT_DIR))
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

import build_worldcup_full_card as F  # noqa: E402  (reuse es_name/score_matrix/props_block/fmt_ko)

CARDS = OUT_DIR / "worldcup_cards.csv"
SENT = OUT_DIR / "worldcup_preko_sent.csv"          # dedup state: one row per alerted fixture
PENDING = OUT_DIR / "worldcup_preko_pending.csv"    # fixtures selected this run, not yet marked
MANIFEST = OUT_DIR / "worldcup_preko_manifest.txt"  # 'path|title' per message (workflow send loop)
PREVIEW = OUT_DIR / "worldcup_preko_preview.txt"    # combined preview for the CI log
WINDOW_MIN = 90.0                                   # alert fixtures kicking off within this window
SENT_COLUMNS = ["fixture_id", "kickoff_utc", "home", "away", "sent_at_utc"]


def _now():
    return datetime.now(timezone.utc)


def _parse_ko(s):
    """Parse a kickoff_utc cell -> aware UTC datetime, or None (soft)."""
    return F._parse_ko(s)


def _load_sent_ids():
    """Set of fixture_ids already alerted pre-KO. {} on any problem (soft -> may re-alert once)."""
    try:
        if SENT.exists():
            df = pd.read_csv(SENT)
            if "fixture_id" in df.columns:
                return set(pd.to_numeric(df["fixture_id"], errors="coerce").dropna().astype(int))
    except Exception:
        pass
    return set()


def _is_conf(v):
    return str(v).strip().lower() == "conf"


def select_candidates(cards, sent_ids, now, window_min=WINDOW_MIN):
    """Pure selection: rows that are (a) imminent & not started, (b) both XI confirmed,
    (c) not already alerted. Returns list of (row, minutes_to_ko) sorted by soonest KO."""
    out = []
    if cards is None or len(cards) == 0:
        return out
    for _, r in cards.iterrows():
        fid = r.get("fixture_id")
        if pd.isna(fid):
            continue
        ko = _parse_ko(r.get("kickoff_utc"))
        if ko is None:
            continue
        mins = (ko - now).total_seconds() / 60.0
        # (a) strictly pre-KO (mins>0 => not started, anti-hindsight) AND within the window
        if not (0.0 < mins <= window_min):
            continue
        # (b) BOTH teams' XI confirmed (authoritative /fixtures/lineups startXI in the card)
        if not (_is_conf(r.get("lineup_home")) and _is_conf(r.get("lineup_away"))):
            continue
        # (c) dedup
        if int(fid) in sent_ids:
            continue
        out.append((r, mins))
    out.sort(key=lambda t: t[1])
    return out


def _l3_adj_lines(r, h, a):
    """Optional L3-adj line for today's key absences (same stored fields as the daily ficha)."""
    lines = []
    ah, ad, aa = r.get("adj_home"), r.get("adj_draw"), r.get("adj_away")
    if pd.notna(ah):
        motivo = []
        absh, absa = r.get("adj_absent_home"), r.get("adj_absent_away")
        if isinstance(absh, str) and absh.strip():
            motivo.append(f"{h} sin {absh}")
        if isinstance(absa, str) and absa.strip():
            motivo.append(f"{a} sin {absa}")
        line = (f"↳ Ajuste por bajas (heurístico, orientativo): "
                f"{h} {ah*100:.0f}% · Empate {ad*100:.0f}% · {a} {aa*100:.0f}%")
        if motivo:
            line += f" — {' · '.join(motivo)}"
        lines.append(line)
    return lines


def render_message(r, mins, props_fn=None):
    """(title, body_lines) for one imminent confirmed fixture. Compact, focused, ZERO odds.
    props_fn(fixture_id) -> list[str] (defaults to the shadow props block with '(XI confirmado)')."""
    props_fn = props_fn or F.props_block
    h, a = F.es_name(r.get("home")), F.es_name(r.get("away"))
    grp = str(r.get("home_group") or "").replace("Group ", "Gr. ").strip() or "Gr. ?"
    mins_i = int(round(mins))
    title = f"⚡ Mundial — alineación confirmada: {h} vs {a}"
    lines = [f"⚡ Alineación confirmada — {h} vs {a}",
             f"⏱️ Saque en ~{mins_i} min · {grp} · {F.fmt_ko(r.get('kickoff_utc'))}"]

    lh, ld, la = r.get("our_home"), r.get("our_draw"), r.get("our_away")
    if pd.notna(lh):
        lines.append(f"Resultado L3: {h} {lh*100:.0f}% · Empate {ld*100:.0f}% · {a} {la*100:.0f}% "
                     f"(apenas cambia con el XI — es fuerza de selección)")
        lines += _l3_adj_lines(r, h, a)

    xgh, xga = r.get("our_xg_home"), r.get("our_xg_away")
    if pd.notna(xgh):
        M = F.score_matrix(xgh, xga)
        gh = np.arange(F.KMAX + 1)[:, None]; ga = np.arange(F.KMAX + 1)[None, :]
        o25 = float(M[(gh + ga) >= 3].sum()); btts = float(M[(gh >= 1) & (ga >= 1)].sum())
        lines.append(f"Goles esperados: {xgh:.1f}–{xga:.1f} (total {xgh + xga:.1f}) · "
                     f"Over 2.5: {o25*100:.0f}% · BTTS: {btts*100:.0f}%")

    # player props built on the CONFIRMED XI (the props log basis is lineup_confirmed -> the block
    # carries '(XI confirmado)'). Same shadow numbers as logged; experimental label included.
    try:
        lines += props_fn(r.get("fixture_id"))
    except Exception:
        pass

    lines.append("ℹ️ Valor del aviso: confirmar quién juega de verdad + props con XI confirmado. "
                 "La predicción 1X2 NO mejora por esto (es fuerza de selección).")
    return title, lines


def _write_empty(reason):
    """Anti-spam: no candidates -> empty manifest + empty pending (send nothing)."""
    MANIFEST.write_text("", encoding="utf-8")
    PENDING.write_text("", encoding="utf-8")
    PREVIEW.write_text(f"(pre-KO: {reason} -> no se envía nada)\n", encoding="utf-8")
    # clear any stale page files from a previous run
    for f in OUT_DIR.glob("worldcup_preko_msg_*.txt"):
        try:
            f.unlink()
        except Exception:
            pass


def cmd_select(now=None):
    now = now or _now()
    try:
        cards = pd.read_csv(CARDS)
    except (pd.errors.EmptyDataError, FileNotFoundError):
        cards = pd.DataFrame()
    sent_ids = _load_sent_ids()
    cands = select_candidates(cards, sent_ids, now)
    if not cands:
        _write_empty("sin partidos inminentes con XI confirmado no avisados")
        print("preko select: 0 candidate(s) -> silent (nothing to send).")
        return 0

    for f in OUT_DIR.glob("worldcup_preko_msg_*.txt"):
        try:
            f.unlink()
        except Exception:
            pass

    manifest_lines, pending_rows, combined = [], [], []
    for i, (r, mins) in enumerate(cands, 1):
        title, body = render_message(r, mins)
        fp = OUT_DIR / f"worldcup_preko_msg_{i}.txt"
        fp.write_text("\n".join(body) + "\n", encoding="utf-8")
        manifest_lines.append(f"{fp}|{title}")
        pending_rows.append({"fixture_id": int(r.get("fixture_id")), "kickoff_utc": r.get("kickoff_utc"),
                             "home": r.get("home"), "away": r.get("away"),
                             "sent_at_utc": now.isoformat(timespec="seconds")})
        combined.append(f"===== {title} =====")
        combined.extend(body)
        combined.append("")

    MANIFEST.write_text("\n".join(manifest_lines) + "\n", encoding="utf-8")
    pd.DataFrame(pending_rows, columns=SENT_COLUMNS).to_csv(PENDING, index=False)
    PREVIEW.write_text("\n".join(combined), encoding="utf-8")
    for c in combined:
        print(c)
    print(f"preko select: {len(cands)} candidate(s) -> {MANIFEST.name} (+ pending, not yet marked).")
    return len(cands)


def cmd_mark_sent():
    """Append the pending fixtures to the sent-state file (dedup by fixture_id). Call AFTER the
    send step so a run that dies before sending never marks a fixture as alerted."""
    try:
        pend = pd.read_csv(PENDING) if PENDING.exists() else pd.DataFrame(columns=SENT_COLUMNS)
    except (pd.errors.EmptyDataError, FileNotFoundError):
        pend = pd.DataFrame(columns=SENT_COLUMNS)
    if pend.empty:
        print("preko mark-sent: nothing pending.")
        return
    try:
        sent = pd.read_csv(SENT) if SENT.exists() else pd.DataFrame(columns=SENT_COLUMNS)
    except (pd.errors.EmptyDataError, FileNotFoundError):
        sent = pd.DataFrame(columns=SENT_COLUMNS)
    both = pd.concat([sent, pend], ignore_index=True)
    for c in SENT_COLUMNS:
        if c not in both.columns:
            both[c] = np.nan
    both = both[SENT_COLUMNS].drop_duplicates(subset=["fixture_id"], keep="first")
    both.to_csv(SENT, index=False)
    # clear pending so a later mark-sent is a no-op
    PENDING.write_text("", encoding="utf-8")
    print(f"preko mark-sent: +{len(pend)} fixture(s) marked -> {SENT.name} ({len(both)} total).")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="World Cup PRE-KO focused alert (isolated, no API).")
    ap.add_argument("cmd", choices=["select", "mark-sent"])
    a = ap.parse_args()
    if a.cmd == "select":
        cmd_select()
    else:
        cmd_mark_sent()
