#!/usr/bin/env python3
"""Repository and bundled helper tests."""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable


class CommandTests(unittest.TestCase):
    @staticmethod
    def visual_limits() -> dict[str, int]:
        return {
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
        self.assertEqual(result["skill_count"], 10)
        self.assertEqual(result["errors"], [])

    def test_project_package_name_is_leeskills(self) -> None:
        manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["name"], "leeskills")
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.assertEqual(manifest["version"], version)
        pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
        self.assertRegex(pyproject, r'(?m)^name = "leeskills"$')
        self.assertIn(f'version = "{version}"', pyproject)
        for skill_md in sorted((ROOT / "skills").glob("*/SKILL.md")):
            self.assertIn(f'version: "{version}"', skill_md.read_text(encoding="utf-8"))

    def test_contextual_spacing_layout_and_typography_contract(self) -> None:
        source_notes = (ROOT / "docs/source-notes.md").read_text(encoding="utf-8")
        for foundation in ("spacing", "layout", "radius", "typography"):
            self.assertIn(
                f"https://design.codeit.com/foundations/{foundation}",
                source_notes,
            )

        budget_rules = (
            ROOT / "skills/review-visuals/references/budget-rules.md"
        ).read_text(encoding="utf-8")
        for role in ("content-gap", "section-gap", "container-padding"):
            self.assertIn(role, budget_rules)
        self.assertRegex(
            budget_rules,
            r"no single numeric range is universally\s+correct",
        )
        self.assertIn("project's breakpoints and container tokens", budget_rules)

        visual_evals = json.loads(
            (
                ROOT / "skills/review-visuals/evals/evals.json"
            ).read_text(encoding="utf-8")
        )
        eval_ids = {item["id"] for item in visual_evals["evals"]}
        self.assertIn("semantic-responsive-spacing", eval_ids)
        self.assertIn("font-context-typesetting", eval_ids)
        self.assertIn("token-proposal-html", eval_ids)

        token_template = (
            ROOT
            / "skills/review-visuals/assets/token-proposal-template.html"
        ).read_text(encoding="utf-8")
        for section_id in (
            "overview",
            "color",
            "typography",
            "spacing",
            "layout",
            "radius",
            "changes",
            "decisions",
        ):
            self.assertIn(f'id="{section_id}"', token_template)
        self.assertIn("{{PROJECT_NAME}}", token_template)
        self.assertIn("Primitive tokens", token_template)
        self.assertIn("Semantic tokens", token_template)
        self.assertNotRegex(
            token_template,
            r'(?:src|href)=["\']https?://',
        )

        accessibility = (
            ROOT
            / "skills/check-accessibility/references/wcag-checklist.md"
        ).read_text(encoding="utf-8")
        self.assertIn("resilience test, not a prescription", accessibility)

    def test_audit_example_scores_as_redesign(self) -> None:
        result = self.run_json(
            "skills/audit-design/scripts/score_audit.py",
            "skills/audit-design/assets/audit-example.json",
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
                "skills/audit-design/scripts/score_audit.py",
                str(path),
                expected=2,
            )
        self.assertIn("evidence_state is unknown", completed.stderr)

    def test_content_inventory_example_is_valid(self) -> None:
        result = self.run_json(
            "skills/verify-content/scripts/validate_inventory.py",
            "skills/verify-content/assets/content-inventory-example.json",
        )
        self.assertTrue(result["valid"])
        self.assertEqual(result["status_counts"]["placeholder"], 1)
        self.assertEqual(result["status_counts"]["prohibited"], 1)
        self.assertEqual(result["status_counts"]["verified"], 1)

    def test_structure_example_is_valid(self) -> None:
        result = self.run_json(
            "skills/plan-structure/scripts/validate_structure.py",
            "skills/plan-structure/assets/structure-decision-example.json",
        )
        self.assertTrue(result["valid"])
        self.assertEqual(result["dominant_grammar"], "portfolio-index")

    def test_delivery_convention_is_identical_in_every_skill(self) -> None:
        blocks = {}
        for skill in sorted((ROOT / "skills").glob("*/SKILL.md")):
            text = skill.read_text(encoding="utf-8")
            start = text.index("## Delivery\n")
            end = text.index("\n## ", start + 1)
            blocks[skill.parent.name] = text[start:end]
        self.assertEqual(len(blocks), 10)
        self.assertEqual(len(set(blocks.values())), 1, msg="Delivery sections drifted apart")

    def token_proposal(self) -> dict[str, object]:
        return json.loads(
            (ROOT / "skills/review-visuals/assets/token-proposal-example.json").read_text(encoding="utf-8")
        )

    def test_token_proposal_example_is_valid_with_explicit_unknowns(self) -> None:
        result = self.run_json(
            "skills/review-visuals/scripts/validate_token_proposal.py",
            "skills/review-visuals/assets/token-proposal-example.json",
        )
        self.assertTrue(result["valid"])
        proposal = result["proposal"]
        self.assertIn("text-secondary@dark", proposal["unknown_values"])
        self.assertTrue(all(item["status"] == "pass" for item in proposal["contrast"]))

    def test_token_proposal_rejects_unsupported_or_unsafe_values(self) -> None:
        script = "skills/review-visuals/scripts/validate_token_proposal.py"
        cases = []

        no_evidence = self.token_proposal()
        no_evidence["foundations"]["spacing"]["primitives"][0]["evidence"] = []
        cases.append((no_evidence, "requires evidence"))

        unsafe = self.token_proposal()
        unsafe["foundations"]["color"]["primitives"][0]["value"] = "url(https://example.com/x.png)"
        cases.append((unsafe, "not allowed"))

        low_contrast = self.token_proposal()
        low_contrast["foundations"]["color"]["primitives"][3]["value"] = "#bbbbbb"
        cases.append((low_contrast, "below the declared"))

        adopted = self.token_proposal()
        adopted["status"] = "adopted"
        cases.append((adopted, "status must be"))

        dangling = self.token_proposal()
        dangling["foundations"]["spacing"]["semantic"][0]["references"]["wide"] = "space-99"
        cases.append((dangling, "unknown primitive"))

        for document, message in cases:
            result = self.run_json_document(script, document, expected=1)
            errors = "\n".join(result["proposal"]["errors"])
            self.assertIn(message, errors)

    def new_system_proposal(self) -> dict[str, object]:
        return json.loads(
            (
                ROOT / "skills/review-visuals/assets/token-proposal-new-system-example.json"
            ).read_text(encoding="utf-8")
        )

    def test_token_proposal_hypotheses_require_new_system_mode_and_rationale(self) -> None:
        script = "skills/review-visuals/scripts/validate_token_proposal.py"
        result = self.run_json(script, "skills/review-visuals/assets/token-proposal-new-system-example.json")
        proposal = result["proposal"]
        self.assertEqual(proposal["mode"], "new-system")
        self.assertIn("space-4", proposal["hypothesis_values"])
        self.assertNotIn("teal-700", proposal["hypothesis_values"])
        self.assertIn("type-body.letter_spacing", proposal["unknown_values"])

        cases = []
        normalize = self.new_system_proposal()
        normalize["mode"] = "normalize"
        cases.append((normalize, "only allowed in new-system mode"))

        no_rationale = self.new_system_proposal()
        del no_rationale["foundations"]["spacing"]["primitives"][0]["rationale"]
        cases.append((no_rationale, "requires a rationale"))

        observed_without_evidence = self.new_system_proposal()
        observed_without_evidence["foundations"]["color"]["primitives"][0]["evidence"] = []
        cases.append((observed_without_evidence, "requires evidence"))

        unsafe = self.new_system_proposal()
        unsafe["foundations"]["spacing"]["primitives"][0]["value"] = "url(https://example.com/x)"
        cases.append((unsafe, "not allowed"))

        low_contrast = self.new_system_proposal()
        low_contrast["foundations"]["color"]["primitives"][2]["value"] = "#dddddd"
        cases.append((low_contrast, "below the declared"))

        bad_mode = self.new_system_proposal()
        bad_mode["mode"] = "freeform"
        cases.append((bad_mode, "mode must be one of"))

        for document, message in cases:
            result = self.run_json_document(script, document, expected=1)
            self.assertIn(message, "\n".join(result["proposal"]["errors"]))

        existing = self.token_proposal()
        existing["foundations"]["spacing"]["primitives"][0]["basis"] = "hypothesis"
        existing["foundations"]["spacing"]["primitives"][0]["rationale"] = "Guess."
        result = self.run_json_document(script, existing, expected=1)
        self.assertIn("only allowed in new-system mode", "\n".join(result["proposal"]["errors"]))

    def test_token_proposal_renders_design_hypothesis_markers(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            for language, label in (("en", "Design hypothesis"), ("ko", "설계 가설"), ("ja", "設計仮説")):
                document = self.new_system_proposal()
                document["language"] = language
                source = Path(directory) / f"{language}.json"
                output = Path(directory) / f"{language}.html"
                source.write_text(json.dumps(document, ensure_ascii=False), encoding="utf-8")
                rendered = self.run_json(
                    "skills/review-visuals/scripts/render_token_proposal.py",
                    str(source),
                    "--output",
                    str(output),
                )
                self.assertTrue(rendered["rendered"])
                html = output.read_text(encoding="utf-8")
                self.assertEqual(
                    html.count('data-basis="hypothesis"'), len(rendered["hypothesis_values"])
                )
                self.assertIn(label, html)
                checked = self.run_json(
                    "skills/review-visuals/scripts/validate_token_proposal.py",
                    str(source),
                    "--html",
                    str(output),
                )
                self.assertTrue(checked["valid"])

            stripped = Path(directory) / "stripped.html"
            stripped.write_text(
                (Path(directory) / "en.html")
                .read_text(encoding="utf-8")
                .replace('data-basis="hypothesis"', ""),
                encoding="utf-8",
            )
            checked = self.run_json(
                "skills/review-visuals/scripts/validate_token_proposal.py",
                str(Path(directory) / "en.json"),
                "--html",
                str(stripped),
                expected=1,
            )
            self.assertIn("design hypothesis", "\n".join(checked["html"]["errors"]))

            normalize = Path(directory) / "normalize.html"
            source = Path(directory) / "normalize.json"
            source.write_text(json.dumps(self.token_proposal(), ensure_ascii=False), encoding="utf-8")
            self.run_json(
                "skills/review-visuals/scripts/render_token_proposal.py",
                str(source),
                "--output",
                str(normalize),
            )
            self.assertNotIn('data-basis="hypothesis"', normalize.read_text(encoding="utf-8"))

    def test_token_proposal_renders_localized_page_without_placeholders(self) -> None:
        template = (
            ROOT / "skills/review-visuals/assets/token-proposal-template.html"
        ).read_text(encoding="utf-8")
        style = template.split("<style>", 1)[1].split("</style>", 1)[0]
        defined = set(re.findall(r"\.([a-z][a-z0-9-]*)", style))
        with tempfile.TemporaryDirectory() as directory:
            for language, expected in (("ko", "디자인 토큰 제안"), ("ja", "デザイントークン提案"), ("en", "Design token proposal")):
                document = self.token_proposal()
                document["language"] = language
                source = Path(directory) / f"{language}.json"
                output = Path(directory) / f"{language}.html"
                source.write_text(json.dumps(document, ensure_ascii=False), encoding="utf-8")
                result = self.run_json(
                    "skills/review-visuals/scripts/render_token_proposal.py", str(source), "--output", str(output),
                )
                self.assertTrue(result["rendered"])
                html = output.read_text(encoding="utf-8")
                self.assertIn(f'<html lang="{language}">', html)
                self.assertIn(expected, html)
                self.assertNotRegex(html, r"\{\{[A-Z0-9_]+\}\}")
                self.assertNotIn("Manual fill:", html)
                for section in ("overview", "color", "typography", "spacing", "layout", "radius", "changes", "decisions"):
                    self.assertIn(f'<section id="{section}"', html)
                self.assertIn('data-proposal-status="proposed"', html)
                self.assertIn('class="unknown"', html)
                shell = html.split("<!-- shell:start -->", 1)[1].split("<!-- shell:end -->", 1)[0]
                used = {
                    name
                    for value in re.findall(r'class="([^"]+)"', shell)
                    for name in value.split()
                }
                self.assertEqual(sorted(used - defined), [], msg="rendered classes missing from the template stylesheet")
                checked = self.run_json(
                    "skills/review-visuals/scripts/validate_token_proposal.py", "--html", str(output),
                )
                self.assertTrue(checked["valid"])

            omitted = self.token_proposal()
            del omitted["foundations"]["layout"]
            source = Path(directory) / "partial.json"
            output = Path(directory) / "partial.html"
            source.write_text(json.dumps(omitted, ensure_ascii=False), encoding="utf-8")
            self.run_json("skills/review-visuals/scripts/render_token_proposal.py", str(source), "--output", str(output))
            html = output.read_text(encoding="utf-8")
            self.assertNotIn('<section id="layout"', html)
            self.assertNotIn('href="#layout"', html)

    def test_token_proposal_renderer_refuses_invalid_input(self) -> None:
        document = self.token_proposal()
        document["foundations"]["radius"]["primitives"][0]["evidence"] = []
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "invalid.json"
            output = Path(directory) / "invalid.html"
            source.write_text(json.dumps(document, ensure_ascii=False), encoding="utf-8")
            result = self.run_json(
                "skills/review-visuals/scripts/render_token_proposal.py", str(source), "--output", str(output),
                expected=1,
            )
            self.assertFalse(result["rendered"])
            self.assertFalse(output.exists())

    def test_token_proposal_template_flags_placeholders_and_keeps_its_budget(self) -> None:
        path = ROOT / "skills/review-visuals/assets/token-proposal-template.html"
        result = self.run_json(
            "skills/review-visuals/scripts/validate_token_proposal.py", "--html", str(path), expected=1,
        )
        self.assertFalse(result["valid"])
        self.assertTrue(result["html"]["placeholders"])

        template = path.read_text(encoding="utf-8")
        strings = json.loads(
            template.split('<script type="application/json" id="chrome-strings">', 1)[1].split("</script>", 1)[0]
        )
        self.assertEqual(set(strings), {"en", "ko", "ja"})
        self.assertEqual(set(strings["en"]), set(strings["ko"]))
        self.assertEqual(set(strings["en"]), set(strings["ja"]))
        used_keys = set(re.findall(r'data-i18n="([a-z_-]+)"', template))
        self.assertEqual(sorted(used_keys - set(strings["en"])), [])

        style = template.split("<style>", 1)[1].split("</style>", 1)[0]
        self.assertLessEqual(len(set(re.findall(r"--radius-[a-z]+:", style))), 2)
        self.assertLessEqual(len(set(re.findall(r"--text-[a-z]+:", style))), 6)
        font_sizes = set(re.findall(r"font-size:\s*([^;]+);", style))
        self.assertTrue(all(value.startswith("var(--") for value in font_sizes), msg=font_sizes)
        self.assertNotIn("box-shadow: 0", style)
        self.assertNotRegex(style, r"(?:https?:)?//[a-z]")
        self.assertIn("prefers-reduced-motion", style)
        self.assertIn("@media print", style)
        self.assertIn("html:lang(ko) body { word-break: keep-all; }", style)


    def test_visual_budget_example_exposes_overages(self) -> None:
        result = self.run_json(
            "skills/review-visuals/scripts/check_budget.py",
            "skills/review-visuals/assets/visual-budget-example.json",
            expected=1,
        )
        self.assertFalse(result["pass"])
        self.assertEqual(result["unresolved_overages"], 10)
        self.assertEqual(result["unresolved_radius_relationships"], 1)
        self.assertEqual(result["documented_exceptions"], 1)

    def test_visual_budget_rejects_empty_metric_maps(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "budget.json"
            path.write_text(
                json.dumps({"artifact": "x", "observed": {}, "limits": {}, "exceptions": []}),
                encoding="utf-8",
            )
            completed = self.run_command(
                "skills/review-visuals/scripts/check_budget.py",
                str(path),
                expected=2,
            )
        self.assertIn("limits missing core metrics", completed.stderr)

    def test_visual_budget_exception_requires_human_review(self) -> None:
        limits = self.visual_limits()
        observed = dict(limits)
        observed["typeface_families"] = 2
        result = self.run_json_document(
            "skills/review-visuals/scripts/check_budget.py",
            {
                "artifact": "Editorial site",
                "observed": observed,
                "limits": limits,
                "radius_scope": "none",
                "radius_scope_evidence": "The inspected article layout has no nested rounded surfaces.",
                "radius_relationships": [],
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

    def test_visual_budget_rejects_same_radius_on_shared_nested_contour(self) -> None:
        limits = self.visual_limits()
        result = self.run_json_document(
            "skills/review-visuals/scripts/check_budget.py",
            {
                "artifact": "Nested card",
                "observed": dict(limits),
                "limits": limits,
                "radius_scope": "evaluated",
                "radius_scope_evidence": "Computed radius tokens were inspected.",
                "radius_relationships": [
                    {
                        "id": "card-panel",
                        "location": "Card > inset panel",
                        "kind": "shared-contour",
                        "rule": "semantic-step",
                        "outer_token": "radius-20",
                        "inner_token": "radius-20",
                        "token_steps_inward": 0,
                        "evidence_state": "measured",
                        "evidence": "Both computed radii are 20px.",
                    }
                ],
                "exceptions": [],
            },
            expected=1,
        )
        self.assertFalse(result["pass"])
        self.assertEqual(result["unresolved_radius_relationships"], 1)
        self.assertEqual(result["radius"]["relationships"][0]["status"], "mismatch")

    def test_visual_budget_accepts_measured_concentric_radius(self) -> None:
        limits = self.visual_limits()
        result = self.run_json_document(
            "skills/review-visuals/scripts/check_budget.py",
            {
                "artifact": "Nested card",
                "observed": dict(limits),
                "limits": limits,
                "radius_scope": "evaluated",
                "radius_scope_evidence": "Computed contour values were measured.",
                "radius_relationships": [
                    {
                        "id": "card-image",
                        "location": "Card > inset image",
                        "kind": "shared-contour",
                        "rule": "concentric-offset",
                        "outer_radius": 20,
                        "inner_radius": 12,
                        "inset": 8,
                        "tolerance": 1,
                        "evidence_state": "measured",
                        "evidence": "Computed values match the declared 8px contour inset.",
                    }
                ],
                "exceptions": [],
            },
        )
        self.assertTrue(result["pass"])
        relationship = result["radius"]["relationships"][0]
        self.assertEqual(relationship["status"], "conforming")
        self.assertEqual(relationship["expected_inner_radius"], 12.0)

    def test_visual_budget_unknown_radius_scope_requires_review(self) -> None:
        limits = self.visual_limits()
        result = self.run_json_document(
            "skills/review-visuals/scripts/check_budget.py",
            {
                "artifact": "Uninspected interface",
                "observed": dict(limits),
                "limits": limits,
                "exceptions": [],
            },
            expected=1,
        )
        self.assertFalse(result["pass"])
        self.assertTrue(result["review_required"])
        self.assertEqual(result["budget_status"], "review-required")
        self.assertEqual(result["radius"]["scope"], "unknown")

    def test_visual_budget_radius_exception_requires_human_review(self) -> None:
        limits = self.visual_limits()
        result = self.run_json_document(
            "skills/review-visuals/scripts/check_budget.py",
            {
                "artifact": "Branded nested card",
                "observed": dict(limits),
                "limits": limits,
                "radius_scope": "evaluated",
                "radius_scope_evidence": "Computed tokens were inspected.",
                "radius_relationships": [
                    {
                        "id": "brand-frame",
                        "location": "Brand frame > media panel",
                        "kind": "shared-contour",
                        "rule": "semantic-step",
                        "outer_token": "brand-radius",
                        "inner_token": "brand-radius",
                        "token_steps_inward": 0,
                        "evidence_state": "measured",
                        "evidence": "Both contours use the approved brand token.",
                        "exception": {
                            "reason": "The repeated superellipse is a documented brand signature.",
                            "evidence": "The approved brand specification requires the shared shape.",
                        },
                    }
                ],
                "exceptions": [],
            },
            expected=1,
        )
        self.assertFalse(result["pass"])
        self.assertTrue(result["review_required"])
        self.assertEqual(result["unresolved_radius_relationships"], 0)
        self.assertEqual(result["documented_radius_exceptions"], 1)

    def test_motion_example_has_no_hard_failure(self) -> None:
        result = self.run_json(
            "skills/review-motion/scripts/validate_motion_inventory.py",
            "skills/review-motion/assets/motion-inventory-example.json",
        )
        self.assertTrue(result["valid"])
        self.assertEqual(result["hard_failures"], [])

    def test_accessibility_example_blocks_release(self) -> None:
        result = self.run_json(
            "skills/check-accessibility/scripts/validate_accessibility_report.py",
            "skills/check-accessibility/assets/accessibility-report-example.json",
            expected=1,
        )
        self.assertTrue(result["valid_report"])
        self.assertFalse(result["release_ready"])
        self.assertEqual(len(result["blockers"]), 2)

    def test_accessibility_optional_failure_still_blocks_release(self) -> None:
        result = self.run_json_document(
            "skills/check-accessibility/scripts/validate_accessibility_report.py",
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

    def test_verify_changes_example_is_release_ready_with_declared_scope(self) -> None:
        result = self.run_json(
            "skills/verify-changes/scripts/validate_verification.py",
            "skills/verify-changes/assets/verification-example.json",
        )
        self.assertTrue(result["valid_report"])
        self.assertTrue(result["release_ready"])
        self.assertEqual(result["status_counts"]["pass"], 11)
        self.assertEqual(result["status_counts"]["unknown"], 1)

    def targeted_report(self) -> dict[str, object]:
        return json.loads(
            (
                ROOT / "skills/verify-changes/assets/verification-targeted-example.json"
            ).read_text(encoding="utf-8")
        )

    def test_verify_changes_targeted_example_is_never_release_ready(self) -> None:
        result = self.run_json(
            "skills/verify-changes/scripts/validate_verification.py",
            "skills/verify-changes/assets/verification-targeted-example.json",
        )
        self.assertTrue(result["valid_report"])
        self.assertTrue(result["targeted_pass"])
        self.assertFalse(result["release_ready"])
        self.assertEqual(result["verdict"], "targeted-pass")
        self.assertIn("deletion", result["not_checked"])
        self.assertEqual(result["status_counts"]["out-of-scope"], 1)

    def test_verify_changes_targeted_failure_still_blocks(self) -> None:
        report = self.targeted_report()
        report["checks"][0]["status"] = "fail"
        result = self.run_json_document(
            "skills/verify-changes/scripts/validate_verification.py", report, expected=1
        )
        self.assertTrue(result["valid_report"])
        self.assertFalse(result["targeted_pass"])
        self.assertEqual(result["verdict"], "blocked")

    def test_verify_changes_scope_rules_are_enforced(self) -> None:
        release = self.targeted_report()
        release["scope"]["verification"] = "release"
        result = self.run_json_document(
            "skills/verify-changes/scripts/validate_verification.py", release, expected=1
        )
        self.assertFalse(result["valid_report"])
        self.assertTrue(any("out-of-scope is only valid" in e for e in result["errors"]))

        unscoped = self.targeted_report()
        unscoped["scope"]["changed_surfaces"] = []
        del unscoped["scope"]["rationale"]
        result = self.run_json_document(
            "skills/verify-changes/scripts/validate_verification.py", unscoped, expected=1
        )
        self.assertIn("targeted verification must name its changed_surfaces", result["errors"])
        self.assertIn("targeted verification requires a scope.rationale", result["errors"])

        required_out = self.targeted_report()
        required_out["checks"][3]["required"] = True
        result = self.run_json_document(
            "skills/verify-changes/scripts/validate_verification.py", required_out, expected=1
        )
        self.assertFalse(result["valid_report"])

    def test_verify_changes_accepts_documented_conditional_checks(self) -> None:
        skill = (ROOT / "skills/verify-changes/SKILL.md").read_text(encoding="utf-8")
        schema = json.loads(
            (ROOT / "skills/verify-changes/assets/verification.schema.json").read_text(
                encoding="utf-8"
            )
        )
        enum = schema["properties"]["checks"]["items"]["properties"]["test"]["enum"]
        report = self.targeted_report()
        for test in (
            "affordance-mapping",
            "action-hierarchy",
            "action-visibility",
            "grouping-cues",
            "system-lifecycle",
        ):
            self.assertIn(f"`{test}`", skill)
            self.assertIn(test, enum)
            report["checks"][0]["test"] = test
            result = self.run_json_document(
                "skills/verify-changes/scripts/validate_verification.py", report
            )
            self.assertTrue(result["valid_report"], msg=result["errors"])

    def test_verify_changes_baseline_failure_cannot_be_marked_optional(self) -> None:
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
            "skills/verify-changes/scripts/validate_verification.py",
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
        queries_path = ROOT / "skills" / "design-workflow" / "evals" / "trigger_queries.json"
        queries = json.loads(queries_path.read_text(encoding="utf-8"))
        measurements = {
            "client": "example-agent",
            "skill_name": "design-workflow",
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
        self.assertEqual(result["status"], "pass")
        self.assertEqual(set(result["languages"]), {"en", "ko", "ja"})
        self.assertEqual(result["insufficient_attempts"], [])

    def trigger_measurements(self, attempts: int) -> tuple[Path, dict[str, object]]:
        queries_path = ROOT / "skills" / "design-workflow" / "evals" / "trigger_queries.json"
        queries = json.loads(queries_path.read_text(encoding="utf-8"))
        return queries_path, {
            "client": "example-agent",
            "skill_name": "design-workflow",
            "results": [
                {
                    "id": item["id"],
                    "attempts": attempts,
                    "triggered": attempts if item["should_trigger"] else 0,
                }
                for item in queries
            ],
        }

    def test_trigger_results_with_too_few_attempts_are_insufficient(self) -> None:
        queries_path, measurements = self.trigger_measurements(1)
        with tempfile.TemporaryDirectory() as directory:
            result_path = Path(directory) / "results.json"
            result_path.write_text(json.dumps(measurements), encoding="utf-8")
            result = self.run_json(
                "scripts/evaluate_trigger_results.py",
                str(queries_path),
                str(result_path),
                expected=1,
            )
        self.assertFalse(result["pass"])
        self.assertEqual(result["status"], "insufficient")
        self.assertEqual(result["languages"]["en"]["status"], "insufficient")

    def test_trigger_results_report_individual_and_critical_failures(self) -> None:
        queries_path, measurements = self.trigger_measurements(3)
        queries = json.loads(queries_path.read_text(encoding="utf-8"))
        # One missed positive keeps the English average above the threshold.
        missed = "en-positive-1"
        for item in measurements["results"]:
            if item["id"] == missed:
                item["triggered"] = 0
        with tempfile.TemporaryDirectory() as directory:
            result_path = Path(directory) / "results.json"
            result_path.write_text(json.dumps(measurements), encoding="utf-8")
            averaged = self.run_json(
                "scripts/evaluate_trigger_results.py", str(queries_path), str(result_path)
            )
            self.assertEqual(averaged["status"], "pass")
            self.assertEqual([item["id"] for item in averaged["failures"]], [missed])

            for item in queries:
                if item["id"] == missed:
                    item["critical"] = True
            critical_path = Path(directory) / "queries.json"
            critical_path.write_text(json.dumps(queries), encoding="utf-8")
            critical = self.run_json(
                "scripts/evaluate_trigger_results.py",
                str(critical_path),
                str(result_path),
                expected=1,
            )
        self.assertEqual(critical["status"], "fail")
        self.assertTrue(critical["failures"][0]["critical"])

    def routing_record(
        self, case_id: str, language: str, attempt: int, **fields: object
    ) -> dict[str, object]:
        record: dict[str, object] = {
            "eval_kind": "routing",
            "eval_id": case_id,
            "language": language,
            "attempt": attempt,
            "status": "executed",
        }
        record.update(fields)
        return record

    def test_catalog_routing_cases_reference_catalog_skills(self) -> None:
        manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
        names = {item["name"] for item in manifest["skills"]}
        document = json.loads(
            (ROOT / "evals" / "catalog-routing.json").read_text(encoding="utf-8")
        )
        ids = {case["id"] for case in document["cases"]}
        self.assertTrue(
            {
                "single-button-copy",
                "screenshot-quick-pass",
                "radius-only-no-html",
                "new-system-no-tokens",
                "workflow-only-install",
                "no-python-no-browser",
                "already-appropriate-keep",
                "locale-runtime-edit",
                "instructions-in-artifact",
                "install-dir-differs",
            }.issubset(ids)
        )
        for case in document["cases"]:
            self.assertEqual(set(case["queries"]), {"en", "ko", "ja"})
            self.assertTrue(set(case["primary_skills"]) <= names)
            self.assertTrue(set(case["allowed_secondary"]) <= names)

    def test_routing_results_separate_not_run_forbidden_and_extra_skills(self) -> None:
        cases_path = ROOT / "evals" / "catalog-routing.json"
        document = json.loads(cases_path.read_text(encoding="utf-8"))
        single = {"cases": [c for c in document["cases"] if c["id"] == "radius-only-no-html"]}
        clean = [
            self.routing_record(
                "radius-only-no-html", language, attempt, activated_skills=["review-visuals"]
            )
            for language in ("en", "ko", "ja")
            for attempt in (1, 2, 3)
        ]
        with tempfile.TemporaryDirectory() as directory:
            cases_file = Path(directory) / "cases.json"
            cases_file.write_text(json.dumps(single), encoding="utf-8")
            results_file = Path(directory) / "results.json"

            def run(records: list[dict[str, object]], expected: int) -> dict[str, object]:
                results_file.write_text(
                    json.dumps({"client": "example-agent", "records": records}),
                    encoding="utf-8",
                )
                return self.run_json(
                    "scripts/evaluate_routing_results.py",
                    str(cases_file),
                    str(results_file),
                    expected=expected,
                )

            self.assertEqual(run(clean, 0)["status"], "pass")

            not_run = [r for r in clean if r["language"] != "ja"] + [
                self.routing_record(
                    "radius-only-no-html", "ja", 1, status="not-run",
                    not_run_reason="fixture unavailable",
                )
            ]
            result = run(not_run, 1)
            self.assertEqual(result["status"], "not-run")
            self.assertEqual(
                result["cases"]["radius-only-no-html"]["languages"]["ja"]["status"], "not-run"
            )

            forbidden = [dict(r) for r in clean]
            forbidden[0]["observed_actions"] = ["create-html"]
            result = run(forbidden, 1)
            self.assertEqual(result["status"], "fail")
            self.assertEqual(
                result["cases"]["radius-only-no-html"]["languages"]["en"][
                    "forbidden_actions_observed"
                ],
                ["create-html"],
            )

            extra = [dict(r) for r in clean]
            extra[0]["activated_skills"] = ["review-visuals", "design-workflow"]
            self.assertEqual(run(extra, 1)["status"], "review")

    def test_edit_copy_integrates_voice_and_locale_review(self) -> None:
        skill_dir = ROOT / "skills" / "edit-copy"
        language_reference = (
            skill_dir / "references" / "language-and-voice.md"
        ).read_text(encoding="utf-8")
        source_notes = (ROOT / "docs" / "source-notes.md").read_text(
            encoding="utf-8"
        )
        source_urls = (
            "https://digital.gov/guides/plain-language/principles",
            "https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/writing-guidelines/clear-language/",
            "https://www.korean.go.kr/front/etcData/etcDataView.do?etc_seq=399&mn_id=62",
            "https://www.bunka.go.jp/seisaku/kokugo_nihongo/kokugo_shisaku/94336802.html",
            "https://www.bunka.go.jp/seisaku/kokugo_nihongo/kyoiku/pdf/92484001_01.pdf",
        )
        for url in source_urls:
            self.assertIn(url, language_reference)
            self.assertIn(url, source_notes)
        for source_title in (
            "Principles of plain language",
            "公用文作成の考え方（建議）",
            "在留支援のためのやさしい日本語ガイドライン",
        ):
            self.assertIn(source_title, language_reference)
            self.assertIn(source_title, source_notes)
        self.assertIn("出入国在留管理庁・文化庁", language_reference)

        skill_text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
        rewrite_template = (skill_dir / "assets" / "rewrite-template.md").read_text(
            encoding="utf-8"
        )
        report_template = (
            ROOT / "skills" / "design-workflow" / "assets" / "full-report-template.md"
        ).read_text(encoding="utf-8")
        fallback_contract = (
            ROOT
            / "skills"
            / "design-workflow"
            / "references"
            / "composition-map.md"
        ).read_text(encoding="utf-8")
        audit_skill = (
            ROOT / "skills" / "audit-design" / "SKILL.md"
        ).read_text(encoding="utf-8")

        self.assertIn("Source language or canonical locale:", rewrite_template)
        self.assertIn("| Locale | Location | Decision |", rewrite_template)
        self.assertIn("| Locale | Location | Decision | Original label |", rewrite_template)
        self.assertIn("localized runtime messages", rewrite_template)
        self.assertIn("Catalog key mapping", rewrite_template)
        self.assertIn("Runtime constraints checked", rewrite_template)
        self.assertIn("Unresolved |", rewrite_template)
        self.assertIn("| Locale | Location | Decision |", report_template)
        self.assertIn("Issue | Evidence status |", report_template)
        self.assertIn("Catalog key mapping", report_template)
        self.assertIn("Runtime constraints checked", report_template)
        for contract_term in (
            "`correct`, `suggest`, or `keep`",
            "placeholders",
            "locale-aware formatting",
            "unresolved information",
        ):
            self.assertIn(contract_term, fallback_contract)
        self.assertIn("message keys", skill_text)
        self.assertIn("canonical key maps", skill_text)
        self.assertIn("approved nearby copy", audit_skill)

        output_evals = json.loads(
            (skill_dir / "evals" / "evals.json").read_text(encoding="utf-8")
        )
        output_by_id = {item["id"]: item for item in output_evals["evals"]}
        output_ids = set(output_by_id)
        self.assertTrue(
            {
                "english-product-voice",
                "korean-product-voice",
                "japanese-product-voice",
                "multilingual-screen-parity",
                "localization-runtime-integrity",
            }.issubset(output_ids)
        )
        runtime_prompt = output_by_id["localization-runtime-integrity"]["prompt"]
        for runtime_token in (
            "settings.saveSummary",
            "<strong>{workspace}</strong>",
            "{audience, select",
            "{count, plural",
            "{storageUsed}",
            "{savedAt",
            "Intl.NumberFormat",
            "unit formatting",
        ):
            self.assertIn(runtime_token, runtime_prompt)

        orchestrator_evals = json.loads(
            (
                ROOT / "skills" / "design-workflow" / "evals" / "evals.json"
            ).read_text(encoding="utf-8")
        )
        orchestrator_by_id = {
            item["id"]: item for item in orchestrator_evals["evals"]
        }
        self.assertIn("multilingual-copy-handoff", orchestrator_by_id)
        self.assertTrue(
            any(
                "Evidence status" in assertion
                for assertion in orchestrator_by_id["multilingual-copy-handoff"][
                    "assertions"
                ]
            )
        )

        triggers = json.loads(
            (skill_dir / "evals" / "trigger_queries.json").read_text(
                encoding="utf-8"
            )
        )
        triggers_by_id = {item["id"]: item for item in triggers}
        for language in ("en", "ko", "ja"):
            item = triggers_by_id[f"{language}-positive-3"]
            self.assertEqual(item["language"], language)
            self.assertTrue(item["should_trigger"])

    def test_copy_linter_flags_review_items_without_failing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "copy.txt"
            path.write_text(
                "A seamless platform that empowers every team and improves results by 40%.",
                encoding="utf-8",
            )
            result = self.run_json(
                "skills/edit-copy/scripts/lint_copy.py",
                str(path),
                "--format",
                "json",
            )
        self.assertGreaterEqual(result["finding_count"], 4)
        finding_types = {item["type"] for item in result["findings"]}
        self.assertIn("watchlist-phrase", finding_types)
        self.assertIn("numeric-claim", finding_types)
        self.assertIn("universal-claim", finding_types)

    def test_copy_linter_prefers_longest_watchlist_match(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "copy.txt"
            path.write_text("Integrates seamlessly.", encoding="utf-8")
            result = self.run_json(
                "skills/edit-copy/scripts/lint_copy.py",
                str(path),
                "--format",
                "json",
            )
        watchlist = [
            item for item in result["findings"] if item["type"] == "watchlist-phrase"
        ]
        self.assertEqual(len(watchlist), 1)
        self.assertEqual(watchlist[0]["match"], "seamlessly")

    def test_copy_linter_reports_correct_offsets_after_casefold_growth(self) -> None:
        # "ß".casefold() == "ss" shifts casefolded offsets; original-text
        # matching must keep the reported column and match text accurate.
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "copy.txt"
            path.write_text("ß seamless", encoding="utf-8")
            result = self.run_json(
                "skills/edit-copy/scripts/lint_copy.py",
                str(path),
                "--format",
                "json",
            )
        watchlist = [
            item for item in result["findings"] if item["type"] == "watchlist-phrase"
        ]
        self.assertEqual(len(watchlist), 1)
        self.assertEqual(watchlist[0]["match"], "seamless")
        self.assertEqual(watchlist[0]["line"], 1)
        self.assertEqual(watchlist[0]["column"], 3)

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
                "verify-content",
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
                "verify-content",
            )
            self.assertEqual(installed["installed"], ["verify-content"])
            self.assertTrue((target / "verify-content" / "SKILL.md").is_file())

            conflict = self.run_json(
                "scripts/install.py",
                "--client",
                "generic",
                "--target",
                str(target),
                "--skill",
                "verify-content",
                expected=1,
            )
            self.assertEqual(len(conflict["conflicts"]), 1)

    @staticmethod
    def package_link_targets(package: Path) -> list[tuple[Path, Path]]:
        link_re = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
        targets = []
        for markdown in sorted(package.rglob("*.md")):
            for raw in link_re.findall(markdown.read_text(encoding="utf-8")):
                if raw.startswith(("#", "http://", "https://", "mailto:")):
                    continue
                relative = raw.split("#", 1)[0]
                if relative:
                    targets.append((markdown, (markdown.parent / relative).resolve()))
        return targets

    def test_skill_packages_resolve_links_inside_their_own_directory(self) -> None:
        for package in sorted((ROOT / "skills").iterdir()):
            if not package.is_dir():
                continue
            for markdown, target in self.package_link_targets(package):
                self.assertTrue(
                    str(target).startswith(str(package.resolve())),
                    msg=f"{markdown} links outside its package: {target}",
                )

    def test_references_are_reachable_one_level_from_skill(self) -> None:
        # A reference may cross-link another, but SKILL.md must link it directly
        # so that no instruction is reachable only through a chain of references.
        for package in sorted((ROOT / "skills").iterdir()):
            references = package / "references"
            if not references.is_dir():
                continue
            direct = {
                target
                for markdown, target in self.package_link_targets(package)
                if markdown.name == "SKILL.md" and markdown.parent == package
            }
            for markdown, target in self.package_link_targets(references):
                if target.parent == references.resolve():
                    self.assertIn(
                        target,
                        direct,
                        msg=f"{markdown} chains to {target.name}, which SKILL.md does not link",
                    )

    def test_optional_procedures_load_conditionally_and_keep_core_gates(self) -> None:
        components = ROOT / "skills" / "review-components"
        visuals = ROOT / "skills" / "review-visuals"
        conditional = {
            components / "references" / "interaction-governance.md": components,
            components / "references" / "system-lifecycle.md": components,
            visuals / "references" / "token-proposal.md": visuals,
        }
        for reference, package in conditional.items():
            text = reference.read_text(encoding="utf-8")
            self.assertRegex(text.split("\n## ", 1)[0], r"Read this file (?:only )?when")
            skill = (package / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn(f"](references/{reference.name})", skill)

        component_skill = (components / "SKILL.md").read_text(encoding="utf-8")
        hard_gates = component_skill.split("## Hard gates", 1)[1].split("\n## ", 1)[0]
        for phrase in (
            "accessible name, keyboard path, or visible",
            "competing primary actions",
            "hidden behind disclosure",
            "design-system lifecycle remains `fail` or `unknown`",
        ):
            self.assertIn(phrase, " ".join(hard_gates.split()))
        rules = (components / "references" / "contract-rules.md").read_text(encoding="utf-8")
        for moved in ("## Affordance mapping", "## Design-system lifecycle and adoption"):
            self.assertNotIn(moved, rules)

        visual_skill = (visuals / "SKILL.md").read_text(encoding="utf-8")
        self.assertNotIn("### Build the page", visual_skill)
        self.assertNotIn("render_token_proposal.py", visual_skill)
        token_summary = " ".join(visual_skill.split("## Token proposal", 1)[1].split("\n## ", 1)[0].split())
        for phrase in (
            "only when the user asks",
            "stay `unknown`",
            "design hypotheses with a rationale",
            "not evidence that the project adopted",
        ):
            self.assertIn(phrase, token_summary)

    def test_workflow_only_install_is_self_contained_from_another_workdir(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workdir = Path(directory) / "project"
            workdir.mkdir()
            alone = Path(directory) / "alone"
            catalog = Path(directory) / "catalog"
            for target, skills in (
                (alone, ["--skill", "design-workflow"]),
                (catalog, []),
            ):
                completed = subprocess.run(
                    [
                        PYTHON,
                        str(ROOT / "scripts" / "install.py"),
                        "--client",
                        "generic",
                        "--target",
                        str(target),
                        *skills,
                    ],
                    cwd=workdir,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(completed.returncode, 0, msg=completed.stderr)
            self.assertEqual([path.name for path in alone.iterdir()], ["design-workflow"])
            self.assertEqual(list(workdir.iterdir()), [])

            package = alone / "design-workflow"
            for markdown, target in self.package_link_targets(package):
                self.assertTrue(target.is_file(), msg=f"{markdown}: missing {target}")

            workflow = (package / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("## Skill availability", workflow)
            self.assertIn("relative to this file's directory", workflow)
            focused = re.findall(r"`([a-z]+-[a-z]+)`", workflow)
            focused = sorted(set(focused) & {p.name for p in (ROOT / "skills").iterdir()})
            self.assertIn("review-visuals", focused)
            for name in focused:
                sibling = (catalog / "design-workflow" / ".." / name / "SKILL.md").resolve()
                self.assertTrue(sibling.is_file(), msg=f"sibling package missing: {name}")
                self.assertFalse((alone / name).exists())

            composition = (
                package / "references" / "composition-map.md"
            ).read_text(encoding="utf-8")
            self.assertIn("### Audit design (`audit-design`)", composition)
            self.assertIn("limited level", composition)

    def test_repo_installer_new_catalog_preserves_custom_legacy_copy(self) -> None:
        expected_names = {
            "design-workflow", "audit-design", "verify-content", "plan-structure",
            "review-components", "review-visuals", "edit-copy", "review-motion",
            "check-accessibility", "verify-changes",
        }
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / ".agents" / "skills"
            legacy = target / "content-grounding"
            legacy.mkdir(parents=True)
            custom = legacy / "SKILL.md"
            custom.write_text("A locally customized installation.\n", encoding="utf-8")
            before = custom.read_bytes()

            installed = self.run_json(
                "scripts/install.py", "--client", "codex", "--scope", "repo",
                "--repo", directory,
            )
            self.assertEqual(set(installed["installed"]), expected_names)
            self.assertEqual(custom.read_bytes(), before)
            self.assertEqual(
                {path.name for path in target.iterdir()},
                expected_names | {"content-grounding"},
            )
            for name in expected_names:
                source = ROOT / "skills" / name
                destination = target / name
                self.assertIn(
                    f"name: {name}\n",
                    (destination / "SKILL.md").read_text(encoding="utf-8"),
                )
                source_files = {
                    path.relative_to(source) for path in source.rglob("*") if path.is_file()
                }
                copied_files = {
                    path.relative_to(destination)
                    for path in destination.rglob("*") if path.is_file()
                }
                self.assertEqual(copied_files, source_files)
                for relative in source_files:
                    self.assertEqual(
                        (source / relative).read_bytes(),
                        (destination / relative).read_bytes(),
                    )

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
                "review-motion",
                "--mode",
                "symlink",
            )
            self.assertEqual(result["installed"], ["review-motion"])
            destination = target / "review-motion"
            self.assertTrue(destination.is_symlink())
            self.assertTrue((destination / "SKILL.md").is_file())

            replaced = self.run_json(
                "scripts/install.py",
                "--client",
                "generic",
                "--target",
                str(target),
                "--skill",
                "review-motion",
                "--mode",
                "symlink",
                "--force",
            )
            self.assertEqual(replaced["installed"], ["review-motion"])
            self.assertTrue(destination.is_symlink())


if __name__ == "__main__":
    unittest.main()
