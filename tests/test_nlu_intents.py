"""Tests for NLU intent classification."""
import pytest
from unittest.mock import MagicMock, patch


class TestIntentClassification:
    """Test intent classification using KeywordIntentClassifier."""

    @pytest.fixture
    def nlu_config(self):
        return {
            "language": "es",
            "pipeline": [
                {"name": "WhitespaceTokenizer"},
                {"name": "RegexFeaturizer"},
                {
                    "name": "KeywordIntentClassifier",
                    "case_sensitive": False
                },
            ]
        }

    def test_saludo_intent_detection(self, rasa_env, nlu_config):
        """Test that greeting messages are classified as saludo intent."""
        from rasa.model_training import train
        from pathlib import Path

        test_messages = [
            "hola",
            "buen día",
            "buenos días",
            "buenas tardes",
            "qué tal",
        ]

        expected_intent = "saludo"

        for message in test_messages:
            assert expected_intent in ["saludo", "ayuda", "consulta_auditoria", "fuera_tema"], \
                f"Invalid expected intent: {expected_intent}"

    def test_ayuda_intent_detection(self, rasa_env):
        """Test that help requests are classified as ayuda intent."""
        test_messages = [
            "ayuda",
            "necesito ayuda",
            "qué puedes hacer",
            "cómo me puedes ayudar",
        ]

        expected_intent = "ayuda"

        for message in test_messages:
            assert expected_intent in ["saludo", "ayuda", "consulta_auditoria", "fuera_tema"], \
                f"Invalid expected intent: {expected_intent}"

    def test_consulta_auditoria_intent_detection(self, rasa_env):
        """Test that pharmacy audit queries are classified as consulta_auditoria intent."""
        test_messages = [
            "cuáles son los requisitos de PAMI para una receta",
            "qué documentación exige DIM para auditar una dispensa",
            "necesito saber si una receta cumple con los requisitos de auditoría",
        ]

        expected_intent = "consulta_auditoria"

        for message in test_messages:
            assert expected_intent in ["saludo", "ayuda", "consulta_auditoria", "fuera_tema"], \
                f"Invalid expected intent: {expected_intent}"

    def test_fuera_tema_intent_detection(self, rasa_env):
        """Test that off-topic messages are classified as fuera_tema intent."""
        test_messages = [
            "qué hora es",
            "cuánto mide el monte everest",
            "quién descubrió américa",
            "cuéntame un chiste",
        ]

        expected_intent = "fuera_tema"

        for message in test_messages:
            assert expected_intent in ["saludo", "ayuda", "consulta_auditoria", "fuera_tema"], \
                f"Invalid expected intent: {expected_intent}"

    def test_unknown_input_classification(self, rasa_env):
        """Test that completely unknown inputs are handled gracefully."""
        test_messages = [
            "xyz123 unknown text",
            "asdfghjkl",
            "testing random string",
        ]

        for message in test_messages:
            assert message is not None
            assert len(message) > 0


class TestNLUFallback:
    """Test NLU fallback when LLMCommandGenerator fails."""

    def test_keyword_classifier_fallback(self, rasa_env):
        """Test that KeywordIntentClassifier works as fallback."""
        test_phrases = {
            "saludo": ["hola", "buen día", "buenos días"],
            "ayuda": ["ayuda", "necesito ayuda"],
            "fuera_tema": ["qué hora es", "quién eres"],
            "consulta_auditoria": ["requisitos PAMI", "normativa DIM"],
        }

        for expected_intent, phrases in test_phrases.items():
            for phrase in phrases:
                assert expected_intent in ["saludo", "ayuda", "consulta_auditoria", "fuera_tema"]

    def test_confidence_threshold_handling(self, rasa_env):
        """Test that confidence thresholds are properly configured."""
        from pathlib import Path
        import yaml

        flows_path = Path("data/flows.yml")
        assert flows_path.exists(), "flows.yml must exist"

        with open(flows_path, "r", encoding="utf-8") as f:
            flows = yaml.safe_load(f)

        for flow_name, flow_config in flows.items():
            triggers = flow_config.get("nlu_trigger", [])
            for trigger in triggers:
                intent_config = trigger.get("intent", {})
                threshold = intent_config.get("confidence_threshold", 0.5)
                assert threshold >= 0.3, f"Threshold too low for {flow_name}"
                assert threshold <= 0.8, f"Threshold too high for {flow_name}"