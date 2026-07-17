---
name: component-contract-audit
description: Use this skill to audit or define reusable UI component contracts across design files, documentation, Storybook, source code, and live usage. Use when anatomy, required and optional parts, variants, states, content constraints, responsive behavior, accessibility behavior, semantic tokens, or design-code parity need review. Do not use it for a visual-token-only request or to copy another design system's component specifications.
license: MIT
compatibility: Agent Skills-compatible clients. Core workflow is instruction-only; optional Python 3.9+ scripts use the standard library and no network.
metadata:
  author: leeskills contributors
  version: "0.5.0"
  languages: "en, ko, ja"
---

# Component Contract Audit

Treat a reusable component as a behavioral, content, and implementation contract,
not as a screenshot or a collection of visual variants.

## Goal

Make the component predictable for users and maintainers across design,
documentation, code, responsive contexts, languages, input methods, and
accessibility settings.

## Inputs

Use as available:

- component purpose and primary user task;
- project source of truth and ownership;
- design-library component and variants;
- documentation or Storybook;
- source code, tests, and rendered examples;
- real product usage;
- project tokens, breakpoints, and content rules;
- supported browsers, devices, input methods, and accessibility baseline.

Record missing surfaces as `unknown`. Do not infer runtime behavior from a
design file or screenshot.

## Evidence states

Use exactly:

- `observed`
- `measured`
- `inferred`
- `unknown`

An observed visual state is not measured runtime support. Keep those statements
separate.

## Contract dimensions

Review the applicable dimensions:

1. **Purpose and selection** — when to use the component and when not to.
2. **Anatomy** — required, optional, and conditional parts.
3. **Variants and sizes** — distinct communication or task roles.
4. **States** — visual state, behavior, feedback, and accessible representation.
5. **Interaction** — keyboard, pointer, touch, focus, timing, and dismissal.
6. **Content** — labels, length, localization, truncation, overflow, and errors.
7. **Responsive behavior** — what changes and what information must remain.
8. **Tokens** — semantic color, type, spacing, radius, elevation, and icon roles.
9. **Composition** — nesting, adjacency, priority, and repeated-group behavior.
10. **Accessibility** — name, role, value, relationships, focus, status, and target.
11. **Ownership** — source of truth, change process, exceptions, and deprecation.
12. **Parity** — alignment among design, documentation, code, and live usage.

Read [references/contract-rules.md](references/contract-rules.md) before
normalizing another system's component guidance.

## Procedure

1. Restate the component purpose, primary user, task, and success condition.
2. Identify the project-owned source of truth and accountable owner. When
   ownership is shared or disputed, record that as a finding.
3. Inventory design, documentation, code, tests, and representative live usage.
4. Define anatomy with required, optional, and conditional parts.
5. Define applicable variants and states from the component's behavior. Do not
   require every possible state by default.
6. Record visual treatment, behavior, accessible representation, and evidence
   separately for every applicable state.
7. Test content expansion, localization, empty values, long labels, and error
   or status messages where applicable.
8. Test representative responsive contexts and input paths. Preserve task,
   meaning, and recovery rather than only matching dimensions.
9. Map visual values to project semantic tokens. Route detailed token-system
   consolidation to `visual-entropy-budget`.
10. Compare design, documentation, code, and live usage. Classify each inspected
    surface as `aligned`, `drift`, `unknown`, or `not-inspected`.
11. Record justified identity or task exceptions with evidence, owner, and a
    review trigger. Do not erase distinctive choices merely to match a generic
    component library.
12. Prioritize the smallest changes that restore user-facing behavior and
    maintainer clarity.
13. Validate the structured report.

## State scope

Consider, when applicable:

- default;
- hover for pointer input;
- focus-visible;
- active or pressed;
- selected or checked;
- expanded or collapsed;
- disabled or read-only;
- loading or progress;
- empty;
- error, warning, success, or confirmation;
- dragging, dropping, or reordered;
- timed, dismissed, or interrupted.

A state is covered only when its required behavior and accessible representation
are supported. A static variant alone does not prove coverage.

## Design-code parity

Inspect these surfaces independently:

- design library;
- component documentation;
- source code and tests;
- representative live usage.

Use:

- `aligned` — inspected behavior matches the declared contract;
- `drift` — inspected behavior materially differs;
- `unknown` — evidence exists but is insufficient;
- `not-inspected` — the surface was outside the supplied scope.

A project may intentionally make one surface authoritative. The other required
surfaces still need an update path; source-of-truth status does not excuse drift.

## Hard gates

Block a mechanical release-ready result when directly supported evidence shows:

- an operable component lacks an accessible name, keyboard path, or visible
  focus where required;
- required error, status, selection, or progress information is absent or
  available only through color, motion, hover, or pointer input;
- a required responsive context clips, hides, or reorders information so the
  primary task or recovery path is lost;
- design or documentation presents required behavior that the implementation
  does not support;
- mock component behavior is presented as live product capability without
  disclosure;
- a required state or accessibility check remains `fail` or `unknown`.

An accepted risk records an owner decision but does not mechanically convert a
failure or unknown into a pass.

## Output

Use:

- [assets/component-contract.schema.json](assets/component-contract.schema.json)
- [assets/component-contract-example.json](assets/component-contract-example.json)

Validate:

```bash
python scripts/validate_component_contract.py path/to/component-contract.json
```

The validator checks report structure and declared release blockers. It does not
render the component, operate a browser, compare screenshots, or run assistive
technology.

## Recommendation format

For each material finding include:

- evidence state;
- exact component, surface, and state;
- contract expectation;
- observed drift or unknown;
- user and maintainer impact;
- smallest effective change;
- verification method;
- owner and confidence.

## Completion

The audit is complete when applicable anatomy, states, content, responsive
behavior, accessibility, tokens, ownership, and parity are explicit; required
failures and unknowns remain visible; and every recommended change has a
repeatable verification method.
