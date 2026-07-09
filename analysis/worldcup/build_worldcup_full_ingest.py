"""
build_worldcup_full_ingest.py — INGESTA COMPREHENSIVA no-apuesta de API-Football (Fase A).

Captura TODO el dato NO-apuesta que la API ofrece para el scope del Mundial 2026, y (nivel 2)
el dato de CLUB de los jugadores implicados (alimenta también el data-core de clubes de agosto).

REGLA ABSOLUTA — CERO APUESTA:
    /odds y /predictions están PROHIBIDOS y BLOQUEADOS a nivel de request (_guard). Cualquier
    intento de llamarlos lanza excepción ANTES de tocar la red. Además, TODA ruta usada debe estar
    en ALLOWED (whitelist explícita). No hay forma de que este módulo emita una llamada de apuesta.

SEGURIDAD OPERATIVA:
    - Store-guarded: un id ya capturado hace CERO llamadas (idempotente, re-ejecutable).
    - Cacheado "para siempre" (TTL enorme) para el dato inmutable (partido acabado, perfil, squad).
    - Soft-fail: un error en una llamada NUNCA aborta la ingesta; se registra en el trace.
    - Contador de llamadas + tope duro (--max-calls) como red de seguridad anti-runaway.
    - DEFAULT = ESTIMATE (0 API). La captura real exige --execute. Con OK de Jorge se lanza.

NIVELES:
    1  WC 2026: torneo (standings, topscorers/assists/cards, teams, venues, leagues/seasons),
       equipos (teams/statistics, squads, injuries, coachs, sidelined), fixtures (statistics,
       events, players, lineups, headtohead), jugadores (perfil + stats WC).
    2  CLUB de esos jugadores: su temporada de club (/players season de club) + teams/statistics
       de sus clubes. Cobertura rica de liga que enriquece el modelo y el data-core de agosto.

Uso:
    python build_worldcup_full_ingest.py --estimate            # (default) plan de llamadas, 0 API
    python build_worldcup_full_ingest.py --level 1 --execute   # captura real nivel 1
    python build_worldcup_full_ingest.py --level all --execute --max-calls 8000
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

WC_LEAGUE = 1
WC_SEASON = 2026
CLUB_SEASON = 2025  # temporada de club para el nivel 2 (cobertura rica de liga)

STORE = ROOT / "data" / "processed" / "worldcup" / "full_ingest"
INT_RESULTS = HERE / "international_results.csv"
LOG = HERE / "worldcup_predictions_log.csv"

# TTLs (horas). El dato inmutable se cachea "para siempre"; lo semi-vivo, corto.
TTL_FOREVER = 24 * 3650      # partido acabado, perfil, squad histórico, trofeos
TTL_SLOW = 24 * 7            # standings, teams/statistics, topscorers (cambian lento en torneo)
TTL_LIVE = 6                 # /fixtures index, injuries (semi-vivo)

# ----------------------------------------------------------------------- CERO-APUESTA (guard)
FORBIDDEN = ("/odds", "/predictions")   # NUNCA. Bloqueo duro.
ALLOWED = {
    # torneo / catálogo
    "/leagues", "/leagues/seasons", "/standings", "/venues", "/teams", "/teams/statistics",
    "/players", "/players/squads", "/players/topscorers", "/players/topassists",
    "/players/topyellowcards", "/players/topredcards", "/players/profiles",
    # equipo / staff
    "/coachs", "/transfers", "/trophies", "/sidelined", "/injuries",
    # partido
    "/fixtures", "/fixtures/statistics", "/fixtures/events", "/fixtures/lineups",
    "/fixtures/players", "/fixtures/headtohead",
    # meta
    "/status",
}


def _guard(path: str) -> None:
    """Bloqueo duro anti-apuesta + whitelist. Lanza ANTES de tocar la red."""
    p = path.split("?")[0].rstrip("/")
    for bad in FORBIDDEN:
        if p == bad or p.startswith(bad + "/") or bad in path.lower():
            raise RuntimeError(f"BLOQUEADO (apuesta): {path} — /odds y /predictions están prohibidos.")
    if p not in ALLOWED:
        raise RuntimeError(f"BLOQUEADO (no whitelist): {path} — ruta no permitida en la ingesta no-apuesta.")


# ----------------------------------------------------------------------- infra
class Counter:
    def __init__(self, max_calls: int):
        self.n = 0
        self.max = max_calls
        self.trace = []

    def hit(self, sig: str):
        self.n += 1
        self.trace.append(sig)
        if self.n > self.max:
            raise RuntimeError(f"TOPE de llamadas alcanzado (--max-calls={self.max}). Parada dura.")


def _client():
    from api_football_client import APIFootballClient
    return APIFootballClient()


def _get(client, path, params, ttl, counter):
    """Una llamada guarded, cacheada, soft-fail. Devuelve el 'response' o None. Cuenta la llamada."""
    _guard(path)
    counter.hit(f"{path} {params}")
    try:
        resp = client.request(path, params, ttl_hours=ttl)
        return resp.get("response", []) if isinstance(resp, dict) else None
    except Exception as exc:  # noqa: BLE001 — soft-fail, nunca aborta
        counter.trace[-1] += f"  [ERR {type(exc).__name__}]"
        return None


def _store_path(category: str, key) -> Path:
    return STORE / category / f"{key}.json"


def _stored(category: str, key) -> bool:
    return _store_path(category, key).exists()


def _save(category: str, key, data) -> None:
    p = _store_path(category, key)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def _now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


# ----------------------------------------------------------------------- scope helpers (offline)
def _read_csv(path):
    import csv
    if not path.exists():
        return []
    with open(path, encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def wc_team_ids() -> set[int]:
    """IDs de selección del torneo, desde int_results (WC2026)."""
    ids = set()
    for r in _read_csv(INT_RESULTS):
        if str(r.get("league_id")) == str(WC_LEAGUE) and str(r.get("season")) == str(WC_SEASON):
            for k in ("home_id", "away_id"):
                try:
                    ids.add(int(float(r[k])))
                except (TypeError, ValueError, KeyError):
                    pass
    return ids


def wc_fixture_ids(settled_only=False) -> list[int]:
    ids = []
    for r in _read_csv(INT_RESULTS):
        if str(r.get("league_id")) == str(WC_LEAGUE) and str(r.get("season")) == str(WC_SEASON):
            try:
                ids.append(int(float(r["fixture_id"])))
            except (TypeError, ValueError, KeyError):
                pass
    return ids


# ----------------------------------------------------------------------- NIVEL 1
def ingest_tournament(client, counter):
    """Datos únicos de torneo. ~pocas llamadas."""
    jobs = [
        ("meta", "leagues_seasons", "/leagues/seasons", None, TTL_FOREVER),
        ("meta", "league_wc", "/leagues", {"id": WC_LEAGUE}, TTL_SLOW),
        ("standings", f"{WC_LEAGUE}_{WC_SEASON}", "/standings", {"league": WC_LEAGUE, "season": WC_SEASON}, TTL_SLOW),
        ("teams", f"list_{WC_LEAGUE}_{WC_SEASON}", "/teams", {"league": WC_LEAGUE, "season": WC_SEASON}, TTL_SLOW),
        ("tops", "topscorers", "/players/topscorers", {"league": WC_LEAGUE, "season": WC_SEASON}, TTL_SLOW),
        ("tops", "topassists", "/players/topassists", {"league": WC_LEAGUE, "season": WC_SEASON}, TTL_SLOW),
        ("tops", "topyellowcards", "/players/topyellowcards", {"league": WC_LEAGUE, "season": WC_SEASON}, TTL_SLOW),
        ("tops", "topredcards", "/players/topredcards", {"league": WC_LEAGUE, "season": WC_SEASON}, TTL_SLOW),
    ]
    got = 0
    for cat, key, path, params, ttl in jobs:
        if _stored(cat, key):
            continue
        resp = _get(client, path, params, ttl, counter)
        if resp is not None:
            _save(cat, key, {"fetched_at": _now(), "path": path, "params": params, "response": resp})
            got += 1
    return got


def ingest_teams(client, counter, team_ids):
    """Por selección: teams/statistics, squads, injuries, coachs, sidelined(coach)."""
    got = 0
    for tid in sorted(team_ids):
        # teams/statistics (WC)
        if not _stored("team_statistics", tid):
            r = _get(client, "/teams/statistics", {"team": tid, "league": WC_LEAGUE, "season": WC_SEASON}, TTL_SLOW, counter)
            if r is not None:
                _save("team_statistics", tid, {"fetched_at": _now(), "team": tid, "response": r}); got += 1
        # squad
        if not _stored("squads", tid):
            r = _get(client, "/players/squads", {"team": tid}, TTL_SLOW, counter)
            if r is not None:
                _save("squads", tid, {"fetched_at": _now(), "team": tid, "response": r}); got += 1
        # injuries (WC)
        if not _stored("injuries", tid):
            r = _get(client, "/injuries", {"team": tid, "league": WC_LEAGUE, "season": WC_SEASON}, TTL_LIVE, counter)
            if r is not None:
                _save("injuries", tid, {"fetched_at": _now(), "team": tid, "response": r}); got += 1
        # coach
        if not _stored("coachs", tid):
            r = _get(client, "/coachs", {"team": tid}, TTL_SLOW, counter)
            if r is not None:
                _save("coachs", tid, {"fetched_at": _now(), "team": tid, "response": r}); got += 1
    return got


def ingest_fixtures(client, counter, fixture_ids, settled_ids):
    """Por fixture: headtohead(1x pareja), y para los liquidados statistics/events/players/lineups."""
    got = 0
    settled = set(settled_ids)
    for fid in fixture_ids:
        if fid in settled:
            for cat, path in (("fx_statistics", "/fixtures/statistics"),
                              ("fx_events", "/fixtures/events"),
                              ("fx_players", "/fixtures/players"),
                              ("fx_lineups", "/fixtures/lineups")):
                if not _stored(cat, fid):
                    r = _get(client, path, {"fixture": fid}, TTL_FOREVER, counter)
                    if r is not None:
                        _save(cat, fid, {"fetched_at": _now(), "fixture": fid, "response": r}); got += 1
    return got


def ingest_players_wc(client, counter, player_ids):
    """Perfil + stats WC de cada jugador implicado (/players id+season=2026)."""
    got = 0
    for pid in sorted(player_ids):
        if _stored("player_wc", pid):
            continue
        r = _get(client, "/players", {"id": pid, "season": WC_SEASON}, TTL_SLOW, counter)
        if r is not None:
            _save("player_wc", pid, {"fetched_at": _now(), "player": pid, "response": r}); got += 1
    return got


def ingest_player_profiles(client, counter, player_ids):
    """Bio/perfil estable de cada jugador (/players/profiles?player=id). Inmutable → cache forever."""
    got = 0
    for pid in sorted(player_ids):
        if _stored("player_profile", pid):
            continue
        r = _get(client, "/players/profiles", {"player": pid}, TTL_FOREVER, counter)
        if r is not None:
            _save("player_profile", pid, {"fetched_at": _now(), "player": pid, "response": r}); got += 1
    return got


def ingest_venues(client, counter):
    """Estadios del torneo: ids desde el /fixtures index (cache), luego /venues?id por sede única."""
    got = 0
    idx = _get(client, "/fixtures", {"league": WC_LEAGUE, "season": WC_SEASON}, TTL_LIVE, counter)
    venue_ids = set()
    for row in (idx or []):
        vid = ((row.get("fixture") or {}).get("venue") or {}).get("id")
        if vid:
            venue_ids.add(int(vid))
    for vid in sorted(venue_ids):
        if _stored("venues", vid):
            continue
        r = _get(client, "/venues", {"id": vid}, TTL_FOREVER, counter)
        if r is not None:
            _save("venues", vid, {"fetched_at": _now(), "venue": vid, "response": r}); got += 1
    return got


# ----------------------------------------------------------------------- NIVEL 2 (club)
def ingest_players_club(client, counter, player_ids):
    """Temporada de CLUB de cada jugador (/players id+season=2025). Deriva clubes → teams/statistics.
    Idempotente: fase 1 pide solo los player_club que falten; fase 2 recolecta los club_ids desde
    TODOS los player_club ya en el store (no solo los recién pedidos) y pide los teams/statistics que
    falten. Un club se pide UNA vez (keyed por team_id) para acotar el fan-out."""
    got = 0
    # fase 1 — temporada de club de cada jugador (store-guarded)
    for pid in sorted(player_ids):
        if _stored("player_club", pid):
            continue
        r = _get(client, "/players", {"id": pid, "season": CLUB_SEASON}, TTL_SLOW, counter)
        if r is not None:
            _save("player_club", pid, {"fetched_at": _now(), "player": pid, "season": CLUB_SEASON, "response": r})
            got += 1
    # fase 2 — recolectar clubes desde TODO el store player_club (real leagues only, sin selecciones)
    club_ids = set()
    d = STORE / "player_club"
    for p in (d.glob("*.json") if d.exists() else []):
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            continue
        for row in data.get("response", []) or []:
            for st in row.get("statistics", []) or []:
                tid = (st.get("team") or {}).get("id")
                lid = (st.get("league") or {}).get("id")
                if tid and lid and int(lid) != WC_LEAGUE:   # clubes reales; descarta None y selección
                    club_ids.add((int(tid), int(lid)))
    for tid, lid in sorted(club_ids):
        if _stored("club_team_statistics", tid):
            continue
        r = _get(client, "/teams/statistics", {"team": tid, "league": lid, "season": CLUB_SEASON}, TTL_SLOW, counter)
        if r is not None:
            _save("club_team_statistics", tid, {"fetched_at": _now(), "team": tid, "league": lid, "response": r}); got += 1
    return got


def _player_ids_from_store() -> set[int]:
    """IDs de jugador desde los squads ya capturados (nivel 1 los llena)."""
    ids = set()
    for p in (STORE / "squads").glob("*.json") if (STORE / "squads").exists() else []:
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            for team in data.get("response", []) or []:
                for pl in team.get("players", []) or []:
                    if pl.get("id"):
                        ids.add(int(pl["id"]))
        except Exception:  # noqa: BLE001
            pass
    return ids


# ----------------------------------------------------------------------- ESTIMATE (0 API)
def estimate():
    teams = wc_team_ids()
    fixtures = wc_fixture_ids()
    settled = len(wc_settled_ids())
    n_teams = len(teams) or 48
    n_fx = len(fixtures) or 104
    n_settled = settled or n_fx
    n_players = n_teams * 26  # squad WC ~26/selección
    lines = []
    lines.append(f"Scope detectado: {n_teams} selecciones · {n_fx} fixtures WC ({n_settled} liquidados) · ~{n_players} jugadores (26/squad)")
    lines.append("")
    lines.append("NIVEL 1 (WC 2026):")
    lines.append(f"  torneo (standings, tops×4, teams, leagues×2)         ~   8")
    lines.append(f"  equipos: 4 endpoints × {n_teams}                       ~ {4*n_teams:4d}  (teams/stats, squads, injuries, coachs)")
    lines.append(f"  fixtures liquidados: 4 × {n_settled}                    ~ {4*n_settled:4d}  (statistics, events, players, lineups)")
    lines.append(f"  venues (index 1 + ~16 sedes)                         ~   17  (/fixtures idx + /venues)")
    lines.append(f"  jugadores WC: 1 × {n_players}                          ~ {n_players:4d}  (/players id+season2026)")
    lines.append(f"  player profiles: 1 × {n_players}                       ~ {n_players:4d}  (/players/profiles)")
    l1 = 8 + 4*n_teams + 4*n_settled + 17 + 2*n_players
    lines.append(f"  --------------------------------------------------  SUBTOTAL N1 ≈ {l1}")
    lines.append("")
    lines.append("NIVEL 2 (club de esos jugadores):")
    lines.append(f"  players club: 1 × {n_players}                          ~ {n_players:4d}  (/players id+season2025)")
    lines.append(f"  teams/statistics de clubes (dedupe ~350)             ~  350")
    l2 = n_players + 350
    lines.append(f"  --------------------------------------------------  SUBTOTAL N2 ≈ {l2}")
    lines.append("")
    lines.append(f"TOTAL ≈ {l1 + l2} llamadas  (tope diario Ultra = 75.000 → cabe holgado en 1 día)")
    lines.append("Nota: store-guarded → en re-ejecuciones solo se piden ids nuevos (≈0 en estado estable).")
    return "\n".join(lines)


def wc_settled_ids() -> list[int]:
    ids = []
    for r in _read_csv(LOG):
        try:
            if str(r.get("settled")) in ("1", "1.0") and r.get("result_ft_gh") not in (None, ""):
                ids.append(int(float(r["fixture_id"])))
        except (TypeError, ValueError, KeyError):
            pass
    if ids:
        return ids
    # fallback: los que están en int_results (todos tienen gh/ga reales)
    return wc_fixture_ids()


# ----------------------------------------------------------------------- main
def main(argv=None):
    ap = argparse.ArgumentParser(description="Ingesta comprehensiva no-apuesta WC2026 (Fase A).")
    ap.add_argument("--level", choices=["1", "2", "all"], default="1")
    ap.add_argument("--estimate", action="store_true", help="(default si no --execute) plan de llamadas, 0 API")
    ap.add_argument("--execute", action="store_true", help="captura REAL (requiere OK). Sin él, solo estimate.")
    ap.add_argument("--max-calls", type=int, default=10000, help="tope duro de llamadas (red anti-runaway)")
    a = ap.parse_args(argv)

    print("=" * 84)
    print("INGESTA COMPREHENSIVA WC2026 — Fase A (NO-APUESTA; /odds y /predictions BLOQUEADOS)")
    print("=" * 84)
    print(f"generated_at_utc: {_now()}")

    if not a.execute:
        print("\nMODO: ESTIMATE (0 API — no se hace ninguna llamada).\n")
        print(estimate())
        print("\nPara lanzar la captura real: --execute (con OK de Jorge).")
        return 0

    client = _client()
    counter = Counter(a.max_calls)
    teams = wc_team_ids()
    fixtures = wc_fixture_ids()
    settled = wc_settled_ids()
    print(f"\nMODO: EXECUTE · nivel={a.level} · max-calls={a.max_calls}")
    print(f"scope: {len(teams)} selecciones · {len(fixtures)} fixtures ({len(settled)} liquidados)")

    got = {}
    if a.level in ("1", "all"):
        got["tournament"] = ingest_tournament(client, counter)
        got["teams"] = ingest_teams(client, counter, teams)
        got["fixtures"] = ingest_fixtures(client, counter, fixtures, settled)
        got["venues"] = ingest_venues(client, counter)
        players = _player_ids_from_store()
        got["players_wc"] = ingest_players_wc(client, counter, players)
        got["player_profiles"] = ingest_player_profiles(client, counter, players)
    if a.level in ("2", "all"):
        players = _player_ids_from_store()
        got["players_club"] = ingest_players_club(client, counter, players)

    print(f"\nCapturado (nuevos): {json.dumps(got)}")
    print(f"Llamadas API realizadas: {counter.n} (tope {a.max_calls})")
    (STORE).mkdir(parents=True, exist_ok=True)
    (STORE / "_last_ingest_trace.txt").write_text("\n".join(counter.trace), encoding="utf-8")
    print(f"Trace -> {STORE / '_last_ingest_trace.txt'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
