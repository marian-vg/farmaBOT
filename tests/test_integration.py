"""Integration tests for end-to-end flows."""
import pytest
import requests
from unittest.mock import Mock, patch
import json


class TestFarmaRAGIntegration:
    """Test integration with FarmaRAG backend."""

    @pytest.fixture
    def farmarag_url(self):
        return "http://127.0.0.1:8000"

    @pytest.fixture
    def farmarag_health_url(self):
        return "http://127.0.0.1:8000/health"

    def test_farmarag_health_check(self, farmarag_health_url):
        """Test that FarmaRAG backend is healthy and responsive."""
        try:
            response = requests.get(farmarag_health_url, timeout=5)
            assert response.status_code == 200, \
                f"FarmaRAG health check failed with status {response.status_code}"

            data = response.json()
            assert data.get("status") == "healthy", \
                f"FarmaRAG reports unhealthy status: {data}"
            assert data.get("engine_loaded") is True, \
                "FarmaRAG engine should be loaded"

        except requests.exceptions.ConnectionError:
            pytest.fail("Cannot connect to FarmaRAG at localhost:8000. Is it running?")
        except requests.exceptions.Timeout:
            pytest.fail("FarmaRAG health check timed out")

    def test_farmarag_root_endpoint(self, farmarag_url):
        """Test that FarmaRAG root endpoint returns correct info."""
        try:
            response = requests.get(farmarag_url, timeout=5)
            assert response.status_code == 200

            data = response.json()
            assert data.get("status") == "online"
            assert data.get("system") == "FarmaRAG Auditor"
            assert data.get("engine_loaded") is True

        except requests.exceptions.ConnectionError:
            pytest.fail("Cannot connect to FarmaRAG at localhost:8000")
        except requests.exceptions.Timeout:
            pytest.fail("FarmaRAG root endpoint timed out")

    def test_farmarag_ask_endpoint_success(self, farmarag_url):
        """Test successful query to FarmaRAG /ask endpoint."""
        try:
            payload = {
                "question": "¿Cuáles son los requisitos de PAMI para recetas?"
            }
            headers = {"Content-Type": "application/json"}

            response = requests.post(
                farmarag_url + "/ask",
                json=payload,
                headers=headers,
                timeout=30
            )

            assert response.status_code == 200, \
                f"FarmaRAG /ask failed with status {response.status_code}"

            data = response.json()
            assert "answer" in data, "Response must contain 'answer' field"
            assert isinstance(data["answer"], str), "Answer must be a string"
            assert len(data["answer"]) > 0, "Answer must not be empty"

        except requests.exceptions.ConnectionError:
            pytest.fail("Cannot connect to FarmaRAG at localhost:8000")
        except requests.exceptions.Timeout:
            pytest.fail("FarmaRAG /ask endpoint timed out")

    def test_farmarag_ask_endpoint_validation(self, farmarag_url):
        """Test that /ask endpoint validates input correctly."""
        try:
            response = requests.post(
                farmarag_url + "/ask",
                json={"question": ""},
                timeout=10
            )

            assert response.status_code == 400, \
                "Empty question should return 400 Bad Request"

        except requests.exceptions.ConnectionError:
            pytest.fail("Cannot connect to FarmaRAG at localhost:8000")

    def test_farmarag_aliases_endpoint(self, farmarag_url):
        """Test that /aliases endpoint returns model aliases."""
        try:
            response = requests.get(farmarag_url + "/aliases", timeout=5)

            assert response.status_code == 200

            data = response.json()
            assert "friendly_to_technical" in data, \
                "Response must contain 'friendly_to_technical' field"

        except requests.exceptions.ConnectionError:
            pytest.fail("Cannot connect to FarmaRAG at localhost:8000")


class TestEndToEndFlows:
    """Test complete flows from user input to FarmaRAG response."""

    @pytest.fixture
    def rasa_shell_url(self):
        return "http://localhost:5005"

    @pytest.fixture
    def rasa_rest_webhook(self):
        return "http://localhost:5005/webhooks/rest/webhook"

    def test_rasa_server_running(self, rasa_shell_url):
        """Test that Rasa server is running and accessible."""
        try:
            response = requests.get(
                rasa_shell_url + "/",
                timeout=5,
                allow_redirects=True
            )
            assert response.status_code in [200, 404], \
                f"Rasa server returned unexpected status {response.status_code}"

        except requests.exceptions.ConnectionError:
            pytest.fail("Cannot connect to Rasa server at localhost:5005. Is it running?")

    def test_rasa_webhook_endpoint(self, rasa_rest_webhook):
        """Test Rasa REST webhook endpoint."""
        try:
            payload = {
                "sender": "test_user",
                "message": "Hola"
            }

            response = requests.post(
                rasa_rest_webhook,
                json=payload,
                timeout=30
            )

            assert response.status_code == 200, \
                f"Rasa webhook failed with status {response.status_code}"

            data = response.json()
            assert isinstance(data, list), "Response should be a list of bot messages"

        except requests.exceptions.ConnectionError:
            pytest.fail("Cannot connect to Rasa webhook at localhost:5005")
        except requests.exceptions.Timeout:
            pytest.fail("Rasa webhook timed out")

    def test_saludo_flow_integration(self, rasa_rest_webhook):
        """Test saludo flow end-to-end."""
        try:
            payload = {
                "sender": "test_user_saludo",
                "message": "Hola"
            }

            response = requests.post(
                rasa_rest_webhook,
                json=payload,
                timeout=30
            )

            assert response.status_code == 200

            messages = response.json()
            assert len(messages) > 0, "Should receive at least one response"

            first_message = messages[0].get("text", "")
            assert len(first_message) > 0, "Response text should not be empty"

        except requests.exceptions.ConnectionError:
            pytest.skip("Rasa server not running - cannot test integration")

    def test_fuera_tema_flow_integration(self, rasa_rest_webhook):
        """Test fuera_tema flow end-to-end."""
        try:
            payload = {
                "sender": "test_user_fuera_tema",
                "message": "Qué hora es?"
            }

            response = requests.post(
                rasa_rest_webhook,
                json=payload,
                timeout=30
            )

            assert response.status_code == 200

            messages = response.json()
            assert len(messages) > 0, "Should receive at least one response"

        except requests.exceptions.ConnectionError:
            pytest.skip("Rasa server not running - cannot test integration")

    def test_consulta_auditoria_flow_integration(self, rasa_rest_webhook):
        """Test consulta_auditoria flow with FarmaRAG integration."""
        try:
            payload = {
                "sender": "test_user_auditoria",
                "message": "Cuáles son los requisitos de PAMI para una receta?"
            }

            response = requests.post(
                rasa_rest_webhook,
                json=payload,
                timeout=60
            )

            assert response.status_code == 200

            messages = response.json()
            assert len(messages) > 0, "Should receive at least one response"

            first_message = messages[0].get("text", "")
            assert len(first_message) > 0, "Response text should not be empty"

        except requests.exceptions.ConnectionError:
            pytest.skip("Rasa server not running - cannot test integration")
        except requests.exceptions.Timeout:
            pytest.fail("consulta_auditoria flow timed out - possible FarmaRAG issue")


class TestConfigurationFiles:
    """Test that all configuration files are valid."""

    def test_config_yml_valid(self):
        """Test that config.yml is valid YAML and has required keys."""
        from pathlib import Path
        import yaml

        config_path = Path("config.yml")
        assert config_path.exists(), "config.yml must exist"

        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)

        assert config.get("recipe") == "default.v1"
        assert config.get("language") == "es"
        assert "pipeline" in config
        assert "policies" in config

        pipeline_names = [p.get("name") for p in config["pipeline"]]
        assert "WhitespaceTokenizer" in pipeline_names
        assert "KeywordIntentClassifier" in pipeline_names
        assert "CompactLLMCommandGenerator" in pipeline_names

    def test_endpoints_yml_valid(self):
        """Test that endpoints.yml is valid."""
        from pathlib import Path
        import yaml

        endpoints_path = Path("endpoints.yml")
        assert endpoints_path.exists(), "endpoints.yml must exist"

        with open(endpoints_path, "r", encoding="utf-8") as f:
            endpoints = yaml.safe_load(f)

        assert "action_endpoint" in endpoints
        assert "url" in endpoints["action_endpoint"]
        assert "model_groups" in endpoints

    def test_credentials_yml_valid(self):
        """Test that credentials.yml is valid."""
        from pathlib import Path
        import yaml

        cred_path = Path("credentials.yml")
        assert cred_path.exists(), "credentials.yml must exist"

        with open(cred_path, "r", encoding="utf-8") as f:
            credentials = yaml.safe_load(f)

        assert "rest" in credentials