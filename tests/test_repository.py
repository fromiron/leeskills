#!/usr/bin/env python3
"""Repository and bundled helper tests."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable


class CommandTests(unittest.TestCase):
    def run_command(
        self,
        *args: str,
        expected: int = 0,
        input_text: str | None = None,
    ) -> subprocess.CompletedProcess[str]:
        completed = subprocess.run(
            [PYTHON, *args],
            cwd=ROOT,
            input=input_text,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(
            completed.returncode,
            expected,
            msg=(
                f"command returned {completed.returncode}, expected {expected}\n"
                f"stdout:\n{completed.stdout}\nstderr:\n{completed.stderr}"
            ),
        )
        return completed

    def run_json(self, *args: str, expected: int = 0) -> dict[str, object]:
        completed = self.run_command(*args, expected=expected)
        try:
            value = json.loads(completed.stdout)
        except json.JSONDecodeError as exc:
            self.fail(f"command did not emit JSON: {exc}\n{completed.stdout}")
        self.assertIsInstance(value, dict)
        return value

    def run_json_document(
        self,
        script: str,
        document: dict[str, object],
        *,
        expected: int = 0,
    ) -> dict[str, object]:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "input.json"
            path.write_text(json.dumps(document), encoding="utf-8")
            return self.run_json(script, str(path), expected=expected)

    def test_repository_validator(self) -> None:
        result = self.run_json("scripts/validate_repo.py")
        self.assertTrue(result["valid"])
        self.assertEqual(result["name"], "leeskills")
        self.assertEqual(result["skill_count"], 9)
        self.assertEqual(result["errors"], [])

    def test_project_package_name_is_leeskills(self) -> None:
        manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["name"], "leeskills")
        pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
        self.assertRegex(pyproject, r'(?m)^name = "leeskills"$')

    def test_audit_example_scores_as_redesign(self) -> None:
        result = self.run_json(
            "skills/slop-signal-audit/scripts/score_audit.py",
            "skills/slop-signal-audit/assets/audit-example.json",
        )
        self.assertEqual(result["quality_score"], 57.0)
        self.assertEqual(result["slop_risk_score"], 43.0)
        self.assertEqual(result["verdict"], "redesign")

    def test_audit_unknown_evidence_cannot_receive_full_credit(self) -> None:
        maxima = {
            "content_grounding": 20,
            "task_structure": 15,
            "visual_entropy": 15,
            "typography_spacing_alignment": 15,
            "component_necessity": 10,
            "image_relevance_authenticity": 10,
            "accessibility": 10,
            "motion_interaction": 5,
        }
        document = {
            "categories": {
                name: {
                    "score": maximum,
                    "max": maximum,
                    "evidence_state": "unknown",
                    "evidence": "Not inspected.",
                }
                for name, maximum in maxima.items()
            },
            "hard_failures": [],
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "audit.json"
            path.write_text(json.dumps(document), encoding="utf-8")
            completed = self.run_command(
                "skills/slop-signal-audit/scripts/score_audit.py",
                str(path),
                expected=2,
            )
        self.assertIn("evidence_state is unknown", completed.stderr)

    def test_content_inventory_example_is_valid(self) -> None:
        result = self.run_json(
            "skills/content-grounding/scripts/validate_inventory.py",
            "skills/content-grounding/assets/content-inventory-example.json",
        )
        self.assertTrue(result["valid"])
        self.assertEqual(result["status_counts"]["placeholder"], 1)
        self.assertEqual(result["status_counts"]["prohibited"], 1)
        self.assertEqual(result["status_counts"]["verified"], 1)

    def test_structure_example_is_valid(self) -> None:
        result = self.run_json(
            "skills/structure-selector/scripts/validate_structure.py",
            "skills/structure-selector/assets/structure-decision-example.json",
        )
        self.assertTrue(result["valid"])
        self.assertEqual(result["dominant_grammar"], "portfolio-index")

    def test_visual_budget_example_exposes_overages(self) -> None:
        result = self.run_json(
            "skills/visual-entropy-budget/scripts/check_budget.py",
            "skills/visual-entropy-budget/assets/visual-budget-example.json",
            expected=1,
        )
        self.assertFalse(result["pass"])
        self.assertEqual(result["unresolved_overages"], 10)
        self.assertEqual(result["documented_exceptions"], 1)

    def test_visual_budget_rejects_empty_metric_maps(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "budget.json"
            path.write_text(
                json.dumps({"artifact": "x", "observed": {}, "limits": {}, "exceptions": []}),
                encoding="utf-8",
            )
            completed = self.run_command(
                "skills/visual-entropy-budget/scripts/check_budget.py",
                str(path),
                expected=2,
            )
        self.assertIn("limits missing core metrics", completed.stderr)

    def test_visual_budget_exception_requires_human_review(self) -> None:
        limits = {
            "layout_grammars": 1,
            "typeface_families": 1,
            "type_roles": 6,
            "accent_colors": 1,
            "radius_tokens": 2,
            "shadow_levels": 1,
            "surface_styles": 3,
            "primary_cta_styles": 1,
            "secondary_cta_styles": 1,
            "motion_patterns": 2,
            "decorative_image_families": 0,
        }
        observed = dict(limits)
        observed["typeface_families"] = 2
        result = self.run_json_document(
            "skills/visual-entropy-budget/scripts/check_budget.py",
            {
                "artifact": "Editorial site",
                "observed": observed,
                "limits": limits,
                "exceptions": [
                    {
                        "metric": "typeface_families",
                        "reason": "Code and prose have distinct reading roles.",
                        "evidence": "The content inventory includes long-form prose and code blocks.",
                    }
                ],
            },
            expected=1,
        )
        self.assertFalse(result["pass"])
        self.assertTrue(result["review_required"])
        self.assertEqual(result["budget_status"], "review-required")

    def test_motion_example_has_no_hard_failure(self) -> None:
        result = self.run_json(
            "skills/motion-necessity-gate/scripts/validate_motion_inventory.py",
            "skills/motion-necessity-gate/assets/motion-inventory-example.json",
        )
        self.assertTrue(result["valid"])
        self.assertEqual(result["hard_failures"], [])

    def test_accessibility_example_blocks_release(self) -> None:
        result = self.run_json(
            "skills/accessibility-simplicity-guard/scripts/validate_accessibility_report.py",
            "skills/accessibility-simplicity-guard/assets/accessibility-report-example.json",
            expected=1,
        )
        self.assertTrue(result["valid_report"])
        self.assertFalse(result["release_ready"])
        self.assertEqual(len(result["blockers"]), 2)

    def test_accessibility_optional_failure_still_blocks_release(self) -> None:
        result = self.run_json_document(
            "skills/accessibility-simplicity-guard/scripts/validate_accessibility_report.py",
            {
                "artifact": "Example form",
                "target": {"standard": "WCAG 2.2", "level": "AA"},
                "evidence": ["Keyboard test"],
                "accepted_risks": ["focus-visible:fail"],
                "checks": [
                    {
                        "id": "focus-visible",
                        "criterion": "2.4.7",
                        "level": "AA",
                        "required": False,
                        "status": "fail",
                        "evidence": "Focus is not visible.",
                        "impact": "Keyboard users lose location.",
                        "fix": "Restore a visible focus indicator.",
                        "verification": "Repeat the keyboard test.",
                    }
                ],
            },
            expected=1,
        )
        self.assertTrue(result["valid_report"])
        self.assertFalse(result["release_ready"])
        self.assertIn("owner decision still required", result["blockers"][0])

    def test_schema_examples_include_required_top_level_fields(self) -> None:
        for schema_path in sorted((ROOT / "skills").glob("*/assets/*.schema.json")):
            example_path = schema_path.with_name(schema_path.name.replace(".schema", "-example"))
            self.assertTrue(example_path.is_file(), msg=f"missing example for {schema_path}")
            schema = json.loads(schema_path.read_text(encoding="utf-8"))
            example = json.loads(example_path.read_text(encoding="utf-8"))
            missing = sorted(set(schema.get("required", [])) - set(example))
            self.assertEqual(missing, [], msg=f"{example_path} does not satisfy {schema_path}")

    def test_prune_example_is_release_ready_with_declared_scope(self) -> None:
        result = self.run_json(
            "skills/prune-and-verify/scripts/validate_verification.py",
            "skills/prune-and-verify/assets/verification-example.json",
        )
        self.assertTrue(result["valid_report"])
        self.assertTrue(result["release_ready"])
        self.assertEqual(result["status_counts"]["pass"], 10)
        self.assertEqual(result["status_counts"]["unknown"], 1)

    def test_prune_baseline_failure_cannot_be_marked_optional(self) -> None:
        baseline = {
            "deletion",
            "substitution",
            "semantic-structure",
            "glance-hierarchy",
            "primary-task",
            "growth",
            "reflow",
            "keyboard-focus",
            "reduced-motion",
            "provenance",
        }
        checks = [
            {
                "id": test,
                "test": test,
                "required": False,
                "status": "fail",
                "evidence_state": "observed",
                "evidence": "The check failed.",
                "impact": "The declared requirement is not preserved.",
                "remediation": "Fix the failure.",
                "verification": "Repeat the check.",
                "owner": "QA",
            }
            for test in sorted(baseline)
        ]
        result = self.run_json_document(
            "skills/prune-and-verify/scripts/validate_verification.py",
            {
                "artifact": "Example redesign",
                "primary_user": "User",
                "primary_task": "Complete the task",
                "success_condition": "The task succeeds",
                "evidence": [],
                "changes": [],
                "checks": checks,
                "accepted_risks": [],
                "limitations": [],
            },
            expected=1,
        )
        self.assertTrue(result["valid_report"])
        self.assertFalse(result["release_ready"])
        self.assertGreaterEqual(len(result["blockers"]), 10)

    def test_trigger_evals_cover_english_korean_and_japanese(self) -> None:
        for skill_dir in sorted((ROOT / "skills").iterdir()):
            if not skill_dir.is_dir():
                continue
            path = skill_dir / "evals" / "trigger_queries.json"
            queries = json.loads(path.read_text(encoding="utf-8"))
            counts = {
                language: {True: 0, False: 0}
                for language in ("en", "ko", "ja")
            }
            for item in queries:
                counts[item["language"]][item["should_trigger"]] += 1
            for language in ("en", "ko", "ja"):
                self.assertGreaterEqual(counts[language][True], 2, msg=f"{path}: {language}")
                self.assertGreaterEqual(counts[language][False], 2, msg=f"{path}: {language}")

    def test_measured_trigger_results_are_evaluated_per_language(self) -> None:
        queries_path = ROOT / "skills" / "anti-ai-slop" / "evals" / "trigger_queries.json"
        queries = json.loads(queries_path.read_text(encoding="utf-8"))
        measurements = {
            "client": "example-agent",
            "skill_name": "anti-ai-slop",
            "results": [
                {
                    "id": item["id"],
                    "attempts": 3,
                    "triggered": 2 if item["should_trigger"] else 1,
                }
                for item in queries
            ],
        }
        with tempfile.TemporaryDirectory() as directory:
            result_path = Path(directory) / "results.json"
            result_path.write_text(json.dumps(measurements), encoding="utf-8")
            result = self.run_json(
                "scripts/evaluate_trigger_results.py",
                str(queries_path),
                str(result_path),
            )
        self.assertTrue(result["pass"])
        self.assertEqual(set(result["languages"]), {"en", "ko", "ja"})

    def test_specificity_linter_flags_review_items_without_failing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "copy.txt"
            path.write_text(
                "A seamless platform that empowers every team and improves results by 40%.",
                encoding="utf-8",
            )
            result = self.run_json(
                "skills/specificity-editor/scripts/lint_copy.py",
                str(path),
                "--format",
                "json",
            )
        self.assertGreaterEqual(result["finding_count"], 4)
        finding_types = {item["type"] for item in result["findings"]}
        self.assertIn("watchlist-phrase", finding_types)
        self.assertIn("numeric-claim", finding_types)
        self.assertIn("universal-claim", finding_types)

    def test_generic_installer_dry_run_copy_and_conflict_guard(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "skills"
            dry = self.run_json(
                "scripts/install.py",
                "--client",
                "generic",
                "--target",
                str(target),
                "--skill",
                "content-grounding",
                "--dry-run",
            )
            self.assertEqual(dry["installed"], [])
            self.assertFalse(target.exists())

            installed = self.run_json(
                "scripts/install.py",
                "--client",
                "generic",
                "--target",
                str(target),
                "--skill",
                "content-grounding",
            )
            self.assertEqual(installed["installed"], ["content-grounding"])
            self.assertTrue((target / "content-grounding" / "SKILL.md").is_file())

            conflict = self.run_json(
                "scripts/install.py",
                "--client",
                "generic",
                "--target",
                str(target),
                "--skill",
                "content-grounding",
                expected=1,
            )
            self.assertEqual(len(conflict["conflicts"]), 1)

    @unittest.skipIf(os.name == "nt", "directory symlink permissions vary on Windows")
    def test_generic_installer_symlink_mode(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "skills"
            result = self.run_json(
                "scripts/install.py",
                "--client",
                "generic",
                "--target",
                str(target),
                "--skill",
                "motion-necessity-gate",
                "--mode",
                "symlink",
            )
            self.assertEqual(result["installed"], ["motion-necessity-gate"])
            destination = target / "motion-necessity-gate"
            self.assertTrue(destination.is_symlink())
            self.assertTrue((destination / "SKILL.md").is_file())

            replaced = self.run_json(
                "scripts/install.py",
                "--client",
                "generic",
                "--target",
                str(target),
                "--skill",
                "motion-necessity-gate",
                "--mode",
                "symlink",
                "--force",
            )
            self.assertEqual(replaced["installed"], ["motion-necessity-gate"])
            self.assertTrue(destination.is_symlink())


if __name__ == "__main__":
    unittest.main()
