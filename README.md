<p align="center">
  <strong>English</strong> · <a href="README.ko.md">한국어</a> · <a href="README.ja.md">日本語</a>
</p>

<h1 align="center">leeskills</h1>

<p align="center">
  Agent Skills that review interface work for unsupported claims,<br>
  generic copy, and design that does not help the user's task.
</p>

<p align="center">
  <a href="https://github.com/fromiron/leeskills/actions/workflows/validate.yml"><img alt="Validation status" src="https://github.com/fromiron/leeskills/actions/workflows/validate.yml/badge.svg"></a>
  <img alt="Version 0.6.0" src="https://img.shields.io/badge/version-0.6.0-007FA8?style=flat-square">
  <img alt="Open Agent Skills format" src="https://img.shields.io/badge/format-Agent_Skills-111111?style=flat-square">
  <a href="LICENSE"><img alt="MIT license" src="https://img.shields.io/badge/license-MIT-F4E9D8?style=flat-square"></a>
</p>

<p align="center">
  <img src=".github/assets/leeskills-hero.png" width="720" alt="Noisy interface fragments passing through a review frame and becoming a clear information hierarchy">
  <br>
  <sub>An illustration of the review process, not a product screenshot.</sub>
</p>

leeskills gives a coding or design agent ten review skills: one workflow skill
that plans the review, and nine focused skills for content, information
structure, components, visual systems, copy, motion, accessibility, and final
verification. They work in English, Korean, and Japanese.

The skills judge the artifact in front of them. They do not guess who made it
or whether AI was involved, and they do not fill gaps with invented customers,
metrics, quotes, or results.

## Quick start

```bash
npx skills add fromiron/leeskills
```

The open [`skills` CLI](https://skills.sh/docs/cli) fetches this GitHub
repository and installs the packages under `skills/`. Nothing is published to
npm. Then ask your agent in plain language:

> Review this landing page with leeskills. Point out generic copy, unsupported
> claims, and design choices that do not help the main task. Keep the product's
> actual voice, required actions, and accessibility. Separate observations from
> inferences, make the smallest complete fix, and check the main flow again.

To inspect the catalog or install only the workflow skill:

```bash
npx skills add fromiron/leeskills --list
npx skills add fromiron/leeskills --skill design-workflow
```

Upgrading from the previous skill names, such as `anti-ai-slop`? Follow the
[migration guide](docs/skill-name-migration.md) so local changes are kept and
old and new packages are not both discovered.

## What you get back

| You ask for | You receive |
|---|---|
| A review | Each finding with its location, evidence, the smallest fix, and how to verify it. Artifact files stay unchanged. |
| Edits | The actual changes, then a final check, the checks run, items left unverified, and how to roll back. |
| A quick look at a small draft | The `audit-design` quick pass: up to five findings, no score or release verdict, and a list of skipped checks. |

Every material finding carries one evidence label:

| Label | Meaning |
|---|---|
| **Observed** | Shown directly by the supplied copy, screenshot, markup, code, design file, or tokens |
| **Measured** | Produced by a deterministic test or calculation |
| **Inferred** | Supported by the evidence, but not shown directly |
| **Unknown** | The supplied material cannot answer it |

When something cannot be checked, the report says so.

## Skills

Start with `design-workflow` for a broad review; it picks only the checks the
artifact needs. Use a focused skill when the job is narrow.

| Skill | Use it to | Output |
|---|---|---|
| `design-workflow` | Review an interface end to end | A scoped sequence of skills and one combined result |
| `audit-design` | Diagnose an existing artifact | Observed problems, risk scores, and a cleanup order |
| `verify-content` | Check which claims the sources support | A source-traced content inventory with gaps left visible |
| `plan-structure` | Choose content order and navigation | A task-based structure, with rejected options recorded |
| `review-components` | Define a reusable UI contract | Anatomy, states, behavior, accessibility, ownership, and design-code parity |
| `review-visuals` | Tighten the visual system | A visual budget, responsive, typography, and nested-radius checks, and an optional HTML token proposal page rendered from validated JSON |
| `edit-copy` | Edit product copy | Specific, supported copy in the product's voice for each locale |
| `review-motion` | Review animation and transitions | Keep, reduce, replace, or remove decisions, with reduced-motion support |
| `check-accessibility` | Simplify without losing access | Semantics, keyboard, focus, reflow, contrast, and status checks |
| `verify-changes` | Check the finished work | Deletion, growth, reflow, provenance, and primary-task checks |

`verify-content` decides what may be claimed; `edit-copy` decides how to say
it. Cards, gradients, and motion are not banned. They stay when they help the
task and there is a reason for them.

## Typical sequences

| Situation | Sequence |
|---|---|
| New interface or landing page | `verify-content` → `plan-structure` → `review-visuals` → `edit-copy` → `review-motion` → `check-accessibility` → edits → `verify-changes` |
| Existing interface | `audit-design` → focused skills as needed → edits → `verify-changes` |
| Design system or component | `review-components` → `review-visuals` → `check-accessibility` → edits → `verify-changes` |
| Copy only | `verify-content` → `edit-copy` → edits → `verify-changes` |

The edit step runs only when you ask for changes.

More requests and data examples are in [`examples/`](examples/README.md),
including a [full audit request](examples/full-audit-request.md) and a
[manual integration](examples/manual-agent-integration.md) for clients without
native skill discovery.

## Other ways to install

Client-specific notes are in the [Codex](adapters/codex/README.md),
[Claude Code](adapters/claude-code/README.md), and
[generic](adapters/generic/README.md) adapters.

From a clone, or to install into a specific folder, use the bundled installer.
Remove `--dry-run` to write files. It does not overwrite existing skills unless
you pass `--force`.

```bash
python scripts/install.py --client codex --scope repo --mode copy --dry-run
python scripts/install.py --client claude-code --scope repo --mode copy --dry-run
python scripts/install.py --client generic --target /path/to/skills --mode copy --dry-run
```

## Package layout

```text
skill-name/
├── SKILL.md      # instructions
├── references/   # material loaded when needed
├── assets/       # schemas and templates
├── scripts/      # optional repeatable checks
└── evals/        # trigger and output fixtures
```

- `SKILL.md` files use only open Agent Skills frontmatter fields.
- Judgment lives in Markdown. Repeatable checks, such as required fields and
  file structure, are optional Python 3.9+ scripts that use only the standard
  library, run non-interactively, and make no network requests.
- Trigger fixtures cover English, Korean, and Japanese, including near-miss
  negatives. They check fixture coverage, not real activation rates in a
  client.

## Development

```bash
make check
```

This runs `python scripts/validate_repo.py` and
`python -m unittest discover -s tests -v`. Without `make`, run those two
commands directly; use `python3` or `py -3` if that is your Python 3.9+
launcher. CI runs the same checks on Ubuntu and Windows with Python 3.9 and
3.12. See [CONTRIBUTING.md](CONTRIBUTING.md) before adding a skill.

## Documentation

| Document | Contents |
|---|---|
| [Architecture](docs/architecture.md) | Composition, data contracts, and portability boundaries |
| [Integration](docs/integration.md) | Client setup and invocation strategy |
| [Name migration](docs/skill-name-migration.md) | Old-to-new names and safe installation updates |
| [Evaluation](docs/evaluation.md) | Trigger measurement, output comparison, and release gates |
| [Design foundations](docs/design-foundations.md) | Product and design principles used by the skills |
| [Source notes](docs/source-notes.md) | Provenance and the use of outside guidance |
| [Changelog](CHANGELOG.md) | Release history |

## License

[MIT](LICENSE)
