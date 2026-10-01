# Component contract rules

## Project ownership first

Use the project's established design library, documentation, code, tokens,
platform constraints, and decision records before consulting an external design
system. External systems can supply questions and documentation patterns; they
do not establish this project's variants, dimensions, names, behavior, or
organizational model.

Record one source-of-truth declaration:

- authoritative surface;
- location;
- accountable owner;
- contribution or change process;
- deprecation path;
- review trigger.

When the project intentionally shares authority, define which surface owns each
dimension instead of writing only `shared`.

## Purpose and selection

A component needs:

- a task or communication purpose;
- conditions for using it;
- conditions for selecting another component;
- priority relative to adjacent actions or information;
- composition rules when repeated or nested.

Do not create a variant only to reproduce a visual difference. A variant should
communicate priority, state, content type, behavior, platform need, or identity.

## Anatomy

For every part record:

- name;
- `required`, `optional`, or `conditional`;
- semantic or interaction role;
- dependency on another part;
- content constraints;
- evidence state.

A part is not optional merely because a design tool property can hide it.
Determine whether the user's task, accessible name, status, or recovery depends
on it.

## State coverage

Define applicable states from behavior rather than from a universal checklist.
For each applicable state record:

- trigger;
- visual change;
- behavioral change;
- accessible representation or announcement;
- exit or recovery path;
- evidence source;
- pass, fail, or unknown.

Pointer hover does not replace focus-visible. Color does not replace text,
shape, semantics, or status messaging when those are required. A disabled state
needs a reason and an alternative path when the user still must complete the
task.

## Content and localization

Test representative content, not only ideal labels:

- shortest and longest supported labels;
- multiple scripts and language expansion;
- multiline wrapping;
- truncation and full-value access;
- empty and missing values;
- helper, error, status, and limit text;
- dates, numbers, currencies, and bidirectional text when relevant.

Write content rules as constraints and examples. Do not silently solve overflow
by reducing text below the accessibility baseline or removing necessary
information.

## Responsive and input behavior

Record what changes at each project-relevant condition:

- width or container;
- input modality;
- orientation;
- zoom or text enlargement;
- reduced motion;
- contrast or theme preference;
- virtual keyboard or safe area when relevant.

Responsive behavior may change layout, order, density, width, or presentation.
It must preserve the primary task, meaningful order, status, and recovery.

## Semantic color and iconography

Use project semantic token names rather than raw values when a token exists.
Record theme mappings and required contrast separately.

For icons record:

- semantic name and meaning;
- source family;
- style and optical treatment;
- size role and interactive target;
- text alternative or accessible name;
- whether the icon is decorative, supporting, or the sole label.

When an icon and text form one label or control, inspect their optical weight,
baseline, spacing, and state treatment together. Do not force arithmetic equality
when the glyph's visual mass requires optical correction.

Do not copy another system's color scale, icon grid, stroke, or dimensions as a
universal rule. Use its documentation structure only when it helps the project
state its own contract.

## Affordance mapping

Record the relationship among:

- visual treatment;
- perceived role or expected operation;
- actual behavior;
- state meaning;
- input paths;
- evidence and exception status.

Check both directions:

1. Elements with the same or materially similar treatment should support
   compatible expectations. A filled action surface should not also represent
   inert metadata unless the difference remains clear through semantics,
   context, and interaction cues.
2. Elements with materially different behavior, risk, or state should remain
   distinguishable when users must tell them apart.

This is not a requirement for every action to look unique. Reuse is desirable
when behavior and priority are compatible. A different treatment also needs a
reason; decorative variation is not a substitute for a contract.

A justified exception records the expected interpretation, evidence, owner,
accessibility representation, and review trigger.

## Action priority by decision context

Evaluate action hierarchy within one user decision, task stage, or repeated
record—not as a universal rule that an entire page or application may contain
only one primary action.

For each decision context record:

- user decision;
- primary action, when one exists;
- secondary alternatives;
- destructive or exceptional actions;
- keyboard and reading order;
- visual prominence;
- evidence for equal priority or for intentionally having no primary action.

Prefer one primary action when the task has a default next step. Do not invent a
primary action for neutral navigation, peer choices, editors with independent
tool groups, or other contexts where the product evidence establishes no single
default.

Keep destructive actions distinguishable from routine primary actions. Visual
priority must not change accessible order or naming in a way that obscures the
task.

## Action visibility and disclosure cost

Classify actions as:

- `persistent` — directly available in the current context;
- `contextual` — appears when the relevant object or state is active;
- `disclosed` — available after opening an explicit menu, panel, or details
  control;
- `unavailable` — not provided in the current context or reachable path.

For each action record importance, expected frequency, recovery value,
disclosure steps, available-space evidence, hiding reason, and any equivalent
visible path.

An overflow menu is not automatically a defect. Disclosure may be appropriate
for destructive, advanced, low-frequency, permission-sensitive, or
space-constrained actions. Conversely, a primary, frequent, or recovery action
should not pass merely because it technically exists. Hiding it requires a
supported reason and an adequate discoverable path.

Do not infer frequency from visual prominence. Use research, analytics, product
requirements, or an explicit inference label.

## Grouping cues and container strength

Relationships can be communicated through:

- proximity;
- alignment;
- similarity;
- a shared container.

A container is a strong cue and adds visual and implementation weight. Use the
lightest sufficient set of cues for the relationship, but do not require a fixed
order in every interface.

Retain or add a container when it communicates a real boundary, selected or
editable state, interaction target, repeated record, drag region, ownership,
error scope, or other task-relevant grouping. Remove it when proximity,
alignment, and similarity preserve the same relationship and the container adds
no state, boundary, or interaction value.

Test the result with real content growth, responsive reflow, keyboard focus,
and the semantic source order. A borderless layout is not simpler when the
relationship becomes ambiguous.

## Design-code parity

Use these statuses per inspected surface:

- `aligned`;
- `drift`;
- `unknown`;
- `not-inspected`.

Compare behavior and content, not only visual similarity. Examples of material
drift include:

- design has a loading state but code does not;
- documentation allows an icon-only action but accessible naming is undefined;
- code exposes a variant absent from documentation;
- live usage overrides tokens or composition rules;
- design and code disagree on required or optional anatomy;
- responsive order differs and changes meaning;
- design presents one primary action while code gives multiple actions equal
  prominence;
- an overflow policy exists in documentation but live usage hides a required
  action through a different path.

## Design-system lifecycle and adoption

When a shared system is in scope, inspect more than its final component library.
Record:

1. **Inventory** — current components, raw values, variants, exceptions, live
   usages, and known owners.
2. **Authoritative surfaces** — which dimensions are owned by design,
   documentation, code, tests, or live configuration.
3. **Governance model** — central, federated, distributed, solo, hybrid, or
   unknown. No model passes by name alone.
4. **Contribution process** — proposal, review, decision, implementation, and
   consumer feedback paths.
5. **Versioning and changelog** — how consumers learn what changed and whether
   migration is required.
6. **Legacy-to-target mapping** — exact current component or token, target,
   adoption status, exception, owner, and migration note.
7. **Coexistence rules** — when old and new systems may coexist and how that
   period remains visible and bounded.
8. **Adoption strategy** — such as a coordinated migration, incremental
   replacement during feature work, or a documented hybrid.
9. **Roadmap and review triggers** — priorities grounded in user and maintainer
   impact rather than visual novelty.
10. **Deprecation gate** — measurable conditions for warning, blocking new usage,
    and removing the obsolete API or visual contract.

Do not require a dedicated central team or ambassador program. Those are
possible operating models, not universal requirements. A small project may use
a solo owner; a large product organization may distribute authority by
dimension. The contract must make responsibility and convergence reviewable.

A migration reset does not repair current component defects. Continue to audit
states, affordances, accessibility, content, and behavior in the target system.

## Exceptions and identity anchors

Consistency is a shared default, not a ban on authorship or brand expression.
Keep a distinctive choice when it has a supported identity, content, or task
role and does not break interaction or accessibility.

Every exception needs:

- decision;
- evidence-backed reason;
- task, brand, or identity value;
- owner;
- status;
- review trigger, such as a new theme, platform, component version, or repeated
  exception.

Repeated exceptions are evidence that the contract or token system may need
revision.

## Recommendation order

Prefer:

1. restore missing behavior, meaning, feedback, access, or recovery;
2. correct misleading affordances and essential action discoverability;
3. align required states across design, documentation, and code;
4. resolve content and responsive failures;
5. establish action priority within each real decision context;
6. map raw values to existing semantic tokens;
7. remove unnecessary grouping layers and consolidate variants with no distinct
   role;
8. document lifecycle, migration, ownership, and justified exceptions;
9. deprecate obsolete APIs or visual variants through a bounded migration path.
