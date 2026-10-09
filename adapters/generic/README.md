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

For clients supported by the open `skills` CLI:

```bash
npx skills add fromiron/leeskills
```

For an offline clone or a client-specific destination, use the bundled
installer:

```bash
python scripts/install.py   --client generic   --target /path/to/your/client/skills   --mode copy   --dry-run
```

Remove `--dry-run` after reviewing the plan.

## Clients without skill composition

When an agent cannot invoke one skill from another, `design-workflow` reads
each focused skill's `SKILL.md` from the sibling package directory when it is
installed. When a focused skill is not installed at all, `design-workflow`
falls back to a limited review using the summarized contracts in its
composition map: it reports the missing skills and does not produce scores,
verdicts, release decisions, or rendered token pages. Install the full catalog
for the complete workflow.
