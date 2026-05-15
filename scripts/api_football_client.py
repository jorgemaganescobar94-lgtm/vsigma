from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
import hashlib
import json
import os
import sqlite3
import threading
import time
from typing import Any

import requests


ROOT = Path(__file__).resolve().parents[1]
ENV_PATH = ROOT / ".env"
CACHE_DIR = ROOT / "data" / "cache"
CACHE_DB_PATH = CACHE_DIR / "api_football_cache.sqlite3"

DEFAULT_BASE_URL = "https://v3.football.api-sports.io"


def load_env_file(env_path: Path = ENV_PATH) -> None:
    if not env_path.exists():
        return

    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()

        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")

        if key and key not in os.environ:
            os.environ[key] = value


def get_api_key() -> str:
    load_env_file()

    candidates = [
        "API_FOOTBALL_KEY",
        "APIFOOTBALL_KEY",
        "API_SPORTS_KEY",
        "APISPORTS_KEY",
        "RAPIDAPI_KEY",
        "X_RAPIDAPI_KEY",
    ]

    for name in candidates:
        value = os.environ.get(name)
        if value:
            return value.strip()

    raise RuntimeError(
        "No encuentro la API key.\n"
        "Crea C:\\vsigma\\.env con una línea como:\n"
        "API_FOOTBALL_KEY=TU_API_KEY_AQUI"
    )


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def json_dumps_stable(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def normalize_params(params: dict[str, Any] | None) -> dict[str, Any]:
    if not params:
        return {}

    cleaned: dict[str, Any] = {}

    for key, value in params.items():
        if value is None:
            continue

        if isinstance(value, bool):
            cleaned[key] = int(value)
        else:
            cleaned[key] = value

    return cleaned


def build_params_key(path: str, params: dict[str, Any]) -> str:
    raw = json_dumps_stable({"path": path, "params": params})
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


@dataclass
class APIFootballError(Exception):
    message: str
    status_code: int | None = None
    api_errors: Any = None
    response_text: str | None = None

    @property
    def is_plan_limit(self) -> bool:
        txt = f"{self.message} {self.api_errors} {self.response_text}".lower()
        return (
            "free plans do not have access" in txt
            or "plan" in txt and "access" in txt
            or "not allowed in your current subscription" in txt
        )

    def __str__(self) -> str:
        return self.message


class APIFootballClient:
    def __init__(
        self,
        api_key: str | None = None,
        base_url: str = DEFAULT_BASE_URL,
        cache_db_path: Path = CACHE_DB_PATH,
        timeout_seconds: int = 30,
        min_interval_seconds: float = 0.40,
        default_ttl_hours: float = 24.0,
    ) -> None:
        self.api_key = api_key or get_api_key()
        self.base_url = base_url.rstrip("/")
        self.cache_db_path = cache_db_path
        self.timeout_seconds = timeout_seconds
        self.min_interval_seconds = min_interval_seconds
        self.default_ttl_hours = default_ttl_hours

        self._last_request_ts = 0.0
        self._lock = threading.Lock()

        self._init_cache()

    def _init_cache(self) -> None:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)

        with sqlite3.connect(self.cache_db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS api_cache (
                    params_key TEXT PRIMARY KEY,
                    path TEXT NOT NULL,
                    params_json TEXT NOT NULL,
                    response_json TEXT NOT NULL,
                    fetched_at_utc TEXT NOT NULL,
                    expires_at_utc TEXT NOT NULL
                )
                """
            )
            conn.commit()

    def _sleep_if_needed(self) -> None:
        with self._lock:
            now_ts = time.time()
            elapsed = now_ts - self._last_request_ts

            if elapsed < self.min_interval_seconds:
                time.sleep(self.min_interval_seconds - elapsed)

            self._last_request_ts = time.time()

    def _get_cached(self, params_key: str) -> dict[str, Any] | None:
        with sqlite3.connect(self.cache_db_path) as conn:
            row = conn.execute(
                """
                SELECT response_json, expires_at_utc
                FROM api_cache
                WHERE params_key = ?
                """,
                (params_key,),
            ).fetchone()

        if not row:
            return None

        response_json, expires_at_utc = row
        expires_at = datetime.fromisoformat(expires_at_utc)

        if utc_now() > expires_at:
            return None

        return json.loads(response_json)

    def _set_cached(
        self,
        params_key: str,
        path: str,
        params: dict[str, Any],
        payload: dict[str, Any],
        ttl_hours: float,
    ) -> None:
        fetched_at = utc_now()
        expires_at = fetched_at + timedelta(hours=ttl_hours)

        with sqlite3.connect(self.cache_db_path) as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO api_cache (
                    params_key,
                    path,
                    params_json,
                    response_json,
                    fetched_at_utc,
                    expires_at_utc
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    params_key,
                    path,
                    json_dumps_stable(params),
                    json_dumps_stable(payload),
                    fetched_at.isoformat(),
                    expires_at.isoformat(),
                ),
            )
            conn.commit()

    def clear_expired_cache(self) -> int:
        now_iso = utc_now().isoformat()

        with sqlite3.connect(self.cache_db_path) as conn:
            cur = conn.execute(
                """
                DELETE FROM api_cache
                WHERE expires_at_utc < ?
                """,
                (now_iso,),
            )
            conn.commit()
            return cur.rowcount

    def request(
        self,
        path: str,
        params: dict[str, Any] | None = None,
        *,
        ttl_hours: float | None = None,
        use_cache: bool = True,
        force_refresh: bool = False,
    ) -> dict[str, Any]:
        normalized_params = normalize_params(params)
        params_key = build_params_key(path, normalized_params)
        ttl = self.default_ttl_hours if ttl_hours is None else ttl_hours

        if use_cache and not force_refresh:
            cached = self._get_cached(params_key)
            if cached is not None:
                return cached

        self._sleep_if_needed()

        url = f"{self.base_url}{path}"
        headers = {"x-apisports-key": self.api_key}

        response = requests.get(
            url,
            headers=headers,
            params=normalized_params,
            timeout=self.timeout_seconds,
        )

        response_text = response.text[:1000]

        if response.status_code != 200:
            raise APIFootballError(
                message=f"Error HTTP {response.status_code} en {path}",
                status_code=response.status_code,
                response_text=response_text,
            )

        try:
            payload = response.json()
        except Exception as exc:
            raise APIFootballError(
                message=f"No pude parsear JSON en {path}: {exc}",
                status_code=response.status_code,
                response_text=response_text,
            ) from exc

        errors = payload.get("errors")

        if errors:
            raise APIFootballError(
                message=f"API devolvió errors en {path}",
                status_code=response.status_code,
                api_errors=errors,
                response_text=response_text,
            )

        if use_cache:
            self._set_cached(
                params_key=params_key,
                path=path,
                params=normalized_params,
                payload=payload,
                ttl_hours=ttl,
            )

        return payload

    # Helpers
    def status(self, **kwargs) -> dict[str, Any]:
        return self.request("/status", kwargs or None, ttl_hours=1)

    def leagues(self, **kwargs) -> dict[str, Any]:
        return self.request("/leagues", kwargs or None, ttl_hours=24 * 7)

    def fixtures(self, **kwargs) -> dict[str, Any]:
        return self.request("/fixtures", kwargs or None, ttl_hours=6)

    def standings(self, **kwargs) -> dict[str, Any]:
        return self.request("/standings", kwargs or None, ttl_hours=12)

    def fixture_statistics(self, fixture: int | str) -> dict[str, Any]:
        return self.request("/fixtures/statistics", {"fixture": fixture}, ttl_hours=24 * 30)

    def fixture_events(self, fixture: int | str) -> dict[str, Any]:
        return self.request("/fixtures/events", {"fixture": fixture}, ttl_hours=24 * 30)

    def fixture_lineups(self, fixture: int | str) -> dict[str, Any]:
        return self.request("/fixtures/lineups", {"fixture": fixture}, ttl_hours=24 * 30)

    def injuries(self, **kwargs) -> dict[str, Any]:
        return self.request("/injuries", kwargs or None, ttl_hours=12)

    def odds(self, **kwargs) -> dict[str, Any]:
        return self.request("/odds", kwargs or None, ttl_hours=1)

    def predictions(
        self,
        fixture: int | str,
        *,
        use_cache: bool = True,
        force_refresh: bool = False,
    ) -> dict[str, Any]:
        return self.request(
            "/predictions",
            {"fixture": fixture},
            ttl_hours=6,
            use_cache=use_cache,
            force_refresh=force_refresh,
        )
