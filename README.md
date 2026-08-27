<p align="center">
  <strong>English</strong> · <a href="README.ko.md">한국어</a> · <a href="README.ja.md">日本語</a>
</p>

<h1 align="center">leeskills</h1>

<p align="center">
  <strong>Agent Skills for reviewing generic, unsupported, or unnecessary interface work.</strong>
</p>

<p align="center">
  Ten focused skills cover copy, information structure, components, visual systems,<br>
  motion, accessibility, and final verification.
</p>

<p align="center">
  <a href="https://github.com/fromiron/leeskills/actions/workflows/validate.yml"><img alt="Validation status" src="https://github.com/fromiron/leeskills/actions/workflows/validate.yml/badge.svg"></a>
  <img alt="Version 0.6.0" src="https://img.shields.io/badge/version-0.6.0-007FA8?style=flat-square">
  <img alt="Open Agent Skills format" src="https://img.shields.io/badge/format-Agent_Skills-111111?style=flat-square">
  <a href="LICENSE"><img alt="MIT license" src="https://img.shields.io/badge/license-MIT-F4E9D8?style=flat-square"></a>
</p>

## Install

```bash
npx skills add fromiron/leeskills
```

<p align="center">
  <img src=".github/assets/leeskills-hero.png" width="720" alt="Noisy interface fragments passing through a review frame and becoming a clear information hierarchy">
</p>

<p align="center">An illustration of the review process, not a product screenshot.</p>

`leeskills` reviews the work in front of it. It does not guess who made it or
which tools they used.

The open [`skills` CLI](https://skills.sh/docs/cli) finds the packages under
`skills/` and installs them for a supported agent. List the catalog first, or
install only the main reviewer:

```bash
npx skills add fromiron/leeskills --list
npx skills add fromiron/leeskills --skill anti-ai-slop
```

The installer fetches this GitHub repository. Nothing here needs to be
published to npm.

## How it works

Use one skill when the job is specific. For a broader review, start with
`anti-ai-slop`; it selects the checks that fit the artifact instead of running
every skill by default.

The skills describe the judgment calls in Markdown. Optional schemas and
dependency-free Python scripts handle repeatable checks such as file structure,
required fields, and repository validation.

## Included skills

| Task | Skill | Output |
|---|---|---|
| Review an interface end to end | `anti-ai-slop` | A scoped workflow and one combined result |
| Diagnose an existing artifact | `slop-signal-audit` | Observed problems, risk scores, and an order for cleanup |
| Check the facts behind the copy | `content-grounding` | A source-traced content inventory that leaves gaps visible |
| Pick an information structure | `structure-selector` | A task-based choice with the rejected options recorded |
| Define a reusable UI contract | `component-contract-audit` | Anatomy, states, behavior, accessibility, ownership, and parity checks |
| Tighten the visual system | `visual-entropy-budget` | A visual budget with responsive, typography, and nested-radius checks |
| Rewrite vague copy | `specificity-editor` | Concrete copy tied to the supplied facts |
| Review motion | `motion-necessity-gate` | Keep, reduce, replace, or remove decisions, including reduced-motion support |
| Simplify without losing access | `accessibility-simplicity-guard` | Checks for semantics, keyboard use, focus, reflow, contrast, and status |
| Check the finished work | `prune-and-verify` | Deletion, growth, reflow, provenance, and primary-task checks |

These skills do not ban cards, gradients, motion, or expressive work. Keep them
when they help the task and there is a clear reason to use them.

## Common workflows

**New interface or landing page**

```text
content-grounding
→ structure-selector
→ visual-entropy-budget
→ specificity-editor
→ motion-necessity-gate
→ accessibility-simplicity-guard
→ prune-and-verify
```

**Existing interface audit**

```text
slop-signal-audit
→ focused remediation skills
→ prune-and-verify
```

**Design system or reusable component**

```text
component-contract-audit
→ visual-entropy-budget
→ accessibility-simplicity-guard
→ prune-and-verify
```

**Copy review**

```text
content-grounding → specificity-editor → prune-and-verify
```

For a small draft, use the `slop-signal-audit` quick pass. It reports up to five
useful changes without a score or release verdict and names the checks it did
not run.

## Evidence labels

Each material finding gets one label:

| Label | Use it when |
|---|---|
| **Observed** | The supplied copy, screenshot, markup, code, design file, or token shows it directly |
| **Measured** | A deterministic test or calculation produced it |
| **Inferred** | The evidence supports a conclusion, but does not show it directly |
| **Unknown** | The supplied material cannot answer the question |

If something cannot be checked, the report says so. It does not fill the gap
with a customer, metric, quote, capability, result, or accessibility claim.

## Package layout

```text
skill-name/
├── SKILL.md      # instructions
├── references/   # material loaded when needed
├── assets/       # schemas and templates
├── scripts/      # optional repeatable checks
└── evals/        # trigger and output fixtures
```

- Core instructions use the open Agent Skills fields and no vendor-only
  frontmatter.
- Optional Python 3.9+ scripts use the standard library, run non-interactively,
  and make no network requests.
- Trigger fixtures cover English, Korean, and Japanese, including near-miss
  negatives. They check fixture coverage, not real activation rates.
- Adapters are included for Codex, Claude Code, and other compatible clients.

## Example prompt

After installation, ask your agent in ordinary language:

> Review this landing page with leeskills. Point out generic copy, unsupported
> claims, and design choices that do not help the main task. Keep the product's
> actual voice, required actions, and accessibility. Separate observations from
> inferences, make the smallest complete fix, and check the main flow again.

More examples are in the [full audit request](examples/full-audit-request.md),
the [manual integration example](examples/manual-agent-integration.md), and
the [`examples/` directory](examples/README.md).

## Development

```bash
python scripts/validate_repo.py
python -m unittest discover -s tests -v
```

Use `python3` on Unix-like systems or `py -3` on Windows if that is the
available Python 3.9+ launcher. CI runs the same checks on Ubuntu and Windows
with Python 3.9 and 3.12.

For an offline clone or an explicit destination, use the bundled installer:

```bash
python scripts/install.py --client codex --scope repo --mode copy --dry-run
python scripts/install.py --client claude-code --scope repo --mode copy --dry-run
python scripts/install.py --client generic --target /path/to/skills --mode copy --dry-run
```

Existing skills are not overwritten unless you pass `--force`.

## Documentation

| Document | Contents |
|---|---|
| [Architecture](docs/architecture.md) | Composition, data contracts, and portability boundaries |
| [Integration](docs/integration.md) | Client setup and invocation strategy |
| [Evaluation](docs/evaluation.md) | Trigger measurement, output comparison, and release gates |
| [Design foundations](docs/design-foundations.md) | Product and design principles used by the skills |
| [Source notes](docs/source-notes.md) | Provenance and the use of outside guidance |
| [Contributing](CONTRIBUTING.md) | Repository conventions and contribution flow |

## License

[MIT](LICENSE)
