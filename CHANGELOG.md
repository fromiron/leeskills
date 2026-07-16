# Changelog

All notable changes are documented here.

## [0.3.0] - 2026-07-16

### Added

- Added a generic-default pattern catalog to `slop-signal-audit` covering
  layout, visual-system, copy-shape, imagery, and motion defaults, each
  contrasted with recurring choices in the curated minimal corpus and routed
  to the matching focused skill.
- Added a quick-pass workflow to the orchestrator for small artifacts and
  early drafts, with explicit skipped-check disclosure and unchanged decision
  gates.
- Added output evals for the catalog-driven audit and the quick-pass scope.

### Changed

- Expanded the specificity phrase watchlist from 46 to 102 entries across
  English, Korean, and Japanese, adding `generic-context` and
  `contrast-framing` categories. Matches remain review prompts, not automatic
  failures.
- Recorded the corpus-contrast derivation of the catalog in the source notes.

### Fixed

- Reconfigured script output streams to UTF-8 so non-ASCII findings no longer
  crash on Windows consoles with legacy code pages.

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
