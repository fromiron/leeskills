# Claude Code adapter

The core skills use the open Agent Skills format and avoid Claude-only
frontmatter.

## Install from GitHub

```bash
npx skills add fromiron/leeskills --agent claude-code
```

The CLI installs to the current project by default. Add `--global` for user
scope, `--list` to inspect the catalog without installing, or `--skill <name>`
to select a skill.

## Install from a clone

### Repository scope

```bash
python scripts/install.py --client claude-code --scope repo --mode copy --dry-run
python scripts/install.py --client claude-code --scope repo --mode copy
```

Target:

```text
<repository>/.claude/skills/
```

### User scope

```bash
python scripts/install.py --client claude-code --scope user --mode copy --dry-run
python scripts/install.py --client claude-code --scope user --mode copy
```

Target:

```text
~/.claude/skills/
```

### Symlink mode

Claude Code follows symlinked skill directories in project and personal skill
locations:

```bash
python scripts/install.py --client claude-code --scope user --mode symlink
```

## Optional Claude extensions

Claude Code supports additional fields such as invocation controls and
subagent execution. They are intentionally absent from the core packages.
Maintain any Claude-specific overlays in your own adapter branch so upstream
skills remain portable.

## Invocation

Invoke a skill directly by its directory name or let Claude match the request
to its description. Use the trigger eval files to verify that automatic
activation behaves as intended in your installed version.
