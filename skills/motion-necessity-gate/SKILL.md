---
name: motion-necessity-gate
description: Use this skill to review animations, transitions, parallax, scroll effects, reveals, carousels, and micro-interactions in a website or interface. Keep motion only when it communicates feedback, state, causality, spatial continuity, errors, success, or a user-requested transition. Use when simplifying motion or adding reduced-motion behavior. Do not retain motion merely to make a page feel active.
license: MIT
compatibility: Agent Skills-compatible clients. Core workflow is instruction-only; optional Python 3.9+ scripts use the standard library and no network.
metadata:
  author: leeskills contributors
  version: "0.3.0"
  languages: "en, ko, ja"
---


# Motion Necessity Gate

Require a functional reason, a static equivalent, and an appropriate
reduced-motion path for every retained motion pattern.

## Inputs

Inventory as available:

- trigger;
- affected elements;
- duration and repetition;
- information conveyed;
- user control;
- essential or nonessential status;
- reduced-motion behavior;
- source code or prototype;
- user task and accessibility baseline.

## Allowed functional purposes

A retained motion should communicate at least one:

- direct input feedback;
- state change;
- causal relationship;
- spatial continuity or navigation context;
- progress;
- error or success;
- user-requested content transition;
- authoring or preview of motion itself.

"Feels alive," "looks premium," "fills empty space," and "all sections should
animate in" are not functional purposes.

## Workflow

1. Inventory each distinct motion pattern.
2. Identify its trigger and information role.
3. Mark whether it is essential to functionality or information.
4. Check whether the same information remains available statically.
5. Choose `keep`, `reduce`, `replace`, or `remove`.
6. Define reduced-motion behavior for every retained nonessential pattern.
7. Remove or replace scroll hijacking and nonessential parallax.
8. Check autoplaying, repeated, flashing, and time-based content separately.
9. Verify keyboard, touch, pointer, zoom, and motion-preference behavior.
10. Record unknown behavior rather than assuming support.

Read [references/motion-rules.md](references/motion-rules.md).

Use:

- [assets/motion-inventory.schema.json](assets/motion-inventory.schema.json)
- [assets/motion-inventory-example.json](assets/motion-inventory-example.json)
- [assets/reduced-motion.css](assets/reduced-motion.css)

Validate:

```bash
python scripts/validate_motion_inventory.py path/to/motion-inventory.json
```

## Decisions

### Keep

Use when motion is necessary and the implementation is safe, or when a
nonessential motion has a clear benefit and a complete reduction path.

### Reduce

Shorten, simplify, remove travel, avoid scale or parallax, or switch to an
instant state change when motion preference is reduced.

### Replace

Use a static state, highlight, text change, progress indicator, or direct
transition that conveys the same meaning with less movement.

### Remove

Use when motion provides no information, competes with the task, delays
content, controls scrolling, or lacks a safe alternative.

## Hard gates

Do not pass when:

- scroll movement is hijacked without an equivalent user-controlled path;
- information or operation exists only in animation;
- a retained nonessential interaction animation has no reduction or disable
  path;
- a removed animation also removes status or feedback;
- motion preference is overridden or ignored without an essential reason.

Treat W3C Animation from Interactions as a strong project guardrail. It is a
Level AAA criterion; state the chosen conformance target separately.

## Completion

Every motion pattern has a purpose, decision, static equivalent, and verified
reduced-motion behavior—or is removed.
