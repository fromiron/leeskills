# Skill name migration

The unreleased update renames the entry skill and all nine focused skills.
The repository and package remain `leeskills`. These are replacements, not
additional skills or aliases.

| Previous name | Current name |
|---|---|
| `anti-ai-slop` | `design-workflow` |
| `slop-signal-audit` | `audit-design` |
| `content-grounding` | `verify-content` |
| `structure-selector` | `plan-structure` |
| `component-contract-audit` | `review-components` |
| `visual-entropy-budget` | `review-visuals` |
| `specificity-editor` | `edit-copy` |
| `motion-necessity-gate` | `review-motion` |
| `accessibility-simplicity-guard` | `check-accessibility` |
| `prune-and-verify` | `verify-changes` |

Directory names, frontmatter names, manifest entries, invocation examples,
and helper-script paths move together. Script filenames, JSON data contracts,
existing eval IDs, and trigger queries remain stable. Historical changelog
entries retain the names used at the time. Existing reports need not be
rewritten; use this table when comparing runs.

## Identify an existing installation

Check the actual client scope before installing. The bundled installer uses
`.agents/skills/` for Codex and `.claude/skills/` for Claude Code, under the
project or home directory according to scope. A generic or third-party
installation may use a different location; inspect its recorded destination.

For each old path, record whether it is a copied directory or a symbolic link,
its link target if applicable, and its `SKILL.md` name, author, and version.
A matching folder name or version alone does not establish that its contents
are unmodified. Compare the full installed tree with the original release or
commit, including scripts, references, assets, and any added files. For example,
`git show <installed-commit>:skills/content-grounding/SKILL.md` retrieves the
historical entrypoint without changing the current checkout. If the origin or
local edits are uncertain, preserve the installation for manual review.

A symlink into this checkout can become broken when its target is renamed.
Inspect the link itself even if the old target no longer exists; do not assume
that an absent target means there was no installation.

## Switch without losing local changes

1. Back up the old installation outside every directory the client scans for
   skills. For symlinks, record the link destination and preserve any locally
   modified target contents as well. Do not leave a renamed backup containing
   `SKILL.md` inside the discovery directory.
2. Review the old-to-new mapping and compare local customizations with the new
   packages. Keep changes that remain intentional; do not copy an old
   frontmatter name into a new directory.
3. Preview and run the installer for the same scope. For example, from this
   checkout, to install a single repository-scoped skill:

   ```bash
   python scripts/install.py --client codex --scope repo --skill verify-content --dry-run
   python scripts/install.py --client codex --scope repo --skill verify-content
   ```

   Omit `--skill` to install all ten. Use the other client or target options
   documented in [Integration](integration.md) when appropriate. This installer
   leaves old-name paths untouched. `--force` replaces a selected new-name
   destination; it neither migrates old names nor merges user modifications.
4. Read back the new files and compare them with the intended source plus any
   reviewed local changes. Update explicit skill invocations, registered paths,
   and helper commands to the new names.
5. Move only reviewed old copies out of the client's discovery locations. For
   symlinks, remove only the obsolete link, never the referenced source tree.
   Retain the backup until the new installation is verified.
6. Refresh the client's skill catalog. Confirm the new names are discoverable,
   the old names no longer activate, and a representative request loads the
   expected skill and its resources. Check every enabled scope for duplicates.

To roll back, move the new registration or copy out of discovery, restore the
saved old paths and any required link targets, restore old invocation paths,
and refresh the catalog again. Preserve unrelated skills throughout.
