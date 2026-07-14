# Verification tests

Use these tests as structured questions rather than aesthetic absolutes. Mark
untested conditions as `unknown`.

## 1. Deletion test

For every removable section, component, sentence, image, animation, and token:

1. remove or hide it in a reversible branch;
2. repeat the primary task;
3. identify any lost evidence, context, state, identity, or access cue;
4. retain it only when the loss is material.

A vague preference such as “it feels premium” is not sufficient evidence by
itself. Record the specific communication or business requirement.

## 2. Substitution test

Temporarily replace the subject's name with an unrelated product or
organization. Flag copy, imagery, or structure that remains equally plausible.

This is a specificity heuristic, not proof of AI generation. Some conventional
language is necessary; judge whether it still conveys decision-relevant facts.

## 3. Semantic or unstyled-structure test

Inspect the document order and accessible structure without relying on visual
position, color, shape, or animation. Confirm:

- headings form a meaningful hierarchy;
- lists and tables represent actual relationships;
- controls have persistent names;
- links describe their destination or purpose in context;
- status and errors are programmatically available;
- source order remains understandable.

Disabling all CSS is a useful diagnostic, but it is not itself a standards
requirement or a complete semantic test.

## 4. Glance-hierarchy test

At a brief glance or with the page visually blurred, verify that the primary
identity, task, and next action remain distinguishable. Do not use this test to
judge text readability, semantics, or accessibility.

## 5. Primary-task test

Execute the declared primary task from entry to success. Record:

- starting state;
- required actions;
- decision points;
- errors and recovery;
- completion evidence;
- unnecessary detours.

A five-second impression test may assess initial orientation, but it cannot
prove task success.

## 6. Growth test

Model a realistic larger state, such as ten times more posts, projects,
products, filters, error cases, or navigation items. Confirm the existing
schema and dominant layout grammar still work, or document a deliberate
boundary.

## 7. Reflow test

At the project's target accessibility baseline, verify that content and
functionality reflow without loss or unintended two-dimensional scrolling,
except where two-dimensional presentation is essential. Record viewport,
zoom, text-size, browser, and exceptions.

## 8. Keyboard and focus test

Use the keyboard to operate every interactive path in scope. Confirm:

- all required controls are reachable and operable;
- focus order follows the task;
- focus remains visible and is not obscured;
- no keyboard trap exists;
- overlays return focus appropriately;
- hover-only content has an equivalent path.

## 9. Reduced-motion test

Enable the platform's reduced-motion preference and exercise every retained
motion pattern. Remove, reduce, or replace nonessential movement while
preserving state and task feedback.

## 10. Provenance test

Trace every material customer name, quote, metric, award, result, price,
capability, case study, screenshot, and image to an approved source. Mark
expiry-sensitive facts and confidential or prohibited material.

A generated or mock image may be used when clearly disclosed for illustration;
it must not be presented as proof that a real product capability exists.

## 11. Assistive-technology sampling

Where required by the project, sample supported screen-reader and other
assistive-technology paths. Record software, version, browser, input, task, and
result. Do not generalize a single successful path into complete conformance.

## 12. Before-and-after comparison

Compare task steps, required information, failure recovery, accessibility
signals, visual variants, content volume, and page weight when those metrics
are available. Prefer measurable differences, but preserve qualitative
observations with clear evidence labels.

## 13. Nested-radius coherence test

When rounded surfaces are nested or their radius, padding, gap, border, or
surface treatment changed:

1. classify each pair as a shared contour, independent component, or pill or
   circle;
2. for a shared contour, repeat the declared one-step semantic-token check or
   measured concentric-offset calculation;
3. compare before and after screenshots at representative viewports;
4. confirm that the change did not clip focus, content, targets, or states;
5. record exceptions and their communication evidence.

Do not pass this check from a token count alone. Mark it not applicable only
when no nested rounded relationship exists in scope.
