from __future__ import annotations

from pathlib import Path
import shutil
import pandas as pd
import numpy as np


ROOT = Path(__file__).resolve().parents[1]

MATCHES_CSV = ROOT / "data" / "raw" / "matches.csv"
BACKUP_CSV = ROOT / "data" / "raw" / "matches_before_nan_sanitize_backup.csv"

NUMERIC_COLUMNS = [
    "home_xg_for",
    "home_xg_against",
    "away_xg_for",
    "away_xg_against",
    "home_sot_for",
    "away_sot_for",
    "home_big_for",
    "away_big_for",
    "home_form_pts",
    "away_form_pts",
    "home_scored_rate",
    "away_scored_rate",
    "home_clean_sheet_rate",
    "away_clean_sheet_rate",
]

TEXT_COLUMNS = [
    "home_motivation",
    "away_motivation",
    "home_absences",
    "away_absences",
]


def main() -> None:
    if not MATCHES_CSV.exists():
        raise FileNotFoundError(f"No existe: {MATCHES_CSV}")

    df = pd.read_csv(MATCHES_CSV)

    if not BACKUP_CSV.exists():
        shutil.copy2(MATCHES_CSV, BACKUP_CSV)

    for col in NUMERIC_COLUMNS:
        if col in df.columns:
            s = pd.to_numeric(df[col], errors="coerce")
            if s.notna().sum() > 0 and (s.fillna(0) == 0).all():
                df[col] = np.nan

    for col in TEXT_COLUMNS:
        if col in df.columns:
            s = df[col].astype(str).str.strip()
            if s.replace({"nan": "", "None": ""}).eq("").all():
                df[col] = ""

    df.to_csv(MATCHES_CSV, index=False)

    print("\n=== SANITIZADO COMPLETADO ===")
    print(f"CSV actualizado: {MATCHES_CSV}")
    print(f"Backup: {BACKUP_CSV}")

    print("\nResumen:")
    for col in NUMERIC_COLUMNS:
        if col in df.columns:
            s = pd.to_numeric(df[col], errors="coerce")
            print(f"{col}: non_null={int(s.notna().sum())}, null={int(s.isna().sum())}")


if __name__ == "__main__":
    main()
