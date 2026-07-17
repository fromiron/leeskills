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

### Component contract

Produce:

```json
{
  "component": "",
  "purpose": "",
  "primary_user_task": "",
  "source_of_truth": {
    "surface": "design | documentation | code | live | split",
    "location": "",
    "owner": "",
    "change_process": ""
  },
  "evidence": [],
  "anatomy": [],
  "variants": [],
  "states": [],
  "responsive_behavior": [],
  "content_rules": [],
  "accessibility": [],
  "token_mappings": [],
  "parity": [],
  "exceptions": [],
  "findings": [],
  "accepted_risks": [],
  "unknowns": []
}
```

For each applicable state, separate visual treatment, runtime behavior,
accessible representation, and evidence. Required failures, unknowns, or parity
drift remain release blockers. Do not copy another system's variants or
dimensions into the project. Preserve a justified identity or task exception
with evidence, owner, and a review trigger.

### Visual budget

Produce:

```json
{
  "observed": {},
  "limits": {},
  "radius_scope": "none | evaluated | unknown",
  "radius_scope_evidence": "",
  "radius_relationships": [],
  "token_proposal": {
    "required": false,
    "artifact_path": "",
    "foundations": [],
    "primitive_tokens": [],
    "semantic_tokens": [],
    "current_to_proposed": [],
    "open_questions": []
  },
  "exceptions": []
}
```

For shared nested contours, record either the inward semantic token step or a
measured concentric offset. Classify independent components and pills instead
of forcing them into the shared-contour rule. Produce unresolved overages and
radius mismatches. Do not treat default limits or another system's pixel values
as universal laws. When spacing, containers, or typography are in scope, also
record semantic spacing roles, responsive mappings, container ownership, and
the actual font, fallback, script, language, size, weight, letter spacing, line
height, line length, project token, and rendered evidence. Do not use an
external typography table as a pass/fail threshold.

When shared tokenization is recommended, supply exact proposed names and
values, distinguish primitive values from semantic roles, and create one
self-contained HTML review page for the applicable Typography, Spacing,
Layout, and Radius foundations. Label the page as a proposal and report its
path; do not imply adoption. Trace numeric proposals to inspected project or
rendered evidence. If that evidence is unavailable, leave values `unknown`
instead of inventing a complete scale.

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
keyboard, reduced-motion, and provenance tests. When nested rounded surfaces
exist or changed, also run nested-radius coherence verification. When reusable
components changed, verify required anatomy, states, content, responsive
behavior, accessibility, and design-code parity. Unknown results remain
unknown.

## Dependency rules

- Structure depends on grounded user needs and content.
- Copy cannot add facts absent from grounding.
- Component contracts cannot infer runtime support from a design file.
- Design-code parity cannot pass while a required surface is failed, unknown,
  or materially drifting.
- Visual budgets cannot override accessibility or justified identity.
- External spacing, layout, typography, color, iconography, and component values
  cannot override project tokens, behavior, or rendered evidence.
- A low radius-token count cannot override a measured nested-contour mismatch.
- Motion cannot carry information without a static equivalent.
- Pruning cannot delete evidence required for trust or task completion.
- A score cannot override a hard failure.
