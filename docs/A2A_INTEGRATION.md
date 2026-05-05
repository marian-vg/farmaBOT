# A2A Integration: Rasa CALM + FarmaRAG

## Overview

Rasa CALM acts as conversational orchestrator (port 5005), routing user messages through dialogue flows. Audit queries are forwarded to FarmaRAG via HTTP POST to the `/ask` endpoint (port 8000), which returns RAG-generated responses.

## Architecture

```
User Input (rasa shell / webchat)
    │
    ▼
Rasa CALM (port 5005)
    │
    ├─→ Flow: saludo     → utter_greeting
    ├─→ Flow: ayuda      → utter_help
    ├─→ Flow: fuera_tema → utter_fuera_tema
    │
    └─→ Flow: consulta_auditoria
              │
              ▼ HTTP POST
        FarmaRAG (port 8000 /ask)
              │
              ▼ RAG Chain
        Chroma DB + Gemini 3.1
              │
              ▼ JSON {answer, provider_used}
        Rasa formats response
              │
              ▼
        User sees answer
```

## A2A Contract

### FarmaRAG Sub-Agent

- **URL**: `http://localhost:8000`
- **Endpoint**: `POST /ask`
- **Health**: `GET /`

### Request Format

```json
POST /ask
{
  "question": "¿Cuáles son las normas de PAMI?"
}
```

### Response Format

```json
{
  "answer": "Las normas de PAMI establecen que...",
  "provider_used": "gemini"
}
```

## Configuration Files

### credentials.yml

```yaml
farmarag_agent:
  url: http://localhost:8000
  endpoints:
    call: /ask
    health: /
```

### endpoints.yml

```yaml
action_endpoint:
  url: http://localhost:5055/webhook
```

### actions/actions.py

The `ActionCallFarmaRAG` class handles the A2A communication:

```python
class ActionCallFarmaRAG(Action):
    async def run(self, dispatcher, tracker, domain):
        user_message = tracker.latest_message.get("text", "")
        response = requests.post(
            "http://localhost:8000/ask",
            json={"question": user_message},
            timeout=30
        )
        data = response.json()
        dispatcher.utter_message(text=data["answer"])
```

## Flows

| Flow | Intent | Action |
|------|--------|--------|
| `saludo` | `saludo` | `utter_greeting` |
| `ayuda` | `ayuda` | `utter_help` |
| `fuera_tema` | `fuera_tema` | `utter_fuera_tema` |
| `consulta_auditoria` | `consulta_auditoria` | `action_call_farmarag` |

## Running the Integration

### 1. Start FarmaRAG (port 8000)

```bash
cd farmarag
python server.py
```

### 2. Start Rasa Action Server (port 5055)

```bash
cd farmarag-rasa
.venv\Scripts\rasa run actions
```

### 3. Start Rasa Shell

```bash
.venv\Scripts\rasa shell
```

## Testing

### Health Check

```bash
Invoke-RestMethod -Uri http://localhost:8000/ -Method GET
```

### Manual Test

```bash
# In rasa shell
Hola
# Expected: greeting response

ayuda
# Expected: help information

# Requires FarmaRAG running:
¿Quais son las normas de PAMI?
# Expected: RAG response from FarmaRAG
```

## Dependencies

- **Rasa Pro**: 3.16.5
- **FarmaRAG**: Running on port 8000
- **Python**: 3.13 (Rasa Pro requires 3.10-3.13)
- **RASA_LICENSE**: Configured in `.env`