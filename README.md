<p align="center">
  <strong>English</strong> · <a href="README.ko.md">한국어</a> · <a href="README.ja.md">日本語</a>
</p>

<h1 align="center">leeskills</h1>

<p align="center">
  <strong>Ground the content. Cut the noise. Verify what remains.</strong>
</p>

<p align="center">
  Ten portable Agent Skills for turning generic, unsupported interface output<br>
  into a smaller, clearer, evidence-backed system.
</p>

<p align="center">
  <a href="https://github.com/fromiron/leeskills/actions/workflows/validate.yml"><img alt="Validation status" src="https://github.com/fromiron/leeskills/actions/workflows/validate.yml/badge.svg"></a>
  <img alt="Version 0.6.0" src="https://img.shields.io/badge/version-0.6.0-007FA8?style=flat-square">
  <img alt="Open Agent Skills format" src="https://img.shields.io/badge/format-Agent_Skills-111111?style=flat-square">
  <a href="LICENSE"><img alt="MIT license" src="https://img.shields.io/badge/license-MIT-F4E9D8?style=flat-square"></a>
</p>

## Install in one command

```bash
npx skills add fromiron/leeskills
```

<p align="center">
  <img src=".github/assets/leeskills-hero.png" width="720" alt="Concept illustration of noisy interface fragments passing through an audit frame and becoming a clear hierarchy">
</p>

<p align="center">Concept illustration, not a product screenshot or proof of a real interface.</p>

> [!IMPORTANT]
> `leeskills` audits observable design output. It does **not** determine whether
> AI made it, and it never treats an aesthetic pattern as authorship evidence.

The open [`skills` CLI](https://skills.sh/docs/cli) discovers every package in
`skills/` and lets you choose the target agent and skills. Inspect the catalog
or install only the orchestrator:

```bash
npx skills add fromiron/leeskills --list
npx skills add fromiron/leeskills --skill anti-ai-slop
```

No package from this repository needs to be published to npm. The command uses
the external installer to fetch the GitHub repository.

## Why leeskills

- **Evidence before aesthetics.** Claims, metrics, screenshots, and outcomes
  stay tied to sources. Missing evidence remains missing.
- **Small skills with clear ownership.** Use one focused skill for a narrow
  problem or let `anti-ai-slop` choose the smallest useful sequence.
- **Judgment where it matters, scripts where it helps.** Contextual design
  decisions stay with the agent; schemas and dependency-free Python helpers
  check mechanical contracts.
- **Portable by default.** Core skills use the open Agent Skills format rather
  than vendor-only frontmatter. Adapters cover Codex, Claude Code, and generic
  compatible clients.

## Ten skills, one shared contract

| Need | Skill | What it produces |
|---|---|---|
| A broad end-to-end review | `anti-ai-slop` | The smallest applicable workflow and a consolidated verdict |
| Diagnosis of an existing artifact | `slop-signal-audit` | Observable findings, risk scores, and prioritized removals |
| A factual foundation | `content-grounding` | A source-traced content inventory that blocks fabrication |
| One dominant information structure | `structure-selector` | A task-based structure decision with rejected alternatives |
| A reusable UI contract | `component-contract-audit` | Anatomy, states, behavior, accessibility, ownership, and parity checks |
| A coherent visual system | `visual-entropy-budget` | A visual budget plus responsive, typography, and nested-radius checks |
| Specific product copy | `specificity-editor` | Evidence-aware rewrites that survive the substitution test |
| Necessary motion only | `motion-necessity-gate` | Keep, reduce, replace, or remove decisions with reduced-motion checks |
| Simplicity without lost access | `accessibility-simplicity-guard` | Semantics, keyboard, focus, reflow, contrast, and status safeguards |
| A verified final pass | `prune-and-verify` | Deletion, growth, reflow, provenance, and primary-task verification |

The skills do not ban cards, gradients, motion, or expressive work by category.
They ask what each choice communicates, which task it supports, and what
evidence justifies keeping it.

## Choose the smallest workflow

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

**Copy-only review**

```text
content-grounding → specificity-editor → prune-and-verify
```

For a small artifact or early draft, run `slop-signal-audit` in quick-pass
mode: one pass, no score or verdict, up to five changes, and an explicit list
of skipped checks.

## Evidence, not vibes

Every material finding keeps one evidence state:

| State | Meaning |
|---|---|
| **Observed** | Directly visible in supplied copy, screenshots, markup, code, design files, or tokens |
| **Measured** | Produced by a deterministic test or calculation |
| **Inferred** | Reasoned from available evidence and labeled as inference |
| **Unknown** | Not verifiable from the supplied material |

An inference never becomes a fact by repetition. The skills prohibit invented
customers, metrics, quotes, awards, capabilities, outcomes, and accessibility
claims. Structured validators also keep required unknowns from silently
becoming passes.

## Portable package, deterministic checks

```text
skill-name/
├── SKILL.md      # core workflow
├── references/   # loaded only when needed
├── assets/       # schemas and templates
├── scripts/      # optional deterministic helpers
└── evals/        # trigger and output-quality fixtures
```

- Core instructions use the open Agent Skills fields and stay vendor-neutral.
- Optional Python 3.9+ scripts are non-interactive, standard-library-only, and
  make no network requests.
- Trigger fixtures cover English, Korean, and Japanese, including near-miss
  negatives. Fixtures prove coverage, not real client trigger rates.
- JSON schemas make handoffs reviewable where structure helps; human judgment
  remains required for hierarchy, authenticity, voice, and usability.

## Try it on real work

After installation, ask your agent in ordinary language:

> Audit this landing page for generic, unsupported, or unnecessary design.
> Preserve its real identity, required actions, and accessibility. Label every
> finding by evidence state, make the smallest complete change, then verify the
> primary flow again.

Start with the [full audit request](examples/full-audit-request.md), the
[manual integration example](examples/manual-agent-integration.md), or the
structured artifacts in [`examples/`](examples/README.md).

## Develop and validate

```bash
python scripts/validate_repo.py
python -m unittest discover -s tests -v
```

Use `python3` on Unix-like systems or `py -3` on Windows when that is the
available Python 3.9+ launcher. CI runs the same checks on Ubuntu and Windows
with Python 3.9 and 3.12.

For an offline clone or an explicit destination, use the bundled installer:

```bash
python scripts/install.py --client codex --scope repo --mode copy --dry-run
python scripts/install.py --client claude-code --scope repo --mode copy --dry-run
python scripts/install.py --client generic --target /path/to/skills --mode copy --dry-run
```

Existing skills are not overwritten unless `--force` is supplied.

## Read next

| Document | Use it for |
|---|---|
| [Architecture](docs/architecture.md) | Composition, data contracts, and portability boundaries |
| [Integration](docs/integration.md) | Client setup and invocation strategy |
| [Evaluation](docs/evaluation.md) | Trigger measurement, output comparison, and release gates |
| [Design foundations](docs/design-foundations.md) | Normalized product and design principles |
| [Source notes](docs/source-notes.md) | Provenance and the limits of borrowed guidance |
| [Contributing](CONTRIBUTING.md) | Repository conventions and contribution flow |

## Honest limits

- A screenshot cannot establish runtime behavior or complete accessibility
  conformance.
- A static audit cannot prove comprehension or conversion impact.
- Phrase and pattern linting produces false positives; context decides.
- Visual budgets are defaults, not universal aesthetic laws.
- Skill activation is nondeterministic and must be measured in the target
  client before reporting a trigger rate.

## License

[MIT](LICENSE). Use the skills, adapt them, and keep the evidence boundary
intact.
