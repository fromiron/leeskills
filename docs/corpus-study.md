# Curated minimal-site corpus study

Accessed: **2026-07-17**

## Purpose

This document makes the Dead Simple Sites influence reviewable and repeatable.
It separates the curator's published criteria, direct observations of linked
sites, and maintainer interpretation.

## Authorship boundary

Dead Simple Sites describes itself as a curated collection of minimal sites. A
listing alone does not prove that a site was created entirely by a human or
without generative tools.

Use **curated minimal-site corpus** in repository claims. Do not use
`human-made`, `human-designed`, or similar authorship labels without direct,
site-specific provenance.

## Primary source

- Dead Simple Sites  
  https://deadsimplesites.com/

The homepage directly states these curation constraints:

- no overly animated content;
- no scroll jacking;
- no excessive storytelling;
- less, but better.

Those statements support the repository's motion and narrative guardrails. They
do not by themselves establish layout, typography, color, imagery, component,
accessibility, or authorship rules for every linked site.

## Current encoded evidence

| Evidence | State | What it supports |
|---|---|---|
| Dead Simple Sites homepage criteria | observed | The curator explicitly rejects excessive animation, scroll hijacking, and excessive storytelling. |
| Dead Simple Sites ordered link directory | observed | The corpus is broad and changes over time; a snapshot date is required for repeatable sampling. |
| Juan Abrigo live page, inspected 2026-07-17 | observed | One concrete example of direct identity copy, a small set of links, and a chronological writing index with reading-time metadata. |
| Cross-site structural contrasts in `generic-default-catalog.md` | inferred | Maintainer interpretation from a curated sample; not yet a systematically coded result. |
| Template and generated-page defaults in `generic-default-catalog.md` | inferred | Maintainer heuristic; not a sampled comparison corpus. |

The current repository therefore has source-grounded principles and useful
heuristics, but not a complete empirical corpus study.

## Reproducible sampling protocol

For the next corpus revision:

1. Freeze the Dead Simple Sites link order and access date before reviewing
   individual sites.
2. Choose the sample before coding. Use all visible entries or a fixed rule such
   as the first `N`; record `N`, exclusions, redirects, inaccessible pages, and
   duplicate domains.
3. Store only review metadata needed for provenance: title, URL, access date,
   availability, reviewer, and notes. Do not copy site assets into this
   repository without permission.
4. Inspect representative wide and narrow viewports when the live site is
   available. Record runtime behavior separately from screenshots.
5. Code the visible cue as `observed`. Record interpretation, justification,
   authenticity, task fit, or authorship separately as `measured`, `inferred`,
   or `unknown`.
6. Run a second review on a subset. Record disagreements instead of silently
   merging them.
7. Report counts and denominators. Do not write “most,” “typically,” or
   “recurring” without the supporting `n/N` and missing-data count.
8. Promote a corpus observation to a skill rule only when it also has an
   independent task, content, maintainability, or accessibility rationale.
9. Keep counterexamples. Minimal sites can be expressive, image-led, dense, or
   multi-column when the content and task justify those choices.
10. Never use the corpus to infer AI or human authorship.

## Coding matrix

Record one row per inspected site with these fields:

| Field | Example values |
|---|---|
| Snapshot | source order, title, URL, access date, availability |
| Primary identity | person, studio, product, publication, institution, unknown |
| Primary task | identify, read, compare work, contact, buy, use tool, unknown |
| Dominant grammar | profile, ledger, index, catalog, product explanation, workflow, hybrid |
| First-screen content | identity, offer, work, navigation, image, unknown |
| Navigation | none, linear links, anchors, global, filter, mixed |
| Record schema | fields repeated across projects, posts, products, or rows |
| Containers | plain flow, rules, cards, panels, mixed |
| Typography | type families, semantic roles, hierarchy mechanism |
| Color | accent roles, state roles, theme behavior |
| Imagery | real work, product evidence, people/place, decoration, none, unknown |
| Link and control affordance | native, custom but clear, ambiguous, unknown |
| Motion | none, functional, nonessential, scroll-controlled, unknown |
| Responsive behavior | preserved order, layout change, hidden content, unknown |
| Accessibility evidence | visible focus, semantics, contrast, reflow, unknown |
| Identity anchors | distinctive choices tied to author, content, or brand |
| Evidence notes | observed, measured, inferred, unknown statements kept separate |

## Study record template

```json
{
  "snapshot_order": 1,
  "title": "",
  "url": "",
  "accessed": "YYYY-MM-DD",
  "availability": "available | partial | unavailable",
  "primary_task": "",
  "dominant_grammar": "",
  "observations": [],
  "measurements": [],
  "inferences": [],
  "unknowns": [],
  "reviewer": ""
}
```

## Interpretation rules

- A card, accent color, large type, image, animation, or unusual layout is not a
  defect by itself.
- A low count of visual variants is not proof of coherence.
- Sparse appearance is not proof of usability or accessibility.
- A screenshot cannot prove semantics, keyboard operation, responsive reflow,
  reduced-motion behavior, or authorship.
- A distinctive element should be preserved when it carries supported identity,
  content, or task value.
- Corpus contrasts remain review prompts; the artifact's own evidence decides.

## Maintenance

Update this document when:

- the corpus snapshot or sample changes;
- a coded observation is promoted into a normalized principle;
- a counterexample changes an existing heuristic;
- a source becomes inaccessible;
- a reproducible dataset or review artifact is added.
