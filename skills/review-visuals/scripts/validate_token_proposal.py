#!/usr/bin/env python3
"""Validate a design-token proposal and, optionally, its rendered HTML page.

The JSON check confirms structure, references, evidence for every observed value,
a rationale for every new-system design hypothesis, safe CSS values, and
computable color contrast. The HTML check confirms that no
template placeholders remain and that the page still declares proposal status.
Neither check proves that the values suit the product; render and review them.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, NoReturn

# Keep UTF-8 output stable on Windows consoles with legacy code pages.
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8")

UNKNOWN = "unknown"
FOUNDATIONS = ("color", "typography", "spacing", "layout", "radius")
TYPE_FIELDS = ("font_family", "font_size", "font_weight", "line_height", "letter_spacing")
SEMANTIC_STATUSES = {"proposed", "retained", "unknown"}
CHANGE_ACTIONS = {"merge", "rename", "delete", "retain", "add"}
RELATIONSHIPS = {"shared-contour", "independent", "pill-or-circle"}
DECISION_GROUPS = ("proposed", "retained", "rejected", "open")
MODES = ("normalize", "new-system")
BASES = ("observed", "hypothesis")
LANGUAGES = ("en", "ko", "ja")
QUESTION_BANK = Path(__file__).resolve().parent.parent / "assets" / "token-questions.json"
QUESTION_STAGES = ("approach", "core", "follow-up")
# Four choices fit the structured question tools some clients offer; plain
# text works everywhere.
MAX_OPTIONS = 4
DELEGATE = "delegate"
LAYOUT_DIAGRAMS = ("content-width", "page-padding")
TOKEN_NAME = re.compile(r"^[a-z][a-z0-9]*(?:[-.][a-z0-9]+)*$")
PLACEHOLDER = re.compile(r"\{\{[A-Z0-9_]+\}\}")
# CSS values are written into inline custom properties. Allow plain values only:
# no declarations, blocks, at-rules, escapes, or functions that can load resources.
SAFE_CSS = re.compile(r"^[A-Za-z0-9#%.,+\-*/()\s\"']+$")
UNSAFE_CSS_FUNCTIONS = re.compile(r"(url|image|image-set|cross-fade|element|expression|src)\s*\(", re.I)
HEX_COLOR = re.compile(r"^#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")


def die(message: str) -> NoReturn:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(2)


def read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        die(f"file not found: {path}")
    except json.JSONDecodeError as exc:
        die(f"invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}")
    if not isinstance(data, dict):
        die("top-level value must be an object")
    return data


def non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def load_question_bank(path: Path = QUESTION_BANK) -> dict[str, Any]:
    """Load the guided-proposal question bank and check its structure."""
    bank = read_json(path)
    questions = bank.get("questions")
    if not isinstance(questions, list) or not questions:
        die(f"{path}: questions must be a non-empty array")
    messages = bank.get("messages")
    if not isinstance(messages, dict) or not all(
        isinstance(text, dict) and all(non_empty_string(text.get(lang)) for lang in LANGUAGES)
        for text in messages.values()
    ):
        die(f"{path}: every message needs en, ko, and ja text")
    seen: set[str] = set()
    for index, question in enumerate(questions):
        prefix = f"{path}: questions[{index}]"
        if not isinstance(question, dict) or not non_empty_string(question.get("id")):
            die(f"{prefix} must be an object with an id")
        if question["id"] in seen:
            die(f"{prefix}: duplicate question id {question['id']!r}")
        seen.add(question["id"])
        stage = question.get("stage")
        if stage not in QUESTION_STAGES:
            die(f"{prefix}.stage must be one of {list(QUESTION_STAGES)}")
        texts = [question.get("prompt")]
        if question.get("custom") is not None:
            texts.append(question["custom"])
        options = question.get("options")
        if not isinstance(options, list):
            die(f"{prefix}.options must be an array")
        option_ids = []
        for option in options:
            if not isinstance(option, dict) or not non_empty_string(option.get("id")):
                die(f"{prefix}: every option needs an id")
            option_ids.append(option["id"])
            texts.append(option.get("label"))
        if len(set(option_ids)) != len(option_ids) or "custom" in option_ids:
            die(f"{prefix}: option ids must be unique and must not be 'custom'")
        for text in texts:
            if not isinstance(text, dict) or not all(non_empty_string(text.get(lang)) for lang in LANGUAGES):
                die(f"{prefix}: every prompt, label, and custom hint needs en, ko, and ja text")
        if stage == "core" and (len(options) > MAX_OPTIONS or not options or option_ids[-1] != DELEGATE):
            die(f"{prefix}: a core question has at most {MAX_OPTIONS} options ending with {DELEGATE!r}")
        if stage == "follow-up" and (options or question.get("custom") is None):
            die(f"{prefix}: a follow-up question takes a written answer and has no options")
        if stage == "approach" and len(options) < 2:
            die(f"{prefix}: the approach question needs at least two options")
    core = {question["id"] for question in questions if question["stage"] == "core"}
    for question in questions:
        if question["stage"] == "follow-up" and question.get("after") not in core:
            die(f"{path}: follow-up {question['id']!r} must follow a core question")
    return bank


def string_list(value: Any) -> bool:
    return isinstance(value, list) and all(non_empty_string(item) for item in value)


def css_value_error(value: str) -> str | None:
    if value == UNKNOWN:
        return None
    if not SAFE_CSS.match(value) or UNSAFE_CSS_FUNCTIONS.search(value):
        return "contains characters or functions that are not allowed in a token value"
    return None


def relative_luminance(hex_color: str) -> float:
    digits = hex_color.lstrip("#")
    if len(digits) == 3:
        digits = "".join(char * 2 for char in digits)
    channels = []
    for index in (0, 2, 4):
        channel = int(digits[index:index + 2], 16) / 255
        channels.append(channel / 12.92 if channel <= 0.04045 else ((channel + 0.055) / 1.055) ** 2.4)
    return 0.2126 * channels[0] + 0.7152 * channels[1] + 0.0722 * channels[2]


def contrast_ratio(first: str, second: str) -> float:
    lighter, darker = sorted((relative_luminance(first), relative_luminance(second)), reverse=True)
    return round((lighter + 0.05) / (darker + 0.05), 2)


def resolve_color(name: str, primitives: dict[str, Any], semantic: dict[str, Any]) -> str | None:
    """Return a hex value for a primitive or a semantic token's default mapping."""
    if name in semantic:
        references = semantic[name].get("references")
        if isinstance(references, dict):
            name = references.get("default") or next(iter(references.values()), "")
    value = primitives.get(name)
    if isinstance(value, str) and HEX_COLOR.match(value):
        return value
    return None


def check_basis(
    item: dict[str, Any],
    prefix: str,
    label: str,
    stated: bool,
    mode: str,
    errors: list[str],
    hypotheses: list[str],
) -> None:
    """Observed values need evidence; design hypotheses need a rationale."""
    basis = item.get("basis", "observed")
    if basis not in BASES:
        errors.append(f"{prefix}.basis must be one of {list(BASES)}")
        return
    evidence = item.get("evidence", [])
    if not string_list(evidence):
        errors.append(f"{prefix}.evidence must be an array of strings")
        return
    if basis == "hypothesis":
        if mode != "new-system":
            errors.append(
                f"{prefix}: a design hypothesis is only allowed in new-system mode; "
                "normalizing an existing system requires observed evidence"
            )
        if not non_empty_string(item.get("rationale")):
            errors.append(f"{prefix}: a design hypothesis requires a rationale")
        if stated:
            hypotheses.append(label)
    elif stated and not evidence:
        errors.append(f"{prefix}: a stated value requires evidence; use {UNKNOWN!r} otherwise")


def validate(data: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    unknown_values: list[str] = []
    hypotheses: list[str] = []
    contrast: list[dict[str, Any]] = []

    mode = data.get("mode", "normalize")
    if mode not in MODES:
        errors.append(f"mode must be one of {list(MODES)}")
        mode = "normalize"

    for field in ("project", "language", "title", "summary", "prepared"):
        if not non_empty_string(data.get(field)):
            errors.append(f"{field} must be a non-empty string")
    if data.get("status") != "proposed":
        errors.append('status must be "proposed"; adoption is recorded by project owners, not by this file')
    if not string_list(data.get("evidence_basis")) or not data.get("evidence_basis"):
        errors.append("evidence_basis must be a non-empty array of strings")

    breakpoints = data.get("breakpoints", [])
    breakpoint_names: set[str] = set()
    if not isinstance(breakpoints, list):
        errors.append("breakpoints must be an array")
        breakpoints = []
    for index, item in enumerate(breakpoints):
        prefix = f"breakpoints[{index}]"
        if not isinstance(item, dict) or not non_empty_string(item.get("name")):
            errors.append(f"{prefix} must be an object with a name")
            continue
        breakpoint_names.add(item["name"])
        min_width = item.get("min_width")
        if not non_empty_string(min_width):
            errors.append(f"{prefix}.min_width must be a string or {UNKNOWN!r}")
        elif min_width == UNKNOWN:
            unknown_values.append(f"{prefix}.min_width")
        elif item.get("basis", "observed") == "observed" and (
            not string_list(item.get("evidence")) or not item.get("evidence")
        ):
            errors.append(f"{prefix}: a stated min_width requires evidence")
        else:
            check_basis(
                item, prefix, f"{item['name']}.min_width", True, mode, errors, hypotheses
            )

    foundations = data.get("foundations")
    if not isinstance(foundations, dict) or not foundations:
        errors.append("foundations must be a non-empty object")
        foundations = {}
    unexpected = sorted(set(foundations) - set(FOUNDATIONS))
    if unexpected:
        errors.append(f"unknown foundations: {', '.join(unexpected)}")

    primitive_values: dict[str, Any] = {}
    primitive_foundation: dict[str, str] = {}
    semantic_tokens: dict[str, dict[str, Any]] = {}
    counts: dict[str, dict[str, int]] = {}

    for foundation in FOUNDATIONS:
        block = foundations.get(foundation)
        if block is None:
            continue
        if not isinstance(block, dict):
            errors.append(f"foundations.{foundation} must be an object")
            continue
        primitives = block.get("primitives", [])
        semantic = block.get("semantic", [])
        if not isinstance(primitives, list) or not isinstance(semantic, list):
            errors.append(f"foundations.{foundation}.primitives and .semantic must be arrays")
            continue
        current: set[str] = set()
        for index, item in enumerate(primitives):
            prefix = f"foundations.{foundation}.primitives[{index}]"
            if not isinstance(item, dict):
                errors.append(f"{prefix} must be an object")
                continue
            name = item.get("name")
            if not isinstance(name, str) or not TOKEN_NAME.match(name):
                errors.append(f"{prefix}.name must be a lowercase token name such as space-4")
                continue
            if name in primitive_values:
                errors.append(f"duplicate primitive name: {name}")
                continue
            value = item.get("value")
            stated = False
            if foundation == "typography":
                if not isinstance(value, dict):
                    errors.append(f"{prefix}.value must be an object with {', '.join(TYPE_FIELDS)}")
                    continue
                for field in TYPE_FIELDS:
                    field_value = value.get(field)
                    if not non_empty_string(field_value):
                        errors.append(f"{prefix}.value.{field} must be a string or {UNKNOWN!r}")
                        continue
                    if field_value == UNKNOWN:
                        unknown_values.append(f"{name}.{field}")
                    else:
                        stated = True
                    problem = css_value_error(field_value)
                    if problem:
                        errors.append(f"{prefix}.value.{field} {problem}")
            else:
                if not non_empty_string(value):
                    errors.append(f"{prefix}.value must be a string or {UNKNOWN!r}")
                    continue
                if value == UNKNOWN:
                    unknown_values.append(name)
                else:
                    stated = True
                problem = css_value_error(value)
                if problem:
                    errors.append(f"{prefix}.value {problem}")
                if foundation == "color" and value != UNKNOWN and not HEX_COLOR.match(value):
                    warnings.append(f"{name}: contrast is computed only for #rgb or #rrggbb values")
            check_basis(item, prefix, name, stated, mode, errors, hypotheses)
            current_values = item.get("current_values", [])
            if not string_list(current_values):
                errors.append(f"{prefix}.current_values must be an array of strings")
            else:
                current.update(current_values)
            primitive_values[name] = value
            primitive_foundation[name] = foundation
        counts[foundation] = {
            "current_values": len(current),
            "primitives": len(primitives),
            "semantic": len(semantic),
        }
        for index, item in enumerate(semantic):
            prefix = f"foundations.{foundation}.semantic[{index}]"
            if not isinstance(item, dict):
                errors.append(f"{prefix} must be an object")
                continue
            name = item.get("name")
            if not isinstance(name, str) or not TOKEN_NAME.match(name):
                errors.append(f"{prefix}.name must be a lowercase token name")
                continue
            if name in semantic_tokens or name in primitive_values:
                errors.append(f"duplicate token name: {name}")
                continue
            item = dict(item, _foundation=foundation, _prefix=prefix)
            semantic_tokens[name] = item
            if not non_empty_string(item.get("role")):
                errors.append(f"{prefix}.role must be a non-empty string")
            if item.get("status") not in SEMANTIC_STATUSES:
                errors.append(f"{prefix}.status must be one of {sorted(SEMANTIC_STATUSES)}")
            references = item.get("references")
            if not isinstance(references, dict) or not references:
                errors.append(f"{prefix}.references must map a context (default, a breakpoint, language, or theme) to a primitive")
            if foundation == "radius":
                relationship = item.get("relationship")
                if relationship not in RELATIONSHIPS:
                    errors.append(f"{prefix}.relationship must be one of {sorted(RELATIONSHIPS)}")
            if foundation == "layout":
                if not non_empty_string(item.get("owner")):
                    errors.append(f"{prefix}.owner must name the container that owns the value")
                if item.get("diagram") not in (None, *LAYOUT_DIAGRAMS):
                    errors.append(f"{prefix}.diagram must be one of {sorted(LAYOUT_DIAGRAMS)}")

    color_primitives = {
        name: value for name, value in primitive_values.items() if primitive_foundation[name] == "color"
    }
    color_semantic = {
        name: item for name, item in semantic_tokens.items() if item["_foundation"] == "color"
    }
    for name, item in semantic_tokens.items():
        prefix = item["_prefix"]
        references = item.get("references")
        if not isinstance(references, dict):
            continue
        for context, target in references.items():
            if target == UNKNOWN:
                unknown_values.append(f"{name}@{context}")
                continue
            if target not in primitive_values:
                errors.append(f"{prefix}.references.{context} points to unknown primitive {target!r}")
                continue
            if item["_foundation"] != "layout" and primitive_foundation[target] != item["_foundation"]:
                errors.append(f"{prefix}.references.{context} must point to a {item['_foundation']} primitive")
            if breakpoint_names and context not in breakpoint_names and context != "default":
                # Languages and themes are valid contexts; only flag likely breakpoint typos.
                if context in {"wide", "medium", "narrow", "desktop", "tablet", "mobile"}:
                    warnings.append(f"{prefix}.references.{context} is not a declared breakpoint")
        check = item.get("contrast")
        if check is None:
            continue
        if item["_foundation"] != "color" or not isinstance(check, dict):
            errors.append(f"{prefix}.contrast is only valid on color semantic tokens as an object")
            continue
        against = check.get("against")
        minimum = check.get("minimum")
        if not isinstance(minimum, (int, float)) or minimum <= 1:
            errors.append(f"{prefix}.contrast.minimum must be a number greater than 1")
            continue
        foreground = resolve_color(name, color_primitives, color_semantic)
        background = resolve_color(against, color_primitives, color_semantic) if isinstance(against, str) else None
        if not isinstance(against, str) or (against not in color_primitives and against not in color_semantic):
            errors.append(f"{prefix}.contrast.against must name a color token")
            continue
        if foreground is None or background is None:
            contrast.append({"token": name, "against": against, "ratio": None, "minimum": minimum, "status": "unknown"})
            unknown_values.append(f"{name} contrast")
            continue
        ratio = contrast_ratio(foreground, background)
        passed = ratio >= minimum
        contrast.append({
            "token": name, "against": against, "ratio": ratio, "minimum": minimum,
            "status": "pass" if passed else "fail",
        })
        if not passed:
            errors.append(f"{name} on {against}: contrast {ratio}:1 is below the declared {minimum}:1")

    naming = data.get("naming", {})
    if not isinstance(naming, dict):
        errors.append("naming must be an object")
        naming = {}
    for kind, spec in naming.items():
        prefix = f"naming.{kind}"
        if kind not in {"primitive", "semantic"} or not isinstance(spec, dict):
            errors.append(f"{prefix} must be a primitive or semantic naming object")
            continue
        parts = spec.get("parts")
        if not isinstance(parts, list) or not parts or not all(
            isinstance(part, dict) and non_empty_string(part.get("text")) and non_empty_string(part.get("label"))
            for part in parts
        ):
            errors.append(f"{prefix}.parts must be a non-empty array of {{text, label}} objects")
        if "separator" in spec and not isinstance(spec["separator"], str):
            errors.append(f"{prefix}.separator must be a string")

    for field in ("specimen_text",):
        if field in data and not non_empty_string(data[field]):
            errors.append(f"{field} must be a non-empty string when present")

    changes = data.get("changes")
    if not isinstance(changes, list):
        errors.append("changes must be an array")
        changes = []
    all_names = set(primitive_values) | set(semantic_tokens)
    for index, change in enumerate(changes):
        prefix = f"changes[{index}]"
        if not isinstance(change, dict):
            errors.append(f"{prefix} must be an object")
            continue
        if not non_empty_string(change.get("current")):
            errors.append(f"{prefix}.current must name the current value or alias")
        action = change.get("action")
        if action not in CHANGE_ACTIONS:
            errors.append(f"{prefix}.action must be one of {sorted(CHANGE_ACTIONS)}")
        proposed = change.get("proposed")
        if action == "delete":
            if proposed not in (None, ""):
                errors.append(f"{prefix}: a deletion must not name a proposed token")
        elif proposed not in all_names:
            errors.append(f"{prefix}.proposed must name a token defined in foundations")
        if not string_list(change.get("evidence")) or not change.get("evidence"):
            errors.append(f"{prefix}.evidence must be a non-empty array of strings")

    decisions = data.get("decisions")
    if not isinstance(decisions, dict):
        errors.append("decisions must be an object")
    else:
        for group in DECISION_GROUPS:
            if not string_list(decisions.get(group, [])):
                errors.append(f"decisions.{group} must be an array of strings")

    return {
        "valid": not errors,
        "mode": mode,
        "errors": errors,
        "warnings": warnings,
        "foundation_counts": counts,
        "unknown_values": sorted(set(unknown_values)),
        "hypothesis_values": sorted(set(hypotheses)),
        "contrast": contrast,
    }


class _PageScan(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.lang = ""
        self.title = ""
        self.status = ""
        self._in_title = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        if tag == "html":
            self.lang = attributes.get("lang") or ""
        elif tag == "body":
            self.status = attributes.get("data-proposal-status") or ""
        elif tag == "title":
            self._in_title = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title += data


def validate_html(text: str) -> dict[str, Any]:
    errors: list[str] = []
    placeholders = sorted(set(PLACEHOLDER.findall(text)))
    if placeholders:
        errors.append(f"{len(placeholders)} unresolved placeholder(s): {', '.join(placeholders[:10])}")
    scan = _PageScan()
    scan.feed(text)
    if not re.match(r"^[A-Za-z]{2,3}(?:-[A-Za-z0-9]{2,8})*$", scan.lang):
        errors.append("<html lang> must be a valid language tag")
    if not scan.title.strip():
        errors.append("<title> must not be empty")
    if scan.status != "proposed":
        errors.append('<body data-proposal-status="proposed"> is required until owners adopt the tokens')
    if re.search(r"<(?:link|script|img|iframe)[^>]+(?:src|href)\s*=\s*[\"']?(?:https?:)?//", text, re.I):
        errors.append("the page must not load external resources")
    return {"valid": not errors, "errors": errors, "placeholders": placeholders}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate a design-token proposal JSON file and optionally its HTML page.",
    )
    parser.add_argument("input", type=Path, nargs="?", help="Path to token proposal JSON")
    parser.add_argument("--html", type=Path, help="Rendered or hand-filled proposal page to check")
    parser.add_argument("--output", type=Path, help="Optional JSON result path")
    args = parser.parse_args()
    if args.input is None and args.html is None:
        parser.error("provide a proposal JSON file, --html, or both")
    return args


def main() -> int:
    args = parse_args()
    result: dict[str, Any] = {}
    valid = True
    if args.input is not None:
        result["proposal"] = validate(read_json(args.input))
        valid = valid and result["proposal"]["valid"]
    if args.html is not None:
        try:
            text = args.html.read_text(encoding="utf-8")
        except FileNotFoundError:
            die(f"file not found: {args.html}")
        result["html"] = validate_html(text)
        hypotheses = result.get("proposal", {}).get("hypothesis_values", [])
        marked = len(re.findall(r'data-basis="hypothesis"', text))
        if hypotheses and marked < len(hypotheses):
            result["html"]["errors"].append(
                f"{len(hypotheses)} design hypothesis value(s) but only {marked} "
                'data-basis="hypothesis" marker(s) in the page'
            )
            result["html"]["valid"] = False
        valid = valid and result["html"]["valid"]
    result = {"valid": valid, **result}
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        sys.stdout.write(rendered)
    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
