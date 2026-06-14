#!/usr/bin/env python3
"""Envia una alerta vSIGMA a Telegram.

- Lee TELEGRAM_BOT_TOKEN y TELEGRAM_CHAT_ID SOLO del entorno.
- Fail-soft: si falta cualquiera, loguea y sale 0 (nunca rompe el run).
- NUNCA imprime el token, el chat_id, ni la URL completa de la API
  (la URL contiene el token).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request

TELEGRAM_API = "https://api.telegram.org/bot{token}/sendMessage"
MAX_LEN = 3500  # limite Telegram 4096; margen de seguridad


def log(msg: str) -> None:
    print(f"[telegram-alert] {msg}")


def build_message(title: str, summary: str, day: str, link: str) -> str:
    parts = [f"🚨 {title}"]
    if day:
        parts.append(f"Fecha: {day}")
    if summary:
        parts += ["", summary.strip()]
    if link:
        parts += ["", f"Detalle: {link}"]
    return "\n".join(parts)[:MAX_LEN]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--title", required=True)
    ap.add_argument("--summary", default="")
    ap.add_argument("--date", default="")
    ap.add_argument("--link", default="")
    ap.add_argument("--body-file", default="")
    args = ap.parse_args()

    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "").strip()
    if not token or not chat_id:
        log("TELEGRAM_BOT_TOKEN/CHAT_ID no configurados; omito notificacion (fail-soft).")
        return 0

    summary = args.summary
    if args.body_file and os.path.exists(args.body_file):
        try:
            with open(args.body_file, encoding="utf-8") as fh:
                summary = fh.read()
        except Exception as exc:  # noqa: BLE001
            log(f"no pude leer body-file: {type(exc).__name__}")
    summary = "\n".join(summary.splitlines()[:25])  # corto para movil

    text = build_message(args.title, summary, args.date, args.link)
    payload = json.dumps(
        {"chat_id": chat_id, "text": text, "disable_web_page_preview": True}
    ).encode("utf-8")

    req = urllib.request.Request(
        TELEGRAM_API.format(token=token),
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            log(f"enviado: HTTP {resp.status}")
    except urllib.error.HTTPError as exc:
        # NUNCA imprimir exc.url (contiene el token). Solo code/reason.
        log(f"Telegram HTTPError {exc.code} {exc.reason} (no fatal)")
    except Exception as exc:  # noqa: BLE001
        log(f"Telegram fallo no fatal: {type(exc).__name__}")
    return 0  # siempre fail-soft


if __name__ == "__main__":
    sys.exit(main())
