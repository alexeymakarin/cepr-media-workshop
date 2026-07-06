#!/usr/bin/env python3
"""Extract participant names + affiliations from a workshop spreadsheet.

Prints "Name\tAffiliation" lines to stdout and NOTHING else. Never writes
files. Aborts if any output line would contain an email address, so it is
impossible to leak contact data into the public website by piping this out.

Usage:
    python3 extract_participants.py <file.xlsx> --name-col NAME --aff-col AFF
        [--first-col FIRST --last-col LAST] [--status-col STATUS]
        [--sheet SHEET]

Column arguments are header names (case-insensitive). Rows whose status
column contains "declined" or "cancel" are skipped.
"""

import argparse
import sys

import openpyxl


def fail(msg):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--sheet", default=None)
    ap.add_argument("--name-col", default=None)
    ap.add_argument("--first-col", default=None)
    ap.add_argument("--last-col", default=None)
    ap.add_argument("--aff-col", required=True)
    ap.add_argument("--status-col", default=None)
    args = ap.parse_args()

    wb = openpyxl.load_workbook(args.path, read_only=True, data_only=True)
    ws = wb[args.sheet] if args.sheet else wb.worksheets[0]
    rows = list(ws.iter_rows(values_only=True))
    wb.close()
    if not rows:
        fail("empty sheet")

    header = [str(c).strip().lower() if c is not None else "" for c in rows[0]]

    def col(name):
        if name is None:
            return None
        key = name.strip().lower()
        for i, h in enumerate(header):
            if h.startswith(key):
                return i
        fail(f"column {name!r} not found in header {header}")

    i_name, i_first, i_last = col(args.name_col), col(args.first_col), col(args.last_col)
    i_aff, i_status = col(args.aff_col), col(args.status_col)
    if i_name is None and (i_first is None or i_last is None):
        fail("need --name-col or both --first-col/--last-col")

    out = []
    for row in rows[1:]:
        def get(i):
            v = row[i] if i is not None and i < len(row) else None
            return str(v).strip() if v is not None else ""

        name = get(i_name) if i_name is not None else f"{get(i_first)} {get(i_last)}".strip()
        aff = get(i_aff)
        if not name:
            continue
        if i_status is not None and any(s in get(i_status).lower() for s in ("declined", "cancel")):
            continue
        out.append(f"{name}\t{aff}")

    joined = "\n".join(out)
    if "@" in joined:
        fail("output contains an email address — refusing to print")
    print(joined)


if __name__ == "__main__":
    main()
