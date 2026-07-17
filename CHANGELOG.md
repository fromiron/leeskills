# Changelog

All notable changes are documented here.

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

This is a research-backed initial release. Static validation is included, but
trigger rates and output quality must still be evaluated in each target agent
and on representative project artifacts.
