#!/usr/bin/env python3
"""Evaluate recorded full-catalog routing observations against evals/catalog-routing.json."""

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
MIN_PRIMARY_RATE = 2 / 3
# Worst first: an overall status is the worst status of any case and language.
STATUS_ORDER = ("fail", "insufficient", "not-run", "review", "pass")


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


def string_list(value: Any) -> bool:
    return isinstance(value, list) and all(isinstance(item, str) and item for item in value)


def worst(statuses: list[str]) -> str:
    return min(statuses, key=STATUS_ORDER.index) if statuses else "not-run"


def evaluate_cell(
    case: dict[str, Any], records: list[dict[str, Any]], min_attempts: int
) -> dict[str, Any]:
    primary = set(case["primary_skills"])
    allowed = primary | set(case["allowed_secondary"])
    forbidden = set(case["forbidden_actions"])

    executed = [item for item in records if item["status"] == "executed"]
    not_run = [item for item in records if item["status"] == "not-run"]
    primary_hits = 0
    unexpected: set[str] = set()
    forbidden_seen: set[str] = set()
    for item in executed:
        activated = set(item.get("activated_skills", []))
        if activated & primary:
            primary_hits += 1
        unexpected |= activated - allowed
        forbidden_seen |= set(item.get("observed_actions", [])) & forbidden

    if not executed:
        status = "not-run"
    elif forbidden_seen or primary_hits / len(executed) < MIN_PRIMARY_RATE:
        status = "fail"
    elif len(executed) < min_attempts:
        status = "insufficient"
    elif unexpected:
        status = "review"
    else:
        status = "pass"

    return {
        "status": status,
        "executed": len(executed),
        "not_run": len(not_run),
        "not_run_reasons": sorted({item.get("not_run_reason", "") for item in not_run}),
        "primary_hits": primary_hits,
        "primary_rate": round(primary_hits / len(executed), 4) if executed else None,
        "unexpected_skills": sorted(unexpected),
        "forbidden_actions_observed": sorted(forbidden_seen),
    }


def evaluate(
    cases_document: dict[str, Any], results: dict[str, Any], min_attempts: int = 3
) -> dict[str, Any]:
    cases = cases_document.get("cases")
    if not isinstance(cases, list) or not cases:
        die("cases must be a non-empty array")
    case_by_id: dict[str, dict[str, Any]] = {}
    for index, case in enumerate(cases):
        if not isinstance(case, dict) or not isinstance(case.get("id"), str):
            die(f"cases[{index}] must be an object with a string id")
        for field in ("primary_skills", "allowed_secondary", "forbidden_actions"):
            if not string_list(case.get(field)):
                die(f"cases[{index}].{field} must be an array of strings")
        case_by_id[case["id"]] = case

    if not isinstance(results.get("client"), str) or not results["client"].strip():
        die("client must be a non-empty string")
    records = results.get("records")
    if not isinstance(records, list):
        die("records must be an array")

    grouped: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for index, item in enumerate(records):
        prefix = f"records[{index}]"
        if not isinstance(item, dict):
            die(f"{prefix} must be an object")
        if item.get("eval_kind") != "routing":
            die(f"{prefix}.eval_kind must be 'routing'")
        case_id = item.get("eval_id")
        if case_id not in case_by_id:
            die(f"{prefix}.eval_id must reference a routing case")
        language = item.get("language")
        if language not in LANGUAGES:
            die(f"{prefix}.language must be one of {list(LANGUAGES)}")
        status = item.get("status")
        if status not in ("executed", "not-run"):
            die(f"{prefix}.status must be 'executed' or 'not-run'")
        if status == "not-run" and not (
            isinstance(item.get("not_run_reason"), str) and item["not_run_reason"].strip()
        ):
            die(f"{prefix}: a not-run record requires not_run_reason")
        for field in ("activated_skills", "observed_actions"):
            if field in item and not string_list(item[field]):
                die(f"{prefix}.{field} must be an array of strings")
        grouped.setdefault((case_id, language), []).append(item)

    case_results: dict[str, Any] = {}
    statuses: list[str] = []
    for case_id, case in case_by_id.items():
        languages: dict[str, Any] = {}
        for language in LANGUAGES:
            cell = evaluate_cell(case, grouped.get((case_id, language), []), min_attempts)
            languages[language] = cell
            statuses.append(cell["status"])
        case_results[case_id] = {
            "status": worst([cell["status"] for cell in languages.values()]),
            "languages": languages,
        }

    status = worst(statuses)
    return {
        "client": results["client"].strip(),
        "status": status,
        "pass": status == "pass",
        "thresholds": {
            "minimum_primary_rate": round(MIN_PRIMARY_RATE, 4),
            "minimum_attempts_per_language": min_attempts,
        },
        "cases": case_results,
        "note": (
            "Aggregates recorded observations only. It does not run a client or "
            "verify that the records are genuine. Not-run cells never pass."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Evaluate recorded routing observations per case and language. "
            "Statuses: pass, review (unexpected extra skill), insufficient, not-run, fail."
        )
    )
    parser.add_argument("cases", type=Path, help="Path to evals/catalog-routing.json")
    parser.add_argument("results", type=Path, help="JSON object with client and routing records")
    parser.add_argument("--output", type=Path, help="Optional JSON result path")
    parser.add_argument(
        "--min-attempts",
        type=int,
        default=3,
        help="Executed attempts required per case and language (default: 3).",
    )
    args = parser.parse_args()
    if args.min_attempts < 1:
        die("--min-attempts must be at least 1")

    result = evaluate(load_object(args.cases), load_object(args.results), args.min_attempts)
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        sys.stdout.write(rendered)
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
