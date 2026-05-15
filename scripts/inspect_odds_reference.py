from __future__ import annotations

from pathlib import Path
import json
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
CACHE_DIR = ROOT / "data" / "cache"

BETS_JSON = CACHE_DIR / "odds_bets_reference.json"
BOOKMAKERS_JSON = CACHE_DIR / "odds_bookmakers_reference.json"


def load_payload(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"No existe: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    return data.get("payload", {})


def flatten_bets(payload: dict) -> pd.DataFrame:
    rows = []

    for item in payload.get("response", []):
        rows.append({
            "id": item.get("id"),
            "name": item.get("name"),
        })

    return pd.DataFrame(rows)


def flatten_bookmakers(payload: dict) -> pd.DataFrame:
    rows = []

    for item in payload.get("response", []):
        rows.append({
            "id": item.get("id"),
            "name": item.get("name"),
        })

    return pd.DataFrame(rows)


def main() -> None:
    bets_payload = load_payload(BETS_JSON)
    bookmakers_payload = load_payload(BOOKMAKERS_JSON)

    bets_df = flatten_bets(bets_payload)
    bookmakers_df = flatten_bookmakers(bookmakers_payload)

    print("\n=== INSPECCIÓN ODDS REFERENCE ===")

    print("\nBETS disponibles:")
    if bets_df.empty:
        print("Vacío")
    else:
        print(bets_df.sort_values(["name", "id"]).to_string(index=False))

    print("\nBOOKMAKERS disponibles:")
    if bookmakers_df.empty:
        print("Vacío")
    else:
        print(bookmakers_df.sort_values(["name", "id"]).head(100).to_string(index=False))

    if not bets_df.empty:
        patterns = [
            "match winner",
            "winner",
            "both teams to score",
            "over/under",
            "goals over/under",
            "double chance",
            "draw no bet",
        ]

        print("\nCoincidencias útiles en BETS:")
        for pat in patterns:
            subset = bets_df[bets_df["name"].astype(str).str.contains(pat, case=False, na=False)].copy()
            print(f"\n--- patrón: {pat} ---")
            if subset.empty:
                print("Sin coincidencias")
            else:
                print(subset.sort_values(["name", "id"]).to_string(index=False))


if __name__ == "__main__":
    main()