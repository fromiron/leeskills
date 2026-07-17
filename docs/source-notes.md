# Source notes

Accessed: **2026-07-14**

These sources informed the repository. The skills paraphrase and normalize
their principles rather than copying source text.

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
the current repository and user installation locations.

## Minimal design corpus

- Dead Simple Sites  
  https://deadsimplesites.com/

Its stated curation constraints reject excessive animation, scroll hijacking,
and excessive storytelling and summarize the editorial direction as doing less
but doing it better. The prior visual study of the linked corpus informed the
structural categories used by `structure-selector`.

The generic-default pattern catalog in `slop-signal-audit` was derived by
contrasting common template and generated-page defaults with recurring choices
observed across this curated corpus: text-led single-column structures,
typography-carried identity, restrained accents, evidence images, native link
affordances, and little nonessential motion. These observations are inferences
from a curated sample and are recorded as contrasts, not universal laws or
authorship evidence.

The corpus side of each contrast traces to the curated sample above. The
template-and-generated-defaults side is a maintainer heuristic drawn from
recurring template output the maintainers have reviewed; it was not derived
from a systematically sampled corpus. Treat the catalog as a reviewable
heuristic, not a research-backed finding.

## Interface foundation systems

- [Codeit Design System — Spacing](https://design.codeit.com/foundations/spacing)
- [Codeit Design System — Layout](https://design.codeit.com/foundations/layout)
- [Codeit Design System — Radius](https://design.codeit.com/foundations/radius)
- [Codeit Design System — Typography](https://design.codeit.com/foundations/typography)

Codeit's spacing guidance separates primitive values from semantic content
gaps and section gaps, and adjusts larger spacing at mobile sizes. This
repository adopts the role separation and responsive-relationship checks, but
not Codeit's 4/8 scale or pixel values as universal defaults.

Codeit's layout guidance centralizes page padding, container bounds, and
minimum screen dimensions in responsive tokens. This repository generalizes
the container-ownership and responsive-verification principles. A project's
own breakpoints and constraints take precedence; Codeit's breakpoints and
dimensions are not portable requirements.

Codeit's semantic-radius guidance uses relative size tokens and recommends a
smaller inner token when boxes are nested. This repository generalizes that
relationship without adopting Codeit's project-specific pixel values as
universal defaults. It adds separate handling for shared contours, independent
components, pills and circles, plus an optional measured concentric-offset
check when the curves are intended to remain parallel.

Codeit's typography tokens are defined for its selected typefaces and assign
letter spacing and line height to individual glyph roles. This repository
adopts semantic-role consistency while treating those measurements as
typeface-, script-, size-, weight-, and context-dependent. It never imports a
third-party typography table as a universal pass/fail threshold; require
project-token inconsistency or rendered evidence before recording a defect.

The single-page token proposal template also adopts the documentation pattern
of an overview followed by foundation-specific primitive tokens, semantic
tokens, usage, and specimens. It does not copy Codeit's branding, navigation,
content, token names, or numeric scales.

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
