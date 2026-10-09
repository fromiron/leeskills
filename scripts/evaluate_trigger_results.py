#!/usr/bin/env python3
"""Evaluate measured Agent Skill trigger results by language."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, NoReturn

# Keep UTF-8 output stable on Windows consoles with legacy code pages.
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8")

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


RUN_STRING_FIELDS = ("client_version", "model", "skill_revision", "installed_catalog")
RUN_NUMBER_FIELDS = ("tokens", "elapsed_seconds")


def validate_run(run: Any) -> dict[str, Any]:
    """Validate optional run metadata without estimating missing values."""
    if not isinstance(run, dict):
        die("run must be an object when present")
    for field in RUN_STRING_FIELDS:
        if field in run and (not isinstance(run[field], str) or not run[field].strip()):
            die(f"run.{field} must be a non-empty string; use 'unknown' when unavailable")
    for field in RUN_NUMBER_FIELDS:
        value = run.get(field)
        if field in run and value is not None and (
            isinstance(value, bool) or not isinstance(value, (int, float)) or value < 0
        ):
            die(f"run.{field} must be a non-negative number or null")
    run_ids = run.get("run_ids")
    if run_ids is not None and (
        not isinstance(run_ids, list)
        or any(not isinstance(item, str) or not item.strip() for item in run_ids)
    ):
        die("run.run_ids must be an array of non-empty strings")
    return run


def evaluate(
    queries: list[dict[str, Any]],
    document: dict[str, Any],
    min_attempts: int = 3,
) -> dict[str, Any]:
    for field in ("client", "skill_name"):
        value = document.get(field)
        if not isinstance(value, str) or not value.strip():
            die(f"{field} must be a non-empty string")
    run = validate_run(document["run"]) if "run" in document else None

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
        if "critical" in query and not isinstance(query["critical"], bool):
            die(f"queries[{index}].critical must be boolean when present")
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

    # Individual failures are reported so that a language average cannot hide them.
    failures: list[dict[str, Any]] = []
    insufficient: list[str] = []
    critical_failed = False
    for query_id in sorted(query_by_id):
        query = query_by_id[query_id]
        measured = result_by_id[query_id]
        rate = measured["triggered"] / measured["attempts"]
        if measured["attempts"] < min_attempts:
            insufficient.append(query_id)
        if query["should_trigger"]:
            failed = rate < MIN_POSITIVE_RATE
        else:
            failed = rate > MAX_NEGATIVE_RATE
        if failed:
            critical = query.get("critical") is True
            critical_failed = critical_failed or critical
            failures.append(
                {
                    "id": query_id,
                    "language": query["language"],
                    "should_trigger": query["should_trigger"],
                    "attempts": measured["attempts"],
                    "triggered": measured["triggered"],
                    "trigger_rate": round(rate, 4),
                    "critical": critical,
                }
            )

    by_language: dict[str, Any] = {}
    rates_pass = True
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
        language_insufficient = any(
            query_by_id[query_id]["language"] == language for query_id in insufficient
        )
        rates_pass = rates_pass and language_pass
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
            "pass": language_pass and not language_insufficient,
            "status": (
                "fail"
                if not language_pass
                else "insufficient"
                if language_insufficient
                else "pass"
            ),
        }

    if not rates_pass or critical_failed:
        status = "fail"
    elif insufficient:
        status = "insufficient"
    else:
        status = "pass"

    result: dict[str, Any] = {
        "client": document["client"].strip(),
        "skill_name": document["skill_name"].strip(),
        "pass": status == "pass",
        "status": status,
        "thresholds": {
            "minimum_positive_trigger_rate": round(MIN_POSITIVE_RATE, 4),
            "maximum_negative_trigger_rate": round(MAX_NEGATIVE_RATE, 4),
            "minimum_attempts_per_query": min_attempts,
        },
        "languages": by_language,
        "failures": failures,
        "insufficient_attempts": insufficient,
    }
    if run is not None:
        result["run"] = run
    return result


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Evaluate measured trigger results for English, Korean, and Japanese."
    )
    parser.add_argument("queries", type=Path, help="Path to trigger_queries.json")
    parser.add_argument("results", type=Path, help="Path to measured trigger results JSON")
    parser.add_argument("--output", type=Path, help="Optional JSON result path")
    parser.add_argument(
        "--min-attempts",
        type=int,
        default=3,
        help=(
            "Attempts required per query before a result can pass (default: 3). "
            "Fewer attempts report status 'insufficient', not a pass."
        ),
    )
    args = parser.parse_args()
    if args.min_attempts < 1:
        die("--min-attempts must be at least 1")

    result = evaluate(
        load_array(args.queries), load_object(args.results), args.min_attempts
    )
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        sys.stdout.write(rendered)
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
