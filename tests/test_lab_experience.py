"""Content contract for the Intel AI 201 learner journey.

These tests intentionally inspect the published AsciiDoc source.  They keep the
guide aligned with the single model assigned by Launchpad and require the lab to
end with executable proof and explicit cleanup of learner-created resources.
"""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
PAGES = ROOT / "content" / "modules" / "ROOT" / "pages"


class LabExperienceContract(unittest.TestCase):
    def test_journey_names_story_show_learn_do_and_prove(self):
        welcome = (PAGES / "index.adoc").read_text()

        for stage in ("Story", "Show", "Learn", "Do", "Prove"):
            self.assertIn(f"*{stage}*", welcome)

    def test_guide_does_not_claim_an_unavailable_model_comparison(self):
        content = "\n".join(path.read_text() for path in PAGES.glob("*.adoc"))

        self.assertNotIn("Compare two models", content)
        self.assertNotIn("Compared two models", content)
        self.assertNotIn("phi3-mini-cpu", content)
        self.assertNotIn("qwen25-3b-cpu", content)

    def test_proof_stage_is_executable_and_checks_model_tools_and_output(self):
        proof = (PAGES / "05-prove-and-clean.adoc").read_text()

        self.assertIn('role="execute"', proof)
        self.assertIn("/api/v1/advise", proof)
        self.assertIn(".brief", proof)
        self.assertIn(".inference_log", proof)
        self.assertIn("select(.model != null)", proof)
        self.assertIn("EXPECTED_MODEL=", proof)
        self.assertIn("all(. == $expected_model)", proof)
        self.assertIn("select(.tool != null)", proof)
        self.assertIn("/tmp/intel-ai-201-proof.json", proof)

    def test_deployment_uses_the_model_assigned_to_this_order(self):
        wiring = (PAGES / "03-wire-agent.adoc").read_text()
        component = (ROOT / "content" / "antora.yml").read_text()

        self.assertIn('maas_model: "%maas_model%"', component)
        self.assertIn("ADVISOR_MODEL='{maas_model}'", wiring)

    def test_workload_manifests_are_pinned_to_an_immutable_commit(self):
        content = "\n".join(path.read_text() for path in PAGES.glob("*.adoc"))

        self.assertNotIn("raw.githubusercontent.com/rhpds/triforce/201-v1.0.0", content)
        self.assertIn(
            "raw.githubusercontent.com/rhpds/triforce/"
            "c8dcf5bcef1f926aa5867bcc1b86b69ec33b988d",
            content,
        )

    def test_console_has_a_specific_learning_checkpoint(self):
        content = "\n".join(path.read_text() for path in PAGES.glob("*.adoc"))
        ui_config = (ROOT / "ui-config.yml").read_text()

        self.assertIn("OpenShift Console", content)
        self.assertIn("OCP Console", ui_config)
        self.assertIn("Workloads", content)
        self.assertIn("ConfigMaps", content)

    def test_cleanup_removes_only_learner_created_resources(self):
        proof = (PAGES / "05-prove-and-clean.adoc").read_text()

        for resource in (
            "solution-ui.yaml",
            "solution-agent.yaml",
            "solution-tools.yaml",
            "advisor-prompt",
            "racmaas-connection",
            "litellm-api-key",
        ):
            self.assertIn(resource, proof)
        self.assertIn("--ignore-not-found", proof)
        self.assertIn("oc get deployment,service,route,configmap", proof)
        self.assertIn("oc get secret litellm-api-key -o jsonpath='{.metadata.name}", proof)
        self.assertNotIn("oc get secret litellm-api-key -o yaml", proof)
        self.assertNotIn("oc delete project", proof)

    def test_proof_stage_is_in_navigation(self):
        nav = (ROOT / "content" / "modules" / "ROOT" / "nav.adoc").read_text()

        self.assertIn("05-prove-and-clean.adoc", nav)


if __name__ == "__main__":
    unittest.main()
