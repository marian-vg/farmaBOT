from __future__ import annotations

import logging
import uuid
from typing import Any

import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.events import EventType, SlotSet
from rasa_sdk.executor import CollectingDispatcher


logger = logging.getLogger(__name__)

FARMARAG_ASK_URL = "http://127.0.0.1:8000/ask"
REQUEST_TIMEOUT_SECONDS = 25


class ActionCallFarmaRAG(Action):
    def name(self) -> str:
        return "action_call_farmarag"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: dict[str, Any],
    ) -> list[EventType]:
        del domain

        user_message = (tracker.latest_message or {}).get("text", "").strip()
        correlation_id = str(uuid.uuid4())

        if not user_message:
            dispatcher.utter_message(response="utter_consulta_auditoria_error")
            return [
                SlotSet("correlation_id", correlation_id),
                SlotSet("last_error_code", "empty_question"),
            ]

        payload = {"question": user_message}
        headers = {"X-Correlation-ID": correlation_id}

        logger.info(
            "Calling FarmaRAG backend",
            extra={
                "correlation_id": correlation_id,
                "question_length": len(user_message),
                "url": FARMARAG_ASK_URL,
            },
        )

        try:
            response = requests.post(
                FARMARAG_ASK_URL,
                json=payload,
                headers=headers,
                timeout=REQUEST_TIMEOUT_SECONDS,
            )
        except requests.exceptions.Timeout:
            logger.warning("FarmaRAG request timed out", extra={"correlation_id": correlation_id})
            dispatcher.utter_message(response="utter_timeout")
            return [
                SlotSet("audit_question", user_message),
                SlotSet("correlation_id", correlation_id),
                SlotSet("farmarag_response", None),
                SlotSet("provider_used", None),
                SlotSet("fallback_triggered", False),
                SlotSet("last_error_code", "timeout"),
            ]
        except requests.exceptions.ConnectionError:
            logger.error("FarmaRAG connection error", extra={"correlation_id": correlation_id})
            dispatcher.utter_message(response="utter_backend_unavailable")
            return [
                SlotSet("audit_question", user_message),
                SlotSet("correlation_id", correlation_id),
                SlotSet("farmarag_response", None),
                SlotSet("provider_used", None),
                SlotSet("fallback_triggered", False),
                SlotSet("last_error_code", "connection_error"),
            ]

        if response.status_code == 429:
            logger.warning("FarmaRAG rate limit", extra={"correlation_id": correlation_id})
            dispatcher.utter_message(text="FarmaRAG alcanzó su límite temporal de consultas. Intente nuevamente en unos momentos.")
            return [
                SlotSet("audit_question", user_message),
                SlotSet("correlation_id", correlation_id),
                SlotSet("farmarag_response", None),
                SlotSet("provider_used", None),
                SlotSet("fallback_triggered", False),
                SlotSet("last_error_code", "rate_limit"),
            ]

        if response.status_code in (500, 502, 503, 504):
            logger.error(
                "FarmaRAG service error",
                extra={"correlation_id": correlation_id, "status_code": response.status_code},
            )
            dispatcher.utter_message(response="utter_backend_unavailable")
            return [
                SlotSet("audit_question", user_message),
                SlotSet("correlation_id", correlation_id),
                SlotSet("farmarag_response", None),
                SlotSet("provider_used", None),
                SlotSet("fallback_triggered", False),
                SlotSet("last_error_code", f"http_{response.status_code}"),
            ]

        if not response.ok:
            logger.error(
                "Unexpected FarmaRAG HTTP error",
                extra={"correlation_id": correlation_id, "status_code": response.status_code},
            )
            dispatcher.utter_message(response="utter_consulta_auditoria_error")
            return [
                SlotSet("audit_question", user_message),
                SlotSet("correlation_id", correlation_id),
                SlotSet("farmarag_response", None),
                SlotSet("provider_used", None),
                SlotSet("fallback_triggered", False),
                SlotSet("last_error_code", f"http_{response.status_code}"),
            ]

        try:
            data = response.json()
        except ValueError:
            logger.error("Invalid FarmaRAG JSON response", extra={"correlation_id": correlation_id})
            dispatcher.utter_message(response="utter_consulta_auditoria_error")
            return [
                SlotSet("audit_question", user_message),
                SlotSet("correlation_id", correlation_id),
                SlotSet("farmarag_response", None),
                SlotSet("provider_used", None),
                SlotSet("fallback_triggered", False),
                SlotSet("last_error_code", "invalid_json"),
            ]

        answer = data.get("answer")
        if not isinstance(answer, str) or not answer.strip():
            logger.error("Missing FarmaRAG answer", extra={"correlation_id": correlation_id})
            dispatcher.utter_message(response="utter_consulta_auditoria_error")
            return [
                SlotSet("audit_question", user_message),
                SlotSet("correlation_id", correlation_id),
                SlotSet("farmarag_response", None),
                SlotSet("provider_used", data.get("provider_used")),
                SlotSet("fallback_triggered", bool(data.get("fallback_triggered", False))),
                SlotSet("last_error_code", "missing_answer"),
            ]

        dispatcher.utter_message(text=answer)
        return [
            SlotSet("audit_question", user_message),
            SlotSet("correlation_id", correlation_id),
            SlotSet("farmarag_response", answer),
            SlotSet("provider_used", data.get("provider_used")),
            SlotSet("fallback_triggered", bool(data.get("fallback_triggered", False))),
            SlotSet("last_error_code", None),
        ]
