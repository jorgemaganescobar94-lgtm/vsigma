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
    STAT_CONF = stats_model.stat_confidence()   # {stat: 'media'|'baja'} per measured OOS lift
except Exception:
    SHOW_STATS = {"corners", "cards", "shots"}
    STAT_CONF = {}

# per-stat confidence rendering: honest, data-driven (shots ~43% lift -> media; corners ~24% ->
# baja; cards hidden). One tag PER STAT (not a single global label that mixes media + baja).
_STAT_ES = {"corners": "córners", "shots": "tiros", "cards": "tarjetas"}
_CONF_ES = {"media": "conf media", "baja": "baja conf"}


def _conf_legend(stats):
    """Confidence legend for the given shown stats, most-confident first: 'tiros: conf media ·
    córners: baja conf'. '' if no confidence info (soft-fail -> the line just shows no tag)."""
    order = {"media": 0, "baja": 1}
    items = [(s, STAT_CONF.get(s)) for s in stats if STAT_CONF.get(s) in _CONF_ES]
    items.sort(key=lambda kv: (order.get(kv[1], 9), kv[0]))
    return " · ".join(f"{_STAT_ES.get(s, s)}: {_CONF_ES[lvl]}" for s, lvl in items)
try:
    import build_worldcup_enrichment as wc_enrich  # noqa: E402  (post-FT [REAL] lines, soft)
except Exception:
    wc_enrich = None
try:
    import worldcup_stats_level_correction as stats_correction  # noqa: E402  (shown córners/tiros level fix)
except Exception:
    stats_correction = None
try:
    import worldcup_card_prop_correction as card_correction  # noqa: E402  (shown p_card deflation, reversible)
except Exception:
    card_correction = None

OUT_DIR = Path(__file__).resolve().parent
CARDS = OUT_DIR / "worldcup_cards.csv"
LOG = OUT_DIR / "worldcup_predictions_log.csv"
META = OUT_DIR / "worldcup_render_meta.txt"  # fixture count for the workflow anti-spam gate
MANIFEST = OUT_DIR / "worldcup_messages_manifest.txt"  # paginated send list: "path|title" per line
MXVSL3 = OUT_DIR / "worldcup_mx_vs_l3_scorecard.txt"  # read-only mx-vs-L3 marker (compact line in header)
KMAX = 10


def pmf(lam, k=KMAX):
    ks = np.arange(k + 1)
    logf = np.concatenate([[0.0], np.cumsum(np.log(np.arange(1, k + 1)))])
    return np.exp(ks * np.log(max(lam, 1e-9)) - lam - logf)


def score_matrix(lh, la):
    M = np.outer(pmf(lh), pmf(la))
    return M / M.sum()


# WC-2026 team names in Spanish (public facts); fallback = original name.
NAME_ES = {
    "Algeria": "Argelia", "Australia": "Australia", "Austria": "Austria", "Belgium": "Bélgica",
    "Bosnia & Herzegovina": "Bosnia", "Brazil": "Brasil", "Canada": "Canadá",
    "Cape Verde Islands": "Cabo Verde", "Colombia": "Colombia", "Congo DR": "RD Congo",
    "Croatia": "Croacia", "Curaçao": "Curazao", "Czechia": "Chequia", "Ecuador": "Ecuador",
    "Egypt": "Egipto", "England": "Inglaterra", "France": "Francia", "Germany": "Alemania",
    "Ghana": "Ghana", "Haiti": "Haití", "Iran": "Irán", "Iraq": "Irak",
    "Ivory Coast": "Costa de Marfil", "Japan": "Japón", "Jordan": "Jordania", "Mexico": "México",
    "Morocco": "Marruecos", "Netherlands": "Países Bajos", "New Zealand": "Nueva Zelanda",
    "Norway": "Noruega", "Panama": "Panamá", "Paraguay": "Paraguay", "Portugal": "Portugal",
    "Qatar": "Catar", "Saudi Arabia": "Arabia Saudí", "Scotland": "Escocia", "Senegal": "Senegal",
    "South Africa": "Sudáfrica", "South Korea": "Corea del Sur", "Spain": "España",
    "Sweden": "Suecia", "Switzerland": "Suiza", "Tunisia": "Túnez", "Türkiye": "Turquía",
    "USA": "EE. UU.", "Uruguay": "Uruguay", "Uzbekistan": "Uzbekistán",
}
MONTHS_ES = ["", "ene", "feb", "mar", "abr", "may", "jun",
             "jul", "ago", "sep", "oct", "nov", "dic"]


def es_name(name):
    return NAME_ES.get(str(name), str(name))


def fmt_ko(kickoff_utc):
    """'2026-06-21 16:00' -> '21 jun · 16:00Z'. Fallback to the raw string."""
    ko = _parse_ko(kickoff_utc)
    if ko is None:
        return str(kickoff_utc)[:16]
    return f"{ko.day} {MONTHS_ES[ko.month]} · {ko:%H:%M}Z"


# Knockout round labels (ES). Order matters: 'final' is a substring of 'semi-finals' etc., so the
# more specific keys are checked first (dict iteration is insertion order).
KNOCKOUT_ES = {
    "round of 32": "Dieciseisavos", "round of 16": "Octavos",
    "quarter-finals": "Cuartos", "quarter finals": "Cuartos", "quarterfinals": "Cuartos",
    "semi-finals": "Semifinal", "semi finals": "Semifinal", "semifinals": "Semifinal",
    "3rd place final": "3.º y 4.º puesto", "third place": "3.º y 4.º puesto",
    "final": "Final",
}


def is_knockout(round_str):
    """True for a knockout round (anything that is NOT a group-stage match). Soft on None."""
    return "group" not in str(round_str or "").lower()


def round_label_es(round_str, default="Eliminatoria"):
    """Spanish chip for a knockout round (Octavos/Cuartos/Semifinal/Final/Dieciseisavos);
    raw string if the label is unrecognised. Pure display, no model logic."""
    key = str(round_str or "").strip().lower()
    for k, v in KNOCKOUT_ES.items():
        if k in key:
            return v
    return str(round_str or "").strip() or default


def chip_es(r):
    """Header chip for a fixture: knockout round name in knockouts, group otherwise."""
    if is_knockout(r.get("round")):
        return round_label_es(r.get("round"))
    return str(r.get("home_group") or "").replace("Group ", "Gr. ").strip() or "Gr. ?"


# --------------------------------------------------------------------- player props (SHADOW)
PROPS_LOG = OUT_DIR / "worldcup_player_props_log.csv"
# Per-prop labelling after the historical backtest (N=3062 jugador-partido, internacionales 2024-25)
# AND the re-test con los inputs del MODELO DE STATS de producción (props_retest_stats_inputs_*):
# gol + asistencia GRADUARON (baten baseline en logloss+brier, ECE<=0.02). tarjeta GRADÚA con los
# inputs del modelo (bate baseline logloss+brier, ECE 0.032) -> VALIDADOS, con TOPE de display en la
# cola (p>CARD_CAP_P: calibración optimista/n pequeño en la cola alta). tiros = RANKING validado
# (orden fiable; su % NO se muestra: con inputs del modelo el logloss sigue < baseline). Sin sección
# experimental: todo lo que se muestra está validado, los tiros solo como ORDEN (no probabilidad).
VALID_LABEL = "📊 Validado en backtest histórico (probabilístico):"
VALID_NOTE = "  (Mundial neutral/eliminatoria: se sigue confirmando en vivo.)"
CARD_CAP_P = 0.45                # display cap: card % above this is shown as "45%+"
CARD_CAP_LABEL = "45%+"
CARD_NOTE = ("  (Tarjeta: los % por encima de 45% se muestran como \"45%+\" — calibración "
             "conservadora en la cola alta, muestra pequeña.)")
_props_cache = None


def _card_pct(p):
    """Card % string with the tail cap: p>CARD_CAP_P -> '45%+' (no se muestra el valor inflado)."""
    try:
        p = float(p)
    except (TypeError, ValueError):
        return CARD_CAP_LABEL
    return CARD_CAP_LABEL if p > CARD_CAP_P else f"{p * 100:.0f}%"


def _load_props():
    """Lazy-load the shadow props log ONCE. Returns a DataFrame (empty on any problem)."""
    global _props_cache
    if _props_cache is None:
        try:
            _props_cache = pd.read_csv(PROPS_LOG) if PROPS_LOG.exists() else pd.DataFrame()
        except Exception:
            _props_cache = pd.DataFrame()
    return _props_cache


def _xi_status(sub):
    """XI-provisionality suffix for the props label, read from the logged 'basis' (SAME origin as
    the props themselves). 'probable*' -> provisional note; 'lineup_confirmed' -> confirmed.
    Provisional wins when the two teams disagree (honest). '' if basis missing (soft-fail)."""
    try:
        if sub is None or "basis" not in sub.columns:
            return ""
        vals = [str(b) for b in sub["basis"].dropna().unique() if str(b).strip()]
        if not vals:
            return ""
        if all(v == "lineup_confirmed" for v in vals):
            return " (XI confirmado)"
        if any(v.startswith("probable") for v in vals):
            return (" (XI probable · provisional — se actualiza con la alineación "
                    "oficial ~1h antes del saque)")
        return ""
    except Exception:
        return ""


def props_lines(sub, name_fn=str):
    """VALIDADOS props block from this fixture's logged rows (the SAME numbers as the shadow log;
    NOT recomputed). All shown props are validados: gol + asistencia (ECE<=0.02), tarjeta (con TOPE
    de display en p>CARD_CAP_P, calibración optimista en la cola) y tiros (solo ORDEN, sin %: su
    logloss no bate baseline ni con los inputs del modelo). [] if no usable rows. Soft-fail: any
    error -> []; a missing prop just omits its line. The XI tag rides the VALIDADOS header."""
    try:
        if sub is None or len(sub) == 0:
            return []
        if "is_xi" in sub.columns:
            sub = sub[pd.to_numeric(sub["is_xi"], errors="coerce").fillna(1) == 1]
        if len(sub) == 0:
            return []

        def _top(col, k):
            if col not in sub.columns:
                return []
            t = sub.dropna(subset=[col]).copy()
            t = t[pd.to_numeric(t[col], errors="coerce") > 0].sort_values(col, ascending=False).head(k)
            return list(t.iterrows())

        lines = []
        valid = []
        gl = _top("p_goal", 3)
        if gl:
            valid.append("  Gol: " + " · ".join(
                f"{name_fn(rr['player'])} {float(rr['p_goal']) * 100:.0f}%" for _, rr in gl))
        asst = _top("p_assist", 3)
        if asst:
            valid.append("  Asistencia: " + " · ".join(
                f"{name_fn(rr['player'])} {float(rr['p_assist']) * 100:.0f}%" for _, rr in asst))
        # tarjeta GRADUADA (inputs del modelo: bate baseline logloss+brier, ECE 0.032) con TOPE en cola
        cd = _top("p_card", 2)
        card_capped = False
        if cd:
            valid.append("  Tarjeta: " + " · ".join(
                f"{name_fn(rr['player'])} {_card_pct(rr['p_card'])}" for _, rr in cd))
            card_capped = any(float(rr["p_card"]) > CARD_CAP_P for _, rr in cd)
        # tiros = ranking validado: orden fiable, % NO mostrado (no aporta skill de logloss)
        sh = _top("exp_shots", 3)
        if sh:
            valid.append("  Tiros (orden, no probabilidad): "
                         + " > ".join(name_fn(rr["player"]) for _, rr in sh))
        if valid:
            lines.append(VALID_LABEL + _xi_status(sub))
            lines += valid
            lines.append(VALID_NOTE)
            if card_capped:
                lines.append(CARD_NOTE)
        return lines
    except Exception:
        return []


def props_block(fid):
    """Props lines for a fixture, read from the shadow log. [] if absent/soft-fail."""
    try:
        df = _load_props()
        if df is None or df.empty or "fixture_id" not in df.columns or pd.isna(fid):
            return []
        sub = df[pd.to_numeric(df["fixture_id"], errors="coerce") == int(fid)]
        # 🔴 CARD_PROP_CORRECTION (reversible): deflate the SHOWN p_card only (gol/asistencia untouched),
        # on a COPY -> the props log stays RAW (no leakage; probe/scorecard keep measuring the model).
        # Flag OFF / no state -> Δ=0, identical card. Soft-fail.
        if card_correction is not None:
            try:
                sub = card_correction.apply_to_props_df(sub)
            except Exception:
                pass
        return props_lines(sub, name_fn=lambda n: es_name(str(n)))
    except Exception:
        return []


# Honest framing for the live engine (NO claim of being more accurate; probabilistic, no market).
MX_NOTE = ("Predicción: modelo amplio (núcleo L3 + forma/H2H/descanso) — probabilístico, "
           "sin certeza ni mercado")


def pred_1x2(r):
    """Prediction to DISPLAY/SEND. CHAIN mx -> contexto -> lesiones, so priority is:
    inj_* (LIVE injuries, last link) > ctx_* (group context CHAINED on the shown engine) > mx_* (the
    live MAX engine) > pure L3 our_*. ctx_* is now computed ON TOP of mx_* (base = mx if present, else
    L3) by delta-Poisson, so it already carries the max engine; that is why ctx_* outranks mx_* here.
    our_*/mx_* are NEVER overwritten (shadow for A/B + exact rollback): CONTEXT_LIVE off -> no ctx_* ->
    falls back to mx_* exactly; MAXMODEL_LIVE off too -> L3; INJURIES_LIVE off -> no inj_*.
    Returns (ph,pd,pa,xg_home,xg_away,note). inj_* keeps the engine framing (its label is its OWN ℹ️
    line); ctx_* returns the context_note so the 'por qué' annotates the scenario."""
    if pd.notna(r.get("inj_home")):
        return (r.get("inj_home"), r.get("inj_draw"), r.get("inj_away"),
                r.get("inj_xg_home"), r.get("inj_xg_away"), MX_NOTE)
    if pd.notna(r.get("ctx_home")):
        note = r.get("context_note")
        return (r.get("ctx_home"), r.get("ctx_draw"), r.get("ctx_away"),
                r.get("ctx_xg_home"), r.get("ctx_xg_away"),
                note if isinstance(note, str) and note.strip() else MX_NOTE)
    if pd.notna(r.get("mx_home")):
        return (r.get("mx_home"), r.get("mx_draw"), r.get("mx_away"),
                r.get("mx_xg_home"), r.get("mx_xg_away"), MX_NOTE)
    return (r.get("our_home"), r.get("our_draw"), r.get("our_away"),
            r.get("our_xg_home"), r.get("our_xg_away"), None)


# --------------------------------------------------------------------- briefing digest (display-only)
# Two ADDITIVE briefing extras derived ONLY from the predictions already shown (pred_1x2 -> ctx_* if
# present, else our_*). NO recompute, NO model touch, NO market (so NO "value"/"apuesta" wording —
# this is a digest of the model's most confident calls, not a betting recommendation). Soft-fail:
# any problem -> None/[] and the briefing renders exactly as before.
FIRMEST_LABEL = "🎯 PREDICCIONES MÁS FIRMES DE HOY (mayor confianza del modelo · solo informativo):"


def _displayed_probs(r):
    """(p_home, p_draw, p_away, xg_home, xg_away) as DISPLAYED (ctx_* if present, else our_*).
    None if the 1X2 probabilities are missing."""
    lh, ld, la, xgh, xga, _note = pred_1x2(r)
    if pd.isna(lh) or pd.isna(ld) or pd.isna(la):
        return None
    return float(lh), float(ld), float(la), xgh, xga


def day_summary_line(df):
    """One-line day digest from the DISPLAYED predictions: #matches + clearest favourite (highest
    single-TEAM prob across the slate) + most balanced match (lowest max-class prob). Display only.
    None if no usable prediction. Soft-fail -> None."""
    try:
        best_fav = None    # (team_prob, team_name)
        most_even = None   # (max_class_prob, "home–away")
        n = 0
        for _, r in df.iterrows():
            p = _displayed_probs(r)
            if p is None:
                continue
            n += 1
            ph, pd_, pa, _xgh, _xga = p
            h, a = es_name(r["home"]), es_name(r["away"])
            fav_prob, fav_team = (ph, h) if ph >= pa else (pa, a)
            if best_fav is None or fav_prob > best_fav[0]:
                best_fav = (fav_prob, fav_team)
            mx = max(ph, pd_, pa)
            if most_even is None or mx < most_even[0]:
                most_even = (mx, f"{h}–{a}")
        if n == 0:
            return None
        parts = [f"📅 {len(df)} partido{'s' if len(df) != 1 else ''} hoy"]
        if best_fav is not None:
            parts.append(f"favorito más claro: {best_fav[1]} ({best_fav[0] * 100:.0f}%)")
        if most_even is not None and n >= 2:   # 'most even' only means something with >=2 matches
            parts.append(f"más parejo: {most_even[1]}")
        return " · ".join(parts)
    except Exception:
        return None


def firmest_predictions_block(df, top_n=3):
    """Top-N matches by MODEL CONFIDENCE (highest winning-class prob), with the called outcome,
    its % and xG. A digest of the most confident calls — explicitly NOT value/bets (no market).
    [] if <2 usable predictions (a 'top' needs a ranking) or on soft-fail."""
    try:
        cand = []
        for _, r in df.iterrows():
            p = _displayed_probs(r)
            if p is None:
                continue
            ph, pd_, pa, xgh, xga = p
            probs = [ph, pd_, pa]
            k = int(np.argmax(probs))
            h, a = es_name(r["home"]), es_name(r["away"])
            winner = h if k == 0 else ("Empate" if k == 1 else a)
            cand.append((probs[k], h, a, winner, xgh, xga))
        if len(cand) < 2:
            return []
        cand.sort(key=lambda t: -t[0])
        lines = [FIRMEST_LABEL]
        for conf, h, a, winner, xgh, xga in cand[:top_n]:
            xg = f" · xG {float(xgh):.1f}-{float(xga):.1f}" if pd.notna(xgh) and pd.notna(xga) else ""
            lines.append(f"  {h} vs {a} — {winner} {conf * 100:.0f}%{xg}")
        return lines
    except Exception:
        return []


def match_block(r, show_lineups=False):
    """Readable, labelled per-match card (list of lines). Data model only, ZERO odds."""
    h, a = es_name(r["home"]), es_name(r["away"])
    ko_round = is_knockout(r.get("round"))   # knockout -> round chip + advance line + draw relabel
    lines = [f"🏆 {h} vs {a} — {chip_es(r)} · {fmt_ko(r.get('kickoff_utc'))}"]

    # CONTEXTO EN VIVO: la predicción mostrada/enviada es la ajustada por escenario de grupo (ctx_*)
    # cuando existe; si no (flag off / trivial / soft-fail) -> L3 puro. 'our_*' nunca se sobrescribe.
    lh, ld, la, xgh, xga, ctx_note = pred_1x2(r)
    if pd.notna(lh):
        if ko_round:
            # In a knockout the L3 1X2 is still the 90' result (draw = goes to extra time). Relabel
            # the draw and add a heuristic P(advance) = P(win 90') + P(draw 90')×0.5 (ET/penalties
            # ≈ coin flip). Pure render from the stored probs; the model is NOT touched.
            lines.append(f"Resultado a 90': {h} {lh*100:.0f}% · "
                         f"Empate a 90' (→ prórroga) {ld*100:.0f}% · {a} {la*100:.0f}%")
            pa_h, pa_a = lh + ld * 0.5, la + ld * 0.5
            lines.append(f"Avance (heurístico: prórroga/penaltis ≈ moneda al aire): "
                         f"{h} {pa_h*100:.0f}% · {a} {pa_a*100:.0f}%")
        else:
            lines.append(f"Resultado: {h} {lh*100:.0f}% · Empate {ld*100:.0f}% · {a} {la*100:.0f}%")
        # INJURIES_LIVE: etiqueta honesta del ajuste por bajas (la predicción mostrada YA lo lleva via
        # pred_1x2 -> inj_*). Línea propia, framing transparente. Soft: sin inj_* -> no aparece.
        inj_note = r.get("inj_note")
        if pd.notna(r.get("inj_home")) and isinstance(inj_note, str) and inj_note.strip():
            lines.append(f"ℹ️ {inj_note}")
        # L3-adj SECONDARY heuristic line, UNDER the official L3. Soft: only if an adjustment
        # was logged (Δ≠0). L3 stays first and official; this is labelled, not validated.
        # SUPRIMIDA cuando hay ajuste de bajas EN VIVO (inj_*) para no mostrar dos ajustes a la vez.
        ah, ad, aa = r.get("adj_home"), r.get("adj_draw"), r.get("adj_away")
        if pd.notna(ah) and pd.isna(r.get("inj_home")):
            lines.append(f"↳ Ajuste hoy (heurístico): {h} {ah*100:.0f}% · "
                         f"Empate {ad*100:.0f}% · {a} {aa*100:.0f}%")
            motivo = []
            absh, absa = r.get("adj_absent_home"), r.get("adj_absent_away")
            if isinstance(absh, str) and absh.strip():
                motivo.append(f"{h} sin {absh}")
            if isinstance(absa, str) and absa.strip():
                motivo.append(f"{a} sin {absa}")
            tag = "heurístico EN VIVO, NO validado, orientativo"
            lines.append(f"   ⚠️ {' · '.join(motivo)} — {tag}" if motivo else f"   ⚠️ {tag}")

        # "POR QUÉ": readable explanation, Spanish team names, from the SAME stored fields
        # (strength/xg/probs/adj) — pure rendering, no model recompute. Soft-fail.
        try:
            import worldcup_explain
            why = worldcup_explain.explain_l3(
                h, a, r.get("our_elo_home"), r.get("our_elo_away"), neutral=1,
                xg_home=xgh, xg_away=xga,
                p_home=lh, p_draw=ld, p_away=la,
                adj_basis=r.get("adj_basis"),
                adj_absent_home=r.get("adj_absent_home"), adj_absent_away=r.get("adj_absent_away"),
                adj_delta_home=r.get("adj_delta_home"), adj_delta_away=r.get("adj_delta_away"))
        except Exception:
            why = ""
        # TRANSPARENCIA: si la predicción mostrada lleva el ajuste de contexto, anótalo en el "por qué"
        # (solo cuando lo hay). Frase ya construida por build_worldcup_cards (context_note).
        if isinstance(ctx_note, str) and ctx_note.strip():
            why = (f"{why} · {ctx_note}" if why else ctx_note)
        if why:
            lines.append(why)

    # INFORMACIÓN (no es la predicción): contexto de clasificación del grupo (motor correcto,
    # desempates FIFA). Solo grupos última jornada; soft-fail -> no aparece.
    gi = r.get("group_info")
    if not ko_round and isinstance(gi, str) and gi.strip():
        lines.append(f"ℹ️ Contexto de grupo (información, no es la predicción): {gi}")

    if pd.notna(xgh):
        M = score_matrix(xgh, xga)
        gh = np.arange(KMAX + 1)[:, None]; ga = np.arange(KMAX + 1)[None, :]
        o25 = float(M[(gh + ga) >= 3].sum()); btts = float(M[(gh >= 1) & (ga >= 1)].sum())
        # safety net: OU/BTTS never shown at exactly 0%/100% (honest; harmless for L3 too)
        o25 = min(max(o25, 0.01), 0.99); btts = min(max(btts, 0.01), 0.99)
        lines.append(f"Goles esperados: {xgh:.1f}–{xga:.1f} (total {xgh + xga:.1f}) · "
                     f"Over 2.5: {o25 * 100:.0f}% · BTTS: {btts * 100:.0f}%")
        flat = sorted(((i, j, M[i, j]) for i in range(KMAX + 1) for j in range(KMAX + 1)),
                      key=lambda t: -t[2])[:3]
        lines.append("Marcadores top 3: " + " · ".join(f"{i}-{j} ({p * 100:.0f}%)" for i, j, p in flat))

    # per-team córners/tiros (gated; cards never shown). Confidence PER STAT (tiros media / córners
    # baja), shown once as a legend at the end — not a single global label that mixes the two.
    shown_here = []

    def side(nm, c, s):
        seg = []
        if "corners" in SHOW_STATS and pd.notna(c):
            seg.append(f"córners ~{c:.0f}")
            if "corners" not in shown_here:
                shown_here.append("corners")
        if "shots" in SHOW_STATS and pd.notna(s):
            seg.append(f"tiros ~{s:.0f}")
            if "shots" not in shown_here:
                shown_here.append("shots")
        return f"{nm}: " + ", ".join(seg) if seg else None
    sh = side(h, r.get("st_corners_home"), r.get("st_shots_home"))
    sa = side(a, r.get("st_corners_away"), r.get("st_shots_away"))
    if sh and sa:
        legend = _conf_legend(shown_here)
        tag = f"  ({legend})" if legend else ""
        lines.append(f"Por equipo — {sh} | {sa}{tag}")

    if show_lineups:
        LU = {"conf": "confirmado", "prob": "probable", "pend": "pendiente"}
        lhs, las = r.get("lineup_home"), r.get("lineup_away")
        if pd.notna(lhs) and str(lhs) in LU:
            lines.append(f"Alineaciones — {h}: {LU[str(lhs)]} · {a}: {LU.get(str(las), 'pendiente')}")

    # PLAYER PROPS (shadow · validados): compact, read from the SAME shadow props log
    # (already logged pre-KO -> lock-at-KO coherent; NOT recomputed). Soft: no props -> no block.
    lines += props_block(r.get("fixture_id"))
    return lines


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


def read_mx_vs_l3_line(path):
    """Compact one-liner of the mx-vs-L3 marker (line 1 of worldcup_mx_vs_l3_scorecard.txt), so the
    briefing shows the accumulated 'Motor máximo vs L3' at a glance. [] if absent/empty (soft-fail).
    Display-only: this file is produced by the read-only scorer; the briefing never recomputes it."""
    if not path:
        return []
    p = Path(path)
    if not p.exists():
        return []
    try:
        for ln in p.read_text(encoding="utf-8").splitlines():
            s = ln.rstrip()
            if s.strip():
                # skip the "aún sin partidos liquidados" placeholder (nothing to brag about yet)
                return [] if "aún sin partidos" in s else [s]
    except Exception:
        return []
    return []


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


def _ko_resolution_es(r, h, a):
    """Annotation for a knockout decided beyond 90' — from result_status + result_final ONLY.
    The 1X2 is still scored at 90' (this is just the visible note). For PEN the shootout winner
    is NOT a stored field, so we annotate it WITHOUT naming a winner (never invent match data).
    '' for a normal FT (or missing status)."""
    status = str(r.get("result_status") or "").upper()
    if status == "AET":
        try:
            fgh, fga = int(r["result_final_gh"]), int(r["result_final_ga"])
            who = h if fgh > fga else (a if fga > fgh else "")
            tail = f" · ganó {who} en la prórroga" if who else ""
            return f" ({fgh}-{fga} tras prórroga{tail})"
        except Exception:
            return " (tras prórroga)"
    if status == "PEN":
        return " (empate a 90' · decidido en penaltis)"
    return ""


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
        # 90' score + (if AET/PEN) a note. The L3 hit (l3_s) is judged on the 90' 1X2, unchanged.
        lines.append(f"{h} {score} {a}{_ko_resolution_es(r, h, a)} — L3{l3_s}")
        # [REAL] post-FT enrichment lines (xG/tiros/posesión/córners + 1er gol/tarjetas).
        # SOFT: absent store -> no extra lines, briefing identical to before this feature.
        if wc_enrich is not None and pd.notna(r.get("fixture_id")):
            try:
                for ln in wc_enrich.real_lines_for_fixture(int(r["fixture_id"]), score):
                    lines.append("  " + ln)
            except Exception:
                pass
    return lines


def render_paginated(df, date_from, within_hours, scorecard, show_yesterday,
                     log_path, show_lineups, per_page, max_lines):
    """Split the briefing into SEVERAL Telegram messages so nothing is truncated:
    msg 1 = header (track record + 'ayer'); msg 2.. = COMPLETE match blocks packed by a line
    budget (max_lines) — a match block is never cut mid-way; per_page caps matches/message.
    Writes one file per message + a manifest ('path|title' per line) the workflow loops
    over (dispatch_telegram_alert.py is called once per message — dispatcher untouched).
    Anti-spam: pre-KO with no matches -> empty manifest (send nothing); morning -> header only.
    Returns the number of messages written. ZERO odds; stats gated (cards omitted)."""
    # clean stale page files from a previous (possibly larger) run
    for f in OUT_DIR.glob("worldcup_msg_*.txt"):
        try:
            f.unlink()
        except Exception:
            pass

    sc_block = read_scorecard_block(scorecard)
    mx_block = read_mx_vs_l3_line(MXVSL3)          # 1 compact line (or none) — display-only, soft-fail
    yest_block = build_yesterday_block(log_path or LOG, datetime.now(timezone.utc)) \
        if show_yesterday else []
    META.write_text(str(len(df)), encoding="utf-8")          # anti-spam fixture count
    is_preko = within_hours is not None

    # ----- header message -----
    if is_preko:
        htitle = f"Mundial 2026 — pre-saque ({date_from})"
        hlead = f"🏆 MUNDIAL 2026 — PRE-SAQUE (próximas {within_hours:g}h · modelo propio, sin cuotas)"
    else:
        htitle = f"Mundial 2026 — briefing ({date_from})"
        hlead = f"🏆 MUNDIAL 2026 — briefing {date_from} (modelo propio, sin cuotas)"
    # day-summary digest line right under the banner (1 line, display-only, soft-fail)
    ds_line = day_summary_line(df)
    header = [hlead] + ([ds_line] if ds_line else []) + sc_block + mx_block + yest_block
    if len(df):
        header.append(f"📋 {len(df)} partido(s) abajo (en mensajes siguientes).")
    # honest per-stat confidence summary in the header (data-driven OOS lift), not a single label
    _hdr_conf = _conf_legend([s for s in ("shots", "corners") if s in SHOW_STATS])
    header.append(
        f"ℹ️ Stats por equipo (confianza por stat — {_hdr_conf}). Tarjetas omitidas (ruido)."
        if _hdr_conf else
        "ℹ️ Stats por equipo = orientativas (señal OOS débil). Tarjetas omitidas (ruido).")

    # anti-spam: pre-KO and nothing imminent -> send NOTHING
    if is_preko and len(df) == 0:
        MANIFEST.write_text("", encoding="utf-8")
        (OUT_DIR / "worldcup_full_cards.txt").write_text(
            "(pre-KO sin partidos en ventana → no se envía nada)\n", encoding="utf-8")
        print("paginate: pre-KO sin partidos -> 0 mensajes")
        return 0

    messages = [(htitle, header[:max_lines])]

    # ----- 'predicciones más firmes' digest as its OWN short message (so it never crowds out or
    # truncates the header/match pages). Display-only, soft-fail -> omitted entirely. -----
    firmest = firmest_predictions_block(df)
    if firmest:
        messages.append(("Mundial 2026 — predicciones más firmes", firmest[:max_lines]))

    # ----- match pages: pack COMPLETE match blocks per message by a LINE BUDGET (max_lines, the
    # dispatcher cut). A block is NEVER split: if adding the next block would overflow the budget it
    # goes to the NEXT message; a lone block that alone exceeds the budget still gets its OWN message
    # and is emitted WHOLE (never truncated — the last match keeps its props + nota). per_page is an
    # extra upper cap on matches/message. The budget already accounts for the blank separators. -----
    blocks = [match_block(r, show_lineups) for _, r in df.iterrows()]
    pages, cur, cur_len = [], [], 0
    for b in blocks:
        sep = 1 if cur else 0                                # blank separator before a non-first block
        too_long = bool(cur) and (cur_len + sep + len(b) > max_lines)
        too_many = bool(cur) and per_page and len(cur) >= per_page
        if too_long or too_many:
            pages.append(cur)
            cur, cur_len, sep = [], 0, 0
        cur.append(b)
        cur_len += sep + len(b)
    if cur:
        pages.append(cur)
    npages = len(pages)
    for idx, page in enumerate(pages, 1):
        body = []
        for b in page:
            if body:
                body.append("")                              # blank line between matches
            body.extend(b)
        title = f"Mundial 2026 — partidos ({idx}/{npages})" if npages > 1 else "Mundial 2026 — partidos"
        messages.append((title, body))                       # pre-fit to budget -> NO mid-block cut

    # ----- write files + manifest + combined preview (for the CI log) -----
    manifest_lines, combined = [], []
    for i, (title, body) in enumerate(messages, 1):
        fp = OUT_DIR / f"worldcup_msg_{i}.txt"
        fp.write_text("\n".join(body) + "\n", encoding="utf-8")
        manifest_lines.append(f"{fp}|{title}")
        combined.append(f"===== MENSAJE {i}: {title} =====")
        combined.extend(body)
        combined.append("")
    MANIFEST.write_text("\n".join(manifest_lines) + "\n", encoding="utf-8")
    (OUT_DIR / "worldcup_full_cards.txt").write_text("\n".join(combined), encoding="utf-8")
    for c in combined:
        print(c)
    return len(messages)


def main(date_from, date_to, limit, compact=False, scorecard=None, max_lines=24,
         show_lineups=False, within_hours=None, show_yesterday=False, log_path=None,
         paginate=False, per_page=3):
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

    # 🔴 STATS_LEVEL_CORRECTION (reversible): auto-learned LEVEL fix for the SHOWN córners/tiros only,
    # applied to the DISPLAY df IN MEMORY (the on-disk cards.csv and the learning-loop log stay RAW —
    # no leakage). Tarjetas / 1X2 / goles / props NEVER touched. Flag OFF -> Δ=0. Soft-fail: a missing
    # state / any error -> no correction, identical card.
    if stats_correction is not None:
        try:
            n_corr = stats_correction.apply_to_df(df)
            if n_corr:
                print(f"stats-level correction applied to shown córners/tiros ({n_corr} stat(s)).")
        except Exception:
            pass

    if paginate:
        nmsg = render_paginated(df, date_from, within_hours, scorecard, show_yesterday,
                                log_path, show_lineups, per_page, max_lines)
        print(f"\nPaginated: {nmsg} message(s) -> {MANIFEST}")
        return

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
        _cfoot = _conf_legend([s for s in ("shots", "corners") if s in SHOW_STATS])
        FOOTER = (f"L3 + {_shown} = modelo de datos propio (sin cuotas). "
                  + (f"Stats (confianza por stat — {_cfoot})." if _cfoot
                     else "Stats: orientativas (señal débil OOS)."))
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
            lh3, ld3, la3, xgh, xga, ctx_note = pred_1x2(r)   # ctx_* (ajustado) si existe, si no L3 puro
            ko = str(r["kickoff_utc"])[5:16].replace("T", " ")  # MM-DD HH:MM
            # knockout -> round chip (Octavos/…); group -> short group label
            grp = (round_label_es(r.get("round")) if is_knockout(r.get("round"))
                   else str(r.get("home_group") or "?").replace("Group ", "G"))
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
                seg.append(f"{'L3·ctx' if ctx_note else 'L3'} {lh3*100:.0f}/{ld3*100:.0f}/{la3*100:.0f}")
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
            if ctx_note:                       # transparencia compacta del ajuste de contexto
                out("   ↳ " + ctx_note)
            inj_note_c = r.get("inj_note")     # INJURIES_LIVE: etiqueta honesta (ya aplicada a seg)
            if pd.notna(r.get("inj_home")) and isinstance(inj_note_c, str) and inj_note_c.strip():
                out("   ℹ️ " + inj_note_c)
            gic = r.get("group_info")          # INFORMACIÓN: contexto de clasificación (solo grupos)
            if not is_knockout(r.get("round")) and isinstance(gic, str) and gic.strip():
                out(f"   ℹ️ Contexto: {gic}")
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
        grp = (round_label_es(r.get("round")) if is_knockout(r.get("round"))
               else str(r.get("home_group") or "").replace("Group ", "Gr."))
        lh3, ld3, la3, xgh, xga, ctx_note = pred_1x2(r)   # ctx_* (ajustado) si existe, si no L3 puro

        out("")
        out(f"🏆 {h} vs {a}")
        out(f"   {ko} · {grp}")
        # 1X2 (L3, o L3·ctx si lleva ajuste de contexto de grupo)
        if pd.notna(lh3):
            out(f"1X2  {'L3·ctx' if ctx_note else 'L3'} {lh3*100:.0f}/{ld3*100:.0f}/{la3*100:.0f}")
            out(f"DC   1X {(lh3+ld3)*100:.0f}% · 12 {(lh3+la3)*100:.0f}% · X2 {(ld3+la3)*100:.0f}%")
            if ctx_note:
                out(f"     ({ctx_note})")
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
            _vc = _conf_legend([s for s in ("shots", "corners") if s in SHOW_STATS])
            out("Stats " + " · ".join(st_parts)
                + (f"  (modelo datos · {_vc})" if _vc else "  (modelo datos, orientativo)"))

    out("")
    shown = [n for n, k in [("córners", "corners"), ("tarjetas", "cards"), ("tiros", "shots")]
             if k in SHOW_STATS]
    hidden = [n for n, k in [("córners", "corners"), ("tarjetas", "cards"), ("tiros", "shots")]
              if k not in SHOW_STATS]
    out(f"L3/Poisson + {('/'.join(shown)) or 'stats'} = modelo de datos propio, SIN cuotas.")
    _nc = _conf_legend([s for s in ("shots", "corners") if s in SHOW_STATS])
    note = (f"Stats: opponent-adjusted, confianza por stat — {_nc}."
            if _nc else "Stats: opponent-adjusted, orientativas (señal OOS débil).")
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
    ap.add_argument("--paginate", action="store_true",
                    help="multi-message Telegram output: header + match pages (manifest-driven)")
    ap.add_argument("--per-page", type=int, default=3,
                    help="matches per page message (paginate mode)")
    a = ap.parse_args()
    main(a.dfrom, a.dto, a.limit, a.compact, a.scorecard, a.max_lines,
         a.show_lineups, a.within_hours, a.show_yesterday, a.log_path,
         a.paginate, a.per_page)
