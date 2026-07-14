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
