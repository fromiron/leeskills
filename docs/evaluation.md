# Evaluation guide

## Two separate questions

Evaluate:

1. **Trigger quality** — did the correct skill load?
2. **Output quality** — did the skill improve the result?

A skill can have a good workflow and still be useless if its description does
not trigger reliably.

## Trigger evals

Each skill includes `evals/trigger_queries.json` with stable IDs, language
tags, positive prompts, and near-miss negative prompts. Every skill must include
at least two positive and two negative prompts for each of `en`, `ko`, and
`ja`.

Run every prompt multiple times in the target client because activation is
nondeterministic. Record:

```json
{
  "client": "target-agent-name",
  "skill_name": "content-grounding",
  "results": [
    {
      "id": "ko-positive-1",
      "attempts": 3,
      "triggered": 2
    }
  ]
}
```

Include one result for every query ID, then evaluate the measured file:

```bash
python scripts/evaluate_trigger_results.py \
  skills/content-grounding/evals/trigger_queries.json \
  path/to/measured-trigger-results.json
```

The repository validator checks fixture coverage only. It does not measure
client activation. Do not record a trigger rate until the target client has
actually run the prompt.

Keep a fixed validation split while revising descriptions. Do not optimize on
all prompts at once.

## Output evals

Each skill includes `evals/evals.json` with:

- a realistic prompt;
- a description of successful output;
- observable assertions;
- optional fixture files.

Run each case with and without the skill, or against the previous released
version. Compare quality, omissions, unsupported claims, token use, and time.

## Human review

Human review remains required for:

- visual hierarchy;
- whether a page feels coherent rather than merely sparse;
- whether an image is authentic and relevant;
- whether copy preserves brand voice;
- whether a proposed deletion removes important context;
- assistive-technology usability.

## Suggested release gate

A release candidate should meet all of the following:

- repository validator passes;
- unit tests pass;
- no unresolved hard failure in included sample runs;
- positive trigger rate at least 0.67 over three runs in each language;
- near-miss negative trigger rate at most 0.33 in each language;
- output evals improve or match the previous version without introducing
  fabricated evidence;
- one human reviewer checks each changed skill.
