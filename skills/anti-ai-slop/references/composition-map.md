# Composition map

Use this file when the agent client cannot invoke other skills directly.

## Handoff contracts

### Content grounding

Produce:

```json
{
  "context": {
    "artifact_type": "",
    "primary_user": "",
    "primary_task": "",
    "success_condition": ""
  },
  "facts": [],
  "content_groups": {},
  "contradictions": [],
  "missing": [],
  "prohibited_generation": [],
  "safe_claims": [],
  "allowed_placeholders": [],
  "questions": []
}
```

### Structure selection

Produce:

```json
{
  "primary_user": "",
  "primary_task": "",
  "dominant_grammar": "",
  "organizing_key": "",
  "content_sequence": [],
  "navigation": {"mode": "none", "items": []},
  "responsive_reflow": [],
  "growth_test": "",
  "rejected_patterns": [
    {"pattern": "", "reason": ""},
    {"pattern": "", "reason": ""}
  ],
  "unknowns": []
}
```

### Visual budget

Produce observed counts, default or project limits, exceptions, and unresolved
overages. Do not treat default limits as universal laws.

### Specificity edit

For each changed statement, show:

- original;
- problem;
- supported rewrite;
- evidence used;
- unresolved claim if evidence is missing.

### Motion gate

For each motion pattern, record:

- trigger;
- purpose;
- essential or nonessential;
- keep, reduce, replace, or remove;
- reduced-motion behavior;
- equivalent static state.

### Accessibility guard

For each check, record:

- criterion or requirement;
- status: pass, fail, unknown, or not applicable;
- evidence;
- impact;
- fix;
- verification method.

### Prune and verify

Run the deletion, substitution, semantic, five-second, growth, reflow,
keyboard, reduced-motion, and provenance tests. Unknown results remain unknown.

## Dependency rules

- Structure depends on grounded user needs and content.
- Copy cannot add facts absent from grounding.
- Visual budgets cannot override accessibility.
- Motion cannot carry information without a static equivalent.
- Pruning cannot delete evidence required for trust or task completion.
- A score cannot override a hard failure.
