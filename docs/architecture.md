# Architecture

## Goals

The repository is organized around small, composable skills rather than one
large style guide. Each focused skill owns one decision boundary and produces a
structured handoff that another skill can consume.

The optional `design-workflow` skill is an orchestrator. It does not replace the
focused skills; it selects the smallest useful sequence. Installed alone, it
supports only a limited standalone review: it summarizes each focused skill's
handoff contract but does not bundle their scoring rules, schemas, validators,
or renderers, and it reports which steps ran at which availability level.

## Composition graph

```text
design-workflow selects only the relevant steps:

verify-content → plan-structure → review-components (when relevant)
→ review-visuals → edit-copy / review-motion / check-accessibility
→ change plan → requested edits → verify-changes
```

`audit-design` can run before the graph for an existing artifact and can
run again after remediation to compare results.

Review-only requests leave artifact files unchanged. If verification or a
comparison leads to another requested edit, repeat affected checks against the
updated artifact before concluding.

## Delivery contract

Each skill carries this convention in its own `SKILL.md` so selective installs
remain self-contained:

| Request | Deliverable |
|---|---|
| Review only | Issue location, evidence, smallest fix, and verification method |
| Edits requested | Those findings plus the actual diff or changed-file paths |
| Changes applied | Checks actually run and outcomes, unverified items, and rollback |

The order is diagnosis, change plan, authorized patch, then final verification.
No additional implementation skill or browser/model orchestration CLI is
required. Use the client's existing editing and execution capabilities within
the requested scope. Keep unsupported product behavior unknown even when its
report validates.

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

Repository validation statically rejects a specified set of network-related
imports. It is not an allowlist of all standard-library modules, does not
detect every possible network access, and does not sandbox execution. The
standard-library and no-network requirements remain authoring rules; the
static check detects only some violations. Unit tests also exercise actual
helper behavior, including scoring, invalid-input rejection, and installation
conflicts. Neither kind of check establishes agent design judgment quality.
