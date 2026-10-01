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

The following illustrates the file shape; these numbers are not measured
activation results.

```json
{
  "client": "target-agent-name",
  "skill_name": "verify-content",
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
  skills/verify-content/evals/trigger_queries.json \
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

Cases that refer to a supplied application or file require the evaluator to
provide and record that artifact before running them. Use a representative
project where available. A prompt alone, or an expected-output assertion, is
not an executed case; keep missing-input cases unrun rather than inventing
results. For review-only cases with inline source material, use that exact
material across conditions.

Run the same input in three separate conditions:

| Condition | Setup |
|---|---|
| No skill | The same client and task, without the leeskills catalog |
| Previous version | The recorded previous skill names and exact revision |
| Revised version | The new names and exact revision being evaluated |

Use the same source artifacts, user prompt, client/model settings, tool access,
and execution environment. Start each attempt in a fresh conversation and, for
edits, a clean copy of the same artifact. Preserve the client's actual skill
discovery, prompt construction, model decisions, permissions, and primary user
flow. Do not replace them with fixed routing, expected-output replay, or a
special test-only tool. Trigger evals use ordinary prompts; explicit skill
invocation can assess output quality but does not measure automatic discovery.

Record the client version, verifiable model identity or `unknown`, repository
revision or saved patch, installed catalog, artifact version, query/eval ID,
attempt count, outputs and diffs, checks performed, and unavailable evidence.
Record tokens and elapsed time when the client exposes them; leave unavailable
measurements unknown. Keep full run evidence with the comparison.

Review these dimensions independently, with concrete locations and evidence:

| Dimension | What to record |
|---|---|
| Useful findings | Supported problems that affect the task |
| False positives | Incorrect or unsupported criticisms |
| Omissions | Known relevant problems missed; say when the reference review is incomplete |
| Unnecessary edits | Changes without a supported benefit or beyond requested scope |
| Preserved identity | Product voice, meaningful visual choices, and justified exceptions retained |
| Task and access | Required information, actions, accessibility, and runtime behavior preserved |
| Delivery | Review-only boundaries, actual requested edits, final checks, unknowns, and rollback |
| Cost | Observed token use and elapsed time, with measurement limits |

Do not reward the number of suggested changes. A decision to keep supported
content can be the best result. One real-world case demonstrates use; it does
not establish general quality or justify a maturity change.

## Isolate naming, instructions, and helper changes

Use the [name mapping](skill-name-migration.md) to pair old and new skill names.
Keep existing trigger-query and output-eval IDs stable. Preserve query text
except for explicit invocations that must use the corresponding name, and log
those substitutions.

For a naming comparison, change only names, directory paths, headings, and
their references. Keep descriptions, workflow instructions, helper behavior,
and fixture inputs fixed. Save that revision or patch as a separate candidate.
If delivery instructions or validators also change, evaluate them in separate
follow-up conditions. A comparison of old code with all changes combined
cannot attribute a difference to naming alone. New behavioral evals are
additional coverage, not changes to the existing paired cases.

Use `scripts/evaluate_trigger_results.py` for each measured trigger file and
compare per-language positive and near-miss negative rates. It aggregates
recorded observations; it neither invokes the model nor proves that the
observations are genuine. Do not feed the no-skill condition into it as if a
missing skill were a discovery failure; use that condition for output quality.

Installing the full catalog and loading all skill bodies are different events.
Record the metadata exposed, skills activated, and resources actually loaded
in the target client before drawing conclusions about context cost.

## What local validation establishes

Unit tests exercise deterministic behavior, including the audit example's
57-point quality score, rejection of full credit for unknown evidence, and
installation conflict protection. Symlink tests run only where supported.
These are useful tool checks, not measurements of the agent's design judgment.

The repository validator checks metadata, fixtures, links, Python syntax,
script help interfaces, and a fixed set of prohibited network imports. Its AST
inspection does not enforce all standard-library use or block network access
at runtime. Keep policy, static detection, and runtime isolation separate.

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
