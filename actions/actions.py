from __future__ import annotations

import logging
import uuid
import time
from typing import Any

import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.events import EventType, SlotSet
from rasa_sdk.executor import CollectingDispatcher


logger = logging.getLogger(__name__)

FARMARAG_ASK_URL = "http://127.0.0.1:8000/ask"
REQUEST_TIMEOUT_SECONDS = 25
MAX_RETRIES = 3
RETRY_BACKOFF_FACTOR = 1.5


class ActionCallFarmaRAG(Action):
    def name(self) -> str:
        return "action_call_farmarag"

    def _call_farmarag_with_retry(
        self,
        url: str,
        payload: dict,
        headers: dict,
        max_retries: int = MAX_RETRIES,
    ) -> requests.Response:
        last_exception = None

        for attempt in range(max_retries):
            try:
                response = requests.post(
                    url,
                    json=payload,
                    headers=headers,
                    timeout=REQUEST_TIMEOUT_SECONDS,
                )
                return response
            except requests.exceptions.Timeout as e:
                last_exception = e
                logger.warning(
                    f"FarmaRAG timeout (attempt {attempt + 1}/{max_retries})",
                    extra={"attempt": attempt + 1, "max_retries": max_retries},
                )
                if attempt < max_retries - 1:
                    wait_time = RETRY_BACKOFF_FACTOR ** attempt
                    logger.info(f"Retrying in {wait_time:.1f}s...")
                    time.sleep(wait_time)
            except requests.exceptions.ConnectionError as e:
                last_exception = e
                logger.error(
                    f"FarmaRAG connection error (attempt {attempt + 1}/{max_retries})",
                    extra={"attempt": attempt + 1, "error": str(e)},
                )
                if attempt < max_retries - 1:
                    wait_time = RETRY_BACKOFF_FACTOR ** attempt
                    logger.info(f"Retrying in {wait_time:.1f}s...")
                    time.sleep(wait_time)

        raise last_exception

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: dict[str, Any],
    ) -> list[EventType]:
        del domain

        user_message = (tracker.latest_message or {}).get("text", "").strip()
        correlation_id = str(uuid.uuid4())
        intent_name = (tracker.latest_message or {}).get("intent", {}).get("name", "unknown")

        if not user_message:
            logger.warning("Empty user message received", extra={"correlation_id": correlation_id})
            dispatcher.utter_message(response="utter_consulta_auditoria_error")
            return [
                SlotSet("correlation_id", correlation_id),
                SlotSet("last_error_code", "empty_question"),
            ]

        payload = {"question": user_message}
        headers = {
            "X-Correlation-ID": correlation_id,
            "Content-Type": "application/json",
        }

        logger.info(
            "Calling FarmaRAG backend",
            extra={
                "correlation_id": correlation_id,
                "question_length": len(user_message),
                "intent": intent_name,
                "url": FARMARAG_ASK_URL,
            },
        )

        try:
            response = self._call_farmarag_with_retry(
                FARMARAG_ASK_URL,
                payload,
                headers,
            )
        except requests.exceptions.Timeout:
            logger.warning(
                "FarmaRAG request timed out after retries",
                extra={"correlation_id": correlation_id},
            )
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
            logger.error(
                "FarmaRAG connection error after retries",
                extra={"correlation_id": correlation_id},
            )
            dispatcher.utter_message(response="utter_backend_unavailable")
            return [
                SlotSet("audit_question", user_message),
                SlotSet("correlation_id", correlation_id),
                SlotSet("farmarag_response", None),
                SlotSet("provider_used", None),
                SlotSet("fallback_triggered", False),
                SlotSet("last_error_code", "connection_error"),
            ]
        except Exception as e:
            logger.error(
                "FarmaRAG unexpected error",
                extra={"correlation_id": correlation_id, "error": str(e)},
            )
            dispatcher.utter_message(response="utter_backend_unavailable")
            return [
                SlotSet("audit_question", user_message),
                SlotSet("correlation_id", correlation_id),
                SlotSet("farmarag_response", None),
                SlotSet("provider_used", None),
                SlotSet("fallback_triggered", False),
                SlotSet("last_error_code", "unexpected_error"),
            ]

        if response.status_code == 429:
            logger.warning(
                "FarmaRAG rate limit",
                extra={"correlation_id": correlation_id},
            )
            dispatcher.utter_message(
                text="FarmaRAG alcanzó su límite temporal de consultas. Intente nuevamente en unos momentos."
            )
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
            logger.error(
                "Invalid FarmaRAG JSON response",
                extra={"correlation_id": correlation_id},
            )
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
            logger.error(
                "Missing FarmaRAG answer",
                extra={"correlation_id": correlation_id},
            )
            dispatcher.utter_message(response="utter_consulta_auditoria_error")
            return [
                SlotSet("audit_question", user_message),
                SlotSet("correlation_id", correlation_id),
                SlotSet("farmarag_response", None),
                SlotSet("provider_used", data.get("provider_used")),
                SlotSet("fallback_triggered", bool(data.get("fallback_triggered", False))),
                SlotSet("last_error_code", "missing_answer"),
            ]

        logger.info(
            "FarmaRAG response received",
            extra={
                "correlation_id": correlation_id,
                "provider": data.get("provider_used"),
                "answer_length": len(answer),
            },
        )

        dispatcher.utter_message(text=answer)
        return [
            SlotSet("audit_question", user_message),
            SlotSet("correlation_id", correlation_id),
            SlotSet("farmarag_response", answer),
            SlotSet("provider_used", data.get("provider_used")),
            SlotSet("fallback_triggered", bool(data.get("fallback_triggered", False))),
            SlotSet("last_error_code", None),
        ]
