from __future__ import annotations

import argparse
import csv
import hashlib
import html
import re
import urllib.request
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

P = Path("data/processed")
INPUT_FILES = [
    "vsigma_probable_lineup_sources.csv",
    "vsigma_probable_lineup_sources_quarantine.csv",
    "probable_lineup_sources_autonomous.csv",
]
FIELDS = [
    "target_date", "generated_at", "fixture_id", "home_team", "away_team", "team_side",
    "source_name", "source_url_hash", "source_url_host", "fetch_status", "marker", "marker_count",
    "snippet_excerpt", "snippet_chars", "debug_status", "copyright_guard", "source_guard",
    "auto_apply", "production_change",
]
SUMMARY_FIELDS = [
    "target_date", "generated_at", "urls_reviewed", "rows_written", "fetch_status_counts",
    "marker_counts", "auto_apply", "production_change",
]
MARKERS = [
    "possible starting lineup", "predicted lineup", "possible xi", "predicted xi", "composition probable",
    "possible lineups", "probable lineups", "team news", "lineups",
]
MAX_EXCERPT_CHARS = 260


def s(x):
    return "" if x is None else str(x).strip()


def read(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return [dict(r) for r in csv.DictReader(f)]


def write(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows([{k: r.get(k, "") for k in fields} for r in rows])


def d(day: str, name: str) -> Path:
    return P / "today" / day / name


def url_hash(url: str) -> str:
    return hashlib.sha256(s(url).encode("utf-8")).hexdigest()[:16]


def url_host(url: str) -> str:
    try:
        from urllib.parse import urlparse
        return urlparse(url).netloc.lower().replace("www.", "")
    except Exception:
        return ""


def collect_input_rows(day: str) -> tuple[list[dict[str, str]], str]:
    out: list[dict[str, str]] = []
    used: list[str] = []
    seen = set()
    for name in INPUT_FILES:
        for path in [d(day, name), P / "governance" / name]:
            rows = read(path)
            if not rows:
                continue
            used.append(str(path))
            for r in rows:
                url = s(r.get("source_url") or r.get("url"))
                fid = s(r.get("fixture_id"))
                side = s(r.get("team_side"))
                src = s(r.get("source_name"))
                key = (fid, side, src, url)
                if not url or key in seen:
                    continue
                seen.add(key)
                rr = dict(r)
                rr["_source_file"] = str(path)
                out.append(rr)
    return out, ";".join(used) if used else "NO_INPUT_SOURCE_FILES"


def fetch_text(url: str) -> tuple[str, str]:
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 vSIGMA raw-debug-short-excerpt"},
        )
        with urllib.request.urlopen(req, timeout=12) as response:
            raw = response.read().decode("utf-8", "replace")
        return "OK", raw
    except Exception as exc:
        return f"FETCH_FAILED:{type(exc).__name__}", ""


def structured_text(page: str) -> str:
    page = re.sub(r"<script[\s\S]*?</script>", " ", page, flags=re.I)
    page = re.sub(r"<style[\s\S]*?</style>", " ", page, flags=re.I)
    page = re.sub(r"<br\s*/?>", "; ", page, flags=re.I)
    page = re.sub(r"</(?:p|div|li|h1|h2|h3|h4|strong|b|section|article)>", "\n", page, flags=re.I)
    page = re.sub(r"<[^>]+>", " ", page)
    page = html.unescape(page)
    lines = []
    for line in page.splitlines():
        clean = re.sub(r"\s+", " ", line).strip()
        if clean:
            lines.append(clean)
    return "\n".join(lines)


def short_excerpt(text: str, idx: int, marker: str) -> str:
    start = max(0, idx - 80)
    end = min(len(text), idx + len(marker) + 180)
    excerpt = text[start:end]
    excerpt = re.sub(r"\s+", " ", excerpt).strip()
    if len(excerpt) > MAX_EXCERPT_CHARS:
        excerpt = excerpt[:MAX_EXCERPT_CHARS].rstrip() + "…"
    return excerpt


def marker_snippets(text: str) -> list[tuple[str, int, str]]:
    lowered = text.lower()
    snippets: list[tuple[str, int, str]] = []
    for marker in MARKERS:
        positions = [m.start() for m in re.finditer(re.escape(marker), lowered)]
        if not positions:
            continue
        for idx in positions[:3]:
            snippets.append((marker, len(positions), short_excerpt(text, idx, marker)))
    return snippets[:12]


def build(day: str, tz: str) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    generated = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    input_rows, source_guard = collect_input_rows(day)
    rows: list[dict[str, str]] = []
    cache: dict[str, tuple[str, str]] = {}
    for r in input_rows:
        url = s(r.get("source_url") or r.get("url"))
        if url not in cache:
            status, raw = fetch_text(url)
            text = structured_text(raw) if raw else ""
            cache[url] = (status, text)
        else:
            status, text = cache[url]
        snippets = marker_snippets(text) if status == "OK" else []
        if not snippets:
            rows.append({
                "target_date": day,
                "generated_at": generated,
                "fixture_id": s(r.get("fixture_id")),
                "home_team": s(r.get("home_team")),
                "away_team": s(r.get("away_team")),
                "team_side": s(r.get("team_side")),
                "source_name": s(r.get("source_name")),
                "source_url_hash": url_hash(url),
                "source_url_host": url_host(url),
                "fetch_status": status,
                "marker": "NO_MARKER_FOUND" if status == "OK" else "FETCH_FAILED",
                "marker_count": "0",
                "snippet_excerpt": "",
                "snippet_chars": "0",
                "debug_status": "NO_DEBUG_SNIPPET" if status == "OK" else "FETCH_FAILED",
                "copyright_guard": "short_excerpt_only_no_full_html",
                "source_guard": source_guard,
                "auto_apply": "NO",
                "production_change": "NO",
            })
            continue
        for marker, count, excerpt in snippets:
            rows.append({
                "target_date": day,
                "generated_at": generated,
                "fixture_id": s(r.get("fixture_id")),
                "home_team": s(r.get("home_team")),
                "away_team": s(r.get("away_team")),
                "team_side": s(r.get("team_side")),
                "source_name": s(r.get("source_name")),
                "source_url_hash": url_hash(url),
                "source_url_host": url_host(url),
                "fetch_status": status,
                "marker": marker,
                "marker_count": str(count),
                "snippet_excerpt": excerpt,
                "snippet_chars": str(len(excerpt)),
                "debug_status": "DEBUG_SNIPPET",
                "copyright_guard": "short_excerpt_only_no_full_html",
                "source_guard": source_guard,
                "auto_apply": "NO",
                "production_change": "NO",
            })
    fetch_counts = Counter(r["fetch_status"] for r in rows)
    marker_counts = Counter(r["marker"] for r in rows)
    summary = [{
        "target_date": day,
        "generated_at": generated,
        "urls_reviewed": str(len(cache)),
        "rows_written": str(len(rows)),
        "fetch_status_counts": "; ".join(f"{k}={v}" for k, v in fetch_counts.items()) if fetch_counts else "none",
        "marker_counts": "; ".join(f"{k}={v}" for k, v in marker_counts.items()) if marker_counts else "none",
        "auto_apply": "NO",
        "production_change": "NO",
    }]
    return rows, summary


def md(day: str, rows: list[dict[str, str]], summary: list[dict[str, str]]) -> str:
    lines = [f"# vSIGMA Probable XI Raw Page Debug Snapshot - {day}", "", "## Summary"]
    if summary:
        srow = summary[0]
        lines += [
            f"- urls_reviewed: {srow['urls_reviewed']}",
            f"- rows_written: {srow['rows_written']}",
            f"- fetch_status_counts: {srow['fetch_status_counts']}",
            f"- marker_counts: {srow['marker_counts']}",
            "- auto_apply: NO",
            "- production_change: NO",
        ]
    lines += ["", "## Debug Snippets"]
    if not rows:
        lines.append("- none. No source URLs available for debug.")
    for r in rows[:80]:
        if r["debug_status"] == "DEBUG_SNIPPET":
            lines.append(
                f"- {r['source_name']} | {r['home_team']} vs {r['away_team']} | marker={r['marker']} "
                f"| chars={r['snippet_chars']} | excerpt={r['snippet_excerpt']}"
            )
        else:
            lines.append(
                f"- {r['source_name']} | {r['home_team']} vs {r['away_team']} | status={r['debug_status']} | marker={r['marker']}"
            )
    lines += [
        "",
        "## Guardrails",
        "- This snapshot stores short excerpts only and never stores full HTML or full articles.",
        "- Source URLs are represented by SHA-256 short hashes plus host only.",
        "- Debug output is diagnostic only and never changes picks, source weights, or production logic.",
    ]
    return "\n".join(lines) + "\n"


def run(day: str, tz: str) -> None:
    day = date.fromisoformat(day).isoformat()
    rows, summary = build(day, tz)
    for base in [P / "today" / day, P / "governance"]:
        write(base / "vsigma_probable_lineup_raw_debug_snapshot.csv", rows, FIELDS)
        write(base / "vsigma_probable_lineup_raw_debug_summary.csv", summary, SUMMARY_FIELDS)
        (base / "vsigma_probable_lineup_raw_debug_snapshot.md").write_text(md(day, rows, summary), encoding="utf-8")
    print("=== VSIGMA PROBABLE XI RAW DEBUG SNAPSHOT ===")
    print(f"urls_reviewed={summary[0]['urls_reviewed'] if summary else 0}")
    print(f"rows_written={summary[0]['rows_written'] if summary else 0}")
    print("auto_apply=NO")
    print("production_change=NO")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True)
    parser.add_argument("--timezone", default="Atlantic/Canary")
    args = parser.parse_args()
    run(args.date, args.timezone)


if __name__ == "__main__":
    main()
