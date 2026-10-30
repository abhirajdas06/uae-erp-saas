from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
QUALITY_SCRIPTS = ROOT / "scripts/quality"
sys.path.insert(0, str(QUALITY_SCRIPTS))

import scan_secrets  # noqa: E402
import validate_docs  # noqa: E402
import validate_governance  # noqa: E402
import validate_manifests  # noqa: E402


class ManifestValidatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.phase = json.loads((ROOT / "orchestration/phase-manifest.yml").read_text(encoding="utf-8"))
        cls.task = json.loads((ROOT / "orchestration/task-manifest.yml").read_text(encoding="utf-8"))

    def test_repository_manifests_are_valid(self) -> None:
        findings, metrics = validate_manifests.validate(self.phase, self.task, ROOT)
        self.assertEqual([], findings)
        self.assertEqual(2, metrics["phase_count"])
        self.assertEqual(2, metrics["task_count"])

    def test_dependency_cycle_fails(self) -> None:
        phase = copy.deepcopy(self.phase)
        phase["phases"][0]["dependencies"] = ["P01"]
        findings, _ = validate_manifests.validate(phase, self.task, ROOT)
        self.assertIn("MANIFEST_PHASE_CYCLE", {item["code"] for item in findings})

    def test_unauthorized_active_task_fails(self) -> None:
        task = copy.deepcopy(self.task)
        task["tasks"][0]["implementation_authorized"] = False
        task["tasks"][0]["authorization_reference"] = None
        findings, _ = validate_manifests.validate(self.phase, task, ROOT)
        self.assertIn("MANIFEST_STATUS_GUARD", {item["code"] for item in findings})


class DocumentationValidatorTests(unittest.TestCase):
    def test_missing_internal_link_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            docs = root / "docs"
            docs.mkdir()
            (docs / "a.md").write_text("# A\n\n[missing](missing.md)\n", encoding="utf-8")
            findings, _, _ = validate_docs.validate(root, docs)
            self.assertIn("DOC_LINK_MISSING", {item["code"] for item in findings})

    def test_repository_documentation_is_valid(self) -> None:
        findings, metrics, _ = validate_docs.validate(ROOT, ROOT / "docs")
        self.assertEqual([], findings)
        self.assertGreater(metrics["markdown_file_count"], 50)


class GovernanceValidatorTests(unittest.TestCase):
    def test_repository_governance_is_valid(self) -> None:
        findings, metrics, _ = validate_governance.validate(ROOT, ROOT / "docs")
        self.assertEqual([], findings)
        self.assertEqual(20, metrics["adr_count"])
        self.assertEqual(53, metrics["p01_not_run_count"])


class SecretScannerTests(unittest.TestCase):
    def test_known_token_shape_is_detected_without_exposing_value(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            baseline = root / ".secrets.baseline"
            baseline.write_text('{"allowed_fingerprints": []}\n', encoding="utf-8")
            token = "ghp" + "_" + ("A" * 36)
            (root / "example.txt").write_text(token + "\n", encoding="utf-8")
            findings, _, _ = scan_secrets.scan(root, baseline)
            self.assertIn("GITHUB_TOKEN", {item["code"] for item in findings})
            self.assertNotIn(token, json.dumps(findings))


if __name__ == "__main__":
    unittest.main()

