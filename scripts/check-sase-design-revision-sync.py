#!/usr/bin/env python3
"""Fail if SASE-DESIGN.md header Status / Last updated do not match the latest §10 revision row."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DOC = ROOT / "SASE-DESIGN.md"

STATUS_RE = re.compile(
    r"^\|\s*\*\*Status\*\*\s*\|\s*v?([\d.]+)\s",
    re.MULTILINE,
)
LAST_UPDATED_RE = re.compile(
    r"^\|\s*\*\*Last updated\*\*\s*\|\s*(\d{4}-\d{2}-\d{2})\s*\|",
    re.MULTILINE,
)
REVISION_ROW_RE = re.compile(
    r"^\|\s*([\d.]+)\s*\|\s*(\d{4}-\d{2}-\d{2})\s*\|",
)


def version_key(s: str) -> tuple[int, ...]:
    return tuple(int(p) for p in s.split("."))


def parse_latest_revision(text: str) -> tuple[str, str] | None:
    start = text.find("## 10. Revision History")
    if start == -1:
        return None
    section = text[start:]
    rows: list[tuple[str, str]] = []
    for line in section.splitlines():
        line = line.rstrip()
        m = REVISION_ROW_RE.match(line)
        if not m:
            continue
        ver, date = m.group(1), m.group(2)
        if ver == "Version":
            continue
        rows.append((ver, date))
    if not rows:
        return None
    rows.sort(key=lambda r: version_key(r[0]))
    return rows[-1]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "path",
        nargs="?",
        type=Path,
        default=DEFAULT_DOC,
        help=f"Markdown file (default: {DEFAULT_DOC.name})",
    )
    args = ap.parse_args()
    path: Path = args.path
    if not path.is_file():
        print(f"error: file not found: {path}", file=sys.stderr)
        return 2

    text = path.read_text(encoding="utf-8")

    sm = STATUS_RE.search(text)
    lu = LAST_UPDATED_RE.search(text)
    if not sm:
        print("error: could not parse **Status** from metadata table", file=sys.stderr)
        return 2
    if not lu:
        print("error: could not parse **Last updated** from metadata table", file=sys.stderr)
        return 2

    header_ver, header_date = sm.group(1), lu.group(1)
    latest = parse_latest_revision(text)
    if not latest:
        print("error: could not find revision history data rows", file=sys.stderr)
        return 2

    table_ver, table_date = latest
    errors: list[str] = []
    if header_ver != table_ver:
        errors.append(
            f"Version mismatch: header has v{header_ver}, latest §10 row is {table_ver}"
        )
    if header_date != table_date:
        errors.append(
            f"Date mismatch: header Last updated is {header_date}, latest §10 row is {table_date}"
        )

    if errors:
        ver, date = table_ver, table_date
        print(f"{path}:", file=sys.stderr)
        for e in errors:
            print(f"  {e}", file=sys.stderr)
        print(
            f"  Fix: set **Status** to v{ver} and **Last updated** to {date} (or add a revision row first).",
            file=sys.stderr,
        )
        print(
            f"  Expected: | **Status** | v{ver} - … | ; | **Last updated** | {date} |",
            file=sys.stderr,
        )
        return 1

    print(f"OK: header matches latest revision row v{table_ver} ({table_date})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
