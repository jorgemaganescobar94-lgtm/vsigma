"""
WORLD CUP 2026 — CORRECCIÓN reversible y auto-aprendida de la prop de TARJETA de jugador.
ISOLATED, analysis/worldcup/. NO market/odds, NO betting endpoints, NO API. Espejo de
worldcup_stats_level_correction, pero MULTIPLICATIVA sobre p_card (la prop sale sesgada ALTA:
predice ~16% vs ~10% real, IC95 excluye 0 — ver player_card_bias_probe).

QUÉ HACE: estima desde los partidos LIQUIDADOS el ratio de tarjeta = tasa_real(act_card>=1) /
media_pred(p_card) y aplica una DEFLACIÓN multiplicativa ENCOGIDA por muestra al VALOR MOSTRADO de
p_card en los fixtures futuros:
    factor = 1 − shrink × (1 − ratio),   shrink = N/(N+25)   (N = partidos liquidados)
    p_card_mostrada = p_card × factor
Multiplicativo: el tramo BAJO apenas se mueve (en valor absoluto) y el ALTO se deflacta más. Se
re-estima sola cada día = auto-aprendizaje.

QUÉ NO TOCA: GOL y ASISTENCIA (salen limpios) NO se tocan. 1X2 / goles / stats de equipo tampoco.
READ-ONLY sobre el modelo: corrige SOLO el valor MOSTRADO (la p_card del log queda en CRUDO, así el
probe/scorecard siguen midiendo el modelo real -> sin leakage). Anti-hindsight: estima de partidos
ya liquidados (anteriores), aplica a fixtures futuros; nunca el propio partido.

FLAG: CARD_PROP_CORRECTION. True -> aplica. False -> reversa EXACTA (Δ=0), valores actuales.

SALIDA (read-only, git-add explícito): worldcup_card_prop_correction.csv (estado/auditoría:
n_matches, n_rows, mean_pred, real_rate, ratio, shrink, factor, k, capped).

Run:  python analysis/worldcup/worldcup_card_prop_correction.py
"""
from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
PROPS_LOG = HERE / "worldcup_player_props_log.csv"
STATE_CSV = HERE / "worldcup_card_prop_correction.csv"

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# ----- governance flag: True -> correction applied; False -> exact revert (Δ=0) -----
CARD_PROP_CORRECTION = True

K_SHRINK = 25.0                      # partial-pooling constant (consistent with stats correction)
FACTOR_FLOOR, FACTOR_CEIL = 0.5, 1.5  # sanity clamp on the multiplicative factor
STATE_COLUMNS = ["n_matches", "n_rows", "mean_pred", "real_rate", "ratio", "shrink",
                 "factor", "k", "capped"]


def now_iso():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _clip(v, lo, hi):
    return max(lo, min(hi, v))


# ----------------------------------------------------------------- estimate
def estimate(props_log=PROPS_LOG):
    """Estimate the shrunk multiplicative deflation factor for p_card from settled matches. Pure read.
    ratio = real_rate(act_card>=1) / mean_pred(p_card); factor = 1 − shrink(1−ratio), shrink=N/(N+K),
    N = settled matches. Returns dict (or None if no usable settled card rows)."""
    p = Path(props_log)
    if not p.exists():
        return None
    try:
        df = pd.read_csv(p)
    except Exception:
        return None
    need = {"settled", "p_card", "act_card", "fixture_id"}
    if df.empty or not need <= set(df.columns):
        return None
    s = df[df["settled"].fillna(0).astype(int) == 1]
    s = s.dropna(subset=["p_card", "act_card"])
    if not len(s):
        return None
    n_matches = int(s["fixture_id"].nunique())
    n_rows = int(len(s))
    pred = pd.to_numeric(s["p_card"], errors="coerce").to_numpy(float)
    real = (pd.to_numeric(s["act_card"], errors="coerce").fillna(0) >= 1).astype(int).to_numpy()
    mean_pred = float(np.nanmean(pred))
    real_rate = float(real.mean())
    if mean_pred <= 0:
        return None
    ratio = real_rate / mean_pred
    shrink = n_matches / (n_matches + K_SHRINK) if (n_matches + K_SHRINK) > 0 else 0.0
    raw_factor = 1.0 - shrink * (1.0 - ratio)
    factor = _clip(raw_factor, FACTOR_FLOOR, FACTOR_CEIL)
    return {
        "n_matches": n_matches, "n_rows": n_rows, "mean_pred": mean_pred, "real_rate": real_rate,
        "ratio": ratio, "shrink": shrink, "factor": factor,
        "capped": abs(raw_factor - factor) > 1e-9,
    }


def estimate_and_save(props_log=PROPS_LOG, state_path=STATE_CSV):
    est = estimate(props_log)
    if est is None:
        # write an explicit empty state so downstream readers degrade cleanly (no correction)
        pd.DataFrame(columns=STATE_COLUMNS).to_csv(state_path, index=False)
        return None
    row = {
        "n_matches": est["n_matches"], "n_rows": est["n_rows"],
        "mean_pred": round(est["mean_pred"], 5), "real_rate": round(est["real_rate"], 5),
        "ratio": round(est["ratio"], 5), "shrink": round(est["shrink"], 5),
        "factor": round(est["factor"], 5), "k": K_SHRINK, "capped": est["capped"],
    }
    pd.DataFrame([row], columns=STATE_COLUMNS).to_csv(state_path, index=False)
    return est


def load_factor(state_path=STATE_CSV):
    """The deflation factor from the saved state, or None (no correction). Respects the flag: returns
    None when OFF (exact revert) or the state is absent/empty/unreadable (soft-fail)."""
    if not CARD_PROP_CORRECTION:
        return None
    p = Path(state_path)
    if not p.exists():
        return None
    try:
        df = pd.read_csv(p)
    except Exception:
        return None
    if df.empty or "factor" not in df.columns:
        return None
    try:
        f = float(df["factor"].iloc[0])
    except Exception:
        return None
    return f if np.isfinite(f) else None


# ----------------------------------------------------------------- apply (display only)
def corrected_p_card(series, factor):
    """p_card × factor, clamped to [0,1]. NaN preserved. Vectorised over a Series/array."""
    p = pd.to_numeric(pd.Series(series), errors="coerce").to_numpy(float)
    out = np.clip(p * factor, 0.0, 1.0)
    out[np.isnan(p)] = np.nan
    return out


def apply_to_props_df(sub, state_path=STATE_CSV):
    """Return a COPY of a per-fixture props DataFrame with p_card DEFLATED for DISPLAY (gol/asistencia/
    tiros untouched). No-op copy (Δ=0) when the flag is OFF, no state, or p_card absent. The original
    df / the on-disk log are never mutated -> the model/log stay RAW (no leakage)."""
    if sub is None or len(sub) == 0 or "p_card" not in getattr(sub, "columns", []):
        return sub
    f = load_factor(state_path)
    if f is None or abs(f - 1.0) < 1e-12:
        return sub
    out = sub.copy()
    out["p_card"] = corrected_p_card(out["p_card"], f)
    return out


def main(props_log=PROPS_LOG, state_path=STATE_CSV):
    est = estimate_and_save(props_log, state_path)
    on = "ON" if CARD_PROP_CORRECTION else "OFF (revert, Δ=0)"
    if est is None:
        print(f"card-prop correction [{on}] -> {state_path}  (sin partidos liquidados con tarjeta -> sin corrección)")
        return None
    print(f"card-prop correction [{on}] -> {state_path}")
    print(f"  N={est['n_matches']} partidos ({est['n_rows']} filas) · media_pred={est['mean_pred']*100:.2f}% "
          f"real={est['real_rate']*100:.2f}% · ratio={est['ratio']:.3f} · shrink={est['shrink']:.3f} "
          f"-> factor={est['factor']:.4f}" + ("  (CAP)" if est["capped"] else ""))
    return est


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="World Cup player CARD prop correction (shown p_card).")
    ap.add_argument("--log", default=str(PROPS_LOG))
    ap.add_argument("--state", default=str(STATE_CSV))
    a = ap.parse_args()
    main(a.log, a.state)
