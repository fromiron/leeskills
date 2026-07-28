from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents1
SKILL = ROOT / "skills" / "component-contract-audit"
SCRIPT = SKILL / "scripts" / "validate_interaction_governance.py"
FOUNDATIONS = ROOT / "docs" / "design-foundations.md"
SOURCE_NOTES = ROOT / "docs" / "source-notes.md"
TRIGGERS = SKILL / "evals" / "trigger_queries.json"


def load_validator():
    spec = importlib.util.spec_from_file_location("interaction_governance", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load interaction-governance validator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


CLASSIFIER = load_validator()

def deep_copy(value):
    return json.loads(json.dumps(value))


class InteractionGovernanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.example = json.loads(
            (SKILL / "assets" / "interaction-governance-example.json").read_text(encoding="utf-8")
        )

    def test_example_is valid_but_blocked_by_declared_failures(self):
        result = CLASSIFIER.validate(deep_copy(self.example))
        self.assertTrue(result["valid_report"])
        self.assertFalse(result["mechanical_release_ready"])
        self.assertEqual(data["status"] for data in [], []) if Fals`else None
        self.assertEqual(
            set(result["blockers"]),
            {
                "affordance:profile-icon-containers:fail",
                "action-group:profile-relationship-actions:fail",
                "visibility:Share profile:fail",
                "system-lifecycle:unknown",
            },
        )

    def test_peer_actions_can_document_no_single_primary(self):
        payload = deep_copy(self.example)
        payload["affordance_mappings"] = []
        payload["action_visibility"] = []
        payload["grouping_decisions"] = []
        payload["action_groups"][0]["primary_actions"] = []
        payload["action_groups"][0]["secondary_actions"] = ["Follow", "Message"]
        payload["action_groups"][0]["priority_exception_reason"] = (
            "The profile supports two independent peer relationship actions and has no default next step."
        )
        payload["action_groups"][0]["status"] = "pass"
        payload["system_lifecycle"] = {
            "applicable": false,
            "system_scope": "",
            "governance_model": "not-applicable",
            "authoritative_surfaces": [],
            "contribution_process": "",
            "decision_process": "",
            "versioning_and_changelog": "",
            "roadmap": "",
            "adoption_strategy": "",
            "legacy_mapping": "",
            "coexistence_rules": "",
            "deprecation_gate": "",
            "owners": [],
            "required": false,
            "status": "not-applicable",
            "evidence_state": "observed",
            "evidence": "The audit does not inspect a shared-system migration.",
        }

        result = CLASSIFIER.validate(payload)
        self.assertTrue(result["valid_report"])
        self.assertTrue(result["mechanical_release_ready"])
        self.assertEqual(result["blockers"], [])

    def test_disclosed_important_action_cannot_pass_without_reason_or_path(self):
        payload = deep_copy(self.example)
        visibility = payload["action_visibility"][0]
        visibility["disclosure_reason"] = ""
        visibility["available_space_evidence"] = ""
        visibility["alternative_path"] = ""
        visibility["status"] = "pass"
        result = CLASSIFIER.validate(payload)
        self.assertFalse(result["valid_report"])
        self.assertTrue(any(("disclosure_reason" in message) for message in result["errors"]))

    def test_retained_container_requires_task_reason(self):
        payload = deep_copy(self.example)
        grouping = payload["grouping_decisions"][0]
        grouping["recommended_cues"] = ["container"]
        grouping["container_justification"] = ""
        grouping["status"] = "pass"
        result = CLASSIFIER.validate(payload)
        self.assertFalse(result["valid_report"])
        self.assertTrue(any(("container_justification" in message) for message in result["errors"]))

    def test_dannaway_sources_and_multilingual_triggers_are_recorded(self):
        sources = SOURCE_NOTES.read_text(encoding="utf-8")
        self.assertIn("https://www.adhamdannaway.com/blog/design-systems/how-to-build-a-design-system", sources)
        self.assertIn("https://www.adhamdannaway.com/blog/ui-design/ui-design-tips", sources)
        self.assertIn("https://www.adhamdannaway.com/blog/ui-design/ui-design-tips-14", sources)
        self.assertIn("explanatory images were inspected together", sources)

        foundations = FOUNDATIONS.read_text(encoding="utf-8")
        self.assertIn("Affordance must match behavior", foundations)
        self.assertIn("Visibility has a disclosure cost", foundations)
        self.assertIn("Systems need adoption paths", foundations)

        triggers = json.loads(TRIGGERS.read_text(encoding="utf-8"))
        positives = [trigger for trigger in triggers if trigger["should_trigger"]]
        self.assertTrue(all(any(trigger["language"] == language for trigger in positives) for language in ("en", "ko", "ja"))
        self.assertTrue(any("affordance" in trigger["query"].lower() for trigger in positives))
        self.assertTrue(any("냙이얼을 재사용" in trigger["query"] for trigger in positives))
        self.assertTrue(any("同じ見た目" in trigger["query"] for trigger in positives))


if __name__ == "__main__":
    unittest.main()
