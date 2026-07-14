#!/usr/bin/env python3
"""Evaluate measured Agent Skill trigger results by language."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, NoReturn

LANGUAGES = ("en", "ko", "ja")
MIN_POSITIVE_RATE = 2 / 3
MAX_NEGATIVE_RATE = 1 / 3


def die(message: str) -> NoReturn:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(2)


def load_object(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        die(f"file not found: {path}")
    except json.JSONDecodeError as exc:
        die(f"invalid JSON {path}:{exc.lineno}:{exc.colno}: {exc.msg}")
    if not isinstance(value, dict):
        die(f"{path}: top-level value must be an object")
    return value


def load_array(path: Path) -> list[dict[str, Any]]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        die(f"file not found: {path}")
    except json.JSONDecodeError as exc:
        die(f"invalid JSON {path}:{exc.lineno}:{exc.colno}: {exc.msg}")
    if not isinstance(value, list) or any(not isinstance(item, dict) for item in value):
        die(f"{path}: top-level value must be an array of objects")
    return value


def evaluate(queries: list[dict[str, Any]], document: dict[str, Any]) -> dict[str, Any]:
    for field in ("client", "skill_name"):
        value = document.get(field)
        if not isinstance(value, str) or not value.strip():
            die(f"{field} must be a non-empty string")

    query_by_id: dict[str, dict[str, Any]] = {}
    for index, query in enumerate(queries):
        query_id = query.get("id")
        if not isinstance(query_id, str) or not query_id:
            die(f"queries[{index}].id must be a non-empty string")
        if query_id in query_by_id:
            die(f"duplicate query id: {query_id}")
        if query.get("language") not in LANGUAGES:
            die(f"queries[{index}].language must be one of {list(LANGUAGES)}")
        if not isinstance(query.get("should_trigger"), bool):
            die(f"queries[{index}].should_trigger must be boolean")
        query_by_id[query_id] = query

    runs = document.get("results")
    if not isinstance(runs, list) or any(not isinstance(item, dict) for item in runs):
        die("results must be an array of objects")

    result_by_id: dict[str, dict[str, Any]] = {}
    for index, item in enumerate(runs):
        query_id = item.get("id")
        if not isinstance(query_id, str) or query_id not in query_by_id:
            die(f"results[{index}].id must reference a query id")
        if query_id in result_by_id:
            die(f"duplicate result id: {query_id}")
        attempts = item.get("attempts")
        triggered = item.get("triggered")
        if not isinstance(attempts, int) or isinstance(attempts, bool) or attempts < 1:
            die(f"results[{index}].attempts must be a positive integer")
        if (
            not isinstance(triggered, int)
            or isinstance(triggered, bool)
            or triggered < 0
            or triggered > attempts
        ):
            die(f"results[{index}].triggered must be between 0 and attempts")
        result_by_id[query_id] = item

    missing = sorted(set(query_by_id) - set(result_by_id))
    extra = sorted(set(result_by_id) - set(query_by_id))
    if missing:
        die("results missing query ids: " + ", ".join(missing))
    if extra:
        die("results contain unknown query ids: " + ", ".join(extra))

    by_language: dict[str, Any] = {}
    passed = True
    for language in LANGUAGES:
        positive_attempts = 0
        positive_triggers = 0
        negative_attempts = 0
        negative_triggers = 0
        for query_id, query in query_by_id.items():
            if query["language"] != language:
                continue
            measured = result_by_id[query_id]
            if query["should_trigger"]:
                positive_attempts += measured["attempts"]
                positive_triggers += measured["triggered"]
            else:
                negative_attempts += measured["attempts"]
                negative_triggers += measured["triggered"]

        if positive_attempts == 0 or negative_attempts == 0:
            die(f"language {language!r} requires positive and negative measurements")
        positive_rate = positive_triggers / positive_attempts
        negative_rate = negative_triggers / negative_attempts
        language_pass = (
            positive_rate >= MIN_POSITIVE_RATE and negative_rate <= MAX_NEGATIVE_RATE
        )
        passed = passed and language_pass
        by_language[language] = {
            "positive": {
                "attempts": positive_attempts,
                "triggers": positive_triggers,
                "trigger_rate": round(positive_rate, 4),
            },
            "negative": {
                "attempts": negative_attempts,
                "triggers": negative_triggers,
                "false_trigger_rate": round(negative_rate, 4),
            },
            "pass": language_pass,
        }

    return {
        "client": document["client"].strip(),
        "skill_name": document["skill_name"].strip(),
        "pass": passed,
        "thresholds": {
            "minimum_positive_trigger_rate": round(MIN_POSITIVE_RATE, 4),
            "maximum_negative_trigger_rate": round(MAX_NEGATIVE_RATE, 4),
        },
        "languages": by_language,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Evaluate measured trigger results for English, Korean, and Japanese."
    )
    parser.add_argument("queries", type=Path, help="Path to trigger_queries.json")
    parser.add_argument("results", type=Path, help="Path to measured trigger results JSON")
    parser.add_argument("--output", type=Path, help="Optional JSON result path")
    args = parser.parse_args()

    result = evaluate(load_array(args.queries), load_object(args.results))
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        sys.stdout.write(rendered)
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
