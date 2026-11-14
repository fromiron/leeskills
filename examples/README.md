# Examples

These fixtures demonstrate how to invoke and exchange data with the skills.
They are not claims about a real product and are not production accessibility
or usability evidence.

- `full-audit-request.md` — representative end-to-end request.
- `content-inventory.json` — grounded content contract.
- `visual-budget.json` — complexity-budget contract with deliberate overages.
- `manual-agent-integration.md` — minimal integration for clients without native
  Agent Skills discovery.
- `token-proposal-guided.en.json`, `token-proposal-guided.ja.json` — English and
  Japanese copies of the Korean guided token proposal in
  `skills/review-visuals/assets/token-proposal-guided-example.json`. The README
  screenshots in `.github/assets/showcase/` are rendered from these three files
  with `render_token_proposal.py`.

A complete flow map store, with runs recorded by a real browser and a before
and after to compare, lives in
[`evals/fixtures/flow-app/`](../evals/fixtures/flow-app/README.md). The flow
map screenshots in the READMEs are rendered from its `before/` store with
`render_flow.py`.

Canonical schemas and richer examples remain inside each skill's `assets/`
directory so the skill can be distributed independently.
