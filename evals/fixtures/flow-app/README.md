# flow-app fixture

A three-screen workout log, built to be walked. It exists in two variants so
`map-flows` can be exercised on a real before and after:

| | `before/` | `after/` |
|---|---|---|
| Add set | A `div` with a click handler: pointer only | A button |
| Finish workout | Only inside the More menu | A button on the workout screen |
| Discard workout | Removes the workout at once | Asks for confirmation |
| Failed save | Offers only Discard | Offers Try again |

The defects in `before/` are planted on purpose. The app keeps its state in
`sessionStorage` and sends nothing anywhere. A labeled fixture control at the
bottom of each screen simulates a lost connection.

## Stored flow knowledge

Each variant has its own store, as a project would:

```text
<variant>/ux-flows/
├── log-workout.flow.json     the map: two journeys over one graph
└── runs/*.run.json           runs recorded against that variant
```

`skills/map-flows/assets/flow-map-example.json` and `flow-run-example.json`
are copies of `after/ux-flows/log-workout.flow.json` and
`after/ux-flows/runs/after-pointer-default.run.json`; a test keeps them
identical.

## How the runs were recorded

The run files were produced by `record_runs.js`, which drives Chromium with
Playwright, performs each action by pointer or by Tab and Enter, reads the
resulting state from what the page shows, and writes one run file per walk:

```bash
node evals/fixtures/flow-app/record_runs.js
```

The script is evaluation tooling. No skill depends on it, the repository
validation does not run it, and Playwright is not a dependency of leeskills.
Re-recording changes `recorded_at` and, with another browser version, `tool`.

What the runs show is limited to this fixture: a static page opened from a
file URL, one viewport, pointer and keyboard input in one browser, and no
assistive technology. They are not usability evidence for any product.

## Try it

```bash
python skills/map-flows/scripts/validate_flow.py evals/fixtures/flow-app/before/ux-flows/log-workout.flow.json
python skills/map-flows/scripts/analyze_flow.py evals/fixtures/flow-app/before/ux-flows/log-workout.flow.json
python skills/map-flows/scripts/compare_flows.py \
  evals/fixtures/flow-app/before/ux-flows/log-workout.flow.json \
  evals/fixtures/flow-app/after/ux-flows/log-workout.flow.json
python skills/map-flows/scripts/render_flow.py evals/fixtures/flow-app/after/ux-flows/log-workout.flow.json --output flow-map.html
```
