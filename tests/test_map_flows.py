#!/usr/bin/env python3
"""Behavior tests for the map-flows skill: validation, analysis, comparison, rendering."""

from __future__ import annotations

import copy
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
PYTHON = sys.executable
SKILL = ROOT / "skills" / "map-flows"
SCRIPTS = SKILL / "scripts"
FIXTURE = ROOT / "evals" / "fixtures" / "flow-app"
BEFORE = FIXTURE / "before" / "ux-flows" / "log-workout.flow.json"
AFTER = FIXTURE / "after" / "ux-flows" / "log-workout.flow.json"


def evidence(state: str = "unknown") -> dict[str, str]:
    if state == "unknown":
        return {"state": "unknown"}
    return {"state": state, "source": "code", "ref": "src/app.tsx", "revision": "r1"}


def transition(tid: str, source: str, target: str, **extra: Any) -> dict[str, Any]:
    item = {
        "id": tid,
        "from": source,
        "to": target,
        "action": f"Do {tid}",
        "actor": "user",
        "intent": "approved",
        "evidence": evidence(),
    }
    item.update(extra)
    return item


def sign_in_map() -> dict[str, Any]:
    """A guest must sign in before paying; a declined card can be corrected."""
    return {
        "schema_version": "1.0",
        "map": "checkout",
        "title": "Checkout",
        "product": "Test shop",
        "facts": [
            {"id": "signed-in", "description": "The visitor has a session."},
            {"id": "card-declined", "description": "The provider rejects the card."},
        ],
        "states": [
            {"id": "cart", "kind": "screen", "label": "Cart"},
            {"id": "sign-in", "kind": "screen", "label": "Sign in"},
            {"id": "payment", "kind": "screen", "label": "Payment"},
            {"id": "declined", "kind": "inline", "role": "failure", "label": "Card declined"},
            {"id": "done", "kind": "screen", "label": "Order confirmed"},
        ],
        "transitions": [
            transition("cart.pay", "cart", "payment", requires=["signed-in"]),
            transition("cart.wall", "cart", "sign-in", actor="system", requires=["!signed-in"]),
            transition("sign-in.submit", "sign-in", "cart", effects=["signed-in"], inputs=2),
            transition("payment.pay", "payment", "done", requires=["!card-declined"], inputs=1),
            transition("payment.decline", "payment", "declined", requires=["card-declined"], inputs=1),
            transition("declined.fix", "declined", "payment", effects=["!card-declined"], inputs=1),
        ],
        "journeys": [
            {
                "id": "buy",
                "user": "A shopper",
                "goal": "Pay for the cart",
                "success_condition": "An order number is shown.",
                "entry": "cart",
                "success": ["done"],
                "start_facts": ["signed-in"],
                "critical": True,
                "scenarios": [
                    {"id": "guest", "description": "The shopper has no session.", "facts": ["!signed-in"]},
                    {"id": "declined-card", "description": "The card is declined.", "facts": ["card-declined"]},
                ],
            }
        ],
        "unknowns": [],
    }


class FlowTests(unittest.TestCase):
    maxDiff = None

    def run_script(self, script: str, *args: str, expected: int = 0) -> subprocess.CompletedProcess[str]:
        completed = subprocess.run(
            [PYTHON, str(SCRIPTS / script), *args],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )
        self.assertEqual(
            completed.returncode,
            expected,
            msg=f"{script} returned {completed.returncode}\nstdout:\n{completed.stdout}\nstderr:\n{completed.stderr}",
        )
        return completed

    def run_json(self, script: str, *args: str, expected: int = 0) -> dict[str, Any]:
        return json.loads(self.run_script(script, *args, expected=expected).stdout)

    def with_store(self, flow: dict[str, Any], runs: list[dict[str, Any]] | None = None) -> tuple[Any, Path]:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        path = Path(directory.name) / f"{flow.get('map', 'broken')}.flow.json"
        path.write_text(json.dumps(flow, ensure_ascii=False), encoding="utf-8")
        if runs:
            (path.parent / "runs").mkdir()
            for run in runs:
                (path.parent / "runs" / f"{run['run']}.run.json").write_text(
                    json.dumps(run, ensure_ascii=False), encoding="utf-8"
                )
        return directory, path

    def analyze(self, flow: dict[str, Any], runs: list[dict[str, Any]] | None = None, *args: str) -> dict[str, Any]:
        _, path = self.with_store(flow, runs)
        return self.run_json("analyze_flow.py", str(path), *args)

    @staticmethod
    def scenario(analysis: dict[str, Any], scenario_id: str, journey: int = 0) -> dict[str, Any]:
        return next(item for item in analysis["journeys"][journey]["scenarios"] if item["id"] == scenario_id)

    @staticmethod
    def run_for(flow: dict[str, Any], steps: list[dict[str, Any]], **extra: Any) -> dict[str, Any]:
        run = {
            "schema_version": "1.0",
            "run": "walk-1",
            "map": flow["map"],
            "journey": flow["journeys"][0]["id"],
            "recorded_at": "2026-11-14",
            "revision": "r1",
            "method": "manual",
            "tool": "A person with a browser",
            "environment": {"target": "local build", "viewport": "1280x800", "input": "pointer"},
            "steps": steps,
            "outcome": "abandoned",
            "limitations": [],
        }
        run.update(extra)
        return run

    # --- Fixture stores -------------------------------------------------

    def test_fixture_stores_and_recorded_runs_are_valid(self) -> None:
        for path, runs in ((BEFORE, 4), (AFTER, 5)):
            result = self.run_json("validate_flow.py", str(path))
            self.assertTrue(result["valid"], msg=result["errors"])
            self.assertEqual(len(result["runs"]), runs)
            self.assertTrue(all(run["valid"] for run in result["runs"]))
            self.assertIn("not opened", result["checked"])

    def test_bundled_examples_are_copies_of_the_fixture(self) -> None:
        self.assertEqual(
            (SKILL / "assets" / "flow-map-example.json").read_text(encoding="utf-8"),
            AFTER.read_text(encoding="utf-8"),
        )
        self.assertEqual(
            (SKILL / "assets" / "flow-run-example.json").read_text(encoding="utf-8"),
            (AFTER.parent / "runs" / "after-pointer-default.run.json").read_text(encoding="utf-8"),
        )
        result = self.run_json(
            "validate_flow.py",
            str(SKILL / "assets" / "flow-map-example.json"),
            "--run",
            str(SKILL / "assets" / "flow-run-example.json"),
        )
        self.assertTrue(result["valid"], msg=result["errors"])

    # --- Map contract ---------------------------------------------------

    def test_map_cannot_claim_measured_or_invent_paths(self) -> None:
        measured = sign_in_map()
        measured["transitions"][0]["evidence"] = {"state": "measured", "source": "live", "ref": "it worked"}
        _, path = self.with_store(measured)
        result = self.run_json("validate_flow.py", str(path), expected=1)
        self.assertTrue(any("record a run" in error for error in result["errors"]))

        invented = sign_in_map()
        invented["transitions"][0]["intent"] = "none"
        _, path = self.with_store(invented)
        result = self.run_json("validate_flow.py", str(path), expected=1)
        self.assertTrue(any("invented" in error for error in result["errors"]))

        unsupported = sign_in_map()
        unsupported["transitions"][0]["evidence"] = {"state": "observed"}
        _, path = self.with_store(unsupported)
        result = self.run_json("validate_flow.py", str(path), expected=1)
        self.assertTrue(any("evidence.ref" in error for error in result["errors"]))

    def test_map_rejects_broken_references_and_conditions(self) -> None:
        cases = {
            "not a declared state": lambda flow: flow["transitions"][0].update({"to": "nowhere"}),
            "undeclared fact": lambda flow: flow["transitions"][0].update({"requires": ["vip"]}),
            "both required true and false": lambda flow: flow["transitions"][0].update(
                {"requires": ["signed-in", "!signed-in"]}
            ),
            "duplicate transition id": lambda flow: flow["transitions"].append(copy.deepcopy(flow["transitions"][0])),
            "cannot be a failure state": lambda flow: flow["journeys"][0].update({"success": ["declined"]}),
            "reserved": lambda flow: flow["journeys"][0]["scenarios"][0].update({"id": "default"}),
            "unknowns must be": lambda flow: flow.pop("unknowns"),
        }
        for message, mutate in cases.items():
            flow = sign_in_map()
            mutate(flow)
            _, path = self.with_store(flow)
            result = self.run_json("validate_flow.py", str(path), expected=1)
            self.assertTrue(any(message in error for error in result["errors"]), msg=(message, result["errors"]))

    # --- Runs -----------------------------------------------------------

    def test_run_must_be_one_continuous_honest_walk(self) -> None:
        flow = sign_in_map()
        good = [
            {"transition": "cart.pay", "result": "reached", "landed": "payment", "evidence": "Payment form is shown."},
            {"transition": "payment.pay", "result": "reached", "landed": "done", "evidence": "Order number 1042."},
        ]
        _, path = self.with_store(flow, [self.run_for(flow, good, outcome="success", success_evidence="Order 1042 shown.")])
        self.assertTrue(self.run_json("validate_flow.py", str(path))["valid"])

        broken = {
            "the run was at": [good[1]],
            "use diverged": [{**good[0], "landed": "sign-in"}],
            "ended at": [good[0]],
            "success_evidence": good,
        }
        for message, steps in broken.items():
            extra = {"outcome": "success"}
            if message != "success_evidence":
                extra["success_evidence"] = "Claimed."
            _, path = self.with_store(flow, [self.run_for(flow, steps, **extra)])
            result = self.run_json("validate_flow.py", str(path), expected=1)
            errors = [error for run in result["runs"] for error in run["errors"]]
            self.assertTrue(any(message in error for error in errors), msg=(message, errors))

    def test_baseline_must_be_a_recorded_successful_run(self) -> None:
        flow = sign_in_map()
        flow["journeys"][0]["baseline_run"] = "walk-1"
        blocked = [{"transition": "cart.pay", "result": "blocked", "evidence": "The Pay button is disabled."}]
        _, path = self.with_store(flow, [self.run_for(flow, blocked, outcome="blocked")])
        result = self.run_json("validate_flow.py", str(path), expected=1)
        self.assertTrue(any("reached success" in error for error in result["errors"]))

        flow["journeys"][0]["baseline_run"] = "missing"
        _, path = self.with_store(flow, [self.run_for(flow, blocked, outcome="blocked")])
        result = self.run_json("validate_flow.py", str(path), expected=1)
        self.assertTrue(any("no recorded run" in error for error in result["errors"]))

    # --- Analysis -------------------------------------------------------

    def test_conditions_and_effects_decide_what_is_reachable(self) -> None:
        analysis = self.analyze(sign_in_map())
        member = self.scenario(analysis, "default")["intended"]
        self.assertEqual(member["route"], ["cart.pay", "payment.pay"])
        self.assertEqual((member["user_actions"], member["inputs"], member["screens"]), (2, 1, 3))
        self.assertIsNone(self.scenario(analysis, "default")["as_built"])

        guest = self.scenario(analysis, "guest")["intended"]
        self.assertEqual(guest["route"], ["cart.wall", "sign-in.submit", "cart.pay", "payment.pay"])
        self.assertEqual((guest["user_actions"], guest["system_steps"]), (3, 1))
        self.assertIn("sign-in.submit", guest["mandatory_transitions"])
        self.assertEqual([item["transition"] for item in guest["unavailable_transitions"]], ["payment.decline"])

        declined = self.scenario(analysis, "declined-card")["intended"]
        self.assertTrue(declined["meets_expectation"])
        self.assertEqual(declined["failure_states"], [{"state": "declined", "recovery": "recoverable"}])

    def test_missing_recovery_and_loops_are_reported_as_stuck(self) -> None:
        flow = sign_in_map()
        flow["transitions"] = [item for item in flow["transitions"] if item["id"] != "declined.fix"]
        analysis = self.analyze(flow)
        declined = self.scenario(analysis, "declined-card")["intended"]
        self.assertFalse(declined["meets_expectation"])
        self.assertEqual(declined["failure_states"], [{"state": "declined", "recovery": "trapped"}])
        self.assertIn("declined", declined["dead_ends"])
        kinds = {signal["signal"] for signal in analysis["signals"]}
        self.assertTrue({"goal-unreachable", "dead-end", "failure-without-recovery"} <= kinds)

        # A way out turns a trap into an exit-only failure; a loop with no way out stays a dead end.
        flow["states"].append({"id": "left", "kind": "screen", "label": "Left checkout"})
        flow["transitions"].append(transition("declined.leave", "declined", "left"))
        flow["journeys"][0]["exits"] = ["left"]
        flow["states"] += [
            {"id": "help", "kind": "screen", "label": "Help"},
            {"id": "faq", "kind": "screen", "label": "FAQ"},
        ]
        flow["transitions"] += [
            transition("cart.help", "cart", "help"),
            transition("help.faq", "help", "faq"),
            transition("faq.help", "faq", "help"),
        ]
        analysis = self.analyze(flow)
        declined = self.scenario(analysis, "declined-card")["intended"]
        self.assertEqual(declined["failure_states"], [{"state": "declined", "recovery": "exit-only"}])
        self.assertEqual(self.scenario(analysis, "default")["intended"]["dead_ends"], ["help", "faq"])

    def test_design_and_product_are_analyzed_separately(self) -> None:
        analysis = self.run_json("analyze_flow.py", str(BEFORE))
        default = self.scenario(analysis, "default")
        self.assertEqual(default["intended"]["user_actions"], 4)
        self.assertEqual(default["as_built"]["user_actions"], 5)
        self.assertEqual(default["as_built"]["route"][-2:], ["workout.more", "more.finish"])
        self.assertEqual(default["as_built"]["route_evidence"]["measured"], 5)

        offline = self.scenario(analysis, "offline-at-save")
        self.assertTrue(offline["intended"]["meets_expectation"])
        self.assertFalse(offline["as_built"]["meets_expectation"])
        self.assertEqual(offline["as_built"]["failure_states"], [{"state": "save-failed", "recovery": "exit-only"}])

        self.assertEqual(analysis["evidence"], {"measured": 7, "observed": 6, "inferred": 0, "unknown": 6})
        self.assertEqual(analysis["parity"]["drift"], 4)
        signals = {signal["signal"]: signal for signal in analysis["signals"]}
        self.assertTrue(signals["goal-unreachable"]["designed"])
        self.assertEqual(signals["mandatory-step-not-persistent"]["route_to"], "review-components")
        self.assertEqual(signals["unplanned-path"]["subjects"][0], "more.finish")
        keyboard = next(
            signal for signal in analysis["signals"] if signal["signal"] == "run-drift" and signal["working"]
        )
        self.assertEqual((keyboard["subjects"], keyboard["broken"]), (["workout.add-set"], ["keyboard"]))
        self.assertEqual(keyboard["route_to"], "check-accessibility")

        after = self.run_json("analyze_flow.py", str(AFTER))
        self.assertEqual(after["signals"], [])
        self.assertEqual(after["parity"]["drift"], 0)

    def test_static_evidence_never_counts_as_measured(self) -> None:
        analysis = self.run_json("analyze_flow.py", str(BEFORE), "--no-runs")
        self.assertEqual(analysis["evidence"]["measured"], 0)
        self.assertEqual(analysis["parity"]["aligned"], 0)
        self.assertIn("critical-route-unverified", {signal["signal"] for signal in analysis["signals"]})

    def test_runs_reveal_unenforced_conditions_and_unmapped_actions(self) -> None:
        flow = sign_in_map()
        flow["journeys"][0]["start_facts"] = []
        steps = [
            {"transition": "cart.pay", "result": "reached", "landed": "payment", "evidence": "Payment opened for a guest."},
            {"result": "unmapped", "from": "payment", "action": "Pressed Escape", "landed": "cart", "evidence": "Back on the cart."},
        ]
        analysis = self.analyze(flow, [self.run_for(flow, steps)])
        signals = {signal["signal"]: signal for signal in analysis["signals"]}
        self.assertEqual(signals["guard-not-enforced"]["unmet"], ["signed-in"])
        self.assertEqual(signals["unmapped-step"]["action"], "Pressed Escape")

    def test_evidence_from_another_revision_is_stale(self) -> None:
        fresh = self.run_json("analyze_flow.py", str(AFTER), "--revision", "flow-app-after")
        self.assertNotIn("stale-evidence", {signal["signal"] for signal in fresh["signals"]})
        stale = self.run_json("analyze_flow.py", str(AFTER), "--revision", "next-release")
        signal = next(item for item in stale["signals"] if item["signal"] == "stale-evidence")
        self.assertEqual(len(signal["subjects"]), 16)
        self.assertEqual(signal["route_to"], "verify-changes")

    def test_analysis_refuses_invalid_input_instead_of_guessing(self) -> None:
        flow = sign_in_map()
        flow["transitions"][0]["to"] = "nowhere"
        _, path = self.with_store(flow)
        completed = self.run_script("analyze_flow.py", str(path), expected=2)
        self.assertIn("not a valid flow map", completed.stderr)
        self.assertEqual(completed.stdout, "")

    # --- Comparison -----------------------------------------------------

    def test_comparison_names_regressions_only_when_something_stops_working(self) -> None:
        forward = self.run_json("compare_flows.py", str(BEFORE), str(AFTER))
        self.assertEqual(forward["verdict"], "no-regression")
        self.assertEqual(forward["regressions"], [])
        gained = {item["improvement"] for item in forward["improvements"]}
        self.assertTrue({"expected-end-gained", "recovery-gained", "run-result-gained", "run-outcome-gained"} <= gained)
        # Discarding now takes one more action because it asks first: a change, not a regression.
        discard = next(
            item
            for item in forward["changes"]
            if item["change"] == "effort-changed" and item["journey"] == "discard-workout" and item["layer"] == "as-built"
        )
        self.assertEqual(discard["effort"]["user_actions"], {"before": 2, "after": 3})
        self.assertTrue(any(item.get("scenario") == "reps-left-empty" for item in forward["not_compared"]))

        backward = self.run_json("compare_flows.py", str(AFTER), str(BEFORE), expected=1)
        self.assertEqual(backward["verdict"], "regression")
        lost = {item["regression"] for item in backward["regressions"]}
        self.assertEqual(lost, {"expected-end-lost", "recovery-lost", "run-result-lost", "run-outcome-lost"})
        keyboard = next(
            item for item in backward["regressions"] if item["regression"] == "run-result-lost" and item["input"] == "keyboard"
        )
        self.assertEqual(keyboard["subject"], "workout.add-set")

    def test_comparison_detects_a_new_dead_end_and_refuses_unrelated_maps(self) -> None:
        before = sign_in_map()
        after = sign_in_map()
        after["transitions"] = [item for item in after["transitions"] if item["id"] != "declined.fix"]
        _, before_path = self.with_store(before)
        _, after_path = self.with_store(after)
        result = self.run_json("compare_flows.py", str(before_path), str(after_path), expected=1)
        kinds = {item["regression"] for item in result["regressions"]}
        self.assertTrue({"expected-end-lost", "dead-end-added", "recovery-lost"} <= kinds)

        other = sign_in_map()
        other["map"] = "onboarding"
        _, other_path = self.with_store(other)
        result = self.run_json("compare_flows.py", str(before_path), str(other_path), expected=1)
        self.assertEqual(result["verdict"], "not-comparable")

    # --- Rendering ------------------------------------------------------

    def test_rendered_page_is_self_contained_deterministic_and_localized(self) -> None:
        pages = {}
        for language in ("en", "ko", "ja"):
            html = self.run_script("render_flow.py", str(BEFORE), "--language", language).stdout
            pages[language] = html
            self.assertIn(f'<html lang="{language}">', html)
            self.assertNotIn("{{", html)
            self.assertNotRegex(html, r'(?:src|href)=["\']https?://')
            self.assertEqual(html.count("<svg xmlns"), 2, msg="one map per journey")
            self.assertIn('role="img"', html)
        self.assertEqual(pages["en"], self.run_script("render_flow.py", str(BEFORE), "--language", "en").stdout)
        self.assertIn("BLOCKED · KEYBOARD", pages["en"])
        self.assertIn("Hand to check-accessibility", pages["en"])
        self.assertIn("막힘 · 키보드", pages["ko"])
        self.assertIn("ブロック · キーボード", pages["ja"])

        template = (SKILL / "assets" / "flow-page-template.html").read_text(encoding="utf-8")
        style = template.split("<style>", 1)[1].split("</style>", 1)[0]
        self.assertIn('@media (prefers-color-scheme: dark)', style)
        self.assertIn(':root[data-theme="dark"]', style)
        defined = set(re.findall(r"\.([a-z][a-z0-9-]*)", style))
        used = {name for group in re.findall(r'class="([^"]+)"', pages["en"]) for name in group.split()}
        self.assertEqual(sorted(used - defined), [], msg="rendered classes missing from the template stylesheet")

    def test_page_strings_are_complete_in_every_language(self) -> None:
        bank = json.loads((SKILL / "assets" / "flow-page-strings.json").read_text(encoding="utf-8"))
        self.assertEqual(set(bank), {"en", "ko", "ja"})
        self.assertEqual(set(bank["en"]), set(bank["ko"]))
        self.assertEqual(set(bank["en"]), set(bank["ja"]))
        for language, strings in bank.items():
            for key, text in strings.items():
                self.assertTrue(text.strip(), msg=(language, key))
                self.assertEqual(
                    sorted(re.findall(r"\{(\w+)\}", text)),
                    sorted(re.findall(r"\{(\w+)\}", bank["en"][key])),
                    msg=f"{language}:{key} placeholders differ from English",
                )

    def test_mermaid_output_marks_evidence_in_words(self) -> None:
        text = self.run_script("render_flow.py", str(BEFORE), "--format", "mermaid").stdout
        self.assertTrue(text.startswith("flowchart TD\n"))
        self.assertIn('workout ==>|"Open the “More” menu [Verified by a run]"| more_menu', text)
        self.assertIn("--x|", text)
        self.assertIn("[No evidence]", text)

    def test_text_wrapping_handles_long_and_unspaced_labels(self) -> None:
        spec = importlib.util.spec_from_file_location("render_flow", SCRIPTS / "render_flow.py")
        assert spec and spec.loader
        module = importlib.util.module_from_spec(spec)
        sys.path.insert(0, str(SCRIPTS))
        try:
            spec.loader.exec_module(module)
        finally:
            sys.path.remove(str(SCRIPTS))
        for text in (
            "Choose an exercise, enter weight and reps, then activate “Save set” and wait for the list to refresh",
            "運動の種類を選び重量と回数を入力してから保存ボタンを押して一覧が更新されるのを待つ",
            "Supercalifragilisticexpialidocious-and-then-some-more-without-any-space",
        ):
            lines = module.wrap_text(text, 13, 300, 2)
            self.assertLessEqual(len(lines), 2)
            for line in lines:
                self.assertLessEqual(module.text_width(line, 13), 300.5, msg=line)
        # One-letter words keep their spaces; only an over-long word breaks per character.
        self.assertEqual(module.wrap_text("Enter a value in I/O", 13, 300, 2), ["Enter a value in I/O"])
        self.assertEqual(module.wrap_text("Pick a plan, then confirm it on the next screen", 13, 150, 3)[0], "Pick a plan, then")

    # --- Contracts shared with the rest of the catalog --------------------

    def test_schema_enums_match_validator_constants(self) -> None:
        spec = importlib.util.spec_from_file_location("validate_flow", SCRIPTS / "validate_flow.py")
        assert spec and spec.loader
        validator = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(validator)
        flow = json.loads((SKILL / "assets" / "flow-map.schema.json").read_text(encoding="utf-8"))["properties"]
        run = json.loads((SKILL / "assets" / "flow-run.schema.json").read_text(encoding="utf-8"))["properties"]
        state = flow["states"]["items"]["properties"]
        item = flow["transitions"]["items"]["properties"]
        journey = flow["journeys"]["items"]["properties"]
        pairs = [
            (state["kind"]["enum"], validator.STATE_KINDS),
            (state["role"]["enum"], validator.STATE_ROLES),
            (item["actor"]["enum"], validator.ACTORS),
            (item["visibility"]["enum"], validator.VISIBILITIES),
            (item["intent"]["enum"], validator.INTENTS),
            (item["evidence"]["properties"]["state"]["enum"], validator.MAP_EVIDENCE_STATES),
            (item["evidence"]["properties"]["source"]["enum"], validator.EVIDENCE_SOURCES),
            (journey["expect"]["enum"], validator.EXPECTATIONS),
            (run["method"]["enum"], validator.RUN_METHODS),
            (run["environment"]["properties"]["input"]["enum"], validator.RUN_INPUTS),
            (run["steps"]["items"]["properties"]["result"]["enum"], validator.STEP_RESULTS),
            (run["outcome"]["enum"], validator.RUN_OUTCOMES),
        ]
        for schema_values, constants in pairs:
            self.assertEqual(list(schema_values), list(constants))
        self.assertEqual(flow["schema_version"]["const"], validator.SCHEMA_VERSION)
        self.assertNotIn("measured", item["evidence"]["properties"]["state"]["enum"])

    def test_existing_skills_know_how_to_cooperate(self) -> None:
        workflow = (ROOT / "skills/design-workflow/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("### Journey or flow request", workflow)
        self.assertIn("`map-flows` in design mode", workflow)
        composition = (ROOT / "skills/design-workflow/references/composition-map.md").read_text(encoding="utf-8")
        limited = composition.split("### Map flows (`map-flows`)", 1)[1].split("\n### ", 1)[0]
        for phrase in ("do not record a run", "do not write flow map files", "not evidence that the product has it"):
            self.assertIn(phrase, " ".join(limited.split()))
        for skill, phrase in (
            ("plan-structure", "hand the decision to `map-flows`"),
            ("review-components", "flow map findings from `map-flows`"),
            ("check-accessibility", "recorded by `map-flows`"),
            ("audit-design", "to `map-flows`"),
            ("verify-changes", "`journey-paths`"),
        ):
            text = (ROOT / "skills" / skill / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn(phrase, " ".join(text.split()), msg=skill)

        report = json.loads(
            (ROOT / "skills/verify-changes/assets/verification-targeted-example.json").read_text(encoding="utf-8")
        )
        report["checks"].append(
            {
                "id": "journey-log-workout",
                "test": "journey-paths",
                "required": True,
                "status": "pass",
                "evidence_state": "measured",
                "evidence": "compare_flows.py reported no regression; runs after-pointer-default and after-keyboard-default.",
                "impact": "Members can still log and save a workout.",
                "remediation": "None.",
                "verification": "Repeat the two runs after the next change to the workout screen.",
                "owner": "Product team",
            }
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "verification.json"
            path.write_text(json.dumps(report), encoding="utf-8")
            completed = subprocess.run(
                [PYTHON, str(ROOT / "skills/verify-changes/scripts/validate_verification.py"), str(path)],
                capture_output=True,
                text=True,
                encoding="utf-8",
                check=False,
            )
        self.assertEqual(completed.returncode, 0, msg=completed.stdout + completed.stderr)
        self.assertTrue(json.loads(completed.stdout)["valid_report"])

    def test_installed_alone_the_skill_runs_from_another_directory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "skills"
            workdir = Path(directory) / "project"
            workdir.mkdir()
            completed = subprocess.run(
                [PYTHON, str(ROOT / "scripts" / "install.py"), "--client", "generic", "--target", str(target), "--skill", "map-flows"],
                cwd=workdir,
                capture_output=True,
                text=True,
                encoding="utf-8",
                check=False,
            )
            self.assertEqual(completed.returncode, 0, msg=completed.stderr)
            package = target / "map-flows"
            rendered = subprocess.run(
                [
                    PYTHON,
                    str(package / "scripts" / "render_flow.py"),
                    str(package / "assets" / "flow-map-example.json"),
                    "--run",
                    str(package / "assets" / "flow-run-example.json"),
                ],
                cwd=workdir,
                capture_output=True,
                text=True,
                encoding="utf-8",
                check=False,
            )
            self.assertEqual(rendered.returncode, 0, msg=rendered.stderr)
            self.assertIn("Log a workout", rendered.stdout)
            self.assertEqual(list(workdir.iterdir()), [])


if __name__ == "__main__":
    unittest.main()
