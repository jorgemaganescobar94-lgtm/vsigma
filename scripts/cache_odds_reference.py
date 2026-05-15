from __future__ import annotations

from pathlib import Path
from datetime import datetime, timezone
import json

from api_football_client import APIFootballClient, APIFootballError


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "data" / "cache"

BETS_JSON = OUTPUT_DIR / "odds_bets_reference.json"
BOOKMAKERS_JSON = OUTPUT_DIR / "odds_bookmakers_reference.json"


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    client = APIFootballClient()

    print("\n=== CACHE ODDS REFERENCE ===")

    try:
        bets_payload = client.request("/odds/bets", ttl_hours=24 * 30)
        BETS_JSON.write_text(
            json.dumps(
                {
                    "generated_at_utc": datetime.now(timezone.utc).isoformat(),
                    "payload": bets_payload,
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
        print(f"OK odds bets -> {BETS_JSON}")
    except APIFootballError as e:
        print(f"API_ERROR /odds/bets -> {e}")
        return
    except Exception as e:
        print(f"ERROR /odds/bets -> {e}")
        return

    try:
        bookmakers_payload = client.request("/odds/bookmakers", ttl_hours=24 * 30)
        BOOKMAKERS_JSON.write_text(
            json.dumps(
                {
                    "generated_at_utc": datetime.now(timezone.utc).isoformat(),
                    "payload": bookmakers_payload,
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
        print(f"OK odds bookmakers -> {BOOKMAKERS_JSON}")
    except APIFootballError as e:
        print(f"API_ERROR /odds/bookmakers -> {e}")
        return
    except Exception as e:
        print(f"ERROR /odds/bookmakers -> {e}")
        return

    print("\nCompletado.")


if __name__ == "__main__":
    main()