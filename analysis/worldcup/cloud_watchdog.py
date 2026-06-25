"""
CLOUD WATCHDOG — World Cup daily-run FRESHNESS monitor.  ISOLATED (analysis/worldcup/).

Checks whether the daily World Cup run actually updated its output. It reads the
freshest available signal — `generated_at_utc:` inside worldcup_scorecard.txt, with
the git last-commit time of the scorecard/log as a fallback — and if the freshest
output is older than ~26h (or cannot be read at all) it sends ONE Telegram alert by
REUSING the existing dispatcher (scripts/dispatch_telegram_alert.py) and the same
TELEGRAM_* GitHub secrets as the main workflow. If the output is fresh: total silence.

Design rules:
  * Soft / robust: any read error -> ALERT (not a crash). main() never raises.
  * NEVER prints secrets (it never even touches them; the dispatcher reads them).
  * ZERO odds / predictions: it only ever reads TIMESTAMPS, never model values.
  * No third-party deps (stdlib only) -> the workflow needs no pip install.

HONEST CAVEAT: this watchdog runs INSIDE GitHub Actions. If the WHOLE Actions
account were down it could not run either. But the repo is PUBLIC, so there is no
billing/spending block anymore; this covers the common failure mode — "the main
cron was skipped / didn't update, but Actions itself is working".
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SCORECARD = HERE / "worldcup_scorecard.txt"
LOG = HERE / "worldcup_predictions_log.csv"
DISPATCHER = ROOT / "scripts" / "dispatch_telegram_alert.py"

STALE_HOURS = float(os.environ.get("WC_WATCHDOG_STALE_HOURS", "26"))
HINT = "el cron diario del Mundial no se ejecutó/actualizó — revisa GitHub Actions"
TS_RE = re.compile(r"generated_at_utc:\s*([0-9T:+\-]+)")


def log(msg: str) -> None:
    print(f"[wc-watchdog] {msg}")


def _to_utc(s: str):
    try:
        dt = datetime.fromisoformat(s.strip())
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except Exception:
        return None


def parse_scorecard_ts(text: str):
    """Extract the generated_at_utc timestamp from scorecard text, or None."""
    m = TS_RE.search(text or "")
    return _to_utc(m.group(1)) if m else None


def read_scorecard_ts(path: Path):
    try:
        return parse_scorecard_ts(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        log(f"no pude leer scorecard: {type(exc).__name__}")
        return None


def git_last_commit_ts(path: Path):
    """Last-commit time of a file (UTC), or None. Pure fallback; never raises."""
    try:
        r = subprocess.run(
            ["git", "log", "-1", "--format=%cI", "--", str(path)],
            cwd=str(ROOT), capture_output=True, text=True, timeout=15,
        )
        return _to_utc(r.stdout) if r.stdout.strip() else None
    except Exception as exc:  # noqa: BLE001
        log(f"git fallback no disponible: {type(exc).__name__}")
        return None


def latest_output_time():
    """Freshest of: scorecard generated_at_utc, git commit of scorecard, git commit of log."""
    cands = [read_scorecard_ts(SCORECARD), git_last_commit_ts(SCORECARD), git_last_commit_ts(LOG)]
    cands = [c for c in cands if c is not None]
    return max(cands) if cands else None


def decide(now, latest, stale_hours):
    """Return (is_stale, age_hours_or_None). Unreadable output (latest=None) -> stale."""
    if latest is None:
        return True, None
    age = (now - latest).total_seconds() / 3600.0
    return age > stale_hours, age


def build_alert(latest, age, stale_hours):
    if latest is None:
        return ("No pude leer la salida del daily del Mundial "
                "(scorecard/log ausentes o ilegibles).\n"
                f"Umbral de frescura: {stale_hours:.0f}h.\n"
                f"Pista: {HINT}.")
    return (f"Última salida del daily: {latest.isoformat(timespec='seconds')}\n"
            f"Antigüedad: {age:.1f}h (umbral {stale_hours:.0f}h).\n"
            f"Pista: {HINT}.")


def send(title: str, body: str) -> None:
    """Reuse the shared dispatcher (reads TELEGRAM_* from env; fail-soft; no secrets printed)."""
    try:
        subprocess.run(
            [sys.executable, str(DISPATCHER),
             "--title", title,
             "--date", datetime.now(timezone.utc).strftime("%Y-%m-%d"),
             "--summary", body],
            cwd=str(ROOT), timeout=30,
        )
    except Exception as exc:  # noqa: BLE001
        log(f"dispatcher fallo no fatal: {type(exc).__name__}")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="World Cup daily-run freshness watchdog (cloud).")
    ap.add_argument("--test", action="store_true",
                    help="enviar UN mensaje '✅ Watchdog activo' y salir (confirmación de vía Telegram)")
    ap.add_argument("--stale-hours", type=float, default=STALE_HOURS,
                    help=f"umbral de frescura en horas (def {STALE_HOURS:.0f})")
    ap.add_argument("--dry-run", action="store_true",
                    help="evalúa e imprime, pero NO envía a Telegram")
    args = ap.parse_args(argv)

    if args.test:
        body = ("Confirmación de activación: la vía Telegram del watchdog del Mundial "
                "funciona. A partir de ahora: callado salvo que el daily no actualice.")
        log("modo --test: enviando confirmación de activación")
        if not args.dry_run:
            send("✅ Watchdog Mundial (nube) activo", body)
        return 0

    try:
        now = datetime.now(timezone.utc)
        latest = latest_output_time()
        is_stale, age = decide(now, latest, args.stale_hours)
        if not is_stale:
            log(f"FRESCO: última salida {latest.isoformat(timespec='seconds')} "
                f"({age:.1f}h <= {args.stale_hours:.0f}h). Silencio.")
            return 0
        body = build_alert(latest, age, args.stale_hours)
        log("STALE/ILEGIBLE -> enviando alerta")
        for line in body.splitlines():
            log("  " + line)
        if not args.dry_run:
            send("🚨 Mundial: el daily no se ha actualizado", body)
        return 0
    except Exception as exc:  # noqa: BLE001  — never crash the workflow; alert instead
        log(f"watchdog error inesperado: {type(exc).__name__} -> intento alerta soft")
        if not args.dry_run:
            send("🚨 Mundial: watchdog con error interno",
                 f"El watchdog del Mundial falló al evaluar la frescura ({type(exc).__name__}).\n"
                 f"Pista: {HINT}.")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
