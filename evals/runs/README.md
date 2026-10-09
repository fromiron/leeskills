# Client run records

No real client runs have been recorded in this repository yet. The v0.6.0
baseline (`1100ae3`) and later revisions are **not run** for every trigger,
routing, and output eval. Do not read the fixtures or assertions as measured
results.

## Recording a run

1. Pick the condition: `no-skill`, `baseline` (the recorded previous revision),
   or `revised`. Keep the client, model settings, tools, permissions, and
   inputs identical across conditions.
2. Start a fresh session for every attempt. For edit cases, start from a clean
   copy of the same fixture files.
3. Write one record per attempt that matches
   [run-record.schema.json](../run-record.schema.json). Use `"unknown"` for a
   model identity the client does not expose, and `null` for tokens or time it
   does not report. Do not estimate missing values.
4. When a fixture, tool, permission, or environment is missing, record the
   attempt as `"status": "not-run"` with `not_run_reason`. A not-run attempt is
   never counted as a pass.
5. Keep transcripts, final answers, and diffs next to the records and point to
   them with `output_path` and `diff_path`.

## Evaluating

Trigger results, per skill:

```bash
python scripts/evaluate_trigger_results.py skills/<skill>/evals/trigger_queries.json path/to/trigger-results.json
```

Routing results, for the full catalog:

```bash
python scripts/evaluate_routing_results.py evals/catalog-routing.json path/to/routing-results.json
```

Both scripts require three attempts by default. Fewer attempts report
`insufficient`. A smoke run with fewer attempts can be useful while drafting,
but it is not release evidence.

## What not to store

Do not commit secrets, credentials, private customer material, or client
session tokens. Redact them from transcripts before saving.
