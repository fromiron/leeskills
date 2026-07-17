---
name: structure-selector
description: Use this skill to choose the dominant information structure for a website, interface, portfolio, archive, product page, profile, institution, or task flow after the user and content are grounded. Use when deciding between a list, timeline, index, catalog, product explanation, or workflow. Do not use visual style trends or a default card grid as the primary selection criterion.
license: MIT
compatibility: Agent Skills-compatible clients. Core workflow is instruction-only; optional Python 3.9+ scripts use the standard library and no network.
metadata:
  author: leeskills contributors
  version: "0.5.0"
  languages: "en, ko, ja"
---


# Structure Selector

Choose one dominant content grammar that best supports the primary user task and
can scale as content grows.

## Prerequisite

Use a grounded content inventory when available. If the primary user, task, or
publishable content is unknown, mark the decision provisional rather than
inventing a structure around placeholder sections.

## Available dominant grammars

1. `identity-profile`
2. `chronological-ledger`
3. `writing-index`
4. `portfolio-index`
5. `product-service`
6. `collection-catalog`
7. `institution-information`
8. `task-workflow`
9. `justified-hybrid`

Read [references/patterns.md](references/patterns.md) when choosing among
similar patterns.

## Selection procedure

1. Restate the primary user and task.
2. List the minimum content records needed to complete that task.
3. Identify the natural organizing key: identity, time, title, project, offer,
   category, document, or action.
4. Choose the grammar that expresses that key directly.
5. Define the primary content sequence.
6. Define navigation only where the content volume or multiple tasks require it.
7. Specify the mobile and zoomed reflow order.
8. Run the growth test: model ten times the current records.
9. Reject at least two plausible alternatives and explain why.
10. Use `justified-hybrid` only when distinct user tasks cannot share one
    coherent grammar.

## Rules

- One page may contain many records while still using one grammar.
- A card is not a grammar. It is a possible container with a specific boundary
  or interaction.
- A hero is not automatically the first section. Start with the information
  needed to identify the artifact and proceed.
- Do not add testimonials, feature grids, FAQs, logo walls, statistics, or
  process sections unless grounded content and user needs require them.
- Use chronology when time explains the content.
- Use an index when names or titles are the primary retrieval keys.
- Use a catalog when repeated records share a stable schema.
- Use a task workflow when state and action order determine success.
- Responsive order must preserve meaning without relying on two-dimensional
  layout except where the content truly requires it.

## Output

Use:

- [assets/structure-decision.schema.json](assets/structure-decision.schema.json)
- [assets/structure-decision-example.json](assets/structure-decision-example.json)

Validate:

```bash
python scripts/validate_structure.py path/to/structure-decision.json
```

The decision must include:

- primary task;
- chosen grammar;
- organizing key;
- content sequence;
- navigation mode;
- responsive reflow;
- growth test;
- rejected patterns;
- hybrid justification when applicable;
- unresolved evidence gaps.

## Completion

A structure is ready when a new content item can be added without inventing a
new component family or changing the page's organizing logic.
