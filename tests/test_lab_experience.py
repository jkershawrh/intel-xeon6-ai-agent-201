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

        # Braces collide with Antora attribute substitution because the
        # corresponding lowercase attributes are supplied in antora.yml.
        self.assertIn('ADVISOR_MODEL="$MAAS_MODEL"', wiring)
        self.assertIn('--from-literal=api-base="$MAAS_ENDPOINT"', wiring)
        self.assertIn('--from-literal=api-key="$MAAS_API_KEY"', wiring)
        self.assertNotIn('${MAAS_MODEL}', wiring)
        self.assertNotIn('${MAAS_ENDPOINT}', wiring)
        self.assertNotIn('${MAAS_API_KEY}', wiring)
        self.assertNotIn("%maas_url%", wiring)
        self.assertNotIn("%litellm_api_key%", wiring)

    def test_showroom_uses_the_launchpad_partnership_header(self):
        supplemental = ROOT / "content" / "supplemental-ui"
        header = (supplemental / "partials" / "header-content.hbs").read_text()
        css = (supplemental / "css" / "site-extra.css").read_text()
        site = (ROOT / "site.yml").read_text()

        self.assertIn("supplemental_files: ./content/supplemental-ui", site)
        self.assertIn("Red Hat and Intel AI Launchpad home", header)
        self.assertIn("redhat-logo.svg", header)
        self.assertIn("intel-logo.svg", header)
        self.assertIn("launchpad-showroom-title", header)
        self.assertIn(".launchpad-showroom-brand", css)
        self.assertIn(".launchpad-showroom-redhat", css)
        self.assertIn("height: 2rem", css)
        self.assertIn("height: 1.55rem", css)
        self.assertTrue((supplemental / "img" / "redhat-logo.svg").is_file())
        self.assertTrue((supplemental / "img" / "intel-logo.svg").is_file())

    def test_workload_manifests_are_pinned_to_an_immutable_commit(self):
        content = "\n".join(path.read_text() for path in PAGES.glob("*.adoc"))

        self.assertNotIn("raw.githubusercontent.com/rhpds/triforce/201-v1.0.0", content)
        self.assertIn(
            "raw.githubusercontent.com/rhpds/triforce/"
            "f484cb66c3dcddff323df8814f637dc92c73c179",
            content,
        )

    def test_console_has_a_specific_learning_checkpoint(self):
        content = "\n".join(path.read_text() for path in PAGES.glob("*.adoc"))
        ui_config = (ROOT / "ui-config.yml").read_text()

        self.assertIn("OpenShift Console", content)
        self.assertIn("OCP Console", ui_config)
        self.assertIn("Workloads", content)
        self.assertIn("ConfigMaps", content)

    def test_operator_tabs_match_the_guided_journey(self):
        ui_config = (ROOT / "ui-config.yml").read_text()

        self.assertIn("name: Terminal", ui_config)
        self.assertIn("name: Solution Architect", ui_config)
        self.assertIn("name: OCP Console", ui_config)
        self.assertLess(ui_config.index("name: Terminal"), ui_config.index("name: Solution Architect"))
        self.assertLess(ui_config.index("name: Solution Architect"), ui_config.index("name: OCP Console"))

    def test_terminal_calls_stay_inside_the_namespace_without_disabling_tls(self):
        tools = (PAGES / "02-deploy-tools.adoc").read_text()
        agent = (PAGES / "03-wire-agent.adoc").read_text()
        tune = (PAGES / "04-test-and-tune.adoc").read_text()
        proof = (PAGES / "05-prove-and-clean.adoc").read_text()
        content = "\n".join((tools, agent, tune, proof))

        self.assertIn('MCP_URL="http://solution-tools:8095"', tools)
        self.assertNotIn("oc get route solution-tools", tools)
        self.assertIn('ADVISOR_URL="http://solution-agent:8082"', agent)
        self.assertIn('ADVISOR_URL="http://solution-agent:8082"', tune)
        self.assertIn('ADVISOR_URL="http://solution-agent:8082"', proof)
        self.assertIn("`solution-agent` port `8082`", proof)
        self.assertNotIn("`solution-agent` port `8080`", proof)
        self.assertNotIn("oc get route solution-agent", "\n".join((agent, tune, proof)))
        self.assertNotIn("curl -k", content)
        self.assertNotIn("curl --insecure", content)

    def test_short_route_adapter_preserves_the_pinned_triforce_contract(self):
        tools = (PAGES / "02-deploy-tools.adoc").read_text()
        wiring = (PAGES / "03-wire-agent.adoc").read_text()
        cleanup = (PAGES / "05-prove-and-clean.adoc").read_text()

        assert "f484cb66c3dcddff323df8814f637dc92c73c179" in tools
        assert "text.count(source) != 1" in tools
        assert "text.replace(source, target, 1)" in tools
        assert "/tmp/apply-triforce-201 solution-tools.yaml solution-tools tools" in tools
        assert "/tmp/apply-triforce-201 solution-agent.yaml solution-agent agent" in wiring
        assert "/tmp/apply-triforce-201 solution-ui.yaml solution-ui app" in wiring
        assert "oc get route app" in wiring
        assert "route/tools route/agent route/app" in cleanup
        assert "route/solution-tools route/solution-agent route/solution-ui" not in cleanup

    def test_cleanup_removes_only_learner_created_resources(self):
        proof = (PAGES / "05-prove-and-clean.adoc").read_text()

        for resource in (
            "deployment/solution-ui service/solution-ui route/app",
            "deployment/solution-agent service/solution-agent route/agent",
            "deployment/solution-tools service/solution-tools route/tools",
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
