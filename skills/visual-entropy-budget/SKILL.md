---
name: visual-entropy-budget
description: Use this skill to audit or define a constrained visual system for a website, interface, landing page, portfolio, or design system. Use when there are too many layout grammars, typefaces, type roles, accent colors, radii, shadows, surfaces, CTA styles, decorative image families, or motion patterns. Treat the limits as defaults that require justification when exceeded, not as universal aesthetic laws.
license: MIT
compatibility: Agent Skills-compatible clients. Core workflow is instruction-only; optional Python 3.9+ scripts use the standard library and no network.
metadata:
  author: leeskills contributors
  version: "0.1.0"
  languages: "en, ko, ja"
---


# Visual Entropy Budget

Limit the number of unrelated visual rules so content and interaction remain
legible.

## Definition

This skill uses "entropy budget" as a practical inventory of visual variants.
It is not a formal information-theory calculation.

## Inputs

Use as available:

- design tokens;
- component inventory;
- screenshots or rendered pages;
- CSS or theme definitions;
- brand requirements;
- data-visualization needs;
- interaction and state requirements;
- selected information structure.

## Default budget

| Metric | Default |
|---|---:|
| Dominant layout grammars | 1 |
| Typeface families | 1 |
| Typeface families, maximum without exception | 2 |
| Type roles | 4–6 |
| Accent colors | 0–1 |
| Radius tokens | 0–2 |
| Shadow levels | 0–1 |
| Surface styles | 1–3 |
| Primary CTA styles | 1 |
| Secondary CTA styles | 0–1 |
| Motion patterns | 0–2 |
| Decorative image families | 0 |

Read [references/budget-rules.md](references/budget-rules.md) before applying
the defaults to data-rich, editorial, expressive, or brand-led work.

## Workflow

1. Identify the selected dominant structure.
2. Inventory observed values for every budget metric.
3. Merge aliases that are visually or semantically equivalent.
4. Distinguish semantic variants from decorative variants.
5. Compare observed counts with project limits or defaults.
6. Require an exception for each overage.
7. Test whether removing or merging the variant loses state, hierarchy,
   meaning, brand recognition, or accessibility.
8. Consolidate duplicate CTA, card, surface, radius, shadow, and type patterns.
9. Preserve exceptions that have a documented communication job.
10. Produce a budget report and verification plan.

Use:

- [assets/visual-budget.schema.json](assets/visual-budget.schema.json)
- [assets/visual-budget-example.json](assets/visual-budget-example.json)

Check a structured budget:

```bash
python scripts/check_budget.py path/to/visual-budget.json
```

The script requires every core metric in both `observed` and `limits`.
Documented exceptions return `review-required`, not an automatic pass.

## Rules

- Do not count text colors required for data or status as arbitrary accents.
- Do not merge states that must remain distinguishable.
- Do not remove focus indicators, error states, selected states, or disabled
  states to meet a budget.
- A second typeface may be justified by an editorial, language, code, or brand
  role.
- A shadow may communicate elevation or drag state; a decorative glow does not
  inherit that justification.
- Cards are justified by meaningful boundaries, repeated records, or
  interaction—not by a desire to make every item look designed.
- Decorative images and authentic work samples are different categories.
- A documented exception is reviewable, not automatically acceptable.

## Output

For each metric include:

- observed count;
- limit;
- source of limit;
- overage;
- semantic roles;
- duplicate candidates;
- exception and evidence;
- consolidation recommendation;
- verification method.

## Completion

The budget passes automatically only when no overage remains. A documented
exception requires human review of the communication need before acceptance,
and accessibility states must remain intact.
