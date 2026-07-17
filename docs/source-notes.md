# Source notes

Accessed: **2026-07-17**

These sources informed the repository. The skills paraphrase and normalize
their principles rather than copying source text, numerical scales, component
names, or branding.

## Agent Skills format

- Agent Skills overview  
  https://agentskills.io/home
- Agent Skills specification  
  https://agentskills.io/specification
- Best practices for skill creators  
  https://agentskills.io/skill-creation/best-practices
- Optimizing skill descriptions  
  https://agentskills.io/skill-creation/optimizing-descriptions
- Evaluating skill output quality  
  https://agentskills.io/skill-creation/evaluating-skills
- Using scripts in skills  
  https://agentskills.io/skill-creation/using-scripts
- Reference implementation  
  https://github.com/agentskills/agentskills/tree/main/skills-ref

Key decisions derived from these sources:

- one `SKILL.md` per skill directory;
- required `name` and `description`;
- concise, intent-oriented descriptions;
- progressive disclosure through `references/`, `assets/`, and `scripts/`;
- realistic trigger and output evals;
- deterministic scripts for mechanical validation;
- non-interactive script interfaces with helpful errors.

## Client adapters

- OpenAI Codex skills documentation  
  https://learn.chatgpt.com/docs/build-skills
- Claude Code skills documentation  
  https://code.claude.com/docs/en/skills

The core skills avoid client-specific frontmatter. Adapter documents record
current repository and user installation locations.

## Curated minimal-site corpus

- Dead Simple Sites  
  https://deadsimplesites.com/
- Corpus evidence boundary and sampling protocol  
  [corpus-study.md](corpus-study.md)

Dead Simple Sites directly states that its curation rejects excessive
animation, scroll hijacking, and excessive storytelling, summarized as doing
less but doing it better. Those statements support the motion and narrative
guardrails.

The directory is treated as a **curated minimal-site corpus**, not as proof that
every listed site was created entirely by a human or without generative tools.
The prior visual study informed structural categories and contrasts, but it was
not a systematically coded sample. The new corpus protocol requires a fixed
snapshot, declared sample, evidence-state split, counts with denominators,
missing-data reporting, and counterexamples before stronger recurring-pattern
claims are made.

The generic-default pattern catalog in `slop-signal-audit` contrasts common
template and generated-page defaults with choices observed by maintainers in a
curated sample: text-led structures, typography-carried identity, restrained
accents, evidence images, native link affordances, and little nonessential
motion. The corpus side remains an inference until encoded with the protocol.
The template side is a maintainer heuristic, not a systematically sampled
comparison corpus. Neither side is authorship evidence.

## Codeit Design System

### Principles and foundations

- Codeit Design System overview and principles  
  https://design.codeit.com/
- Spacing  
  https://design.codeit.com/foundations/spacing
- Layout  
  https://design.codeit.com/foundations/layout
- Radius  
  https://design.codeit.com/foundations/radius
- Typography  
  https://design.codeit.com/foundations/typography
- Color  
  https://design.codeit.com/foundations/color
- Iconography  
  https://design.codeit.com/foundations/iconography

The overview frames the system as a promise of consistent experience,
cross-functional collaboration, and autonomy within a shared direction. This
repository generalizes those ideas as explicit ownership, reviewable contracts,
and evidence-backed exception paths.

Codeit's spacing guidance separates primitive values from semantic content gaps
and section gaps, and adjusts larger spacing at mobile sizes. This repository
adopts role separation and responsive-relationship checks, but not Codeit's
4/8 scale or pixel values as universal defaults.

Codeit's layout guidance centralizes page padding, container bounds, and minimum
screen dimensions in responsive tokens. This repository generalizes container
ownership and responsive verification. A project's own breakpoints and
constraints take precedence.

Codeit's semantic-radius guidance uses relative size tokens and recommends a
smaller inner token when boxes are nested. This repository generalizes that
relationship without adopting project-specific pixel values. It adds separate
handling for shared contours, independent components, pills, and circles, plus
an optional measured concentric-offset check.

Codeit's typography tokens are defined for selected typefaces and assign letter
spacing and line height to individual roles. This repository adopts semantic
role consistency while treating those measurements as typeface-, fallback-,
script-, language-, size-, weight-, and context-dependent.

Codeit's color guidance uses shared token names rather than raw values, separates
primitive and semantic roles, includes theme mapping and contrast, and treats
repeated new colors as a governance decision. This repository adopts those
collaboration and semantic-role principles, not the palette or token names.

Codeit's iconography guidance documents semantic naming, a consistent visual
language, optical correction, interactive target considerations, and icon
button usage. This repository adopts those questions without copying its grid,
size, stroke, radius, or theme values.

### Components

- Components overview  
  https://design.codeit.com/components
- Buttons  
  https://design.codeit.com/components/buttons/detail
- Text Field  
  https://design.codeit.com/components/textfield
- Tabs  
  https://design.codeit.com/components/tabs

The component documentation repeatedly separates purpose, anatomy, essential
and optional parts, states, properties, specification, responsive behavior,
usage, and interaction expectations. Buttons require meaningful labels and
document priority and keyboard behavior. Text fields document labels, helper
and error feedback, state variants, and mobile constraints. Tabs document
selection state and keyboard movement.

`component-contract-audit` generalizes this documentation pattern into a
project-owned contract spanning design, documentation, code, tests, and live
usage. It does not copy Codeit's component inventory, variant names, dimensions,
or implementation choices.

The token proposal template adopts the documentation pattern of an overview
followed by foundation-specific primitive tokens, semantic tokens, usage, and
specimens. It does not copy Codeit's branding, navigation, content, token names,
or numeric scales.

## Accessibility

- WCAG 2.2 Quick Reference  
  https://www.w3.org/WAI/WCAG22/quickref/
- Contrast Minimum  
  https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html
- Non-text Contrast  
  https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html
- Reflow  
  https://www.w3.org/WAI/WCAG22/Understanding/reflow.html
- Focus Visible  
  https://www.w3.org/WAI/WCAG22/Understanding/focus-visible.html
- Focus Not Obscured  
  https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum.html
- Target Size Minimum  
  https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html
- Info and Relationships  
  https://www.w3.org/WAI/WCAG22/Understanding/info-and-relationships.html
- Animation from Interactions  
  https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.html

The accessibility skill treats automated checks as partial evidence and
requires manual keyboard, zoom/reflow, and assistive-technology review where
appropriate.

## Content design

- GOV.UK content planning guidance  
  https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/plan-manage-content/plan-new-govuk-content/

The content workflow adopts task-oriented organization, avoids duplicate
content, and separates current facts from uncertain future claims.
