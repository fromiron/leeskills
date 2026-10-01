---
name: verify-changes
description: Use this skill after grounding, redesign, rewriting, or simplification to remove unsupported or unnecessary elements and verify that the result still preserves user tasks, evidence, identity, accessibility, responsive behavior, and reduced-motion behavior. Use it for final anti-slop QA, deletion tests, before-and-after verification, release checks, or a reversible change plan. Do not use it as a substitute for full usability research or complete accessibility conformance testing.
license: MIT
compatibility: Agent Skills-compatible clients. Core workflow is instruction-only; optional Python 3.9+ scripts use the standard library and no network.
metadata:
  author: leeskills contributors
  version: "0.6.0"
  languages: "en, ko, ja"
---

# Verify Changes

Remove the least necessary material first, then prove that the remaining
artifact still supports its user, content, identity, and access needs.

## Delivery

For a review-only request, report each material issue's location, evidence,
smallest fix, and verification method; leave the artifact files unchanged.

For requested edits, follow **diagnosis → change plan → authorized patch →
final verification**. Include the actual diff or changed-file paths. A proposal
is not an applied fix. Report checks actually run and their outcomes, unverified
items, and how to undo your changes while preserving unrelated work.

Verify through the intended user flow where available and state environment
limits. Bundled report validators check declarations, not product behavior.
Re-run affected checks after any later edit. Keep the delivery proportionate to
the request; a small fix does not need a full report.

## Boundary

This skill verifies an artifact against supplied evidence and declared project
requirements. It does not establish conversion lift, user comprehension, legal
compliance, or complete WCAG conformance without the corresponding research and
testing.

## Inputs

Use as available:

- before and after artifacts;
- primary user, primary task, and success condition;
- grounded content inventory;
- structure decision and visual budget;
- component, affordance, action-governance, and design-system lifecycle reports
  when those dimensions changed;
- motion and accessibility reports;
- supported viewport, input, browser, and assistive-technology requirements;
- release constraints and explicitly accepted risks.

Record untested conditions as `unknown`. Do not silently treat absence of
evidence as a pass.

## Evidence states

For findings and test evidence, use:

- `observed`
- `measured`
- `inferred`
- `unknown`

For test status, use:

- `pass`
- `fail`
- `unknown`
- `not-applicable`

## Procedure

1. Restate the user, task, success condition, and artifact scope.
2. Compare the before and after versions where both exist.
3. Inventory proposed deletions and consolidations, with the smallest reversible
   change plan, rollback method, and checks needed after each change.
4. Apply the deletion test: identify the exact task, evidence, identity, or
   accessibility value lost. When edits are requested, apply justified removals
   or consolidations before the final checks below. For review-only requests,
   leave files unchanged and label untested predictions as inferred or unknown.
5. Apply the substitution test: replace names, products, or organizations with
   unrelated ones and flag copy or imagery that still appears equally valid.
6. Check semantic resilience: confirm the reading order, headings, labels,
   links, and controls remain understandable without decorative styling.
7. Check visual hierarchy at a glance without using style as proof of meaning.
8. When nested rounded surfaces exist or changed, repeat the declared semantic
   step or concentric-offset check and compare before and after contours.
9. Check growth: model substantially more records, projects, posts, or states
   without adding an unrelated layout grammar.
10. Check reflow and input paths at the declared accessibility baseline.
11. Check reduced-motion behavior for retained nonessential motion.
12. Check provenance for claims, images, metrics, quotes, and product evidence.
13. When interaction treatments changed, repeat the applicable affordance,
    action-hierarchy, action-visibility, and grouping-cue checks.
14. When a design-system migration or adoption plan changed, verify inventory,
    mappings, coexistence, ownership, changelog, and deprecation gates.
15. Classify each check as pass, fail, unknown, or not applicable.
16. Block release for required failures or unknowns unless the exact risk is
    documented and explicitly accepted by an accountable owner.
17. If a check leads to another authorized edit, apply it and repeat the affected
    checks against the changed artifact. Report applied and proposed changes
    separately, with actual outcomes, remaining unknowns, and rollback steps.

Use [references/verification-tests.md](references/verification-tests.md) for
check definitions.

## Required verification set

Unless the artifact makes a check genuinely irrelevant, include:

- deletion;
- substitution;
- semantic or unstyled structure;
- glance hierarchy;
- primary-task completion path;
- growth;
- reflow;
- keyboard and visible focus;
- reduced motion;
- provenance.

Also include `nested-radius-coherence` when nested rounded surfaces exist or a
radius, padding, border, or surface relationship changed. Mark it genuinely not
applicable when the artifact has no such relationship.

Include these checks when their corresponding scope exists or changed:

- `affordance-mapping`;
- `action-hierarchy`;
- `action-visibility`;
- `grouping-cues`;
- `system-lifecycle`.

A screenshot can support visual observations but cannot pass keyboard,
semantics, runtime behavior, reflow, assistive-technology, reduced-motion,
action frequency, or design-system adoption checks by itself.

## Accepted-risk syntax

Use the exact token:

```text
<check-id>:<status>
```

Examples:

```text
assistive-technology:unknown
legacy-reflow:fail
```

An accepted risk does not convert a failed check into a pass or clear the
mechanical `release_ready` blocker. It records an owner decision outside the
validator.

## Structured report

Use:

- [assets/verification.schema.json](assets/verification.schema.json)
- [assets/verification-example.json](assets/verification-example.json)
- [assets/change-plan-template.md](assets/change-plan-template.md)

Validate a report with:

```bash
python scripts/validate_verification.py path/to/verification.json
```

The script validates the report contract and required-check gates. It does not
inspect CSS, render contours, operate disclosures, measure discoverability, or
perform browser, accessibility, usability, or adoption testing.

## Recommendation order

Prefer, in order:

1. remove unsupported claims or fabricated proof;
2. restore misleading or missing interaction and accessibility cues;
3. expose or provide an adequate path to required primary, frequent, or
   recovery actions;
4. remove duplicate sections and actions;
5. consolidate variants that communicate no distinct state;
6. replace decorative evidence substitutes with real evidence or nothing;
7. reduce purposeless motion;
8. simplify copy without removing necessary constraints;
9. remove grouping containers only when lighter cues preserve the relationship;
10. preserve or restore labels, semantics, focus, errors, alternatives, and
    bounded migration paths.

## Completion rule

Stop pruning when another removal would make the primary task harder, weaken
verified evidence, erase meaningful identity, create a false affordance, hide a
necessary action, break a component contract or migration path, or reduce
accessibility.

Conclude with:

- release readiness;
- required failures and unknowns;
- accepted risks;
- deleted, consolidated, retained, and restored elements;
- verification methods and owners;
- remaining assumptions and limitations.
