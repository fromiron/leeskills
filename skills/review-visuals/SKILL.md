---
name: review-visuals
description: Use this skill to audit or define a constrained visual system for a website, interface, landing page, portfolio, or design system. Use when layout grammars, spacing scales, responsive containers, typefaces, type roles, typography settings, colors, radii, shadows, surfaces, CTA styles, imagery, or motion need consolidation or contextual review. Treat count limits as defaults, nested-radius rules as relationship checks, and letter spacing or line height as font- and context-dependent rather than universal numeric laws.
license: MIT
compatibility: Agent Skills-compatible clients. Core workflow is instruction-only; optional Python 3.9+ scripts use the standard library and no network.
metadata:
  author: leeskills contributors
  version: "0.6.0"
  languages: "en, ko, ja"
---


# Review Visuals

Limit the number of unrelated visual rules so content and interaction remain
legible.

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

## Definition

This skill uses "entropy budget" as a practical inventory of visual variants.
It is not a formal information-theory calculation.

## Choose a path

Identify the path from the request before inspecting values. Paths can
combine, but each keeps its own evidence rule.

| Path | When | Numbers come from | Output |
|---|---|---|---|
| Audit or normalize an existing system | Default for an existing artifact | Project tokens, CSS or theme values, computed styles, rendered evidence | Findings and recommendations |
| Propose a new system | The user asks for a new visual system and no project system exists for the scope | Stated requirements, content, brand, and platform constraints, labeled as design hypotheses | Proposal with rationale, assumptions, and open decisions |
| Verify a proposal | After a proposal is rendered | Contrast, reflow, and relationship checks run on the rendered proposal | Check results; unrendered values stay unverified |
| Build a token proposal file | Only when the user asks for, or explicitly chooses, a proposal JSON or HTML page | One of the paths above | Proposal JSON and HTML page |

- Never present a design hypothesis as an existing project value, standard, or
  measurement. Never present an unrendered value as measured.
- Leave contexts the user has not decided, such as a dark theme, as open
  decisions instead of filling values.
- An audit can end with findings. When a shared system would help, recommend a
  token proposal and offer the file; do not create files the user did not ask
  for.

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
- [assets/token-proposal.schema.json](assets/token-proposal.schema.json)
- [assets/token-proposal-example.json](assets/token-proposal-example.json)
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

Recommend a token proposal when repeated raw values, inconsistent naming,
responsive drift, or unclear ownership indicate that a shared system is
needed. Build the proposal files only when the user asks for token
definitions or a proposal page, or explicitly chooses that deliverable. The
page presents the applicable Color, Typography, Spacing, Layout, and Radius
foundations in one self-contained HTML file.

Evidence gate for normalizing an existing system (`"mode": "normalize"`, the
default): inspect the project's source tokens, CSS or theme values, computed
styles, representative content, and rendered viewports before filling numeric
proposals. If that evidence is unavailable, stop numeric design work, request
or locate it, and provide only a name-and-role scaffold with values marked
`unknown`. Do not invent a convenient scale merely to complete the page.

New system (`"mode": "new-system"`): when the user asks for a new system and
the project has no tokens for the scope, a value may be a design hypothesis.
Mark it `"basis": "hypothesis"` with a `rationale` tied to the stated
requirements, content, brand, or platform. Keep values the project already
supplied, such as an approved brand color, as observed with evidence. The
validator rejects hypotheses in normalize mode and hypotheses without a
rationale. Render the proposal and run its checks before reporting any result
as measured.

### Decide the tokens

1. Inventory current names, raw values, usage frequency, responsive mappings,
   aliases, and exceptions before proposing a scale.
2. Extend the project's naming convention when one exists. Otherwise propose a
   consistent namespace and show its parts, for example category and step for
   primitives and category and role for semantic tokens.
3. Propose primitive tokens as single reusable values without component
   meaning. Do not give a primitive per-breakpoint values.
4. Propose semantic tokens by role, such as text primary, content gap, section
   gap, container padding, page title, card corner, or pill corner. Map each
   semantic token to primitives per context: `default`, a breakpoint, a
   language, or a theme such as `light` and `dark`.
5. Record current-to-proposed mappings, merged and renamed aliases, deletions,
   retained exceptions, rationale, evidence, and adoption status. Label
   unverified recommendations as `proposed` or `unknown`, never as existing
   standards.
6. In normalize mode, derive values by clustering the project's current system
   and testing the rendered result. In new-system mode, derive each hypothesis
   from the stated requirements, content, and platform, then render and test
   it. Do not copy Codeit or another system's numbers, token names, or
   branding unless the project explicitly adopts that system.
7. For color, keep status, data, and validation colors separate from accents
   and declare the background each text or status color must meet, with the
   required contrast ratio.
8. For typography, propose letter spacing and line height separately for the
   actual font, fallback, script, language, size, weight, and role. Do not
   extrapolate one font's values across unrelated roles.

### Build the page

Prefer the data path, which keeps the page consistent and checkable:

1. Write the proposal as JSON matching
   [assets/token-proposal.schema.json](assets/token-proposal.schema.json);
   [assets/token-proposal-example.json](assets/token-proposal-example.json)
   shows every field of a normalize proposal, and
   [assets/token-proposal-new-system-example.json](assets/token-proposal-new-system-example.json)
   shows design hypotheses in a new-system proposal. Set `language` to the
   reader's language (`en`, `ko`, or `ja` chrome is bundled) and write titles,
   roles, and notes in that language.
2. Validate it. The validator rejects observed values without evidence,
   hypotheses without a rationale or outside new-system mode, references to
   undefined primitives, CSS values that could inject rules or load resources,
   and computable contrast below the declared minimum:

   ```bash
   python scripts/validate_token_proposal.py proposal.json
   ```

3. Render the page from the validated JSON. The renderer reuses the
   template's stylesheet and localized chrome, omits foundations that are not
   in scope, and refuses invalid input:

   ```bash
   python scripts/render_token_proposal.py proposal.json --output design-token-proposal.html
   ```

4. Open the page at a wide viewport and at about 375 CSS px. Confirm that
   previews draw the proposed values, unknown values show the unknown marker,
   design hypotheses show the hypothesis marker,
   the page does not scroll horizontally, and tables scroll only inside their
   own regions. Fix the data, not the generated markup, then render again.
5. Check the final file and report the output path, unknown values, and open
   decisions:

   ```bash
   python scripts/validate_token_proposal.py proposal.json --html design-token-proposal.html
   ```

Without Python, copy
[assets/token-proposal-template.html](assets/token-proposal-template.html),
replace or explicitly resolve every placeholder, duplicate rows, ramp steps,
and frames as needed, delete out-of-scope sections from both the page and its
navigation, and state that the deterministic checks were not run.

The page must keep: the status badge and `data-proposal-status="proposed"`;
previews drawn from the proposed values (color ramps and pairs, type
specimens, spacing bars, radius corners, container frames); one column per
mapping context; the unknown marker instead of guessed values; the
design-hypothesis marker on new-system values; the changes and
decisions sections; semantic headings, table captions, keyboard-scrollable
table regions, visible focus, reflow, reduced-motion behavior, and print
readability; and no network requests. The template's own chrome follows the
default budget in this skill; do not add decorative gradients, glows, or
shadows to it.

When the user requested the files, write them where the user asked, or to an
established project documentation or artifact directory; otherwise write
`design-token-proposal.html` to the project root and report the path. The
artifact is a review proposal, not evidence that the project has adopted the
tokens.

## Rules

- Do not count text colors required for data or status as arbitrary accents.
- Prefer project tokens and breakpoints over values imported from another
  design system.
- When proposing a shared system, provide concrete token names and values
  rather than only saying to "standardize" them. Trace normalized values to
  project evidence; label new-system values as design hypotheses with a
  rationale.
- Leave a proposed numeric value `unknown` when neither project evidence nor a
  requested new-system rationale supports it. Do not fabricate completeness.
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
