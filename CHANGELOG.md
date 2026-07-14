# Changelog

All notable changes are documented here.

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
