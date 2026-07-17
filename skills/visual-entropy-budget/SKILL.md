---
name: visual-entropy-budget
description: Use this skill to audit or define a constrained visual system for a website, interface, landing page, portfolio, or design system. Use when layout grammars, spacing scales, responsive containers, typefaces, type roles, typography settings, colors, radii, shadows, surfaces, CTA styles, imagery, or motion need consolidation or contextual review. Treat count limits as defaults, nested-radius rules as relationship checks, and letter spacing or line height as font- and context-dependent rather than universal numeric laws.
license: MIT
compatibility: Agent Skills-compatible clients. Core workflow is instruction-only; optional Python 3.9+ scripts use the standard library and no network.
metadata:
  author: leeskills contributors
  version: "0.4.0"
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
- spacing, breakpoint, and container tokens;
- typography specimens and computed styles;
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

Do not set universal numeric defaults for breakpoint values, spacing steps,
letter spacing, or line height. Use the project's tokens and rendered evidence.

Read [references/budget-rules.md](references/budget-rules.md) before applying
the defaults to data-rich, editorial, expressive, or brand-led work.

## Workflow

1. Identify the selected dominant structure.
2. Identify project-owned tokens, breakpoints, and documented exceptions before
   consulting external systems or repository defaults.
3. Inventory observed values for every budget metric and declare whether
   spacing, typography, responsive containers, and nested radii were evaluated
   or remain unknown.
4. Classify spacing uses as content gap, section gap, container padding, or a
   documented exception; merge raw values that perform the same role.
5. Compare spacing and container mappings at representative project
   breakpoints. Verify that responsive changes preserve grouping and avoid
   overflow or desktop-sized empty regions.
6. Evaluate typography by semantic role and actual typeface, fallback, script,
   language, size, weight, letter spacing, line height, line length, and
   rendered result.
7. Classify each nested rounded pair as a shared contour, an independent
   component, or a pill or circle, then test the applicable relationship.
8. Merge aliases, distinguish semantic variants from decorative variants, and
   compare observed counts with project limits or defaults.
9. Require an exception for each unexplained overage or measured relationship
   mismatch.
10. Test whether removing, merging, or remapping a variant loses state,
    hierarchy, meaning, brand recognition, readability, or accessibility.
11. Consolidate duplicate CTA, card, surface, radius, shadow, spacing, and type
    patterns while preserving justified communication roles.
12. Produce a budget report and verification plan.

Use:

- [assets/visual-budget.schema.json](assets/visual-budget.schema.json)
- [assets/visual-budget-example.json](assets/visual-budget-example.json)
- [assets/token-proposal-template.html](assets/token-proposal-template.html)

Check a structured budget:

```bash
python scripts/check_budget.py path/to/visual-budget.json
```

The script requires every core metric in both `observed` and `limits`. Omitted
nested-radius scope is treated as unknown. Documented exceptions and unverified
radius scope return `review-required`, not an automatic pass.

The script validates count metrics and declared radius relationships. It cannot
decide whether font-dependent typography or responsive spacing is appropriate;
record those conclusions separately with project and rendered evidence.

## Token proposal artifact

Create a token proposal when repeated raw values, inconsistent naming,
responsive drift, or unclear ownership indicate that a shared system is
needed, or when the user asks for token definitions. If the proposal spans
Typography, Spacing, Layout, or Radius, present the applicable foundations in
one self-contained HTML page.

Evidence gate: inspect the project's source tokens, CSS or theme values,
computed styles, representative content, and rendered viewports before filling
numeric proposals. If that evidence is unavailable, stop numeric design work,
request or locate it, and provide only a name-and-role scaffold with values
marked `unknown`. Do not invent a convenient scale merely to complete the page.

1. Inventory current names, raw values, usage frequency, responsive mappings,
   aliases, and exceptions before proposing a scale.
2. Extend the project's naming convention when one exists. Otherwise propose a
   consistent namespace and explain it.
3. Propose primitive tokens as reusable values without component meaning. Use
   an ordered scale or value-oriented names that remain stable under the
   project's responsive strategy.
4. Propose semantic tokens by role, such as content gap, section gap, container
   padding, body text, page title, card corner, or pill corner. Map each
   semantic token to one or more primitives by breakpoint, language, or theme.
5. Include exact proposed names and values, current-to-proposed mappings,
   deleted aliases, retained exceptions, rationale, evidence, and adoption
   status. Label unverified recommendations as `proposed` or `unknown`, never
   as existing standards.
6. Derive values by clustering the project's current system and testing the
   rendered result. Do not copy Codeit or another system's numbers or token
   names unless the project explicitly adopts that system.
7. For typography, propose letter spacing and line height separately for the
   actual font, fallback, script, language, size, weight, and role. Do not
   extrapolate one font's values across unrelated roles.
8. Copy the HTML template, replace or explicitly resolve every placeholder,
   duplicate rows as needed, and keep only sections supported by the scope.
9. Keep the artifact dependency-free and network-free. Preserve semantic
   headings, table captions, keyboard navigation, visible focus, reflow,
   reduced-motion behavior, and print readability.
10. Render and inspect representative wide and narrow viewports before sharing
    the page. Report the output path and unresolved decisions.

Use an existing project documentation or artifact directory when one is
clearly established; otherwise write `design-token-proposal.html` to the
project root. The artifact is a review proposal, not evidence that the project
has adopted the tokens.

## Rules

- Do not count text colors required for data or status as arbitrary accents.
- Prefer project tokens and breakpoints over values imported from another
  design system.
- When proposing a new shared system, provide concrete token names and values
  rather than only saying to "standardize" them, but only after tracing the
  values to project evidence.
- Leave a proposed numeric value `unknown` when source and rendered evidence
  cannot support it. Do not fabricate completeness.
- Require spacing values to express content grouping, section separation,
  container padding, or a documented exception. Do not require a universal
  4/8 scale.
- Verify responsive spacing and container behavior as relationships. Do not
  require every spacing token to shrink or every inner element to fill 100%.
- Do not apply universal letter-spacing or line-height thresholds. Flag a
  typography defect only from a project-token mismatch or rendered evidence
  such as clipping, overlap, broken wrapping, or impaired reading.
- Do not merge states that must remain distinguishable.
- Do not remove focus indicators, error states, selected states, or disabled
  states to meet a budget.
- A second typeface may be justified by an editorial, language, code, or brand
  role.
- A shadow may communicate elevation or drag state; a decorative glow does not
  inherit that justification.
- Cards are justified by meaningful boundaries, repeated records, or
  interaction—not by a desire to make every item look designed.
- A low radius-token count does not pass by itself. Shared nested contours must
  use a coherent inward relationship; independent components and pills require
  an explicit classification rather than forced arithmetic.
- Decorative images and authentic work samples are different categories.
- A documented exception is reviewable, not automatically acceptable.

## Output

For each metric include:

- observed count;
- limit;
- source of limit;
- overage;
- semantic roles;
- spacing roles and responsive mappings when in scope;
- container padding and width ownership when in scope;
- typography context, project token, and rendered evidence when in scope;
- duplicate candidates;
- nested-radius scope, relationships, rule, and evidence;
- exception and evidence;
- consolidation recommendation;
- verification method.

## Completion

The budget passes automatically only when no overage or measured radius
mismatch remains and nested-radius scope is not unknown. A documented exception
requires human review of the communication need before acceptance, and
accessibility states must remain intact. Do not fail or pass typography or
spacing solely because it differs from an external design system's numeric
table.
