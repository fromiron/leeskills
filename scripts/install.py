#!/usr/bin/env python3
"""Install selected skills into Agent Skills-compatible client locations."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import uuid
from pathlib import Path
from typing import Any, NoReturn

# Keep UTF-8 output stable on Windows consoles with legacy code pages.
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8")

CLIENT_REPO_PATHS = {
    "codex": Path(".agents/skills"),
    "claude-code": Path(".claude/skills"),
}
CLIENT_USER_PATHS = {
    "codex": Path("~/.agents/skills"),
    "claude-code": Path("~/.claude/skills"),
}


def die(message: str, code: int = 2) -> NoReturn:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(code)


def repository_root() -> Path:
    return Path(__file__).resolve().parent.parent


def load_manifest(root: Path) -> dict[str, Any]:
    path = root / "manifest.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        die(f"manifest not found: {path}")
    except json.JSONDecodeError as exc:
        die(f"invalid manifest JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}")
    if not isinstance(data, dict) or not isinstance(data.get("skills"), list):
        die("manifest.json must contain a skills array")
    return data


def remove_existing(path: Path) -> None:
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)


def resolve_target(args: argparse.Namespace) -> Path:
    if args.client == "generic":
        if args.target is None:
            die("--target is required for --client generic")
        return args.target.expanduser().resolve()

    if args.target is not None:
        die("--target is only valid for --client generic")

    if args.scope == "user":
        return CLIENT_USER_PATHS[args.client].expanduser().resolve()

    repo = args.repo.expanduser().resolve()
    return (repo / CLIENT_REPO_PATHS[args.client]).resolve()


def selected_skills(manifest: dict[str, Any], requested: list[str]) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    by_name: dict[str, dict[str, str]] = {}
    for raw in manifest["skills"]:
        if not isinstance(raw, dict):
            die("each manifest skill must be an object")
        name = raw.get("name")
        path = raw.get("path")
        if not isinstance(name, str) or not isinstance(path, str):
            die("each manifest skill requires string name and path fields")
        entry = {"name": name, "path": path}
        entries.append(entry)
        by_name[name] = entry

    names = requested or [entry["name"] for entry in entries]
    if "all" in names:
        if len(names) != 1:
            die("--skill all cannot be combined with other --skill values")
        names = [entry["name"] for entry in entries]

    duplicates = sorted({name for name in names if names.count(name) > 1})
    if duplicates:
        die("duplicate --skill values: " + ", ".join(duplicates))

    unknown = sorted(set(names) - set(by_name))
    if unknown:
        die("unknown skills: " + ", ".join(unknown))
    return [by_name[name] for name in names]


def build_plan(
    source_root: Path,
    target_root: Path,
    entries: list[dict[str, str]],
    mode: str,
    force: bool,
) -> tuple[list[dict[str, Any]], list[str]]:
    plan: list[dict[str, Any]] = []
    conflicts: list[str] = []

    for entry in entries:
        source = (source_root / entry["path"]).resolve()
        destination = target_root / entry["name"]
        if not source.is_dir() or not (source / "SKILL.md").is_file():
            die(f"invalid source skill directory: {source}")

        # Compare lexical absolute paths without following an existing destination
        # symlink. A symlink that already points at the source is replaceable with
        # --force; only an actual source-equals-destination path is unsafe.
        same_location = destination == source
        if same_location:
            die(f"refusing to install a skill onto its own source directory: {source}")

        exists = destination.exists() or destination.is_symlink()
        action = "replace" if exists and force else "create"
        if exists and not force:
            action = "conflict"
            conflicts.append(str(destination))

        plan.append(
            {
                "skill": entry["name"],
                "source": str(source),
                "destination": str(destination),
                "mode": mode,
                "action": action,
            }
        )
    return plan, conflicts


def execute(plan: list[dict[str, Any]], target_root: Path, force: bool) -> None:
    target_root.mkdir(parents=True, exist_ok=True)
    for item in plan:
        source = Path(item["source"])
        destination = Path(item["destination"])
        destination.parent.mkdir(parents=True, exist_ok=True)

        if item["mode"] == "copy":
            staging = destination.parent / f".{destination.name}.install-{uuid.uuid4().hex}"
            try:
                shutil.copytree(source, staging, symlinks=True)
                if destination.exists() or destination.is_symlink():
                    if not force:
                        die(f"destination appeared during installation: {destination}", code=1)
                    remove_existing(destination)
                os.replace(staging, destination)
            finally:
                if staging.exists() or staging.is_symlink():
                    remove_existing(staging)
        else:
            if destination.exists() or destination.is_symlink():
                if not force:
                    die(f"destination appeared during installation: {destination}", code=1)
                remove_existing(destination)
            destination.symlink_to(source, target_is_directory=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install portable leeskills packages into a supported client."
    )
    parser.add_argument(
        "--client",
        choices=("codex", "claude-code", "generic"),
        required=True,
        help="Target client layout.",
    )
    parser.add_argument(
        "--scope",
        choices=("repo", "user"),
        default="repo",
        help="Named-client installation scope. Ignored for generic targets.",
    )
    parser.add_argument(
        "--repo",
        type=Path,
        default=Path.cwd(),
        help="Repository root for repo-scoped named-client installation.",
    )
    parser.add_argument(
        "--target",
        type=Path,
        help="Explicit skills directory for --client generic.",
    )
    parser.add_argument(
        "--mode",
        choices=("copy", "symlink"),
        default="copy",
        help="Copy skill directories or create directory symlinks.",
    )
    parser.add_argument(
        "--skill",
        action="append",
        default=[],
        help="Install one named skill; repeat the flag. Default: all skills.",
    )
    parser.add_argument("--force", action="store_true", help="Replace existing skill paths.")
    parser.add_argument("--dry-run", action="store_true", help="Print the plan without changes.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    source_root = repository_root()
    manifest = load_manifest(source_root)
    entries = selected_skills(manifest, args.skill)
    target_root = resolve_target(args)
    plan, conflicts = build_plan(source_root, target_root, entries, args.mode, args.force)

    result = {
        "client": args.client,
        "scope": args.scope if args.client != "generic" else "explicit-target",
        "target_root": str(target_root),
        "dry_run": args.dry_run,
        "force": args.force,
        "plan": plan,
        "conflicts": conflicts,
    }

    if conflicts:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        print(
            "error: existing skills would be overwritten; use --force after review",
            file=sys.stderr,
        )
        return 1

    if not args.dry_run:
        execute(plan, target_root, args.force)
        result["installed"] = [item["skill"] for item in plan]
    else:
        result["installed"] = []

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
