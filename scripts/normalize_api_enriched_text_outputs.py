from __future__ import annotations

import argparse
import csv
from pathlib import Path
from datetime import date

PROCESSED = Path("data/processed")

TARGET_NAMES = [
    "vsigma_max_coverage_api_enrichment_executor",
    "vsigma_api_enriched_scored_candidates",
    "vsigma_promotion_input_bridge",
    "vsigma_api_enriched_promotion_gate_adapter",
    "vsigma_promoted_api_enriched_candidates",
    "vsigma_api_enriched_review_board",
]

MOJIBAKE_MARKERS = [
    "Ã", "Â", "â€", "â€“", "â€”", "â€˜", "â€™", "â€œ", "â€\x9d",
    "Å¡", "Å¾", "Å™", "Åˆ", "Å", "Ä",
]

def mojibake_score(text: str) -> int:
    return sum(text.count(marker) for marker in MOJIBAKE_MARKERS)

def fix_text(value: object) -> str:
    text = "" if value is None else str(value)
    if not text:
        return text

    if mojibake_score(text) == 0:
        return text

    try:
        fixed = text.encode("latin1").decode("utf-8")
    except UnicodeError:
        return text

    if mojibake_score(fixed) < mojibake_score(text):
        return fixed

    return text

def normalize_text_file(path: Path) -> bool:
    if not path.exists():
        return False

    original = path.read_text(encoding="utf-8", errors="replace")
    lines = original.splitlines(keepends=True)
    fixed_lines = [fix_text(line) for line in lines]
    fixed = "".join(fixed_lines)

    if fixed != original:
        path.write_text(fixed, encoding="utf-8")
        return True
    return False

def normalize_csv_file(path: Path) -> bool:
    if not path.exists():
        return False

    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames or []
        rows = [dict(row) for row in reader]

    if not fieldnames:
        return False

    changed = False
    fixed_rows = []
    for row in rows:
        fixed_row = {}
        for field in fieldnames:
            original = row.get(field, "")
            fixed = fix_text(original)
            if fixed != original:
                changed = True
            fixed_row[field] = fixed
        fixed_rows.append(fixed_row)

    if changed:
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(fixed_rows)

    return changed

def target_paths(processed: Path, day: str) -> list[Path]:
    paths: list[Path] = []
    bases = [processed / "today" / day, processed / "governance"]

    for base in bases:
        for name in TARGET_NAMES:
            paths.append(base / f"{name}.md")
            paths.append(base / f"{name}.csv")
            paths.append(base / f"{name}_summary.csv")

    return paths

def run(day: str, processed: Path) -> None:
    day = date.fromisoformat(day).isoformat()
    changed = 0
    reviewed = 0

    for path in target_paths(processed, day):
        if not path.exists():
            continue

        reviewed += 1
        if path.suffix.lower() == ".csv":
            did_change = normalize_csv_file(path)
        else:
            did_change = normalize_text_file(path)

        if did_change:
            changed += 1

    print("=== VSIGMA API TEXT NORMALIZER ===")
    print(f"files_reviewed={reviewed}")
    print(f"files_changed={changed}")
    print("auto_apply=NO")
    print("production_change=NO")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True)
    parser.add_argument("--processed-dir", type=Path, default=PROCESSED)
    args = parser.parse_args()
    run(args.date, args.processed_dir)

if __name__ == "__main__":
    main()
