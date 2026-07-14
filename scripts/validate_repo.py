#!/usr/bin/env python3
"""Validate repository structure, portable skill metadata, fixtures, and scripts."""

from __future__ import annotations

import argparse
import ast
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Iterable, NoReturn

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
TRIGGER_ID_RE = re.compile(r"^(en|ko|ja)-(positive|negative)-[1-9][0-9]*$")
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
PROJECT_NAME = "leeskills"
TRIGGER_LANGUAGES = {"en", "ko", "ja"}
FORBIDDEN_NETWORK_MODULES = {
    "aiohttp",
    "ftplib",
    "http.client",
    "httpx",
    "requests",
    "smtplib",
    "socket",
    "urllib.request",
}


def die(message: str) -> NoReturn:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(2)


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise ValueError(f"missing file: {path}")
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"invalid JSON {path}:{exc.lineno}:{exc.colno}: {exc.msg}"
        ) from exc


def parse_frontmatter(path: Path) -> tuple[dict[str, str], int]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError(f"{path}: SKILL.md must start with YAML frontmatter")
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration as exc:
        raise ValueError(f"{path}: unterminated YAML frontmatter") from exc

    values: dict[str, str] = {}
    for number, raw in enumerate(lines[1:end], start=2):
        if not raw.strip() or raw[0].isspace() or raw.lstrip().startswith("#"):
            continue
        if ":" not in raw:
            raise ValueError(f"{path}:{number}: invalid top-level frontmatter line")
        key, value = raw.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value.startswith(("'", '"')) and value.endswith(("'", '"')) and len(value) >= 2:
            value = value[1:-1]
        values[key] = value
    return values, len(lines)


def is_within(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def iter_markdown_links(text: str) -> Iterable[str]:
    for match in MARKDOWN_LINK_RE.finditer(text):
        raw = match.group(1).strip()
        if raw.startswith("<") and ">" in raw:
            raw = raw[1:raw.index(">")]
        elif " " in raw:
            raw = raw.split(" ", 1)[0]
        yield raw


def imported_modules(tree: ast.AST) -> set[str]:
    modules: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            modules.add(node.module)
    return modules


def check_script(path: Path, errors: list[str], warnings: list[str]) -> None:
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
        # Reject syntax introduced after the declared Python 3.9 minimum.
        ast.parse(source, filename=str(path), feature_version=9)
        compile(source, str(path), "exec")
    except (SyntaxError, UnicodeDecodeError) as exc:
        errors.append(f"{path}: Python parse/compile failure: {exc}")
        return

    imported = imported_modules(tree)
    forbidden = sorted(
        module
        for module in imported
        if any(module == item or module.startswith(item + ".") for item in FORBIDDEN_NETWORK_MODULES)
    )
    if forbidden:
        errors.append(f"{path}: forbidden network imports: {', '.join(forbidden)}")

    if not source.startswith("#!/usr/bin/env python3"):
        warnings.append(f"{path}: missing portable Python shebang")


def validate_evals(skill_dir: Path, skill_name: str, errors: list[str]) -> None:
    output_path = skill_dir / "evals" / "evals.json"
    trigger_path = skill_dir / "evals" / "trigger_queries.json"

    try:
        output = load_json(output_path)
        if not isinstance(output, dict):
            raise ValueError(f"{output_path}: top-level value must be an object")
        if output.get("skill_name") != skill_name:
            errors.append(f"{output_path}: skill_name must be {skill_name!r}")
        evals = output.get("evals")
        if not isinstance(evals, list) or not evals:
            errors.append(f"{output_path}: evals must be a non-empty array")
        else:
            ids: set[str] = set()
            for index, item in enumerate(evals):
                prefix = f"{output_path}:evals[{index}]"
                if not isinstance(item, dict):
                    errors.append(f"{prefix}: must be an object")
                    continue
                eval_id = item.get("id")
                if not isinstance(eval_id, str) or not eval_id.strip():
                    errors.append(f"{prefix}: id must be a non-empty string")
                elif eval_id in ids:
                    errors.append(f"{prefix}: duplicate id {eval_id!r}")
                else:
                    ids.add(eval_id)
                for field in ("prompt", "expected_output"):
                    if not isinstance(item.get(field), str) or not item[field].strip():
                        errors.append(f"{prefix}: {field} must be a non-empty string")
                assertions = item.get("assertions")
                if not isinstance(assertions, list) or not assertions or any(
                    not isinstance(value, str) or not value.strip() for value in assertions
                ):
                    errors.append(f"{prefix}: assertions must contain non-empty strings")
    except ValueError as exc:
        errors.append(str(exc))

    try:
        triggers = load_json(trigger_path)
        if not isinstance(triggers, list) or not triggers:
            errors.append(f"{trigger_path}: must be a non-empty array")
            return
        counts = {
            language: {"positive": 0, "negative": 0}
            for language in sorted(TRIGGER_LANGUAGES)
        }
        ids: set[str] = set()
        queries: set[str] = set()
        for index, item in enumerate(triggers):
            prefix = f"{trigger_path}[{index}]"
            if not isinstance(item, dict):
                errors.append(f"{prefix}: must be an object")
                continue
            query = item.get("query")
            should = item.get("should_trigger")
            trigger_id = item.get("id")
            language = item.get("language")
            if not isinstance(trigger_id, str) or not TRIGGER_ID_RE.fullmatch(trigger_id):
                errors.append(
                    f"{prefix}: id must match en|ko|ja-positive|negative-N"
                )
            elif trigger_id in ids:
                errors.append(f"{prefix}: duplicate id {trigger_id!r}")
            else:
                ids.add(trigger_id)
            if language not in TRIGGER_LANGUAGES:
                errors.append(
                    f"{prefix}: language must be one of {sorted(TRIGGER_LANGUAGES)}"
                )
            if not isinstance(query, str) or not query.strip():
                errors.append(f"{prefix}: query must be a non-empty string")
            elif query in queries:
                errors.append(f"{prefix}: duplicate query")
            else:
                queries.add(query)
            if not isinstance(should, bool):
                errors.append(f"{prefix}: should_trigger must be boolean")
            else:
                polarity = "positive" if should else "negative"
                if language in counts:
                    counts[language][polarity] += 1
                if isinstance(trigger_id, str) and TRIGGER_ID_RE.fullmatch(trigger_id):
                    id_language, id_polarity, _ = trigger_id.split("-", 2)
                    if id_language != language or id_polarity != polarity:
                        errors.append(
                            f"{prefix}: id language and polarity must match the record"
                        )
        for language, language_counts in counts.items():
            if language_counts["positive"] < 2 or language_counts["negative"] < 2:
                errors.append(
                    f"{trigger_path}: language {language!r} must include at least "
                    "two positive and two near-miss negative prompts"
                )
    except ValueError as exc:
        errors.append(str(exc))


def validate_repository(root: Path, run_help: bool = True) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    checks: list[str] = []

    try:
        manifest = load_json(root / "manifest.json")
    except ValueError as exc:
        return {"valid": False, "errors": [str(exc)], "warnings": [], "checks": []}

    if not isinstance(manifest, dict):
        return {
            "valid": False,
            "errors": ["manifest.json top-level value must be an object"],
            "warnings": [],
            "checks": [],
        }

    try:
        version = (root / "VERSION").read_text(encoding="utf-8").strip()
    except FileNotFoundError:
        version = ""
        errors.append("VERSION is missing")
    if manifest.get("version") != version:
        errors.append("manifest version must match VERSION")
    if manifest.get("name") != PROJECT_NAME:
        errors.append(f"manifest name must be {PROJECT_NAME!r}")
    if manifest.get("format") != "Agent Skills":
        errors.append("manifest format must be 'Agent Skills'")
    if manifest.get("license") != "MIT":
        warnings.append("manifest license differs from the bundled MIT license")
    checks.append("manifest identity and version")

    entries = manifest.get("skills")
    if not isinstance(entries, list) or not entries:
        errors.append("manifest skills must be a non-empty array")
        entries = []

    manifest_names: list[str] = []
    manifest_paths: list[str] = []
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            errors.append(f"manifest skills[{index}] must be an object")
            continue
        name = entry.get("name")
        path_value = entry.get("path")
        if not isinstance(name, str) or not name:
            errors.append(f"manifest skills[{index}].name must be a non-empty string")
            continue
        if not isinstance(path_value, str) or not path_value:
            errors.append(f"manifest skills[{index}].path must be a non-empty string")
            continue
        manifest_names.append(name)
        manifest_paths.append(path_value)

    if len(manifest_names) != len(set(manifest_names)):
        errors.append("manifest skill names must be unique")
    if len(manifest_paths) != len(set(manifest_paths)):
        errors.append("manifest skill paths must be unique")

    skills_root = root / "skills"
    actual_dirs = sorted(
        path.name for path in skills_root.iterdir() if path.is_dir() and not path.name.startswith(".")
    ) if skills_root.is_dir() else []
    if sorted(manifest_names) != actual_dirs:
        errors.append(
            "manifest skill names do not match skills directories: "
            f"manifest={sorted(manifest_names)}, actual={actual_dirs}"
        )

    for entry in entries:
        if not isinstance(entry, dict):
            continue
        name = entry.get("name")
        path_value = entry.get("path")
        if not isinstance(name, str) or not isinstance(path_value, str):
            continue
        expected_path = f"skills/{name}"
        if path_value != expected_path:
            errors.append(f"manifest path for {name!r} must be {expected_path!r}")
        skill_dir = root / path_value
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.is_file():
            errors.append(f"missing {skill_md}")
            continue

        try:
            frontmatter, line_count = parse_frontmatter(skill_md)
        except (ValueError, UnicodeDecodeError) as exc:
            errors.append(str(exc))
            continue

        fm_name = frontmatter.get("name", "")
        description = frontmatter.get("description", "")
        if fm_name != name or fm_name != skill_dir.name:
            errors.append(f"{skill_md}: name must match directory {skill_dir.name!r}")
        if not NAME_RE.fullmatch(fm_name) or len(fm_name) > 64:
            errors.append(f"{skill_md}: name must be lowercase hyphen-case and at most 64 chars")
        if not description or len(description) > 1024:
            errors.append(f"{skill_md}: description must contain 1-1024 characters")
        if not frontmatter.get("license"):
            errors.append(f"{skill_md}: license is required by this repository")
        compatibility = frontmatter.get("compatibility", "")
        if not compatibility or len(compatibility) > 500:
            errors.append(f"{skill_md}: compatibility must contain 1-500 characters")
        if line_count > 500:
            warnings.append(f"{skill_md}: {line_count} lines; keep SKILL.md under 500 lines")

        validate_evals(skill_dir, name, errors)
    checks.append("skill metadata and eval fixtures")

    entrypoint = manifest.get("entrypoint")
    if not isinstance(entrypoint, str) or not (root / entrypoint).is_file():
        errors.append("manifest entrypoint is missing or invalid")

    for path in sorted(root.rglob("*.json")):
        if any(part.startswith(".") and part not in {".github"} for part in path.parts):
            continue
        try:
            load_json(path)
        except ValueError as exc:
            errors.append(str(exc))
    checks.append("JSON syntax")

    for path in sorted(root.rglob("*.md")):
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            errors.append(f"{path}: UTF-8 decode failure: {exc}")
            continue
        for link in iter_markdown_links(text):
            if not link or link.startswith(("#", "http://", "https://", "mailto:", "data:")):
                continue
            target_text = link.split("#", 1)[0]
            if not target_text:
                continue
            target = (path.parent / target_text).resolve()
            if not is_within(target, root):
                errors.append(f"{path}: relative link escapes repository: {link}")
            elif not target.exists():
                errors.append(f"{path}: broken relative link: {link}")
    checks.append("Markdown relative links")

    python_files = sorted(root.rglob("*.py"))
    for path in python_files:
        check_script(path, errors, warnings)
    checks.append("Python syntax and network-import policy")

    if run_help:
        help_scripts = sorted((root / "skills").glob("*/scripts/*.py"))
        help_scripts.extend(sorted((root / "scripts").glob("*.py")))
        for path in help_scripts:
            try:
                completed = subprocess.run(
                    [sys.executable, str(path), "--help"],
                    cwd=root,
                    capture_output=True,
                    text=True,
                    timeout=10,
                    check=False,
                )
            except subprocess.TimeoutExpired:
                errors.append(f"{path}: --help timed out")
                continue
            if completed.returncode != 0:
                errors.append(
                    f"{path}: --help exited {completed.returncode}: {completed.stderr.strip()}"
                )
        checks.append("script --help interfaces")

    return {
        "valid": not errors,
        "name": manifest.get("name"),
        "repository": str(root),
        "skill_count": len(manifest_names),
        "python_file_count": len(python_files),
        "json_file_count": len(list(root.rglob("*.json"))),
        "checks": checks,
        "errors": errors,
        "warnings": warnings,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate the leeskills Agent Skills repository."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=repo_root(),
        help="Repository root. Defaults to the parent of this script.",
    )
    parser.add_argument(
        "--skip-script-help",
        action="store_true",
        help="Skip invoking optional scripts with --help.",
    )
    parser.add_argument(
        "--json-output",
        type=Path,
        help="Also write the validation result as JSON.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.expanduser().resolve()
    if not root.is_dir():
        die(f"repository root not found: {root}")

    result = validate_repository(root, run_help=not args.skip_script_help)
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.json_output:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(rendered, encoding="utf-8")
    sys.stdout.write(rendered)
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
