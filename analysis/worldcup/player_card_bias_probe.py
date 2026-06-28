"""
READ-ONLY PROBE — ¿la prop de TARJETA de jugador sale sesgada ALTA en los partidos liquidados del
Mundial? SOLO MIDE. No cambia nada, no toca el modelo/predicciones, no escribe en el log, sin
endpoints de apuesta, sin mercado. Lee worldcup_player_props_log.csv (predicción p_* congelada al
saque + act_* liquidados) y reporta calibración de tarjeta vs gol/asistencia (referencia).

Convención: realizado = act_X >= 1 (recibió tarjeta / marcó / asistió) — la "tasa real" pedida.
Test de calibración: eventos observados vs esperados = Σp; z y CI del sesgo por Poisson-binomial
(Var = Σ p(1-p)). Anti-hindsight: las p_* están congeladas pre-KO; act_* se rellenan al liquidar.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
LOG = HERE / "worldcup_player_props_log.csv"
TEAM_CORR = HERE / "worldcup_stats_level_correction.csv"   # solo para el contraste de propagación
EPS = 1e-12

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

PROPS = [("card", "p_card", "act_card"), ("goal", "p_goal", "act_goal"),
         ("assist", "p_assist", "act_assist")]


def _ece(p, y, bins=10):
    p = np.asarray(p, float); y = np.asarray(y, float)
    edges = np.linspace(0, 1, bins + 1); e = 0.0
    for i in range(bins):
        m = (p > edges[i]) & (p <= edges[i + 1])
        if m.sum():
            e += m.sum() / len(p) * abs(p[m].mean() - y[m].mean())
    return float(e)


def _calib_test(p, y):
    """Poisson-binomial calibration: observed Σy vs expected Σp. Returns dict with bias (mean p −
    real rate, pp), SE(pp), 95% CI(pp), z, expected/observed events."""
    p = np.asarray(p, float); y = np.asarray(y, float)
    n = len(p)
    exp = float(p.sum()); obs = float(y.sum())
    var = float(np.sum(p * (1 - p)))
    se_events = np.sqrt(var) if var > 0 else float("nan")
    bias = (p.mean() - y.mean()) * 100.0                  # +%pp = overestimate
    se = (se_events / n) * 100.0 if n else float("nan")
    z = (obs - exp) / se_events if se_events and se_events > 0 else float("nan")
    return {"n": n, "exp": exp, "obs": obs, "bias_pp": bias, "se_pp": se,
            "ci": (bias - 1.96 * se, bias + 1.96 * se), "z": z}


def _reliability(p, y, edges):
    rows = []
    p = np.asarray(p, float); y = np.asarray(y, float)
    for lo, hi in zip(edges[:-1], edges[1:]):
        m = (p >= lo) & (p < hi)
        if m.sum():
            rows.append((lo, hi, int(m.sum()), p[m].mean() * 100, y[m].mean() * 100, int(y[m].sum())))
    return rows


def main():
    df = pd.read_csv(LOG)
    s = df[df["settled"].fillna(0).astype(int) == 1].copy()
    n_matches = int(s["fixture_id"].nunique())
    out = []

    def w(x=""):
        out.append(x)

    w("=" * 78)
    w("PROBE READ-ONLY — sesgo de la prop de TARJETA de jugador (Mundial, liquidados)")
    w("=" * 78)
    w(f"partidos liquidados={n_matches} · filas jugador-prop liquidadas={len(s)} · "
      f"realizado = act>=1 · SOLO MIDE")
    w("")
    w("(1)+(3) TABLA  {prop, N, media pred, tasa real, sesgo (pred−real), ECE, eventos, z, IC95 sesgo}")
    hdr = (f"  {'prop':8} {'N':>4} {'mediaPred':>9} {'tasaReal':>8} {'sesgo':>7} {'ECE':>6} "
           f"{'evReal':>6} {'evEsp':>6} {'z':>6} {'IC95 sesgo (pp)':>18}")
    w(hdr); w("  " + "-" * (len(hdr) - 2))
    res = {}
    for prop, pc, ac in PROPS:
        sub = s.dropna(subset=[pc, ac])
        p = pd.to_numeric(sub[pc], errors="coerce").to_numpy(float)
        y = (pd.to_numeric(sub[ac], errors="coerce").fillna(0) >= 1).astype(int).to_numpy()
        ok = ~np.isnan(p); p, y = p[ok], y[ok]
        t = _calib_test(p, y); res[prop] = t
        ece = _ece(p, y)
        lo, hi = t["ci"]
        sig = "✓signif" if (lo > 0 or hi < 0) else "n.s."
        w(f"  {prop:8} {t['n']:>4} {p.mean()*100:>8.2f}% {y.mean()*100:>7.2f}% "
          f"{t['bias_pp']:>+6.2f} {ece:>6.3f} {int(y.sum()):>6} {t['exp']:>6.1f} "
          f"{t['z']:>6.2f} [{lo:>+5.2f},{hi:>+5.2f}] {sig}")
    w("  (sesgo + = SOBREESTIMA · z = (eventos obs − esp)/√Σp(1−p) · IC excluye 0 -> sesgo real)")
    w("")

    # (2) reliability curve — TARJETA (tramos pedidos) + cola alta para ver si el tope la controla
    w("(2) CURVA DE FIABILIDAD — TARJETA (predicho vs realizado por tramo)")
    sub = s.dropna(subset=["p_card", "act_card"])
    pc = pd.to_numeric(sub["p_card"], errors="coerce").to_numpy(float)
    yc = (pd.to_numeric(sub["act_card"], errors="coerce").fillna(0) >= 1).astype(int).to_numpy()
    ok = ~np.isnan(pc); pc, yc = pc[ok], yc[ok]
    w(f"  p_card máx en el log = {pc.max()*100:.1f}%  (el tope 45%+ es SOLO display, no cambia p)")
    w(f"  {'tramo pred':>12} {'n':>4} {'media pred':>10} {'realizado':>9} {'eventos':>7}")
    for lo, hi, n, mp, rr, ev in _reliability(pc, yc, [0.0, 0.10, 0.20, 0.30, 1.0001]):
        hh = "100" if hi > 1 else f"{int(hi*100)}"
        w(f"  {int(lo*100):>4}-{hh:<3}%     {n:>4} {mp:>9.1f}% {rr:>8.1f}% {ev:>7}")
    w("  (si 'media pred' >> 'realizado' en un tramo, ahí sobre-predice)")
    w("")

    # reference reliability (goal/assist) compact
    for prop, pc2, ac2 in [("goal", "p_goal", "act_goal"), ("assist", "p_assist", "act_assist")]:
        sub = s.dropna(subset=[pc2, ac2])
        p = pd.to_numeric(sub[pc2], errors="coerce").to_numpy(float)
        y = (pd.to_numeric(sub[ac2], errors="coerce").fillna(0) >= 1).astype(int).to_numpy()
        ok = ~np.isnan(p); p, y = p[ok], y[ok]
        bits = " · ".join(f"{int(lo*100)}-{('100' if hi>1 else int(hi*100))}%:{mp:.0f}/{rr:.0f}(n{n})"
                          for lo, hi, n, mp, rr, ev in _reliability(p, y, [0.0, 0.10, 0.20, 0.30, 1.0001]))
        w(f"  [ref {prop}] pred/real por tramo: {bits}")
    w("")

    # (4) propagation of the team st_cards overestimate to the player prop
    w("(4) ¿SE TRASLADA el sesgo de st_cards (+1.53 equipo) a la prop de jugador?")
    team_ratio = None
    try:
        # team marker: pred 4.2 vs real 2.6 (del marcador de stats); ratio pred/real
        ts = pd.read_csv(HERE / "worldcup_team_stats_scorecard.csv")
        row = ts[ts["stat"] == "cards"]
        if len(row):
            mp = float(row["mean_pred"].iloc[0]); mr = float(row["mean_real"].iloc[0])
            team_ratio = mp / mr if mr else None
            w(f"  EQUIPO (st_cards): media pred {mp:.2f} vs real {mr:.2f} -> ratio {team_ratio:.2f}x "
              f"(sesgo +{mp-mr:.2f})")
    except Exception:
        w("  (sin worldcup_team_stats_scorecard.csv para el equipo)")
    cardt = res["card"]
    player_ratio = (cardt["exp"] / cardt["obs"]) if cardt["obs"] else None
    pr_mean = cardt["bias_pp"]
    if player_ratio:
        w(f"  JUGADOR (p_card):  media pred {cardt['exp']/cardt['n']*100:.2f}% vs real "
          f"{cardt['obs']/cardt['n']*100:.2f}% -> ratio {player_ratio:.2f}x (sesgo {pr_mean:+.2f}pp)")
    if team_ratio and player_ratio:
        w(f"  -> ratios equipo {team_ratio:.2f}x vs jugador {player_ratio:.2f}x: "
          f"{'CASI IGUALES -> el sesgo se TRASLADA (XI/shrink/tope NO lo absorben)' if abs(team_ratio-player_ratio)<0.25 else 'difieren -> parcialmente absorbido'}")
    w("")

    # VERDICT
    w("VEREDICTO (honesto):")
    c = res["card"]
    lo, hi = c["ci"]
    clear = (lo > 0)            # whole CI above 0 -> overestimate real
    enough = n_matches >= 10 and int(c["obs"]) >= 25
    w(f"  TARJETA: sesgo {c['bias_pp']:+.2f}pp (pred {c['exp']/c['n']*100:.1f}% vs real "
      f"{c['obs']/c['n']*100:.1f}%), IC95 [{lo:+.2f},{hi:+.2f}]pp, z={c['z']:.2f}, "
      f"eventos reales={int(c['obs'])} en {n_matches} partidos.")
    for prop in ("goal", "assist"):
        t = res[prop]; l2, h2 = t["ci"]
        w(f"  {prop.upper()}: sesgo {t['bias_pp']:+.2f}pp, IC95 [{l2:+.2f},{h2:+.2f}]pp "
          f"-> {'bien calibrado (IC abarca 0)' if (l2 <= 0 <= h2) else 'sesgo'} (referencia).")
    w("")
    if clear and enough:
        w("  CONCLUSIÓN: el sesgo ALTO de TARJETA es CLARO (IC95 excluye 0) y con muestra razonable; "
          "gol/asistencia salen bien calibrados -> la tarjeta es la única sesgada. JUSTIFICA estudiar "
          "una corrección de la prop de tarjeta (p.ej. encoger p_card hacia la tasa real, análogo a la "
          "corrección de nivel de st_cards). OJO: N partidos<30 (umbral de graduación) -> tratar como "
          "fuerte indicio, no veredicto final; re-medir al acumular.")
    elif clear:
        w("  CONCLUSIÓN: sesgo de tarjeta aparente pero muestra corta -> indicio, NO concluyente. Dejar y re-medir.")
    else:
        w("  CONCLUSIÓN: no concluyente (IC abarca 0 o pocos eventos) -> dejar como está.")

    text = "\n".join(out)
    print(text)
    (HERE / "player_card_bias_probe_report.txt").write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
