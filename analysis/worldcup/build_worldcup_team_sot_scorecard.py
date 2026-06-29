"""
WORLD CUP 2026 — TEAM SHOTS-ON-TARGET SCORECARD (Fase 4L). READ-ONLY · NO API · NO scraping · NO web ·
NO market/odds/betting · NO fabrication · NO secrets · NO external sources · NO weight changes. Pure
football. MEASURE ONLY — nothing in the model, predictions, Telegram or weights is touched.

GOAL: produce a per-team/fixture scorecard of TEAM shots on target (SOT) — predicted vs real — so the
'Team SOT' module of the Fase-4J global panel can move from NO_EVALUABLE to ACTIVO / INSUFFICIENT_SAMPLE.
No new data source is added: only predictions/actuals the World Cup product already logged are reused.

PREDICTED SOT (source_predicted = player_sot_sum):
  sum of the per-player expected SOT (lam_shot_on, the Poisson λ already logged per probable/XI player)
  over the team's logged players in worldcup_player_props_log.csv. This is the only per-team SOT
  prediction the product produces today; it is NOT recomputed here, only summed.

REAL SOT (actual), in priority order:
  1. /fixtures/statistics store (data/processed/worldcup/api_enrichment/<fixture_id>.json,
     'Shots on Goal' per team) -> source_actual = fixture_statistics. True team total; highest fidelity.
  2. sum of the per-player real SOT (act_shots_on, from the API player-statistics pulled at settle)
     over the same logged players -> source_actual = player_shots_on_sum. Like-for-like with the
     predicted sum (same player set); may slightly undercount the team total (subs not in the props XI).

ANTI-HINDSIGHT / ANTI-LEAKAGE: lam_shot_on is frozen pre-KO by the props logger; act_shots_on is filled
at settle. This scorecard never recomputes a prediction with the result — it only pairs what was logged.
Only settled rows with BOTH a predicted and a real value are counted as evaluable. Rows where the
/fixtures/statistics store has a real SOT but no XI props were logged are surfaced as actual-only (NOT
evaluable) for transparency, never paired retroactively.

HONESTY: the per-player SOT model is low/medium confidence; small samples (N<SMALL_N team-rows) are
flagged "orientativo". Nothing is declared "good/bad" — metrics are only accumulated.

OUTPUT (read-only; explicit git-add only):
  * worldcup_team_sot_scorecard.csv        (one row per team/fixture; the committed track record)
  * worldcup_team_sot_scorecard_summary.json (metrics; regenerable -> gitignored)
  * worldcup_team_sot_scorecard_report.txt   (human report, no betting language; regenerable -> gitignored)

Run:  python analysis/worldcup/build_worldcup_team_sot_scorecard.py
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent

PROPS_LOG = HERE / "worldcup_player_props_log.csv"
FIXTURE_EVENTS = HERE / "worldcup_fixture_events.csv"
PRED_LOG = HERE / "worldcup_predictions_log.csv"
ENRICHMENT_DIR = REPO / "data" / "processed" / "worldcup" / "api_enrichment"

OUT_CSV = HERE / "worldcup_team_sot_scorecard.csv"
OUT_JSON = HERE / "worldcup_team_sot_scorecard_summary.json"
OUT_TXT = HERE / "worldcup_team_sot_scorecard_report.txt"

SMALL_N = 30        # below this (team-rows) the metrics are flagged "orientativo"
MIN_XI = 8          # fewer logged players than this -> partial XI -> confidence downgraded

CSV_COLUMNS = ["fixture_id", "kickoff_utc", "team_id", "team_name", "opponent_id", "opponent_name",
               "side", "predicted_sot", "actual_sot", "error", "abs_error",
               "source_predicted", "source_actual", "data_quality", "confidence", "reason"]

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def now_iso():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _num(v):
    try:
        if v is None:
            return None
        f = float(v)
    except (TypeError, ValueError):
        return None
    return f if (f == f and f not in (float("inf"), float("-inf"))) else None


def _read_csv(path):
    p = Path(path)
    if not p.exists():
        return None
    try:
        df = pd.read_csv(p)
    except Exception:
        return None
    return df if len(df) else None


# ===================================================================== predicted: player SOT sum
def aggregate_player_sot(props_df):
    """Per (fixture, team): sum of lam_shot_on (predicted SOT) and act_shots_on (real SOT) over the
    team's logged players. Only settled rows. Returns {(fid, tid): {...}}. Pure aggregation — no model.
    """
    out = {}
    if props_df is None:
        return out
    df = props_df
    if "settled" in df.columns:
        df = df[df["settled"].fillna(0).astype(int) == 1]
    need = {"fixture_id", "team_id", "lam_shot_on"}
    if df is None or not need <= set(df.columns) or not len(df):
        return out
    for (fid, tid), g in df.groupby(["fixture_id", "team_id"]):
        lam = pd.to_numeric(g.get("lam_shot_on"), errors="coerce")
        n_lam = int(lam.notna().sum())
        pred = float(lam.sum(skipna=True)) if n_lam else None
        act = None
        if "act_shots_on" in g.columns:
            a = pd.to_numeric(g["act_shots_on"], errors="coerce")
            if int(a.notna().sum()):
                act = float(a.sum(skipna=True))
        team = next((str(x) for x in g.get("team", pd.Series()).tolist() if isinstance(x, str)), "")
        ko = next((str(x) for x in g.get("kickoff_utc", pd.Series()).tolist() if isinstance(x, str)), "")
        n_xi = int(pd.to_numeric(g.get("is_xi", pd.Series()), errors="coerce").fillna(0).sum())
        out[(int(fid), int(tid))] = {
            "team_name": team, "kickoff_utc": ko,
            "pred_sot": pred, "act_player_sum": act,
            "n_players": int(len(g)), "n_xi": n_xi,
        }
    return out


# ===================================================================== opponent / side lookups
def load_opponent_map(events_df):
    """{(fixture_id, team_id): (opponent_id, opponent_name)} from the fixture-events log (soft)."""
    out = {}
    if events_df is None:
        return out
    need = {"fixture_id", "team_id", "opponent_id", "opponent_name"}
    if not need <= set(events_df.columns):
        return out
    sub = events_df.drop_duplicates(subset=["fixture_id", "team_id"])
    for _, r in sub.iterrows():
        fid, tid = _num(r.get("fixture_id")), _num(r.get("team_id"))
        oid = _num(r.get("opponent_id"))
        if fid is None or tid is None:
            continue
        out[(int(fid), int(tid))] = (None if oid is None else int(oid),
                                     str(r.get("opponent_name") or "") or None)
    return out


def load_side_map(pred_df):
    """{fixture_id: (home_name, away_name)} from the predictions log (soft) -> used to label side."""
    out = {}
    if pred_df is None or not {"fixture_id", "home", "away"} <= set(pred_df.columns):
        return out
    for _, r in pred_df.drop_duplicates(subset=["fixture_id"]).iterrows():
        fid = _num(r.get("fixture_id"))
        if fid is None:
            continue
        out[int(fid)] = (str(r.get("home") or ""), str(r.get("away") or ""))
    return out


def _side_for(fid, team_name, side_map):
    pair = side_map.get(int(fid))
    if not pair or not team_name:
        return "desconocido"
    home, away = pair
    if team_name == home:
        return "home"
    if team_name == away:
        return "away"
    return "desconocido"


# ===================================================================== real: /fixtures/statistics store
def load_fixture_statistics_sot(enrichment_dir=ENRICHMENT_DIR):
    """{(fixture_id, team_id): {sot, team_name, opponent_id, opponent_name, side, kickoff_utc}} from the
    isolated World Cup /fixtures/statistics store ('Shots on Goal' per team). Soft: missing dir/keys ->
    empty. Never fabricates — only teams with a numeric 'Shots on Goal' are returned."""
    out = {}
    d = Path(enrichment_dir)
    if not d.exists():
        return out
    for jp in sorted(d.glob("*.json")):
        try:
            data = json.loads(jp.read_text(encoding="utf-8"))
        except Exception:
            continue
        fid = _num(data.get("fixture_id"))
        if fid is None:
            continue
        fid = int(fid)
        home_id, away_id = _num(data.get("home_id")), _num(data.get("away_id"))
        stats = (data.get("postft") or {}).get("statistics") or []
        # per-team SOT + id/name first, so we can resolve opponents within the same fixture
        per_team = []
        for t in stats:
            team = t.get("team") or {}
            tid = _num(team.get("id"))
            sot = None
            for s in (t.get("statistics") or []):
                if str(s.get("type")) == "Shots on Goal":
                    sot = _num(s.get("value"))
                    break
            if tid is not None:
                per_team.append((int(tid), str(team.get("name") or ""), sot))
        for tid, name, sot in per_team:
            if sot is None:
                continue
            opp = next(((oid, onm) for (oid, onm, _) in per_team if oid != tid), (None, None))
            side = "home" if (home_id is not None and tid == int(home_id)) else (
                   "away" if (away_id is not None and tid == int(away_id)) else "desconocido")
            out[(fid, tid)] = {"sot": float(sot), "team_name": name,
                               "opponent_id": opp[0], "opponent_name": opp[1] or None,
                               "side": side, "kickoff_utc": ""}
    return out


# ===================================================================== build rows
def build_rows(props_df, events_df, pred_df, fixture_stats):
    """One row per team/fixture. predicted_sot = Σ lam_shot_on (player_sot_sum). actual_sot prefers the
    /fixtures/statistics team total, else Σ act_shots_on (player_shots_on_sum). Rows that only have a
    real SOT (store) but no logged prediction are surfaced as actual-only (NOT evaluable)."""
    agg = aggregate_player_sot(props_df)
    opp_map = load_opponent_map(events_df)
    side_map = load_side_map(pred_df)
    fixture_stats = fixture_stats or {}

    keys = set(agg.keys()) | set(fixture_stats.keys())
    rows = []
    for (fid, tid) in sorted(keys):
        a = agg.get((fid, tid), {})
        fs = fixture_stats.get((fid, tid))
        team_name = a.get("team_name") or (fs or {}).get("team_name") or ""
        ko = a.get("kickoff_utc") or (fs or {}).get("kickoff_utc") or ""

        pred = a.get("pred_sot")
        n_players = a.get("n_players", 0)
        n_xi = a.get("n_xi", 0)

        # actual: priority 1 = fixture statistics store; else player SOT sum
        if fs is not None and fs.get("sot") is not None:
            actual, src_actual = float(fs["sot"]), "fixture_statistics"
        elif a.get("act_player_sum") is not None:
            actual, src_actual = float(a["act_player_sum"]), "player_shots_on_sum"
        else:
            actual, src_actual = None, "none"

        src_pred = "player_sot_sum" if pred is not None else "none"

        # opponent / side (soft; fixture-stats opponent as fallback)
        opp = opp_map.get((fid, tid))
        if opp is None and fs is not None:
            opp = (fs.get("opponent_id"), fs.get("opponent_name"))
        opp_id, opp_name = (opp or (None, None))
        side = _side_for(fid, team_name, side_map)
        if side == "desconocido" and fs is not None:
            side = fs.get("side", "desconocido")

        # status / data_quality / confidence / reason
        err = abs_err = None
        if pred is not None and actual is not None:
            err = round(pred - actual, 4)
            abs_err = round(abs(pred - actual), 4)
            if n_players < MIN_XI:
                data_quality, confidence = "evaluable_partial_xi", "baja"
            else:
                data_quality = "evaluable"
                confidence = "alta" if src_actual == "fixture_statistics" else "media"
            reason = (f"pred=Σλ_sot {n_players} jugadores (XI {n_xi}); "
                      f"real={'SOG /fixtures/statistics' if src_actual=='fixture_statistics' else 'Σ act_shots_on jugadores'}")
        elif pred is None and actual is not None:
            data_quality, confidence = "actual_only_no_prediction", "baja"
            reason = "SOT real disponible pero sin XI/props logueados -> no evaluable (no se empareja a posteriori)"
        elif pred is not None and actual is None:
            data_quality, confidence = "prediction_only_no_actual", "baja"
            reason = "predicción de SOT pero sin SOT real liquidado todavía -> no evaluable"
        else:
            data_quality, confidence, reason = "no_data", "baja", "sin predicción ni real"

        rows.append({
            "fixture_id": fid, "kickoff_utc": ko, "team_id": tid, "team_name": team_name,
            "opponent_id": ("" if opp_id is None else opp_id),
            "opponent_name": (opp_name or ""), "side": side,
            "predicted_sot": ("" if pred is None else round(pred, 3)),
            "actual_sot": ("" if actual is None else round(actual, 3)),
            "error": ("" if err is None else err), "abs_error": ("" if abs_err is None else abs_err),
            "source_predicted": src_pred, "source_actual": src_actual,
            "data_quality": data_quality, "confidence": confidence, "reason": reason,
        })
    return rows


# ===================================================================== metrics
def _safe_corr(x, y):
    if len(x) < 3:
        return None
    sx, sy = np.std(x), np.std(y)
    if sx < 1e-12 or sy < 1e-12:
        return None
    return float(np.corrcoef(x, y)[0, 1])


def compute_summary(rows):
    """Accumulated SOT metrics over evaluable rows (both predicted and real present). Pure read."""
    ev = [r for r in rows if r["predicted_sot"] != "" and r["actual_sot"] != ""]
    preds = np.array([float(r["predicted_sot"]) for r in ev], dtype=float)
    acts = np.array([float(r["actual_sot"]) for r in ev], dtype=float)
    n = len(ev)
    summary = {
        "generated_at_utc": now_iso(),
        "n_team_rows": n,
        "n_fixtures": len({r["fixture_id"] for r in ev}),
        "n_rows_total": len(rows),
        "n_actual_only": sum(1 for r in rows if r["data_quality"] == "actual_only_no_prediction"),
        "small_sample": n < SMALL_N,
        "min_sample_threshold": SMALL_N,
    }
    if n == 0:
        summary["reason"] = ("aún sin equipos-partido con SOT previsto y real; el scorecard se llena "
                             "cuando se liquidan partidos con props de jugador (lam_shot_on/act_shots_on).")
        return summary, ev

    err = preds - acts
    summary.update({
        "mae": round(float(np.mean(np.abs(err))), 4),
        "rmse": round(float(np.sqrt(np.mean(err ** 2))), 4),
        "bias": round(float(np.mean(err)), 4),
        "mean_predicted": round(float(np.mean(preds)), 4),
        "mean_actual": round(float(np.mean(acts)), 4),
        "overprediction_rows": int(np.sum(err > 0)),
        "underprediction_rows": int(np.sum(err < 0)),
        "exact_rows": int(np.sum(err == 0)),
        "correlation": (None if _safe_corr(preds, acts) is None
                        else round(_safe_corr(preds, acts), 4)),
    })
    # MAE by side
    by_side = {}
    for s in ("home", "away"):
        sub = [r for r in ev if r["side"] == s]
        if sub:
            e = np.array([float(r["predicted_sot"]) - float(r["actual_sot"]) for r in sub])
            by_side[s] = {"n": len(sub), "mae": round(float(np.mean(np.abs(e))), 4),
                          "bias": round(float(np.mean(e)), 4)}
    summary["mae_by_side"] = by_side
    # MAE by actual source (transparency: fixture_statistics vs player sum are not identical actuals)
    by_src = {}
    for src in sorted({r["source_actual"] for r in ev}):
        sub = [r for r in ev if r["source_actual"] == src]
        e = np.array([float(r["predicted_sot"]) - float(r["actual_sot"]) for r in sub])
        by_src[src] = {"n": len(sub), "mae": round(float(np.mean(np.abs(e))), 4),
                       "bias": round(float(np.mean(e)), 4)}
    summary["by_source_actual"] = by_src
    # MAE by team (only teams with >=2 rows)
    by_team = {}
    teams = {}
    for r in ev:
        teams.setdefault(r["team_name"] or str(r["team_id"]), []).append(r)
    for name, sub in teams.items():
        if len(sub) >= 2:
            e = np.array([float(r["predicted_sot"]) - float(r["actual_sot"]) for r in sub])
            by_team[name] = {"n": len(sub), "mae": round(float(np.mean(np.abs(e))), 4),
                             "bias": round(float(np.mean(e)), 4)}
    summary["mae_by_team"] = dict(sorted(by_team.items(), key=lambda kv: kv[1]["mae"]))
    summary["ranges_coverage"] = None   # no SOT range/interval is produced today -> not applicable
    summary["status"] = ("ACTIVO" if n >= SMALL_N else "INSUFFICIENT_SAMPLE")
    return summary, ev


# ===================================================================== report
def _bias_es(b):
    if abs(b) < 0.25:
        return "≈ neutral"
    return "infraestima" if b < 0 else "sobrestima"


def render_txt(rows, summary):
    L = []
    n = summary["n_team_rows"]
    if n == 0:
        L.append(f"⚽ SOT por equipo (predicho vs real): aún sin equipos-partido evaluables "
                 f"({now_iso()[:10]}).")
        L.append("")
        L.append(summary.get("reason", ""))
        L.append("")
        L.append(f"generated_at_utc: {summary['generated_at_utc']}")
        return "\n".join(L)

    flag = "  (muestra pequeña, orientativo)" if summary["small_sample"] else ""
    L.append(f"⚽ SOT por equipo vs real (N={n} equipos-partido, {summary['n_fixtures']} partidos): "
             f"MAE {summary['mae']:.2f} · sesgo {summary['bias']:+.2f} "
             f"({_bias_es(summary['bias'])}){flag}")
    L.append("")
    L.append("===== detalle SOT de equipo (predicho vs real) =====")
    L.append("predicted_sot = Σ λ_sot de jugadores (lam_shot_on, congelado pre-KO) · "
             "actual_sot = SOG /fixtures/statistics o Σ act_shots_on (player stats al liquidar) · sin mercado")
    L.append(f"  {'MAE':>6} {'RMSE':>6} {'sesgo':>7} {'μpred':>6} {'μreal':>6} {'corr':>6} "
             f"{'sobre':>6} {'infra':>6}")
    corr = "—" if summary["correlation"] is None else f"{summary['correlation']:.2f}"
    L.append(f"  {summary['mae']:>6.2f} {summary['rmse']:>6.2f} {summary['bias']:>+7.2f} "
             f"{summary['mean_predicted']:>6.2f} {summary['mean_actual']:>6.2f} {corr:>6} "
             f"{summary['overprediction_rows']:>6} {summary['underprediction_rows']:>6}")
    L.append("")
    if summary.get("mae_by_side"):
        L.append("  por localía:")
        for s, m in summary["mae_by_side"].items():
            L.append(f"    {s:6} n={m['n']:>3} MAE {m['mae']:.2f} sesgo {m['bias']:+.2f}")
    if summary.get("by_source_actual"):
        L.append("  por fuente del real (transparencia: SOG total de equipo vs suma de jugadores XI):")
        for s, m in summary["by_source_actual"].items():
            L.append(f"    {s:22} n={m['n']:>3} MAE {m['mae']:.2f} sesgo {m['bias']:+.2f}")
    if summary.get("mae_by_team"):
        L.append("  por equipo (n>=2, mejor MAE primero):")
        for name, m in list(summary["mae_by_team"].items())[:12]:
            L.append(f"    {name:18} n={m['n']:>2} MAE {m['mae']:.2f} sesgo {m['bias']:+.2f}")
    if summary["n_actual_only"]:
        L.append(f"  actual-only (SOG real en el store pero sin props logueados, NO evaluable): "
                 f"{summary['n_actual_only']} fila(s).")
    L.append("")
    L.append("HONESTIDAD: la predicción de SOT por equipo es la SUMA de λ por jugador (modelo de props, "
             "confianza media/baja); con muestra pequeña las métricas son orientativas. NO se declara "
             "nada 'bueno/malo'; solo se acumula. NO se tocan pesos, modelo, predicciones ni Telegram.")
    if summary["small_sample"]:
        L.append(f"  muestra pequeña (N={n} < {SMALL_N}): métricas orientativas, aún no concluyentes.")
    L.append("")
    L.append(f"generated_at_utc: {summary['generated_at_utc']}")
    return "\n".join(L)


# ===================================================================== I/O
def write_csv(rows, path=OUT_CSV):
    df = pd.DataFrame(rows, columns=CSV_COLUMNS)
    df.to_csv(path, index=False)
    return df


def build(props_log=PROPS_LOG, events_log=FIXTURE_EVENTS, pred_log=PRED_LOG,
          enrichment_dir=ENRICHMENT_DIR, write=True,
          csv_path=OUT_CSV, json_path=OUT_JSON, txt_path=OUT_TXT):
    props = _read_csv(props_log)
    events = _read_csv(events_log)
    pred = _read_csv(pred_log)
    fixture_stats = load_fixture_statistics_sot(enrichment_dir)

    rows = build_rows(props, events, pred, fixture_stats)
    summary, _ev = compute_summary(rows)

    if write:
        write_csv(rows, csv_path)
        Path(json_path).write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
        Path(txt_path).write_text(render_txt(rows, summary) + "\n", encoding="utf-8")
    return rows, summary


def main(props_log=PROPS_LOG, events_log=FIXTURE_EVENTS, pred_log=PRED_LOG, enrichment_dir=ENRICHMENT_DIR):
    rows, summary = build(props_log, events_log, pred_log, enrichment_dir)
    n = summary["n_team_rows"]
    if n:
        print(f"team-SOT scorecard: N={n} ({summary['n_fixtures']} fixtures) "
              f"MAE={summary['mae']} bias={summary['bias']} -> {OUT_CSV}")
    else:
        print(f"team-SOT scorecard: 0 evaluable team-rows yet -> {OUT_CSV}")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="World Cup team shots-on-target scorecard (read-only, Fase 4L).")
    ap.add_argument("--props", default=str(PROPS_LOG))
    ap.add_argument("--events", default=str(FIXTURE_EVENTS))
    ap.add_argument("--pred", default=str(PRED_LOG))
    ap.add_argument("--enrichment", default=str(ENRICHMENT_DIR))
    a = ap.parse_args()
    sys.exit(main(a.props, a.events, a.pred, a.enrichment))
