# Generic Agent Skills adapter

Use the directories under `skills/` directly.

## Discovery

At startup, expose only:

- `name`;
- `description`;
- absolute path to `SKILL.md`.

Load the full skill instructions only after activation. Load referenced files
only when the skill says they are needed.

`manifest.json` lists all available skills and identifies the orchestrator.

## Installation

```bash
python scripts/install.py   --client generic   --target /path/to/your/client/skills   --mode copy   --dry-run
```

Remove `--dry-run` after reviewing the plan.

## Clients without skill composition

When an agent cannot invoke one skill from another, use `anti-ai-slop` as a
standalone workflow. It contains a fallback sequence and references the output
contracts of the focused skills.
