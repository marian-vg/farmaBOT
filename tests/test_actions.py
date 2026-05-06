"""Tests for action_call_farmarag custom action."""
import json
import pytest
from unittest.mock import MagicMock, patch, Mock
import requests

from actions.actions import ActionCallFarmaRAG


class TestActionCallFarmaRAG:
    """Test the ActionCallFarmaRAG custom action."""

    @pytest.fixture
    def action(self):
        """Create an instance of ActionCallFarmaRAG."""
        return ActionCallFarmaRAG()

    @pytest.fixture
    def mock_dispatcher(self):
        """Create a mock dispatcher."""
        dispatcher = MagicMock()
        dispatcher.utter_message = MagicMock()
        return dispatcher

    @pytest.fixture
    def mock_tracker(self):
        """Create a mock tracker with a valid message."""
        tracker = MagicMock()
        tracker.latest_message = {
            "text": "Cuáles son los requisitos de PAMI?",
            "intent": {"name": "consulta_auditoria"}
        }
        return tracker

    @pytest.fixture
    def mock_tracker_empty(self):
        """Create a mock tracker with an empty message."""
        tracker = MagicMock()
        tracker.latest_message = {"text": "", "intent": {}}
        return tracker

    def test_action_name(self, action):
        """Test that the action name is correct."""
        assert action.name() == "action_call_farmarag"

    def test_empty_message_handling(self, action, mock_dispatcher, mock_tracker_empty):
        """Test handling of empty user messages."""
        result = action.run(mock_dispatcher, mock_tracker_empty, {})

        mock_dispatcher.utter_message.assert_called_once_with(
            response="utter_consulta_auditoria_error"
        )

        slot_names = [event.name for event in result if hasattr(event, 'name')]
        assert "correlation_id" in slot_names
        assert "last_error_code" in slot_names

    def test_successful_farmarag_call(self, action, mock_dispatcher, mock_tracker):
        """Test successful call to FarmaRAG backend."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.ok = True
        mock_response.json.return_value = {
            "answer": "Los requisitos de PAMI son: formulario específico, DNI del paciente, receta médica.",
            "provider_used": "gemini",
            "fallback_triggered": False
        }

        with patch.object(requests, 'post', return_value=mock_response):
            result = action.run(mock_dispatcher, mock_tracker, {})

            mock_dispatcher.utter_message.assert_called_once_with(
                text="Los requisitos de PAMI son: formulario específico, DNI del paciente, receta médica."
            )

            slot_names = [event.name for event in result if hasattr(event, 'name')]
            assert "audit_question" in slot_names
            assert "correlation_id" in slot_names
            assert "farmarag_response" in slot_names
            assert "provider_used" in slot_names

    def test_timeout_handling(self, action, mock_dispatcher, mock_tracker):
        """Test handling of FarmaRAG timeout."""
        with patch.object(requests, 'post', side_effect=requests.exceptions.Timeout()):
            result = action.run(mock_dispatcher, mock_tracker, {})

            mock_dispatcher.utter_message.assert_called_once_with(
                response="utter_timeout"
            )

            slot_names = [event.name for event in result if hasattr(event, 'name')]
            last_error_slot = next(
                (event.value for event in result if hasattr(event, 'name') and event.name == "last_error_code"),
                None
            )
            assert last_error_slot == "timeout"

    def test_connection_error_handling(self, action, mock_dispatcher, mock_tracker):
        """Test handling of FarmaRAG connection error."""
        with patch.object(requests, 'post', side_effect=requests.exceptions.ConnectionError()):
            result = action.run(mock_dispatcher, mock_tracker, {})

            mock_dispatcher.utter_message.assert_called_once_with(
                response="utter_backend_unavailable"
            )

            last_error_slot = next(
                (event.value for event in result if hasattr(event, 'name') and event.name == "last_error_code"),
                None
            )
            assert last_error_slot == "connection_error"

    def test_rate_limit_handling(self, action, mock_dispatcher, mock_tracker):
        """Test handling of FarmaRAG rate limit (429)."""
        mock_response = Mock()
        mock_response.status_code = 429
        mock_response.ok = False

        with patch.object(requests, 'post', return_value=mock_response):
            result = action.run(mock_dispatcher, mock_tracker, {})

            mock_dispatcher.utter_message.assert_called_once()
            call_args = mock_dispatcher.utter_message.call_args
            assert "límite" in str(call_args).lower() or "rate" in str(call_args).lower()

    def test_server_error_handling(self, action, mock_dispatcher, mock_tracker):
        """Test handling of FarmaRAG server errors (500, 502, 503, 504)."""
        for status_code in [500, 502, 503, 504]:
            mock_dispatcher.reset_mock()

            mock_response = Mock()
            mock_response.status_code = status_code
            mock_response.ok = False

            with patch.object(requests, 'post', return_value=mock_response):
                result = action.run(mock_dispatcher, mock_tracker, {})

                mock_dispatcher.utter_message.assert_called_once_with(
                    response="utter_backend_unavailable"
                )

    def test_invalid_json_response(self, action, mock_dispatcher, mock_tracker):
        """Test handling of invalid JSON response from FarmaRAG."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.ok = True
        mock_response.json.side_effect = ValueError("Invalid JSON")

        with patch.object(requests, 'post', return_value=mock_response):
            result = action.run(mock_dispatcher, mock_tracker, {})

            mock_dispatcher.utter_message.assert_called_once_with(
                response="utter_consulta_auditoria_error"
            )

    def test_missing_answer_field(self, action, mock_dispatcher, mock_tracker):
        """Test handling of response without answer field."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.ok = True
        mock_response.json.return_value = {
            "provider_used": "gemini",
            "fallback_triggered": False
        }

        with patch.object(requests, 'post', return_value=mock_response):
            result = action.run(mock_dispatcher, mock_tracker, {})

            mock_dispatcher.utter_message.assert_called_once_with(
                response="utter_consulta_auditoria_error"
            )

    def test_empty_answer_field(self, action, mock_dispatcher, mock_tracker):
        """Test handling of empty answer in response."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.ok = True
        mock_response.json.return_value = {
            "answer": "",
            "provider_used": "gemini",
            "fallback_triggered": False
        }

        with patch.object(requests, 'post', return_value=mock_response):
            result = action.run(mock_dispatcher, mock_tracker, {})

            mock_dispatcher.utter_message.assert_called_once_with(
                response="utter_consulta_auditoria_error"
            )

    def test_retry_logic_on_timeout(self, action, mock_dispatcher, mock_tracker):
        """Test that retry logic is executed on timeout."""
        call_count = 0

        def mock_post(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise requests.exceptions.Timeout()
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.ok = True
            mock_response.json.return_value = {
                "answer": "Success after retry",
                "provider_used": "gemini",
                "fallback_triggered": False
            }
            return mock_response

        with patch.object(requests, 'post', side_effect=mock_post):
            with patch('time.sleep'):
                result = action.run(mock_dispatcher, mock_tracker, {})

                assert call_count == 3, f"Expected 3 calls, got {call_count}"
                mock_dispatcher.utter_message.assert_called_once_with(text="Success after retry")

    def test_intent_tracking(self, action, mock_dispatcher, mock_tracker):
        """Test that intent information is tracked in slots."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.ok = True
        mock_response.json.return_value = {
            "answer": "Test answer",
            "provider_used": "gemini",
            "fallback_triggered": False
        }

        with patch.object(requests, 'post', return_value=mock_response):
            result = action.run(mock_dispatcher, mock_tracker, {})

            intent_slot = next(
                (event.value for event in result if hasattr(event, 'name') and event.name == "audit_question"),
                None
            )
            assert intent_slot == "Cuáles son los requisitos de PAMI?"