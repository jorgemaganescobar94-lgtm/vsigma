"""
Offline tests for the consolidated track-record panel generator
(build_worldcup_trackrecord_panel). NO network, NO API, NO model import for prediction.

Covers: parses 1X2 / goals / props / context / calibration from sample scorecards · soft-fail to
"sin datos aún" when a source is missing · honest small-sample notes · does NOT recompute (only reads).

Run:  python analysis/worldcup/test_trackrecord_panel.py
"""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_worldcup_trackrecord_panel as P  # noqa: E402

SCORECARD = """📊 Track record (31 resueltos · 2026-06-26)
===== detalle =====
resueltos=31 | 1X2 a 90'
  SEMÁNTICA MIXTA: 25 a 'primera predicción' · 6 a 'última pre-saque'.
predictor    n  logloss   brier   acc%    ECE Skill_base%
---------------------------------------------------------
base-rate   31   1.0341  0.6243   48.4  0.000         0.0
L3          31   0.8284  0.4782   67.7  0.153       +23.4
v2          31   0.8728  0.5065   67.7  0.133       +18.9

--- (1) APUESTAS DERIVADAS — L3 (Poisson xG) vs base-rate (Over2.5, BTTS) ---
  Over 2.5  (real Over=61%):
    L3 (Poisson xG)    n= 31  acc   39%  Brier 0.251  logloss 0.696
    base-rate          n= 31  acc   61%  Brier 0.237  logloss 0.667
  BTTS      (real Yes=42%):
    L3 (Poisson xG)    n= 31  acc   74%  Brier 0.217  logloss 0.631
    base-rate          n= 31  acc   58%  Brier 0.243  logloss 0.680

--- (1b) A/B TOTAL DE GOLES — aún sin filas con xG constante logueado ---
"""

PROPS = """# GOL y ASISTENCIA -> GRADUADOS: baten baseline.
# TARJETA -> GRADUADA tras el RE-TEST.
# TIROS-A-PUERTA -> RANKING ONLY (no gradúa).
partidos liquidados=6 | filas jugador-prop=132 | umbral graduación N>=30
MUESTRA INSUFICIENTE para graduar (N<30).
  prop          n  base%  logloss   brier    ECE  ll_base br_base  mejora?
  goal        132     6%   0.2505  0.0656  0.068   0.2286  0.0569       no
  card        132     5%   0.2626  0.0669  0.114   0.1849  0.0434       no
  shot_on     132    17%   0.4553  0.1541  0.136   0.4506  0.1389       no
  assist      132     7%   0.2636  0.0683  0.044   0.2489  0.0635       no
"""

CONTEXT = """partidos liquidados (total)=0 | con escenario NO trivial=0 | triviales=0 | umbral graduación N>=20
MUESTRA INSUFICIENTE para graduar (N<20). Sigue en SOMBRA.
"""

CALIB = """ESTADO: OK
N=31 | ECE_observado=0.153 | nulo p95(N=31)=0.246 -> ECE dentro del ruido
logloss_L3=0.8284 vs baseline=1.0341 -> bate la tasa base | brier_L3=0.4782 (base 0.6243)
"""


def _write(tmp, name, content):
    p = tmp / name
    p.write_text(content, encoding="utf-8")
    return p


def test_full_panel_parses_all_sections():
    tmp = Path(tempfile.mkdtemp())
    md = P.build_panel_text(
        scorecard=_write(tmp, "sc.txt", SCORECARD), props=_write(tmp, "pr.txt", PROPS),
        context=_write(tmp, "cx.txt", CONTEXT), calib=_write(tmp, "ca.txt", CALIB),
        now="2026-06-26T21:00:00+00:00")
    # header + provenance
    assert "Panel de Track-Record" in md and "no recalcula predicciones" in md.lower()
    assert "2026-06-26T21:00:00+00:00" in md
    # 1X2: the L3 row and skill
    assert "| L3 (oficial) | 31 | 0.8284 | 0.4782 | 67.7 | 0.153 | +23.4% |" in md
    assert "semántica mixta" in md.lower()
    # goals: BTTS L3 row must carry BTTS numbers (not Over's) -> slicing correct
    assert "| BTTS (real 42%) | L3 (Poisson) | 31 | 74 | 0.217 | 0.631 |" in md
    assert "| Over 2.5 (real 61%) | L3 (Poisson) | 31 | 39 | 0.251 | 0.696 |" in md
    # A/B total -> insufficient
    assert "sin filas con total constante" in md
    # props: backtest statuses parsed honestly
    assert "validado (backtest)" in md and "ranking solo (no %)" in md
    assert "tope en cola" in md
    # context + calibration
    assert "sigue en SOMBRA" in md
    assert "🟢 OK" in md and "dentro del ruido" in md and "bate la tasa base" in md


def test_missing_sources_softfail_to_sin_datos():
    tmp = Path(tempfile.mkdtemp())
    md = P.build_panel_text(scorecard=tmp / "nope1.txt", props=tmp / "nope2.txt",
                            context=tmp / "nope3.txt", calib=tmp / "nope4.txt",
                            now="2026-06-26T21:00:00+00:00")
    # every section header still present, each with the "sin datos aún" placeholder; no crash
    for header in ("1X2 — modelo L3", "Goles — Over 2.5", "Props de jugador",
                   "A/B de contexto", "Monitor de calibración"):
        assert header in md
    assert md.count("sin datos aún") >= 5


def test_partial_sources_one_missing():
    tmp = Path(tempfile.mkdtemp())
    md = P.build_panel_text(scorecard=_write(tmp, "sc.txt", SCORECARD),
                            props=tmp / "missing.txt",   # props missing
                            context=_write(tmp, "cx.txt", CONTEXT), calib=_write(tmp, "ca.txt", CALIB),
                            now="x")
    assert "| L3 (oficial) | 31 |" in md          # 1X2 still parsed
    assert "Props de jugador" in md and "sin datos aún" in md   # props softfailed


def test_small_sample_notes_present():
    tmp = Path(tempfile.mkdtemp())
    md = P.build_panel_text(scorecard=_write(tmp, "sc.txt", SCORECARD), props=_write(tmp, "pr.txt", PROPS),
                            context=_write(tmp, "cx.txt", CONTEXT), calib=_write(tmp, "ca.txt", CALIB), now="x")
    assert "muestra pequeña (N=6 < umbral 30)" in md       # props
    assert "muestra pequeña (N=0 < umbral 20)" in md       # context


def test_no_model_recompute_only_reads_files():
    # the generator must not import the predictor/model to make a prediction. A trivial proxy:
    # it produces output from ONLY the text files, with no numeric prediction beyond what's parsed.
    tmp = Path(tempfile.mkdtemp())
    md = P.build_panel_text(scorecard=_write(tmp, "sc.txt", SCORECARD), props=tmp / "x",
                            context=tmp / "x", calib=tmp / "x", now="x")
    assert isinstance(md, str) and md.endswith("\n")
    # value present in the panel must come verbatim from the input file (no recomputation)
    assert "0.8284" in SCORECARD and "0.8284" in md


if __name__ == "__main__":
    import traceback
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    failed = 0
    for fn in fns:
        try:
            fn(); print(f"  ok  {fn.__name__}")
        except Exception:
            failed += 1; print(f" FAIL {fn.__name__}"); traceback.print_exc()
    print(f"\n{len(fns) - failed}/{len(fns)} passed")
    sys.exit(1 if failed else 0)
