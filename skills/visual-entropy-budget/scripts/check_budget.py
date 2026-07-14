#!/usr/bin/env python3
"""Check a visual-entropy budget JSON document."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, NoReturn

DEFAULT_LIMITS = {
    "layout_grammars": 1,
    "typeface_families": 1,
    "type_roles": 6,
    "accent_colors": 1,
    "radius_tokens": 2,
    "shadow_levels": 1,
    "surface_styles": 3,
    "primary_cta_styles": 1,
    "secondary_cta_styles": 1,
    "motion_patterns": 2,
    "decorative_image_families": 0,
}


def die(message: str) -> NoReturn:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(2)


def load(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        die(f"file not found: {path}")
    except json.JSONDecodeError as exc:
        die(f"invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}")
    if not isinstance(data, dict):
        die("top-level JSON value must be an object")
    return data


def as_count_map(value: Any, field: str) -> dict[str, int]:
    if not isinstance(value, dict):
        die(f"{field} must be an object")
    result: dict[str, int] = {}
    for key, count in value.items():
        if not isinstance(key, str):
            die(f"{field} keys must be strings")
        if not isinstance(count, int) or isinstance(count, bool) or count < 0:
            die(f"{field}.{key} must be a non-negative integer")
        result[key] = count
    return result


def check(data: dict[str, Any]) -> dict[str, Any]:
    artifact = data.get("artifact")
    if not isinstance(artifact, str) or not artifact.strip():
        die("artifact must be a non-empty string")

    observed = as_count_map(data.get("observed"), "observed")
    limits_value = data.get("limits")
    limits = as_count_map(limits_value, "limits")

    missing_core_limits = sorted(set(DEFAULT_LIMITS) - set(limits))
    if missing_core_limits:
        die("limits missing core metrics: " + ", ".join(missing_core_limits))

    missing_observed = sorted(set(limits) - set(observed))
    extra_observed = sorted(set(observed) - set(limits))
    if missing_observed:
        die("observed missing metrics: " + ", ".join(missing_observed))
    if extra_observed:
        die("observed metrics missing limits: " + ", ".join(extra_observed))

    exceptions_value = data.get("exceptions", [])
    if not isinstance(exceptions_value, list):
        die("exceptions must be an array")

    exceptions: dict[str, dict[str, str]] = {}
    for index, item in enumerate(exceptions_value):
        if not isinstance(item, dict):
            die(f"exceptions[{index}] must be an object")
        metric = item.get("metric")
        reason = item.get("reason")
        evidence = item.get("evidence")
        if not all(isinstance(x, str) and x.strip() for x in (metric, reason, evidence)):
            die(f"exceptions[{index}] requires non-empty metric, reason, and evidence")
        if metric in exceptions:
            die(f"duplicate exception metric: {metric}")
        exceptions[metric] = {
            "reason": reason.strip(),
            "evidence": evidence.strip(),
        }

    results: dict[str, Any] = {}
    unresolved = 0
    documented = 0

    for metric, limit in limits.items():
        count = observed[metric]
        overage = max(0, count - limit)
        exception = exceptions.get(metric)
        if overage == 0:
            status = "within-budget"
        elif exception:
            status = "documented-exception"
            documented += 1
        else:
            status = "over-budget"
            unresolved += 1
        results[metric] = {
            "observed": count,
            "limit": limit,
            "overage": overage,
            "status": status,
            "exception": exception,
        }

    unused_exceptions = sorted(set(exceptions) - set(limits))
    review_required = documented > 0
    passed = unresolved == 0 and not review_required
    if unresolved:
        budget_status = "fail"
    elif review_required:
        budget_status = "review-required"
    else:
        budget_status = "pass"

    return {
        "artifact": artifact.strip(),
        "pass": passed,
        "budget_status": budget_status,
        "review_required": review_required,
        "unresolved_overages": unresolved,
        "documented_exceptions": documented,
        "unused_exceptions": unused_exceptions,
        "metrics": results,
        "note": "Documented exceptions still require human review.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Check a visual entropy budget.")
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = check(load(args.input))
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        sys.stdout.write(rendered)
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
