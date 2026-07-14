# Architecture

## Goals

The repository is organized around small, composable skills rather than one
large style guide. Each focused skill owns one decision boundary and produces a
structured handoff that another skill can consume.

The optional `anti-ai-slop` skill is an orchestrator. It does not replace the
focused skills; it selects the smallest useful sequence.

## Composition graph

```text
                       ┌───────────────────────┐
                       │ content-grounding     │
                       └──────────┬────────────┘
                                  │
                                  ▼
                       ┌───────────────────────┐
                       │ structure-selector    │
                       └──────────┬────────────┘
                                  │
                                  ▼
                       ┌───────────────────────┐
                       │ visual-entropy-budget │
                       └──────────┬────────────┘
                                  │
             ┌────────────────────┼────────────────────┐
             ▼                    ▼                    ▼
┌────────────────────┐ ┌────────────────────┐ ┌───────────────────────────┐
│ specificity-editor │ │ motion-necessity   │ │ accessibility-simplicity  │
└──────────┬─────────┘ └──────────┬─────────┘ └─────────────┬─────────────┘
           └───────────────────────┼─────────────────────────┘
                                   ▼
                       ┌───────────────────────┐
                       │ prune-and-verify      │
                       └───────────────────────┘
```

`slop-signal-audit` can run before the graph for an existing artifact and can
run again after remediation to compare results.

## Data contracts

The skills exchange small JSON artifacts where deterministic structure helps:

- `content-inventory.json`
- `structure-decision.json`
- `visual-budget.json`
- `motion-inventory.json`
- `accessibility-report.json`
- `verification.json`
- `audit.json`

JSON schemas are bundled as assets. Markdown output remains appropriate for
human review.

## Progressive disclosure

Every `SKILL.md` contains only the core workflow and tells the agent when to
load a reference or template. This reduces context use and avoids forcing
irrelevant details into every run.

## Portability boundary

Core skills use only fields from the open Agent Skills specification:

- `name`
- `description`
- `license`
- `compatibility`
- `metadata`

Vendor-specific installation paths and optional metadata live under
`adapters/`. Core behavior does not depend on slash commands, subagents,
dynamic shell injection, or pre-approved tools.

## Deterministic helpers

Scripts are included only where mechanical validation is more reliable than
language-model judgment. They:

- accept all input through flags or files;
- provide `--help`;
- return structured JSON when useful;
- exit non-zero on invalid input;
- avoid interactive prompts;
- use no network;
- use no third-party packages.

The agent remains responsible for contextual judgments such as whether a
visual hierarchy is clear or a sentence is sufficiently specific.
