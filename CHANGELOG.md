# Changelog

All notable changes are documented here.

## [0.7.0] - 2026-10-09

Changes from the v0.6.0 best-practice review
([tracking issue](https://github.com/fromiron/leeskills/issues/12)). The
effect of these instruction and description changes on real clients is not yet
measured; the new routing and run-record evals exist to measure it.

### Evaluation ([#6](https://github.com/fromiron/leeskills/issues/6))

- `evaluate_trigger_results.py` requires three attempts per query by default
  and reports `insufficient` otherwise, lists individual query failures, and
  supports `critical` queries and run metadata without estimating missing
  values.
- Added `evals/catalog-routing.json` with full-catalog boundary cases, a
  run-record schema, static fixtures, `evaluate_routing_results.py`, and new
  output eval cases. Existing eval IDs and prompts are unchanged. No client
  runs are recorded yet.

### Partial installs ([#7](https://github.com/fromiron/leeskills/issues/7))

- `design-workflow` checks each focused skill: invoke it, read its sibling
  package relative to the installed workflow, or run a limited
  composition-map contract that produces no scores, verdicts, release
  decisions, or rendered token pages and never claims a missing tool ran.
- Documented the limited standalone scope in the READMEs, adapters, and docs.

### Verification scope ([#8](https://github.com/fromiron/leeskills/issues/8))

- `verify-changes` separates operation (`review`/`edit`) from verification
  (`targeted`/`release`). Targeted reports record unaffected checks as
  `out-of-scope` and are never release-ready; reports without `scope` keep the
  release behavior.
- Added the five conditional check IDs that `verify-changes` documented but
  its schema and validator rejected.
- Scoped `verify-content` inventories and `plan-structure` growth and
  alternative tests to the size of the change, and separated review, change,
  and gate completion in `review-motion`.

### Token proposals ([#9](https://github.com/fromiron/leeskills/issues/9))

- `review-visuals` separates normalizing an existing system, proposing a new
  system, verifying a rendered proposal, and building proposal files. Files
  are built only on request.
- The proposal schema accepts `mode: new-system` and per-value
  `basis: hypothesis` with a required rationale; the renderer marks design
  hypotheses in English, Korean, and Japanese. Existing safety checks are
  unchanged.

### Conditional references ([#10](https://github.com/fromiron/leeskills/issues/10))

- Moved the token proposal procedure and the interaction-governance and
  design-system lifecycle procedures into conditional references. Hard gates
  and the delivery convention stay in each `SKILL.md`.

### Descriptions ([#11](https://github.com/fromiron/leeskills/issues/11))

- Rewrote the ten descriptions around role, use conditions, and adjacent
  exclusions without renaming skills, and added near-miss negative trigger
  queries with new IDs.

### README

- Reorganized the English, Korean, and Japanese READMEs: the install command
  is followed by an example request, outputs and evidence labels are grouped
  together, the skill table leads with the skill name, and workflow sequences
  are listed in one table. Described the `review-visuals` token proposal page and its JSON renderer
  and moved clone-based installation next to the adapter links.
- Added light and dark SVG banners and a localized workflow diagram in
  `.github/assets/`, shown with `<picture>` so each follows the GitHub color
  scheme. Collapsed secondary sections, added a format-only finding example,
  and marked the evidence labels with colored badges.

### Skill names

- Renamed the entry skill to `design-workflow` and the nine focused skills to
  short action-and-target names. See the
  [migration table and installation guide](docs/skill-name-migration.md).
- Updated directories, frontmatter names, manifest, routing references, eval
  metadata, tests, and English, Korean, and Japanese installation examples.
  Preserved descriptions, existing eval IDs, trigger queries, helper interfaces,
  and JSON contracts during the rename. Historical entries below retain their
  original names.

### Delivery and evaluation

- Added a shared delivery convention to each independently installable skill:
  review findings include locations, evidence, minimal fixes, and verification;
  requested edits include actual changes; closeout includes checks, unknowns,
  and rollback. Apply changes before final verification and recheck later edits.
- Retained deletion and consolidation decisions in `verify-changes`, and kept
  content evidence, copy editing, and information structure as separate jobs.
- Added behavioral eval cases for review-only scope, authorized edits, and
  verification after the last change. Documented comparison across no-skill,
  previous-version, and revised-version runs, including false positives,
  omissions, unnecessary edits, and preserved product identity.
- Clarified what deterministic tests and the static network-import check
  establish, and distinguished installed packages from loaded skill bodies.
  No new trigger-rate or design-quality measurement is claimed.

### Token proposal page

- Rebuilt the `review-visuals` token proposal page as a documentation-style
  review page: navigation beside one content panel, token-name anatomy,
  color ramps, contrast pairs, type specimens, spacing bars, radius corners,
  container frames, one column per mapping context, and an unknown marker.
  Previews are drawn from the proposed values rather than from page styles.
- Added a Color foundation, current-to-proposed changes with deletions and
  renames, and English, Korean, and Japanese page chrome. Korean text keeps
  words intact when wrapping, and Japanese uses a Japanese font stack.
- Moved breakpoint values from primitives to semantic mappings so the page
  matches the skill's primitive and semantic rules.
- Added `token-proposal.schema.json`, a Korean example, a dependency-free
  validator for evidence, references, safe CSS values, contrast, and leftover
  placeholders, and a renderer that builds the page from validated data with
  the template's stylesheet. Updated the skill procedure, the orchestrator's
  composition map, evals, and tests, including checks that the page chrome
  stays within the skill's own visual budget.
- Structure was informed by the Codeit Design System documentation; no Codeit
  values, names, colors, or branding were copied.

### Maintenance

- Added a test that keeps the shared delivery section identical across skills,
  clarified its validator sentence, renamed composition-map headings and test
  names to the current skill names, and added the missing test shebang.

### Changed

- Expanded `edit-copy` (formerly `specificity-editor`) into one integrated
  product-copy review for factual support, specificity, natural English,
  Korean, and Japanese, product voice, terminology, and multilingual meaning
  and action parity.
- Added source-grounded language guidance, correction/suggestion/keep decisions,
  and multilingual trigger and output evals without adding an authorship
  detector or a second copy-editing skill.
- Preserved localization runtime contracts in copy review, corrected the scope
  and provenance of the Japanese easy-language source, and carried locale,
  decision, evidence, voice, parity, and unresolved fields through orchestrator
  reports and fallback execution.

## [0.6.0] - 2026-07-28

### Added

- Added an optional `component-contract-audit` interaction-governance extension
  for affordance mapping, decision-context action priority, action visibility
  and disclosure cost, grouping cues, and design-system lifecycle and adoption.
- Added a strict JSON schema, a deliberately blocked example, a dependency-free
  validator, and repository tests for the new extension.
- Added English, Korean, and Japanese trigger coverage plus output evals for
  misleading affordances, competing primary actions, hidden important actions,
  and bounded design-system adoption.

### Changed

- Expanded component-contract and final-verification guidance to distinguish CTA
  style counts from action priority, test same-look and same-behavior mappings,
  and verify grouping without requiring decorative containers.
- Added design-system inventory, governance, versioning, legacy mapping,
  coexistence, adoption, and deprecation questions without requiring one team
  structure or migration strategy.
- Added source notes grounded in Adham Dannaway's design-system and UI articles,
  including their explanatory images, while keeping their numerical examples
  out of universal pass/fail rules.

## [0.5.0] - 2026-07-17

### Added

- Added `component-contract-audit` for project-owned component purpose, anatomy,
  variants, applicable states, content constraints, responsive behavior,
  accessibility, token mappings, ownership, exceptions, and design-code parity.
- Added a structured component-contract schema, a deliberately blocked example,
  a deterministic validator, and English, Korean, and Japanese trigger and
  output evals.
- Added a reproducible Dead Simple Sites corpus protocol with an authorship
  boundary, fixed-snapshot sampling rules, a coding matrix, denominator
  reporting, counterexamples, and explicit observed/inferred/unknown states.

### Changed

- Added design-system and reusable-component routes to the orchestrator and its
  fallback composition contract.
- Expanded Codeit provenance from foundation values to its design principles,
  semantic color and iconography governance, and component documentation
  patterns such as anatomy, states, properties, usage, responsive behavior, and
  keyboard expectations.
- Added normalized principles for components as behavioral contracts and for
  evidence-backed identity exceptions within a consistent system.
- Replaced the current release label `research-backed` with `source-grounded`;
  the DSS contrasts remain useful maintainer heuristics until a declared sample
  is systematically coded.

## [0.4.0] - 2026-07-17

### Added

- Added role-based spacing, responsive-container, and font-aware typography
  guidance across the visual budget, slop audit, orchestration, accessibility,
  and final verification workflows.
- Added output evals for semantic responsive spacing, container ownership,
  contextual letter spacing and line height, and the WCAG text-spacing
  resilience boundary, plus multilingual trigger fixtures for the visual
  budget.
- Added a dependency-free single-page HTML template and workflow for proposing
  concrete primitive and semantic token names, values, mappings, evidence, and
  adoption status across Typography, Spacing, Layout, and Radius.
- Documented direct GitHub installation with `npx skills add fromiron/leeskills`,
  including catalog listing and selective installation.
- Added `skills` CLI installation paths to the generic, Codex, and Claude Code
  integration guides while retaining the bundled offline installer.

### Changed

- Expanded the Codeit Design System source notes from radius to spacing,
  layout, radius, and typography while keeping its project-specific scales,
  breakpoints, fonts, and numeric tokens out of universal pass/fail rules.
- Clarified that WCAG text-spacing checks verify resilience and do not prescribe
  ideal default letter spacing or line height for every font.

## [0.3.0] - 2026-07-16

### Added

- Added a generic-default pattern catalog to `slop-signal-audit` covering
  layout, visual-system, copy-shape, imagery, and motion defaults, each
  contrasted with recurring choices in the curated minimal corpus and routed
  to the matching focused skill. Catalog matches record the directly visible
  cue as `observed` and the interpretation with its own evidence state; the
  template-side defaults are classified as a maintainer heuristic.
- Added a quick-pass mode to `slop-signal-audit` (no scores, no verdict, up to
  five unpadded findings, skipped checks disclosed) and a matching quick-pass
  workflow to the orchestrator, with unchanged decision gates.
- Added output evals for the catalog-driven audit and the quick-pass scope,
  and quick-pass trigger fixtures in English, Korean, and Japanese.

### Changed

- Expanded the specificity phrase watchlist from 46 to 102 entries across
  English, Korean, and Japanese, adding `generic-context` and
  `contrast-framing` categories. Matches remain review prompts, not automatic
  failures.
- Recorded the corpus-contrast derivation of the catalog in the source notes.

### Fixed

- Reconfigured script output streams to UTF-8 so non-ASCII findings no longer
  crash on Windows consoles with legacy code pages.
- Matched watchlist phrases against the original text so reported offsets stay
  correct when casefolding changes string length, preferred the longest phrase
  for contained matches at the same position, and validated watchlist
  language, phrase, and category fields on load.

## [0.2.0] - 2026-07-14

### Added

- Added nested-radius scope and relationship records to visual budgets.
- Added deterministic semantic-step and concentric-offset checks for shared
  nested contours, with evidence labels and review-gated exceptions.
- Added English, Korean, and Japanese nested-radius trigger fixtures and output
  evals.

### Changed

- Distinguished radius-token count from nested-contour coherence across the
  visual budget, slop audit, orchestration, and final verification workflows.
- Added Codeit Design System radius guidance to the normalized source notes
  without adopting project-specific pixel tokens as universal defaults.

## [0.1.0] - 2026-07-14

### Added

- Eight focused anti-slop skills and one optional orchestration skill.
- Open Agent Skills-compatible `SKILL.md` packages.
- Deterministic, network-free Python helpers for scoring and validation.
- Trigger and output evaluation fixtures.
- Installation adapters for generic clients, OpenAI Codex, and Claude Code.
- Repository validation, unit tests, and GitHub Actions workflow.

### Changed

- Named the portable skill collection and package `leeskills` while preserving
  all existing individual skill IDs for compatibility.
- Added balanced English, Korean, and Japanese trigger fixtures with stable IDs.
- Added deterministic per-language aggregation for measured trigger results.
- Made unknown audit scores, visual budgets, accessibility checks, and final
  verification gates fail closed instead of accepting incomplete declarations.
- Aligned the orchestrator fallback contracts with focused-skill schemas.
- Added Windows CI coverage and portable Python launcher guidance.

### Status

This was a source-grounded initial release. Static validation is included, but
trigger rates and output quality must still be evaluated in each target agent
and on representative project artifacts.
