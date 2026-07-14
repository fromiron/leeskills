---
name: specificity-editor
description: Use this skill to audit and rewrite vague, interchangeable, inflated, or unsupported copy in a website, interface, landing page, portfolio, case study, or product narrative. Use when copy contains generic AI-marketing language, unverified superlatives, empty benefits, or claims that could fit any company. Ground every rewrite in supplied evidence and preserve the artifact's language and voice.
license: MIT
compatibility: Agent Skills-compatible clients. Core workflow is instruction-only; optional Python 3.9+ scripts use the standard library and no network.
metadata:
  author: leeskills contributors
  version: "0.2.0"
  languages: "en, ko, ja"
---


# Specificity Editor

Replace interchangeable marketing language with concrete, attributable,
task-relevant copy.

## Prerequisite

Use a grounded content inventory when claims, outcomes, customers, prices, or
capabilities are involved. If evidence is missing, flag the claim or write
around it; do not invent support.

## Specificity questions

Use the subset relevant to each statement:

1. Who acts or provides the thing?
2. What exactly happens?
3. For whom?
4. In what context or workflow?
5. What result is supported?
6. What constraint, price, time, or scope matters?
7. What evidence supports the statement?
8. What should the reader do next?

Not every sentence needs all eight answers. It needs enough detail to perform
its job.

## Workflow

1. Preserve the source language unless translation is requested.
2. Split copy into atomic claims and actions.
3. Trace factual claims to grounded evidence.
4. Run the substitution test: replace the name with an unrelated competitor.
5. Flag wording that remains equally plausible after substitution.
6. Flag superlatives, quantified outcomes, universal claims, and social proof
   that lack evidence.
7. Remove duplicated promises and filler transitions.
8. Rewrite with concrete nouns, active verbs, relevant constraints, and one
   clear action.
9. Preserve approved brand voice; specificity is not the same as flat tone.
10. Show unresolved claims rather than silently weakening or fabricating them.

Read [references/copy-rules.md](references/copy-rules.md).

Optional lint:

```bash
python scripts/lint_copy.py path/to/copy.txt
python scripts/lint_copy.py path/to/copy.txt --format json
```

The linter uses [references/phrase-watchlist.txt](references/phrase-watchlist.txt).
A match is a review prompt, not an automatic failure.

## Rewrite rules

- Prefer product, service, task, user, action, price, date, scope, and supported
  result over abstract value language.
- Replace "seamless" with the actual integration or reduced step count only if
  known.
- Replace "powerful" with the capability that matters.
- Replace "innovative" with what is materially different.
- Replace "trusted by" with attributable customers or remove it.
- Replace "save time" with a supported mechanism or measured result.
- Do not transform uncertainty into certainty.
- Do not invent a metric to make a sentence more specific.
- Do not require every sentence to become longer. A concrete sentence can be
  shorter.

## Output

Use [assets/rewrite-template.md](assets/rewrite-template.md).

For every material rewrite include:

- original;
- issue;
- evidence status;
- supported rewrite;
- evidence used;
- unresolved information.

## Completion

Copy passes when the primary identity, offer, task, constraints, proof, and
action are understandable, and every factual claim is supported or explicitly
qualified.
