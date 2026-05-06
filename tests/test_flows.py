"""Tests for flow routing and transitions."""
import pytest
from pathlib import Path
import yaml


class TestFlowDefinitions:
    """Test that flow definitions are properly configured."""

    @pytest.fixture
    def flows_config(self):
        """Load flows.yml configuration."""
        flows_path = Path("data/flows.yml")
        assert flows_path.exists(), "flows.yml must exist"

        with open(flows_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def test_all_required_flows_exist(self, flows_config):
        """Test that all required flows are defined."""
        required_flows = ["saludo", "ayuda", "consulta_auditoria", "fuera_tema"]

        assert "flows" in flows_config, "flows key must exist in flows.yml"

        for flow_name in required_flows:
            assert flow_name in flows_config["flows"], \
                f"Flow '{flow_name}' must be defined in flows.yml"

    def test_saludo_flow_config(self, flows_config):
        """Test saludo flow configuration."""
        flow = flows_config["flows"]["saludo"]

        assert "description" in flow
        assert "nlu_trigger" in flow
        assert "steps" in flow

        assert len(flow["steps"]) > 0
        assert flow["steps"][0]["action"] == "utter_greeting"

    def test_ayuda_flow_config(self, flows_config):
        """Test ayuda flow configuration."""
        flow = flows_config["flows"]["ayuda"]

        assert "description" in flow
        assert "nlu_trigger" in flow
        assert "steps" in flow

        assert len(flow["steps"]) > 0
        assert flow["steps"][0]["action"] == "utter_help"

    def test_fuera_tema_flow_config(self, flows_config):
        """Test fuera_tema flow configuration."""
        flow = flows_config["flows"]["fuera_tema"]

        assert "description" in flow
        assert "nlu_trigger" in flow
        assert "steps" in flow

        assert len(flow["steps"]) > 0
        assert flow["steps"][0]["action"] == "utter_fuera_tema"

    def test_consulta_auditoria_flow_config(self, flows_config):
        """Test consulta_auditoria flow configuration."""
        flow = flows_config["flows"]["consulta_auditoria"]

        assert "description" in flow
        assert "nlu_trigger" in flow
        assert "steps" in flow

        assert len(flow["steps"]) > 0
        assert flow["steps"][0]["action"] == "action_call_farmarag"

    def test_all_flows_have_triggers(self, flows_config):
        """Test that all flows have NLU triggers configured."""
        for flow_name, flow_config in flows_config["flows"].items():
            assert "nlu_trigger" in flow_config, \
                f"Flow '{flow_name}' must have nlu_trigger"

            triggers = flow_config["nlu_trigger"]
            assert len(triggers) > 0, \
                f"Flow '{flow_name}' must have at least one trigger"

            for trigger in triggers:
                assert "intent" in trigger, \
                    f"Trigger in '{flow_name}' must have intent"
                assert "name" in trigger["intent"], \
                    f"Intent in '{flow_name}' must have name"
                assert "confidence_threshold" in trigger["intent"], \
                    f"Intent in '{flow_name}' must have confidence_threshold"

    def test_confidence_thresholds_reasonable(self, flows_config):
        """Test that all confidence thresholds are within reasonable range."""
        for flow_name, flow_config in flows_config["flows"].items():
            for trigger in flow_config.get("nlu_trigger", []):
                threshold = trigger["intent"]["confidence_threshold"]
                assert 0.3 <= threshold <= 0.8, \
                    f"Threshold for '{flow_name}' should be between 0.3 and 0.8, got {threshold}"


class TestDomainConfiguration:
    """Test domain.yml configuration."""

    @pytest.fixture
    def domain_config(self):
        """Load domain.yml configuration."""
        domain_path = Path("domain.yml")
        assert domain_path.exists(), "domain.yml must exist"

        with open(domain_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def test_all_intents_defined(self, domain_config):
        """Test that all required intents are in domain."""
        required_intents = ["saludo", "ayuda", "consulta_auditoria", "fuera_tema"]

        assert "intents" in domain_config, "intents must be defined in domain.yml"

        for intent_name in required_intents:
            assert intent_name in domain_config["intents"], \
                f"Intent '{intent_name}' must be in domain.yml"

    def test_required_responses_defined(self, domain_config):
        """Test that all required responses are in domain."""
        required_responses = [
            "utter_greeting",
            "utter_help",
            "utter_fuera_tema",
            "utter_consulta_auditoria_error",
            "utter_backend_unavailable",
            "utter_timeout"
        ]

        assert "responses" in domain_config, "responses must be defined in domain.yml"

        for response_name in required_responses:
            assert response_name in domain_config["responses"], \
                f"Response '{response_name}' must be in domain.yml"

    def test_required_actions_defined(self, domain_config):
        """Test that all required actions are in domain."""
        required_actions = ["action_call_farmarag"]

        assert "actions" in domain_config, "actions must be defined in domain.yml"

        for action_name in required_actions:
            assert action_name in domain_config["actions"], \
                f"Action '{action_name}' must be in domain.yml"

    def test_slots_defined(self, domain_config):
        """Test that required slots are defined."""
        required_slots = [
            "audit_question",
            "farmarag_response",
            "provider_used",
            "fallback_triggered",
            "correlation_id",
            "last_error_code"
        ]

        assert "slots" in domain_config, "slots must be defined in domain.yml"

        for slot_name in required_slots:
            assert slot_name in domain_config["slots"], \
                f"Slot '{slot_name}' must be in domain.yml"


class TestNLUData:
    """Test NLU training data."""

    @pytest.fixture
    def nlu_data(self):
        """Load NLU data."""
        nlu_path = Path("data/nlu.yml")
        assert nlu_path.exists(), "data/nlu.yml must exist"

        with open(nlu_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def test_all_intents_have_examples(self, nlu_data):
        """Test that all intents have examples."""
        required_intents = ["saludo", "ayuda", "consulta_auditoria", "fuera_tema"]

        assert "nlu" in nlu_data, "nlu key must exist in nlu.yml"

        for intent_data in nlu_data["nlu"]:
            if "intent" in intent_data:
                intent_name = intent_data["intent"]
                if intent_name in required_intents:
                    assert "examples" in intent_data, \
                        f"Intent '{intent_name}' must have examples"
                    examples = intent_data["examples"]
                    assert isinstance(examples, str) or "examples" in intent_data
                    assert len(examples) > 10, \
                        f"Intent '{intent_name}' should have at least 10 examples"

    def test_minimum_examples_per_intent(self, nlu_data):
        """Test that each intent has a minimum number of examples."""
        min_examples = 15

        for intent_data in nlu_data["nlu"]:
            if "intent" in intent_data:
                intent_name = intent_data["intent"]
                if "examples" in intent_data:
                    examples_text = intent_data["examples"]
                    example_lines = [
                        line.strip()
                        for line in examples_text.strip().split("\n")
                        if line.strip().startswith("- ")
                    ]
                    assert len(example_lines) >= min_examples, \
                        f"Intent '{intent_name}' should have at least {min_examples} examples, got {len(example_lines)}"

    def test_saludo_examples_diverse(self, nlu_data):
        """Test that saludo examples cover different greeting styles."""
        for intent_data in nlu_data["nlu"]:
            if intent_data.get("intent") == "saludo" and "examples" in intent_data:
                examples = intent_data["examples"].lower()
                greetings = ["hola", "buen", "buenos", "buenas", "qué tal", "que tal"]
                found = sum(1 for g in greetings if g in examples)
                assert found >= 3, "saludo should have diverse greeting examples"

    def test_fuera_tema_examples_cover_off_topic(self, nlu_data):
        """Test that fuera_tema examples cover various off-topic categories."""
        for intent_data in nlu_data["nlu"]:
            if intent_data.get("intent") == "fuera_tema" and "examples" in intent_data:
                examples = intent_data["examples"].lower()
                categories = [
                    "hora", "clima", "chiste", "quién", "comida",
                    "película", "dólar", "everest"
                ]
                found = sum(1 for c in categories if c in examples)
                assert found >= 4, "fuera_tema should have diverse off-topic examples"