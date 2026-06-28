"""
WORLD CUP 2026 — CONSOLIDATED TRACK-RECORD PANEL (display/report only · NO model touch · NO API).

Reads the scorecards/logs that ALREADY exist and consolidates them into ONE Markdown file. It does
NOT recompute any prediction, does NOT import the model/predictor, and never touches a betting
endpoint. Every section SOFT-FAILS independently: a missing/garbled source -> that section says
"sin datos aún" and the rest of the panel renders fine.

Sources (all produced by the existing pipeline):
  * worldcup_scorecard.txt              -> 1X2 (L3 vs base-rate), Over2.5/BTTS, A/B total de goles.
  * worldcup_player_props_scorecard.txt -> props (gol/asistencia/tarjeta/tiros): N + métricas + estado.
  * worldcup_context_shadow_scorecard.txt -> A/B contexto (L3 puro vs ctx) sobre no triviales.
  * worldcup_calibration_monitor.txt    -> estado del monitor de calibración (OK/alerta, ECE vs nulo).

Output: worldcup_trackrecord_panel.md  (regenerated each run, committed by the workflow).
"""
from __future__ import annotations

import argparse
import re
from datetime import datetime, timezone
from pathlib import Path

OUT_DIR = Path(__file__).resolve().parent
SCORECARD = OUT_DIR / "worldcup_scorecard.txt"
PROPS = OUT_DIR / "worldcup_player_props_scorecard.txt"
CONTEXT = OUT_DIR / "worldcup_context_shadow_scorecard.txt"
CALIB = OUT_DIR / "worldcup_calibration_monitor.txt"
MXVSL3 = OUT_DIR / "worldcup_mx_vs_l3_scorecard.csv"
PANEL = OUT_DIR / "worldcup_trackrecord_panel.md"

NA = "_— sin datos aún (scorecard ausente o aún sin liquidar) —_"


# --------------------------------------------------------------------- tolerant readers
def _read(path) -> str:
    """File text, or '' if missing/unreadable (soft-fail)."""
    try:
        p = Path(path)
        return p.read_text(encoding="utf-8") if p.exists() else ""
    except Exception:
        return ""


def _search(pattern, text, *, cast=str, group=1, flags=re.M):
    """First regex group cast, or None on any miss (soft-fail per field)."""
    try:
        m = re.search(pattern, text, flags)
        if not m:
            return None
        return cast(m.group(group))
    except Exception:
        return None


def _small_n_note(n, thr):
    """Honest small-sample note when N is below the graduation threshold."""
    if n is None:
        return ""
    if thr is not None and n < thr:
        return f"  ⚠️ muestra pequeña (N={n} < umbral {thr}): métricas orientativas, aún no concluyentes."
    return ""


# --------------------------------------------------------------------- sections
def section_1x2(text):
    lines = ["## 1X2 — modelo L3 (oficial)"]
    if not text:
        lines.append(NA); return lines
    n = _search(r"(\d+)\s+resueltos", text, cast=int) or _search(r"resueltos=(\d+)", text, cast=int)
    rows = []
    for name in ("base-rate", "L3", "v2"):
        m = re.search(rf"^\s*{re.escape(name)}\s+(\d+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([+\-]?[\d.]+)",
                      text, re.M)
        if m:
            rows.append((name, *m.groups()))
    lines.append(f"**N = {n if n is not None else '?'}** partidos liquidados · 1X2 a 90' vs resultado real (sin mercado).")
    if rows:
        lines.append("")
        lines.append("| predictor | N | logloss | brier | acc% | ECE | skill vs base |")
        lines.append("|---|---:|---:|---:|---:|---:|---:|")
        for name, rn, ll, br, acc, ece, sk in rows:
            tag = " (oficial)" if name == "L3" else (" (baseline)" if name == "base-rate" else "")
            lines.append(f"| {name}{tag} | {rn} | {ll} | {br} | {acc} | {ece} | {sk}% |")
    else:
        lines.append(NA)
    # honest caveats already in the scorecard
    if "SEMÁNTICA MIXTA" in text:
        lines.append("> ⚠️ semántica mixta: parte de las filas son 'primera predicción (mañana)' y parte "
                     "'última pre-saque' (cambio lock-at-KO a mitad de torneo) — interpretar la mejora con cautela.")
    note = _small_n_note(n, 30)
    if note:
        lines.append(">" + note)
    return lines


def section_goals(text):
    lines = ["## Goles — Over 2.5 y BTTS (L3 Poisson vs base-rate)"]
    if not text:
        lines.append(NA); return lines
    got = False
    lines.append("")
    lines.append("| mercado | modelo | N | acc% | brier | logloss |")
    lines.append("|---|---|---:|---:|---:|---:|")
    for mk, real_pat in (("Over 2.5", r"Over 2\.5\s+\(real Over=(\d+)%\)"),
                         ("BTTS", r"BTTS\s+\(real Yes=(\d+)%\)")):
        rm = re.search(real_pat, text)
        if not rm:
            continue
        seg = text[rm.start():]          # slice from THIS market's data header (not the section title)
        real = rm.group(1)
        for label, pat in (("L3 (Poisson)", r"L3 \(Poisson xG\)\s+n=\s*(\d+)\s+acc\s+(\d+)%\s+Brier\s+([\d.]+)\s+logloss\s+([\d.]+)"),
                           ("base-rate", r"base-rate\s+n=\s*(\d+)\s+acc\s+(\d+)%\s+Brier\s+([\d.]+)\s+logloss\s+([\d.]+)")):
            m = re.search(pat, seg, re.M)
            if m:
                got = True
                rn, acc, br, ll = m.groups()
                suffix = f" (real {real}%)" if label.startswith("L3") else ""
                lines.append(f"| {mk}{suffix} | {label} | {rn} | {acc} | {br} | {ll} |")
    if not got:
        return ["## Goles — Over 2.5 y BTTS (L3 Poisson vs base-rate)", NA]
    # A/B total de goles (matchup vs constante)
    lines.append("")
    lines.append("### A/B total de goles — matchup vs constante")
    ab = _extract_block(text, "(1b)")
    if ab and re.search(r"a[uú]n sin|sin filas", ab, re.I):
        lines.append("_— sin filas con total constante logueado todavía (se llena tras nuevas predicciones NS) —_")
    elif ab:
        for ln in ab.splitlines():
            s = ln.strip().lstrip("-").strip()
            if s and "A/B TOTAL" not in s:
                lines.append(f"- {s}")
    else:
        lines.append(NA)
    return lines


def _extract_block(text, marker):
    """The lines from a '--- (marker) ... ---' header to the next blank line (soft)."""
    try:
        idx = text.find(marker)
        if idx < 0:
            return ""
        tail = text[idx:]
        out = []
        for ln in tail.splitlines():
            if out and not ln.strip():
                break
            out.append(ln)
        return "\n".join(out)
    except Exception:
        return ""


PROP_ES = {"goal": "gol", "assist": "asistencia", "card": "tarjeta", "shot_on": "tiros a puerta"}


def _prop_backtest_status(text, prop):
    """Backtest graduation status parsed from the props scorecard header comment (honest, not invented)."""
    try:
        if prop in ("goal", "assist") and re.search(r"GOL y ASISTENCIA\s*->\s*GRADUAD", text):
            return "validado (backtest)"
        if prop == "card" and re.search(r"TARJETA\s*->\s*GRADUAD", text):
            return "validado (backtest · tope en cola)"
        if prop == "shot_on" and re.search(r"TIROS.*->\s*RANKING", text):
            return "ranking solo (no %)"
    except Exception:
        pass
    return "—"


def section_props(text):
    lines = ["## Props de jugador (SOMBRA · heurístico)"]
    if not text:
        lines.append(NA); return lines
    settled = _search(r"partidos liquidados=(\d+)", text, cast=int)
    rowsN = _search(r"filas jugador-prop=(\d+)", text, cast=int)
    thr = _search(r"umbral graduación N>=(\d+)", text, cast=int)
    lines.append(f"**Liquidados = {settled if settled is not None else '?'}** partidos "
                 f"({rowsN if rowsN is not None else '?'} filas jugador-prop) · umbral graduación N≥{thr or '?'}.")
    prop_rows = []
    for prop in ("goal", "assist", "card", "shot_on"):
        m = re.search(rf"^\s*{prop}\s+(\d+)\s+(\d+)%\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+(\w+)",
                      text, re.M)
        if m:
            prop_rows.append((prop, *m.groups()))
    if prop_rows:
        lines.append("")
        lines.append("| prop | N | base% | logloss | brier | ECE | ¿mejora vivo? | estado backtest |")
        lines.append("|---|---:|---:|---:|---:|---:|---|---|")
        for prop, rn, base, ll, br, ece, _llb, _brb, mejora in prop_rows:
            lines.append(f"| {PROP_ES.get(prop, prop)} | {rn} | {base}% | {ll} | {br} | {ece} | "
                         f"{mejora} | {_prop_backtest_status(text, prop)} |")
    else:
        lines.append(NA)
    note = _small_n_note(settled, thr)
    if note:
        lines.append(">" + note)
    lines.append("> _Validado (backtest) = graduó en el backtest histórico (N=3062 jugador-partido). "
                 "El estado EN VIVO sigue en sombra hasta liquidar N≥umbral en partidos del Mundial._")
    return lines


def section_context(text):
    lines = ["## A/B de contexto — L3 puro vs ajuste de grupo (SOMBRA)"]
    if not text:
        lines.append(NA); return lines
    total = _search(r"liquidados \(total\)=(\d+)", text, cast=int)
    nt = _search(r"escenario NO trivial=(\d+)", text, cast=int)
    thr = _search(r"umbral graduación N>=(\d+)", text, cast=int)
    lines.append(f"**No triviales liquidados = {nt if nt is not None else '?'}** "
                 f"(de {total if total is not None else '?'} liquidados) · umbral N≥{thr or '?'}.")
    if re.search(r"MUESTRA INSUFICIENTE", text):
        lines.append("> Estado: **sigue en SOMBRA** — muestra insuficiente para graduar; los multiplicadores "
                     "son hipótesis (signo ambiguo), el scorecard es el juez.")
    else:
        verdict = _search(r"VEREDICTO:\s*(.+)", text)
        if verdict:
            lines.append(f"> Veredicto: {verdict}")
    note = _small_n_note(nt, thr)
    if note:
        lines.append(">" + note)
    return lines


def section_calib(text):
    lines = ["## Monitor de calibración L3 (1X2)"]
    if not text:
        lines.append(NA); return lines
    estado = _search(r"ESTADO:\s*(\w+)", text)
    n = _search(r"\bN=(\d+)", text, cast=int)
    ece = _search(r"ECE_observado=([\d.]+)", text)
    p95 = _search(r"nulo p95\(N=\d+\)=([\d.]+)", text)
    ll = _search(r"logloss_L3=([\d.]+)", text)
    base = _search(r"baseline=([\d.]+)", text)
    badge = "🟢 OK" if estado == "OK" else (f"🔴 {estado}" if estado else "?")
    lines.append(f"**Estado: {badge}** · N={n if n is not None else '?'}")
    if ece is not None and p95 is not None:
        verdict = "dentro del ruido" if (_to_f(ece) is not None and _to_f(p95) is not None
                                         and _to_f(ece) <= _to_f(p95)) else "por encima del nulo"
        lines.append(f"- ECE observado = **{ece}** vs nulo p95 = {p95} → {verdict}.")
    if ll is not None and base is not None:
        lines.append(f"- logloss L3 = **{ll}** vs baseline {base} "
                     f"({'bate' if (_to_f(ll) is not None and _to_f(base) is not None and _to_f(ll) < _to_f(base)) else 'NO bate'} la tasa base).")
    lines.append("> _Monitor solo alerta; NO toca el modelo._")
    return lines


def _to_f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def section_mx_vs_l3(csv_text):
    """A/B EN VIVO invertido: motor máximo (mx) vs L3, leído del CSV del scorer (read-only).
    El CSV trae una fila por (market,metric) con columnas market,metric,l3,mx,leader,diff,n,since."""
    rows = []
    n, since = None, None
    for i, raw in enumerate(csv_text.splitlines()):
        raw = raw.strip()
        if not raw or (i == 0 and raw.lower().startswith("market,")):
            continue
        parts = raw.split(",")
        if len(parts) < 8:
            continue
        market, metric, l3, mx, leader, diff, nn, since = parts[:8]
        n = nn
        rows.append((market, metric, l3, mx, leader, diff))
    since_tag = f" (en vivo, desde {since})" if since and since != "?" else " (en vivo)"
    lines = [f"## L3 vs Motor máximo{since_tag}"]
    if not rows:
        lines.append("_— sin datos aún: aún no hay partidos liquidados con predicción del motor máximo "
                     "(mx entró en vivo el 27-jun; solo se mide desde entonces, anti-hindsight) —_")
        return lines
    led = {"mx": "**mx**", "L3": "L3", "empate": "empate", "n/d": "—"}
    lines.append(f"**N = {n or '?'}** partidos liquidados con predicción mx · cara a cara congelado al "
                 "saque (lock-at-KO, anti-hindsight) vs resultado real · sin mercado.")
    lines.append("")
    lines.append("| métrica | L3 | mx | líder |")
    lines.append("|---|---:|---:|---|")
    label = {"acc": "acc%", "logloss": "logloss", "brier": "brier"}
    for market, metric, l3, mx, leader, _diff in rows:
        lines.append(f"| {market} {label.get(metric, metric)} | {l3} | {mx} | {led.get(leader, leader)} |")
    n_int = _to_f(n)
    if n_int is not None and n_int < 30:
        lines.append(f"> ⚠️ muestra pequeña (N={n} < 30): **NO se declara ganador**, el acumulado crece "
                     "hasta el final del Mundial. Si el mx queda por detrás, este marcador + el A/B son la "
                     "base para revertir (MAXMODEL_LIVE=False).")
    lines.append("> _Solo mide; NO toca el modelo ni las predicciones (mx_*/l3_* congelados en el log)._")
    return lines


# --------------------------------------------------------------------- assembly
def build_panel_text(scorecard=SCORECARD, props=PROPS, context=CONTEXT, calib=CALIB,
                     mxvsl3=MXVSL3, now=None):
    """Consolidated Markdown panel from the existing scorecards. Pure read + format; soft-fail."""
    gen = now or datetime.now(timezone.utc).isoformat(timespec="seconds")
    out = [
        "# 📊 Panel de Track-Record — Mundial 2026 (vSIGMA)",
        f"_Generado: {gen} · consolidado de scorecards existentes · **solo lectura, no recalcula "
        "predicciones** · sin mercado/cuotas._",
        "",
        "> Honestidad: **validado** = superó el baseline en backtest histórico; **sombra** = en "
        "observación en vivo; donde la muestra aún no basta se marca explícitamente.",
        "",
    ]
    for fn, src in ((section_1x2, scorecard), (section_goals, scorecard),
                    (section_mx_vs_l3, mxvsl3), (section_props, props),
                    (section_context, context), (section_calib, calib)):
        try:
            out += fn(_read(src))
        except Exception as e:  # noqa: BLE001  (soft-fail: a broken section never sinks the panel)
            out += [f"_(sección no disponible: {type(e).__name__})_"]
        out += [""]
    out += ["---", "_Panel generado por build_worldcup_trackrecord_panel.py · no modifica el modelo "
            "ni las predicciones · World Cup = producto en sombra aislado._"]
    return "\n".join(out) + "\n"


def main(out_path=PANEL):
    text = build_panel_text()
    Path(out_path).write_text(text, encoding="utf-8")
    print(f"Written: {out_path}")
    return text


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Consolidated World Cup track-record panel (read-only).")
    ap.add_argument("--out", default=str(PANEL))
    a = ap.parse_args()
    main(a.out)
