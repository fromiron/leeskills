---
name: content-grounding
description: Use this skill before designing or rewriting a website, interface, landing page, portfolio, case study, or product narrative when claims must stay grounded in supplied source material. Use it to build a content inventory, trace evidence, identify missing facts, and prevent invented customers, metrics, quotes, outcomes, capabilities, or sections. Do not use it to fabricate placeholder marketing content.
license: MIT
compatibility: Agent Skills-compatible clients. Core workflow is instruction-only; optional Python 3.9+ scripts use the standard library and no network.
metadata:
  author: leeskills contributors
  version: "0.5.0"
  languages: "en, ko, ja"
---


# Content Grounding

Create an evidence-backed content inventory before structure, copy, or visual
design decisions are made.

## Goal

Separate what is known from what is missing. Give downstream skills enough
specific material to design with, without filling gaps through invention.

## Inputs

Use any supplied:

- briefs and requirements;
- product or project documentation;
- existing page copy;
- verified customer or user research;
- case-study notes;
- prices, dates, scope, constraints, and outcomes;
- screenshots or product behavior;
- source URLs and files.

Do not treat a visual mockup as proof that a capability exists.

## Status model

Every factual statement must have one status:

- `verified` — directly supported by a source.
- `inferred` — reasonably derived from sources; must include rationale.
- `placeholder` — explicitly temporary and must not ship as factual content.
- `prohibited` — known to be false, fabricated, private, expired, or not
  approved for use.

Verified facts require a source reference. Inferences require both supporting
sources and a plain-language rationale.

## Workflow

1. Define the artifact type, primary user, primary task, and success condition.
2. Extract atomic claims from every supplied source.
3. Give each claim a stable ID and one status.
4. Record source location, owner if known, date, and confidence.
5. Group usable content into identity, offer, task support, proof, constraints,
   and actions.
6. List required but missing information.
7. List material that must not be generated or published.
8. Detect contradictions and stale statements.
9. Produce a downstream-safe inventory.
10. Validate structured output with the bundled script.

Use:

- [assets/content-inventory.schema.json](assets/content-inventory.schema.json)
- [assets/content-inventory-example.json](assets/content-inventory-example.json)
- [references/inventory-rules.md](references/inventory-rules.md)

Validation:

```bash
python scripts/validate_inventory.py path/to/content-inventory.json
```

## Design consequences

- No evidence means no factual claim.
- No real testimonial means no testimonial section.
- No verified customer list means no logo wall.
- No quantified result means use a qualitative, attributable description or
  mark the outcome as missing.
- No real feature means do not draw a fake interface that implies it exists.
- A placeholder can be used in a clearly marked internal wireframe, but it must
  not be presented as release-ready proof.
- Duplicate content should be consolidated at the inventory level before
  visual design.

## Output

Produce:

1. content context;
2. facts with status and provenance;
3. contradictions;
4. missing content;
5. prohibited generation;
6. safe claims;
7. allowed placeholders for internal-only use;
8. questions that materially affect structure.

Do not ask for low-impact details merely to fill a template. When the user
cannot provide a missing fact, design around the gap rather than inventing it.

## Completion

The inventory is ready when every publishable factual claim traces to a source,
all unknowns are explicit, and downstream skills can distinguish safe content
from prohibited generation.
