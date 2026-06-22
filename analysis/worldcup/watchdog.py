#!/usr/bin/env python3
"""vSIGMA World Cup pipeline WATCHDOG (independent, local).

Detects when the World Cup pipeline stops producing output (e.g. the GitHub
Actions quota blackout, or a failed local run) and raises a Telegram alert.

DESIGN
  - Freshness = the MOST RECENT of:
      * generated_at_utc in worldcup_scorecard.txt
      * max(logged_at_utc, settled_at_utc) across worldcup_predictions_log.csv
      * last timestamped line in worldcup_local_run.log
  - If the freshest output is OLDER than THRESHOLD_HOURS (~24h)  -> ALERT.
  - If NO output file can be read at all                         -> ALERT (never fail silent).
  - If output is fresh                                           -> stay quiet (no noise).
  - Every check is appended to watchdog.log (gitignored via *.log): timestamp,
    detected freshness, alert yes/no.  NO secrets are ever logged or printed.

SECURITY
  - Contains NO secrets. Reads TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID from the
    process env, loading them from .env.telegram if not already set.
  - NEVER prints/logs the token, chat_id, or the Telegram API URL.

USAGE
  python watchdog.py            # daily check; alerts only if stale/unreadable
  python watchdog.py --startup  # send a one-time "watchdog activo" confirmation
  python watchdog.py --selftest # offline tests (no real Telegram send)
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import os
import sys
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))

SCORECARD = os.path.join(HERE, "worldcup_scorecard.txt")
LOG_CSV = os.path.join(HERE, "worldcup_predictions_log.csv")
LOCAL_RUN_LOG = os.path.join(HERE, "worldcup_local_run.log")
WATCHDOG_LOG = os.path.join(HERE, "watchdog.log")
ENV_TELEGRAM = os.path.join(REPO, ".env.telegram")

THRESHOLD_HOURS = 24.0
TELEGRAM_API = "https://api.telegram.org/bot{token}/sendMessage"


# ----------------------------------------------------------------------------- utils
def now_utc() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def parse_iso(s: str) -> dt.datetime | None:
    """Parse an ISO-8601 timestamp (with 'Z' or +00:00, optional fractional secs)."""
    if not s:
        return None
    s = s.strip()
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    try:
        d = dt.datetime.fromisoformat(s)
    except ValueError:
        return None
    if d.tzinfo is None:
        d = d.replace(tzinfo=dt.timezone.utc)
    return d.astimezone(dt.timezone.utc)


def watchdog_log(line: str) -> None:
    """Append one line to watchdog.log (best-effort; never raises, never logs secrets)."""
    try:
        with open(WATCHDOG_LOG, "a", encoding="utf-8") as fh:
            fh.write(f"[{now_utc().strftime('%Y-%m-%dT%H:%M:%SZ')}] {line}\n")
    except Exception:
        pass


# ----------------------------------------------------------------------------- freshness sources
def from_scorecard() -> dt.datetime | None:
    try:
        with open(SCORECARD, encoding="utf-8") as fh:
            for line in fh:
                if "generated_at_utc:" in line:
                    return parse_iso(line.split("generated_at_utc:", 1)[1])
    except Exception:
        return None
    return None


def from_predictions_csv() -> dt.datetime | None:
    best = None
    try:
        with open(LOG_CSV, encoding="utf-8", newline="") as fh:
            for row in csv.DictReader(fh):
                for col in ("logged_at_utc", "settled_at_utc"):
                    d = parse_iso(row.get(col, ""))
                    if d and (best is None or d > best):
                        best = d
    except Exception:
        return None
    return best


def from_local_run_log() -> dt.datetime | None:
    """Last '[<iso>] ...' timestamp in worldcup_local_run.log."""
    best = None
    try:
        with open(LOCAL_RUN_LOG, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line.startswith("[") and "]" in line:
                    d = parse_iso(line[1:line.index("]")])
                    if d and (best is None or d > best):
                        best = d
    except Exception:
        return None
    return best


def newest_output_time() -> tuple[dt.datetime | None, str, dict]:
    """Most recent freshness signal across all sources. Returns (dt, source, detail)."""
    candidates = {
        "scorecard": from_scorecard(),
        "predictions_csv": from_predictions_csv(),
        "local_run_log": from_local_run_log(),
    }
    readable = {k: v for k, v in candidates.items() if v is not None}
    if not readable:
        return None, "NONE", candidates
    src, best = max(readable.items(), key=lambda kv: kv[1])
    return best, src, candidates


# ----------------------------------------------------------------------------- decision (pure -> testable)
def evaluate(newest: dt.datetime | None, now: dt.datetime,
             threshold_hours: float = THRESHOLD_HOURS) -> tuple[bool, float | None, str]:
    """Return (is_alert, age_hours, reason)."""
    if newest is None:
        return True, None, "unreadable"
    age_h = (now - newest).total_seconds() / 3600.0
    if age_h > threshold_hours:
        return True, age_h, "stale"
    return False, age_h, "fresh"


def build_alert_message(newest: dt.datetime | None, age_h: float | None,
                        reason: str, source: str) -> str:
    if reason == "unreadable":
        return (
            "🚨 vSIGMA Watchdog — ALERTA\n"
            "No puedo leer NINGUNA salida del pipeline del Mundial "
            "(scorecard / predictions_log / local_run.log).\n"
            "Esto es anómalo: posible borrado, ruta movida, o el pipeline nunca corrió.\n"
            "Pista: revisa GitHub Actions (¿cuota agotada?) y el run local."
        )
    ts = newest.strftime("%Y-%m-%d %H:%M UTC") if newest else "desconocido"
    return (
        "🚨 vSIGMA Watchdog — ALERTA\n"
        f"El pipeline del Mundial lleva ~{age_h:.1f}h sin producir salida.\n"
        f"Última salida conocida: {ts} (fuente: {source}).\n"
        f"Umbral: {THRESHOLD_HOURS:.0f}h.\n"
        "Pista: posible bloqueo de GitHub Actions por cuota, o fallo del run local — revisa."
    )


# ----------------------------------------------------------------------------- telegram
def load_env_telegram() -> tuple[bool, str]:
    """Load TELEGRAM_* from .env.telegram into os.environ. Returns (ok, error_msg)."""
    if os.environ.get("TELEGRAM_BOT_TOKEN") and os.environ.get("TELEGRAM_CHAT_ID"):
        return True, ""
    if not os.path.exists(ENV_TELEGRAM):
        return False, f".env.telegram no encontrado en {ENV_TELEGRAM}"
    try:
        with open(ENV_TELEGRAM, encoding="utf-8") as fh:
            for raw in fh:
                line = raw.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())
    except Exception as exc:  # noqa: BLE001
        return False, f"no pude leer .env.telegram: {type(exc).__name__}"
    if not os.environ.get("TELEGRAM_BOT_TOKEN") or not os.environ.get("TELEGRAM_CHAT_ID"):
        return False, ".env.telegram presente pero TELEGRAM_BOT_TOKEN/CHAT_ID vacíos"
    return True, ""


def send_telegram(text: str) -> tuple[bool, str]:
    """POST a message. Never prints token/chat_id/URL. Returns (ok, status_str)."""
    ok, err = load_env_telegram()
    if not ok:
        return False, err
    token = os.environ["TELEGRAM_BOT_TOKEN"].strip()
    chat_id = os.environ["TELEGRAM_CHAT_ID"].strip()
    data = urllib.parse.urlencode({"chat_id": chat_id, "text": text}).encode()
    try:
        req = urllib.request.Request(TELEGRAM_API.format(token=token), data=data)
        with urllib.request.urlopen(req, timeout=20) as resp:
            return (resp.status == 200), f"HTTP {resp.status}"
    except urllib.error.HTTPError as e:
        return False, f"HTTP {e.code}"
    except Exception as e:  # noqa: BLE001
        return False, type(e).__name__


# ----------------------------------------------------------------------------- modes
def run_check(send: bool = True) -> int:
    newest, source, _detail = newest_output_time()
    is_alert, age_h, reason = evaluate(newest, now_utc())
    ts = newest.strftime("%Y-%m-%dT%H:%M:%SZ") if newest else "NONE"
    age_str = f"{age_h:.1f}h" if age_h is not None else "n/a"

    if not is_alert:
        watchdog_log(f"check: freshest={ts} src={source} age={age_str} reason={reason} ALERT=no")
        print(f"[watchdog] FRESCO ({age_str}, fuente {source}) — sin alerta.")
        return 0

    msg = build_alert_message(newest, age_h, reason, source)
    sent_status = "skipped"
    if send:
        ok, sent_status = send_telegram(msg)
        sent_status = f"sent={ok}({sent_status})"
    watchdog_log(f"check: freshest={ts} src={source} age={age_str} reason={reason} ALERT=YES {sent_status}")
    print(f"[watchdog] ALERTA ({reason}, {age_str}). {sent_status}")
    return 1


def run_startup() -> int:
    ok, status = send_telegram("✅ Watchdog vSIGMA activo — vigilando el pipeline del Mundial")
    watchdog_log(f"startup test message: sent={ok} ({status})")
    print(f"[watchdog] mensaje de arranque: sent={ok} ({status})")
    return 0 if ok else 1


def run_selftest() -> int:
    now = parse_iso("2026-06-22T12:00:00Z")
    passed = []

    # 1) STALE (30h old) -> alert, message built, NOT sent
    stale = parse_iso("2026-06-21T06:00:00Z")
    a, age, reason = evaluate(stale, now)
    msg = build_alert_message(stale, age, reason, "scorecard")
    t1 = (a is True and reason == "stale" and 29 < age < 31 and "ALERTA" in msg)
    passed.append(("STALE>24h detecta alerta + construye mensaje (sin enviar)", t1))

    # 2) FRESH (1h old) -> no alert
    fresh = parse_iso("2026-06-22T11:00:00Z")
    a2, age2, reason2 = evaluate(fresh, now)
    t2 = (a2 is False and reason2 == "fresh")
    passed.append(("FRESCO<24h => silencio", t2))

    # 3) UNREADABLE (no sources) -> alert
    a3, age3, reason3 = evaluate(None, now)
    t3 = (a3 is True and reason3 == "unreadable" and age3 is None)
    passed.append(("Salida ilegible => alerta (no falla en silencio)", t3))

    # 4) .env.telegram ausente -> error claro, sin crash
    saved_token = os.environ.pop("TELEGRAM_BOT_TOKEN", None)
    saved_chat = os.environ.pop("TELEGRAM_CHAT_ID", None)
    global ENV_TELEGRAM
    real = ENV_TELEGRAM
    ENV_TELEGRAM = os.path.join(REPO, ".env.telegram.__missing__")
    try:
        ok, err = load_env_telegram()
    finally:
        ENV_TELEGRAM = real
        if saved_token is not None:
            os.environ["TELEGRAM_BOT_TOKEN"] = saved_token
        if saved_chat is not None:
            os.environ["TELEGRAM_CHAT_ID"] = saved_chat
    t4 = (ok is False and "no encontrado" in err)
    passed.append((".env.telegram ausente => error claro, sin crash", t4))

    print("=== watchdog selftest ===")
    allok = True
    for name, ok in passed:
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
        allok = allok and ok
    print("RESULT:", "ALL PASS" if allok else "FAIL")
    return 0 if allok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="vSIGMA World Cup pipeline watchdog")
    ap.add_argument("--startup", action="store_true", help="send one-time activation message")
    ap.add_argument("--selftest", action="store_true", help="offline tests, no real send")
    ap.add_argument("--no-send", action="store_true", help="check but never send (dry run)")
    args = ap.parse_args()

    if args.selftest:
        return run_selftest()
    if args.startup:
        return run_startup()
    return run_check(send=not args.no_send)


if __name__ == "__main__":
    sys.exit(main())
