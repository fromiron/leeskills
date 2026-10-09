# Repository-level evals

Per-skill trigger and output fixtures live in each package under
`skills/<name>/evals/`. This directory holds evaluation material that spans
the whole catalog and is not installed with any skill.

| Path | Purpose |
|---|---|
| [catalog-routing.json](catalog-routing.json) | Full-catalog routing and boundary cases with acceptable primary skills, allowed secondary skills, and forbidden actions |
| [run-record.schema.json](run-record.schema.json) | Shape of one recorded client attempt |
| [fixtures/](fixtures/) | Small static inputs referenced by routing and output evals |
| [runs/](runs/README.md) | Recording procedure; no runs are recorded yet |

See [docs/evaluation.md](../docs/evaluation.md) for the method.
