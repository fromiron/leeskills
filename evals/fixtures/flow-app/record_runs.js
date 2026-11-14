#!/usr/bin/env node
// Records flow runs against the flow-app fixture with a real browser.
//
// Evaluation tooling only. No skill depends on it, and the repository's
// validation does not run it. It needs Playwright with Chromium:
//
//   node evals/fixtures/flow-app/record_runs.js
//
// For each scripted run it performs the actions, reads what the page shows
// afterwards, and writes <variant>/ux-flows/runs/<run>.run.json. A step is
// `reached` only when the page ends up in the state the map declares.

const fs = require("fs");
const path = require("path");
const { chromium } = require("playwright");

const ROOT = __dirname;
const VIEWPORT = { width: 390, height: 844 };
const TAB_LIMIT = 30;

// What each transition means in the fixture: the controls to operate.
const ACTIONS = {
  "today.start": [["activate", "#start-workout"]],
  "workout.add-set": [["activate", "#add-set"]],
  "set-form.save": [["choose", "#exercise", "Bench press"], ["type", "#weight", "60"], ["type", "#reps", "8"], ["activate", "#save-set"]],
  "set-form.save-without-reps": [["choose", "#exercise", "Bench press"], ["type", "#weight", "60"], ["activate", "#save-set"]],
  "set-error.save": [["type", "#reps", "8"], ["activate", "#save-set"]],
  "workout.finish": [["activate", "#workout-view > .row #finish"]],
  "workout.finish-offline": [["activate", "#workout-view > .row #finish"]],
  "workout.more": [["activate", "#more"]],
  "more.finish": [["activate", "#more-menu #finish"]],
  "more.finish-offline": [["activate", "#more-menu #finish"]],
  "more.discard-confirm": [["activate", "#more-menu #discard"]],
  "discard-confirm.discard": [["activate", "#confirm-discard"]],
  "save-failed.reconnect": [["connection", "online"]],
  "save-failed.retry": [["activate", "#retry"]],
};

// `probe: true` marks a step the run attempts and then moves past when blocked.
const RUNS = [
  { variant: "before", run: "before-pointer-default", journey: "log-workout", scenario: "default", input: "pointer",
    steps: ["today.start", "workout.add-set", "set-form.save", { t: "workout.finish", probe: true }, "workout.more", "more.finish"] },
  { variant: "before", run: "before-keyboard-default", journey: "log-workout", scenario: "default", input: "keyboard",
    steps: ["today.start", "workout.add-set", "set-form.save", "workout.more", "more.finish"] },
  { variant: "before", run: "before-pointer-offline", journey: "log-workout", scenario: "offline-at-save", input: "pointer",
    steps: ["today.start", "workout.add-set", "set-form.save", "workout.more", "more.finish-offline", "save-failed.reconnect", "save-failed.retry"] },
  { variant: "before", run: "before-pointer-discard", journey: "discard-workout", scenario: "default", input: "pointer",
    steps: ["workout.more", "more.discard-confirm"] },
  { variant: "after", run: "after-pointer-default", journey: "log-workout", scenario: "default", input: "pointer",
    steps: ["today.start", "workout.add-set", "set-form.save", "workout.finish"] },
  { variant: "after", run: "after-keyboard-default", journey: "log-workout", scenario: "default", input: "keyboard",
    steps: ["today.start", "workout.add-set", "set-form.save", "workout.finish"] },
  { variant: "after", run: "after-pointer-offline", journey: "log-workout", scenario: "offline-at-save", input: "pointer",
    steps: ["today.start", "workout.add-set", "set-form.save", "workout.finish-offline", "save-failed.reconnect", "save-failed.retry"] },
  { variant: "after", run: "after-pointer-reps-left-empty", journey: "log-workout", scenario: "reps-left-empty", input: "pointer",
    steps: ["today.start", "workout.add-set", "set-form.save-without-reps", "set-error.save", "workout.finish"] },
  { variant: "after", run: "after-pointer-discard", journey: "discard-workout", scenario: "default", input: "pointer",
    steps: ["workout.more", "more.discard-confirm", "discard-confirm.discard"] },
];

// Read the state from what the page shows, never from the script's intent.
async function detect(page) {
  const file = path.basename(new URL(page.url()).pathname);
  const visible = async (selector) => (await page.locator(selector).count()) > 0 && page.locator(selector).first().isVisible();
  if (file === "today.html") {
    return (await visible("#discarded-notice"))
      ? { state: "discarded", seen: "today.html shows the notice “Workout discarded.”" }
      : { state: "today", seen: "today.html shows the heading “Today” and “Start workout”" };
  }
  if (file === "summary.html") {
    const sets = await page.locator("#sets li").allTextContents();
    return { state: "summary", seen: `summary.html shows the heading “Workout saved” and ${sets.length} logged set(s): ${sets.join("; ") || "none"}` };
  }
  if (await visible("dialog#discard-confirm[open]")) return { state: "discard-confirm", seen: "workout.html shows the dialog “Discard this workout?”" };
  if (await visible("dialog#set-form[open]")) {
    return (await visible("#reps-error"))
      ? { state: "set-error", seen: "the Add set dialog shows “Enter the number of reps.” with focus on Reps" }
      : { state: "set-form", seen: "workout.html shows the dialog “Add set”" };
  }
  if (await visible("#failed-view")) {
    const controls = await page.locator("#failed-view button").allTextContents();
    return { state: "save-failed", seen: `workout.html shows “${(await page.locator("#failed-view [role=alert]").textContent()).trim()}” with the controls: ${controls.join(", ")}` };
  }
  if (await visible("#more-menu")) {
    const items = await page.locator("#more-menu button").allTextContents();
    return { state: "more-menu", seen: `the More menu is open with: ${items.join(", ")}` };
  }
  const sets = await page.locator("#sets li").count();
  return { state: "workout", seen: `workout.html shows “Active workout” with ${sets} logged set(s)` };
}

async function focusByTab(page, selector) {
  for (let presses = 1; presses <= TAB_LIMIT; presses += 1) {
    await page.keyboard.press("Tab");
    if (await page.evaluate((sel) => document.activeElement?.matches(sel) ?? false, selector)) return presses;
  }
  return null;
}

// Returns null on success, or the reason the action could not be performed.
async function perform(page, [kind, target, value], input) {
  if (kind === "connection") {
    const wanted = value ?? target;
    const state = (await page.locator("#connection-state").textContent()).trim();
    if (state !== wanted) await page.locator("#toggle-connection").click();
    return null;
  }
  const locator = page.locator(target).first();
  if ((await page.locator(target).count()) === 0 || !(await locator.isVisible())) return `no visible control matches ${target}`;
  if (input === "keyboard") {
    const presses = await focusByTab(page, target);
    if (presses === null) return `Tab did not reach ${target} in ${TAB_LIMIT} presses`;
    if (kind === "activate") {
      if (await locator.isDisabled()) return `${target} is disabled`;
      await page.keyboard.press("Enter");
    } else {
      await page.keyboard.type(value);
    }
    return null;
  }
  if (kind === "activate") {
    if (await locator.isDisabled()) return `${target} is disabled`;
    await locator.click();
  } else if (kind === "choose") {
    await locator.selectOption({ label: value });
  } else {
    await locator.fill(value);
  }
  return null;
}

function describe(actions, input) {
  return actions
    .map(([kind, target, value]) => {
      if (kind === "connection") return `switched the fixture's connection control to ${value ?? target}`;
      const how = input === "keyboard" ? "by Tab and keyboard" : "by pointer";
      if (kind === "activate") return `activated ${target} ${how}`;
      return `${kind === "choose" ? "chose" : "typed"} “${value}” in ${target} ${how}`;
    })
    .join(", ");
}

async function record(browser, spec, versions) {
  const mapPath = path.join(ROOT, spec.variant, "ux-flows", "log-workout.flow.json");
  const flow = JSON.parse(fs.readFileSync(mapPath, "utf8"));
  const transitions = Object.fromEntries(flow.transitions.map((item) => [item.id, item]));
  const journey = flow.journeys.find((item) => item.id === spec.journey);
  const entry = flow.states.find((item) => item.id === journey.entry);
  const offline = spec.scenario === "offline-at-save";

  const context = await browser.newContext({ viewport: VIEWPORT });
  const page = await context.newPage();
  const entryFile = entry.route.split("?")[0];
  await page.goto(`file://${path.join(ROOT, spec.variant, entryFile)}${offline ? "?offline=1" : ""}`);

  const steps = [];
  let current = (await detect(page)).state;
  for (const item of spec.steps) {
    const id = typeof item === "string" ? item : item.t;
    const transition = transitions[id];
    if (!transition) throw new Error(`${spec.run}: ${id} is not in ${mapPath}`);
    let reason = null;
    for (const action of ACTIONS[id]) {
      reason = await perform(page, action, spec.input);
      if (reason) break;
    }
    // A key press does not wait for navigation the way a click does.
    await page.waitForTimeout(150);
    await page.waitForLoadState("load");
    const after = await detect(page);
    if (reason) {
      steps.push({ transition: id, result: "blocked", landed: after.state, evidence: `Could not perform the action: ${reason}. Afterwards ${after.seen}.` });
      current = after.state;
      if (typeof item === "string" || !item.probe) break;
      continue;
    }
    const result = after.state === transition.to ? "reached" : "diverged";
    steps.push({ transition: id, result, landed: after.state, evidence: `${describe(ACTIONS[id], spec.input)}; afterwards ${after.seen}.` });
    current = after.state;
    if (result === "diverged") break;
  }
  const final = await detect(page);
  await context.close();

  const failure = flow.states.find((item) => item.id === current)?.role === "failure";
  const outcome = journey.success.includes(current)
    ? "success"
    : steps[steps.length - 1].result === "blocked"
      ? "blocked"
      : failure ? "failure" : "abandoned";
  const run = {
    schema_version: "1.0",
    run: spec.run,
    map: flow.map,
    journey: spec.journey,
    scenario: spec.scenario,
    recorded_at: new Date().toISOString().slice(0, 10),
    revision: `flow-app-${spec.variant}`,
    method: "browser-automation",
    tool: `Playwright ${versions.playwright} (Chromium ${versions.chromium})`,
    environment: {
      target: `evals/fixtures/flow-app/${spec.variant}/${entryFile} opened from a file URL`,
      viewport: `${VIEWPORT.width}x${VIEWPORT.height}`,
      input: spec.input,
      locale: "en",
    },
    steps,
    outcome,
    ...(outcome === "success" ? { success_evidence: `The run ended where ${final.seen}.` } : {}),
    limitations: [
      "A static fixture opened from a file URL; no server, account, or real network is involved.",
      ...(offline ? ["The lost connection is simulated with the fixture's connection control."] : []),
      ...(spec.input === "keyboard" ? ["Keyboard input means Tab, typing, and Enter in Chromium; no screen reader was used."] : []),
    ],
  };
  const out = path.join(ROOT, spec.variant, "ux-flows", "runs", `${spec.run}.run.json`);
  fs.mkdirSync(path.dirname(out), { recursive: true });
  fs.writeFileSync(out, `${JSON.stringify(run, null, 2)}\n`);
  console.log(`${spec.run}: ${outcome} (${steps.map((step) => `${step.transition}=${step.result}`).join(", ")})`);
}

(async () => {
  const browser = await chromium.launch();
  const versions = { playwright: require("playwright/package.json").version, chromium: browser.version() };
  for (const spec of RUNS) await record(browser, spec, versions);
  await browser.close();
})().catch((error) => {
  console.error(error);
  process.exit(1);
});
