---
name: slop-signal-audit
description: Use this skill to audit an existing website, UI, portfolio, landing page, design system, or generated visual artifact for generic, unsupported, redundant, inaccessible, or purposeless design signals. Use when the user asks for an anti-slop review, a simplification audit, a scored diagnosis, or a prioritized removal plan. Do not use it to determine whether AI authored the artifact.
license: MIT
compatibility: Agent Skills-compatible clients. Core workflow is instruction-only; optional Python 3.9+ scripts use the standard library and no network.
metadata:
  author: leeskills contributors
  version: "0.2.0"
  languages: "en, ko, ja"
---


# Slop Signal Audit

Identify observable design and content problems, distinguish evidence from
inference, score the artifact, and prioritize remediation.

## Boundary

This is not an AI-authorship detector. Similar visual patterns can result from
templates, conventions, deadlines, team decisions, or generative tools. Report
the symptom and its impact, not an unsupported origin story.

## Inputs

Collect as available:

- screenshots or live rendered views;
- copy;
- DOM or semantic structure;
- component and token inventory;
- motion inventory;
- user and primary task;
- real proof, constraints, and outcomes;
- target viewport and accessibility baseline.

Record anything not inspected.

## Evidence classes

Use exactly:

- `observed`
- `measured`
- `inferred`
- `unknown`

An inferred finding must state its supporting evidence. An unknown item receives
no passing credit merely because it was not visible.

## Audit procedure

1. Define the artifact, intended user, primary task, and success condition.
2. Inventory all visible sections, component families, CTAs, claims, images,
   motion patterns, and navigation structures.
3. Mark unsupported claims and absent evidence before judging aesthetics.
4. Find repetition that adds no new decision-relevant information.
5. Identify visual variants that do not communicate state, hierarchy, or brand.
6. Inspect nested rounded surfaces for repeated tokens, inward semantic steps,
   or measured contour offsets; do not treat token count alone as coherence.
7. Check whether images demonstrate real work or merely occupy space.
8. Check motion for a functional purpose and reduced-motion behavior.
9. Run the accessibility guard or mark untested items as unknown.
10. Score every category using [references/rubric.md](references/rubric.md).
11. List project hard failures independently of the score.
12. Order recommendations by user impact, confidence, and reversibility.

## Scoring

Use the bundled schema and template:

- [assets/audit.schema.json](assets/audit.schema.json)
- [assets/audit-example.json](assets/audit-example.json)
- [assets/report-template.md](assets/report-template.md)

The score is a decision aid, not a scientific measure.

When a structured audit JSON is available, run:

```bash
python scripts/score_audit.py path/to/audit.json
```

Use `--output result.json` to save the computed result.

## Project hard failures

Block a passing verdict when directly supported evidence shows any of:

- fabricated customer, metric, quote, award, result, capability, or case study;
- mock UI presented as a functioning product without disclosure;
- keyboard focus, labels, errors, semantic structure, or alternatives removed
  for visual cleanliness;
- scroll hijacking without an equivalent user-controlled path;
- essential information available only through motion, color, hover, or a
  pointer-only interaction;
- nonessential interaction motion without a disable or reduction path;
- unsupported claims presented as verified facts.

Label legal or standards compliance separately. A project hard failure is not
by itself a legal conclusion.

## Recommendation format

For every recommendation include:

- evidence state;
- exact location;
- problem;
- user or trust impact;
- smallest effective change;
- verification method;
- confidence.

Prefer removal or consolidation before adding new components.
Route detailed nested-radius measurement to `visual-entropy-budget` and verify
the repaired relationship with `prune-and-verify`.

## Completion

Conclude with:

- quality score;
- derived slop-risk score;
- verdict;
- hard failures;
- top five changes;
- unknowns that could change the result.
