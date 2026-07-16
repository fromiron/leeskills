#!/usr/bin/env python3
"""Flag generic phrase patterns and claims that require evidence review."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, NoReturn

# Keep UTF-8 output stable on Windows consoles with legacy code pages.
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8")


def die(message: str) -> NoReturn:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(2)


def load_watchlist() -> list[dict[str, str]]:
    path = Path(__file__).resolve().parent.parent / "references" / "phrase-watchlist.txt"
    entries: list[dict[str, str]] = []
    for number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split("|")
        if len(parts) != 3:
            die(f"invalid watchlist line {number}: expected language|phrase|category")
        language, phrase, category = (part.strip() for part in parts)
        entries.append({"language": language, "phrase": phrase, "category": category})
    return entries


def line_col(text: str, offset: int) -> tuple[int, int]:
    line = text.count("\n", 0, offset) + 1
    last_break = text.rfind("\n", 0, offset)
    column = offset + 1 if last_break == -1 else offset - last_break
    return line, column


def scan(text: str) -> dict[str, Any]:
    findings: list[dict[str, Any]] = []
    lowered = text.casefold()

    for entry in load_watchlist():
        needle = entry["phrase"].casefold()
        start = 0
        while True:
            index = lowered.find(needle, start)
            if index == -1:
                break
            line, column = line_col(text, index)
            findings.append({
                "type": "watchlist-phrase",
                "language": entry["language"],
                "category": entry["category"],
                "match": text[index:index + len(entry["phrase"])],
                "line": line,
                "column": column,
                "action": "Review context and replace with a supported mechanism, constraint, or outcome when possible.",
            })
            start = index + max(1, len(needle))

    numeric_pattern = re.compile(
        r"(?<!\w)(?:\d+(?:[.,]\d+)?%|\$[0-9][0-9,]*(?:\.[0-9]+)?|"
        r"€[0-9][0-9.,]*|£[0-9][0-9.,]*|¥[0-9][0-9,]*|"
        r"\d+(?:[.,]\d+)?\s*(?:x|times|hours?|days?|users?|customers?))(?!\w)",
        re.IGNORECASE,
    )
    for match in numeric_pattern.finditer(text):
        line, column = line_col(text, match.start())
        findings.append({
            "type": "numeric-claim",
            "category": "evidence-required",
            "match": match.group(0),
            "line": line,
            "column": column,
            "action": "Verify the number, date, scope, and source. A match is not evidence that the claim is false.",
        })

    universal_pattern = re.compile(
        r"\b(always|never|everyone|every team|all users|guaranteed|#1|number one)\b",
        re.IGNORECASE,
    )
    for match in universal_pattern.finditer(text):
        line, column = line_col(text, match.start())
        findings.append({
            "type": "universal-claim",
            "category": "scope-claim",
            "match": match.group(0),
            "line": line,
            "column": column,
            "action": "Check whether the universal scope is directly supported.",
        })

    findings.sort(key=lambda item: (item["line"], item["column"], item["type"]))
    return {
        "finding_count": len(findings),
        "findings": findings,
        "note": (
            "Matches are review prompts, not automatic failures. Determine support "
            "from the grounded content inventory."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Flag generic marketing phrases and evidence-sensitive claims."
    )
    parser.add_argument(
        "input",
        nargs="?",
        type=Path,
        help="Text or Markdown file. Reads stdin when omitted.",
    )
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    if args.input:
        try:
            text = args.input.read_text(encoding="utf-8")
        except FileNotFoundError:
            die(f"file not found: {args.input}")
    else:
        text = sys.stdin.read()

    result = scan(text)
    if args.format == "json":
        rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    else:
        lines = [f"{result['finding_count']} review item(s)"]
        for item in result["findings"]:
            lines.append(
                f"{item['line']}:{item['column']} "
                f"[{item['category']}] {item['match']!r} — {item['action']}"
            )
        lines.append(result["note"])
        rendered = "\n".join(lines) + "\n"

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        sys.stdout.write(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
