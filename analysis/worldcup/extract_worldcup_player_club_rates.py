"""
extract_worldcup_player_club_rates.py — READ-ONLY · NO API · NO producción · NO commit.

player_club (store full_ingest, temporada de CLUB 2025) -> tasas /90 de CLUB por jugador, ponderadas
por minutos, SOLO competiciones de club. Escribe un CSV de tasas; NO toca worldcup_player_props.py.

ANTI-LEAKAGE / ANTI-SELECCIÓN (doble filtro explícito, por bloque de statistics):
  - EXCLUYE cualquier bloque cuyo team.id sea una SELECCIÓN (∈ ids de international_results.csv, 606
    equipos nacionales) -> descarta amistosos/clasificación/Nations League/WC de selección.
  - EXCLUYE cualquier bloque con league.id == 1 (Mundial).
  - La temporada de club 2025 (2025-26) cerró ANTES del Mundial (jun-2026) -> snapshot inmutable
    pre-torneo -> leak-free para predecir CUALQUIER partido WC.
Champions/Europa (país "World", pero CLUB) se CONSERVAN: el filtro es por team.id de selección, no por país.

Salida: worldcup_player_club_rates.csv (una fila por jugador con >=1 minuto de club).
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
STORE = ROOT / "data" / "processed" / "worldcup" / "full_ingest" / "player_club"
INT_RESULTS = HERE / "international_results.csv"
OUT = HERE / "worldcup_player_club_rates.csv"
WC_LEAGUE = 1


def national_team_ids() -> set[int]:
    ids = set()
    with open(INT_RESULTS, encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            for k in ("home_id", "away_id"):
                try:
                    ids.add(int(float(r[k])))
                except (TypeError, ValueError, KeyError):
                    pass
    return ids


def _num(v) -> float:
    try:
        return float(v)
    except (TypeError, ValueError):
        return 0.0


def main():
    nat = national_team_ids()
    files = sorted(STORE.glob("*.json")) if STORE.exists() else []
    rows = []
    tot_blocks = exc_nat = exc_wc = kept = 0
    players_with_club = 0

    for f in files:
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            continue
        resp = data.get("response") or []
        if not resp:
            continue
        item = resp[0]
        player = item.get("player") or {}
        pid = player.get("id")
        if pid is None:
            continue
        club = {"min": 0.0, "g": 0.0, "a": 0.0, "sh": 0.0, "son": 0.0, "cards": 0.0, "comps": 0}
        natl = {"min": 0.0, "g": 0.0, "a": 0.0, "sh": 0.0, "son": 0.0, "cards": 0.0, "comps": 0}
        for st in (item.get("statistics") or []):
            tot_blocks += 1
            tid = (st.get("team") or {}).get("id")
            lid = (st.get("league") or {}).get("id")
            g = st.get("games") or {}; gl = st.get("goals") or {}
            sh = st.get("shots") or {}; cd = st.get("cards") or {}
            mins = _num(g.get("minutes"))
            is_wc = lid is not None and int(lid) == WC_LEAGUE
            is_nat = tid is not None and int(tid) in nat
            # --- FILTRO anti-selección / anti-WC (para las tasas de CLUB) ---
            if is_wc:
                exc_wc += 1
                bucket = None            # WC = leak -> nunca se usa ni como club ni como nat
            elif is_nat:
                exc_nat += 1
                bucket = natl            # bloque de SELECCIÓN (season 2025) -> baseline nacional leak-free
            else:
                kept += 1
                bucket = club            # CLUB real
            if bucket is None or mins <= 0:
                continue
            bucket["min"] += mins
            bucket["g"] += _num(gl.get("total"))
            bucket["a"] += _num(gl.get("assists"))
            bucket["sh"] += _num(sh.get("total"))
            bucket["son"] += _num(sh.get("on"))
            bucket["cards"] += _num(cd.get("yellow")) + _num(cd.get("red"))
            bucket["comps"] += 1
        if club["min"] <= 0 and natl["min"] <= 0:
            continue
        if club["min"] > 0:
            players_with_club += 1

        def _per90(b, k):
            return round(b[k] / b["min"] * 90.0, 5) if b["min"] > 0 else 0.0

        rows.append({
            "player_id": int(pid),
            "name": player.get("name", ""),
            "club_minutes": round(club["min"], 1),
            "n_club_comps": club["comps"],
            "g90_club": _per90(club, "g"), "a90_club": _per90(club, "a"),
            "sh90_club": _per90(club, "sh"), "son90_club": _per90(club, "son"),
            "c90_club": _per90(club, "cards"),
            "nat_minutes": round(natl["min"], 1),
            "g90_nat": _per90(natl, "g"), "a90_nat": _per90(natl, "a"),
            "sh90_nat": _per90(natl, "sh"), "son90_nat": _per90(natl, "son"),
            "c90_nat": _per90(natl, "cards"),
        })

    rows.sort(key=lambda r: -r["g90_club"])
    with open(OUT, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()) if rows else
                           ["player_id", "name", "club_minutes", "n_club_comps",
                            "g90_club", "a90_club", "sh90_club", "son90_club", "c90_club"])
        w.writeheader()
        w.writerows(rows)

    print("=" * 80)
    print("EXTRACTOR player_club -> tasas /90 de CLUB (read-only, sin API)")
    print("=" * 80)
    print(f"ficheros player_club: {len(files)}")
    print(f"bloques statistics totales: {tot_blocks}")
    print(f"  EXCLUIDOS por selección (team.id ∈ {len(nat)} nacionales): {exc_nat}")
    print(f"  EXCLUIDOS por Mundial (league.id==1):                    {exc_wc}")
    print(f"  CONSERVADOS (club real):                                 {kept}")
    print(f"jugadores con datos de club (>=1 min): {players_with_club}")
    print(f"\nCSV -> {OUT}  ({len(rows)} filas)")
    if rows:
        print("\nTop-5 g90_club (sanity):")
        for r in rows[:5]:
            print(f"  {r['name'][:22]:22} g90={r['g90_club']:.3f}  min={r['club_minutes']:.0f}  comps={r['n_club_comps']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
