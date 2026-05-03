from typing import Any, Dict, List
import logging
import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, Event

logger = logging.getLogger(__name__)


class ActionCallFarmaRAG(Action):
    def name(self) -> str:
        return "action_call_farmarag"

    async def run(
        self, dispatcher, tracker: Tracker, domain: Dict[str, Any]
    ) -> List[Event]:
        user_message = tracker.latest_message.get("text", "")

        try:
            response = requests.post(
                "http://localhost:8000/ask",
                json={"question": user_message},
                timeout=30
            )
            response.raise_for_status()
            data = response.json()

            answer = data.get("answer", "No pude obtener respuesta de FarmaRAG.")
            provider = data.get("provider_used", "unknown")

            dispatcher.utter_message(text=answer)

            return [
                SlotSet("farmarag_response", answer),
                SlotSet("provider_used", provider)
            ]

        except requests.exceptions.Timeout:
            logger.error("FarmaRAG timeout")
            dispatcher.utter_message(
                text="Disculpe, la consulta ha excedido el tiempo límite. Por favor, intente nuevamente."
            )
            return [SlotSet("farmarag_response", "timeout")]

        except requests.exceptions.ConnectionError:
            logger.error("FarmaRAG connection error")
            dispatcher.utter_message(
                text="No pude conectarme al servicio FarmaRAG. Verifique que esté corriendo en puerto 8000."
            )
            return [SlotSet("farmarag_response", "connection_error")]

        except Exception as e:
            logger.error(f"FarmaRAG error: {e}")
            dispatcher.utter_message(
                text="Ocurrió un error al procesar su consulta de auditoría."
            )
            return [SlotSet("farmarag_response", "error")]