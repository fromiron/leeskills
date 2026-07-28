# Design foundations

## Operational definition

In this repository, a slop signal is an observable symptom of output that is:

- unsupported by supplied evidence;
- interchangeable across unrelated products or authors;
- structurally redundant;
- visually unnecessary for the user task;
- behaviorally inconsistent across design, documentation, and code;
- inaccessible because simplicity removed needed cues;
- animated without a functional reason;
- presented with false certainty.

A signal does not establish who or what generated the artifact.

## Normalized principles

### 1. Content before chrome

Start with the actual identity, offer, task, proof, constraints, dates, prices,
results, and actions. Do not manufacture sections to fill a familiar landing
page template.

### 2. One dominant grammar

Prefer one primary structure per page or flow:

- profile;
- chronological ledger;
- writing index;
- portfolio index;
- product or service explanation;
- collection or catalog;
- institutional information;
- task workflow.

A hybrid is allowed only when users have materially different tasks and the
boundary is explicit.

### 3. Structure instead of containers

Use headings, lists, tables, alignment, spacing, and rules before wrapping every
item in a rounded card. A container should communicate a real boundary, state,
or interaction.

### 4. Nested curves preserve relationships

Count radius tokens, but also inspect how rounded surfaces relate. When an
inner surface visually follows an outer contour, move inward through the
project's semantic radius scale or verify the intended concentric offset.
Classify independent controls, pills, and circles separately instead of forcing
all nested shapes into one arithmetic rule.

### 5. Typography carries hierarchy

Use a small number of type roles. Do not compensate for weak information
architecture with gradient text, excessive scale jumps, or many unrelated
weights. Evaluate letter spacing and line height in the context of the actual
typeface, fallback stack, script, language, size, weight, role, and rendered
line length. Do not treat another design system's numeric values as universal
typography rules.

### 6. Color has a job

Each color should support identification, state, category, selection, data, or
brand recognition. Prefer project semantic token names over repeated raw
values. Record theme mapping and contrast separately. Decorative color systems
and repeated exceptions require an explicit reason and owner.

### 7. Whitespace communicates relationships

Spacing should indicate grouping and hierarchy, not merely create a sparse
look. Distinguish gaps within content, gaps between sections, and page-container
padding. Prefer the project's semantic spacing scale, and verify that
responsive changes preserve grouping while avoiding desktop-sized empty
regions on narrow screens. Let outer containers own page padding and width
constraints where practical, but do not copy another system's breakpoints or
pixel values as universal defaults. Large empty areas are not automatically
minimal.

### 8. Images are evidence

Prefer real work, products, people, places, processes, or data. Decorative
generative imagery is not automatically prohibited, but it must have a stated
communication role and must not impersonate product evidence.

### 9. Copy is specific and attributable

Use names, dates, prices, actions, constraints, outcomes, and source-backed
claims. Reject copy that remains equally plausible after swapping in an
unrelated company name.

### 10. Motion must explain something

Keep motion when it conveys feedback, state change, causality, spatial
continuity, errors, success, or a user-requested transition. Remove motion that
exists only to make a page feel active.

### 11. Accessibility is not decoration

Do not remove focus indicators, labels, headings, errors, alternatives,
contrast, status, or keyboard behavior to achieve a cleaner surface.

### 12. Complexity can remain

Minimal design does not require little content. Large archives and catalogs can
remain simple when their records use one stable schema and scale without
introducing new visual grammars.

### 13. Prune after grounding

Deletion before grounding can remove necessary information. Establish the user
task and evidence first, then remove elements that do not serve them.

### 14. Components are contracts

A reusable component is more than a visual variant. Define its purpose,
required and optional anatomy, applicable states, content constraints,
responsive and input behavior, accessibility representation, semantic tokens,
ownership, and deprecation path.

Inspect design, documentation, code, tests, and representative live usage
separately. A Figma state does not prove runtime support, and visual similarity
does not prove behavioral parity.

### 15. Consistency needs an exception path

Consistency supports recognition, collaboration, and maintenance; it should not
erase authorship, brand, or content-specific identity. Preserve a distinctive
choice when it has supported task or identity value and remains usable and
accessible.

Every exception needs evidence, an owner, status, and a review trigger.
Repeated exceptions indicate that the shared contract or token system may need
revision.

### 16. Affordance must match behavior

Visual treatment creates an expectation about what can be operated, what will
happen, and which state is current. Similar treatments should support compatible
behavior; materially different behavior must remain distinguishable when the
user needs to tell it apart.

Do not infer behavior from appearance alone. Compare design, semantics, source
code, input paths, feedback, and live usage. Allow evidence-backed exceptions
without turning arbitrary variation into identity.

### 17. Action priority belongs to a decision context

A primary action is the default next step for one user decision or task stage,
not a universal decoration and not a page-wide quota. Prefer one primary action
when the context has a clear default. Permit equal-priority actions or no
primary action when the task evidence requires it and the reason is explicit.

Keep secondary and destructive actions distinguishable without changing the
meaningful source or focus order.

### 18. Visibility has a disclosure cost

An action can exist and still be functionally hard to find. Classify whether it
is persistent, contextual, disclosed, or hidden, and record the steps,
constraints, importance, and alternative path.

Overflow and progressive disclosure are valid for low-frequency, advanced,
destructive, permission-sensitive, or space-constrained actions. Primary,
frequent, and recovery actions need stronger evidence before being hidden.

### 19. Systems need adoption paths

A design system is not complete when tokens and components are documented.
Record the current inventory, authoritative surfaces, governance, contribution
process, legacy-to-target mappings, coexistence rules, adoption status,
versioning, changelog, roadmap, owners, and deprecation gates.

No organization model or migration strategy passes by name alone. The system
must make responsibility, consumer impact, and convergence reviewable while
continuing to audit the current behavior and accessibility of the target
components.
