# Contributing

## Scope

Contributions must improve grounded, minimal, accessible design workflows.
Do not add broad aesthetic opinions without an observable test, a clear user
need, or a cited source.

## Skill rules

- Keep one coherent job per skill.
- Keep `SKILL.md` below 500 lines.
- Put detailed material in `references/`.
- Prefer instructions over code.
- Use scripts only for deterministic checks.
- Use Python standard library only unless a dependency is essential and pinned.
- Add at least one positive, one near-miss negative, and one edge-case eval.
- Never infer AI authorship from visual style alone.
- Mark observations, calculations, inferences, and unknowns separately.
- Do not weaken accessibility to achieve visual simplicity.

## Development

```bash
python scripts/validate_repo.py
python -m unittest discover -s tests -v
```

Optional official validation:

```bash
skills-ref validate skills/<skill-name>
```

The upstream `skills-ref` reference implementation describes itself as
demonstration software, so local validation remains the default CI gate.

## Pull requests

Explain:

1. the failure mode the change addresses;
2. the representative tasks used to test it;
3. the expected improvement over the previous behavior;
4. any new false-positive risk;
5. whether the change affects trigger descriptions.
