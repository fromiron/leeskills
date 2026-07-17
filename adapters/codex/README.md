# OpenAI Codex adapter

The core skills use the open Agent Skills format and require no Codex-only
frontmatter.

## Install from GitHub

```bash
npx skills add fromiron/leeskills --agent codex
```

The CLI installs to the current project by default. Add `--global` for user
scope, `--list` to inspect the catalog without installing, or `--skill <name>`
to select a skill.

## Install from a clone

### Repository scope

```bash
python scripts/install.py --client codex --scope repo --mode copy --dry-run
python scripts/install.py --client codex --scope repo --mode copy
```

Target:

```text
<repository>/.agents/skills/
```

### User scope

```bash
python scripts/install.py --client codex --scope user --mode copy --dry-run
python scripts/install.py --client codex --scope user --mode copy
```

Target:

```text
~/.agents/skills/
```

### Symlink mode

Codex supports symlinked skill directories. For a separately maintained clone:

```bash
python scripts/install.py --client codex --scope user --mode symlink
```

Use copy mode on platforms or filesystems where symlinks are restricted.

## Optional Codex metadata

Codex supports `agents/openai.yaml`, but it is intentionally omitted from the
core packages to preserve portability. Add it in a downstream repository only
when you need UI labels, invocation policy, or MCP dependency declarations.

## Invocation

Use the client skill picker or explicitly mention a skill. Broad requests can
start with `anti-ai-slop`; focused requests should invoke the corresponding
single-purpose skill.
