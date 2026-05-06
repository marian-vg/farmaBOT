# Farmarag-Rasa Chatbot

Chatbot de auditoría farmacéutica construido con Rasa CALM que orquestra consultas hacia el backend FarmaRAG.

## Arquitectura

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Frontend       │     │  Rasa Server    │     │  FarmaRAG       │
│  (Svelte :5174) │────▶│  (CALM :5005)  │────▶│  (RAG :8000)    │
└─────────────────┘     └────────┬────────┘     └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │  Action Server  │
                       │  (:5055)        │
                       └─────────────────┘
```

| Servicio | Puerto | Descripción |
|----------|--------|-------------|
| Frontend | `5174` | Interfaz web del chatbot (Svelte 5) |
| Rasa server | `5005` | Orquestador CALM + API REST |
| Action server | `5055` | Ejecuta `action_call_farmarag` |
| FarmaRAG | `8000` | Backend RAG (FastAPI + Chroma + LLM) |

## Requisitos

- Python 3.10+
- Node.js 20+
- Rasa Pro license (`RASA_LICENSE`)
- API key de Gemini (`GEMINI_API_KEY`) — o modelo Ollama local

## Instalación

### 1. Entorno Python

```bash
# Crear y activar entorno virtual
python -m venv .venv
.\.venv\Scripts\activate      # Windows
# source .venv/bin/activate   # Linux/macOS

# Instalar dependencias
pip install -r requirements.txt
pip install -r requirements-test.txt
```

### 2. Entorno Frontend

```bash
cd frontend
npm install
cd ..
```

### 3. Variables de entorno

Crear archivo `.env` o exportar las siguientes variables:

```bash
export RASA_LICENSE="tu-licencia-aqui"
export GEMINI_API_KEY="tu-api-key-aqui"
```

## Levantar el sistema

Se necesitan **4 servicios** corriendo simultáneamente:

### Terminal 1 — FarmaRAG (backend RAG)

```bash
cd ../farmaRAG
python server.py
```

### Terminal 2 — Rasa Action Server

```bash
rasa run actions
```

### Terminal 3 — Rasa Server

```bash
rasa run --enable-api --cors "*" --inspect
```

### Terminal 4 — Frontend

```bash
cd frontend
npm run dev
```

Una vez iniciado, acceder al chatbot en: **http://localhost:5174**

## Uso del Chatbot

El chatbot responde consultas sobre normativas farmacéuticas:

- **PAMI** — Coberturas, medicamentos esenciales, recetas
- **DIM** — Requisitos de documentación y habilitación
- **COFAER** — Normativas del Consejo Profesional de Farmacéuticos
- **OSER** — Criterios de la obra social
- **Trazabilidad** — Sistema de trazabilidad de medicamentos
- **Cadena de frío** — Control de temperatura en almacenamiento

### Ejemplos de consulta

- "¿Cuáles son los requisitos para la cobertura de medicamentos de PAMI?"
- "¿Qué documentación necesito para gestionar una receta DEX?"
- "¿Cómo funciona el sistema de trazabilidad para medicamentos oncológicos?"

## Estructura del proyecto

```
farmarag-rasa/
├── frontend/                 # Chatbot frontend (Svelte 5)
│   ├── src/
│   │   ├── App.svelte
│   │   ├── components/       # PresentationPanel, ChatWindow, etc.
│   │   └── lib/             # rasaClient, toast, types
│   └── package.json
├── actions/
│   └── actions.py            # ActionCallFarmaRAG
├── data/
│   └── nlu.yml              # Training data (intents en español)
├── models/                   # Modelo entrenado de Rasa
├── config.yml               # Pipeline CALM + NLU
├── domain.yml               # Intents, responses, slots, flows
├── endpoints.yml            # Action server + LLM config
├── credentials.yml           # REST channel
└── README.md                 # Este archivo
```

## Solución de problemas

### Error CORS en el frontend

Si el navegador bloquea requests, verificar que Rasa se ejecutó con `--cors "*"`:

```bash
rasa run --enable-api --cors "*" --inspect
```

### Error 500 al enviar mensaje

1. Verificar que FarmaRAG esté corriendo en `:8000`
2. Revisar logs de errores en `farmaRAG/logs/failed_queries.jsonl`
3. Verificar que `GEMINI_API_KEY` esté configurada correctamente

### Rasa no responde

1. Verificar que el action server esté corriendo en `:5055`
2. Verificar que el modelo esté entrenado: `rasa train`
3. Revisar logs en `rasa_err.log`

## Docker (Próximamente)

El soporte para Docker está en desarrollo. Una vez implementado, será posible levantar todo el sistema con un solo comando:

```bash
docker compose up
```

Próximamente se agregará el archivo `docker-compose.yml` con todos los servicios configurados.

## Configuración de modelos

El orchestrator usa modelos Gemini configurados en `endpoints.yml`:

- **Command generator**: `gemini-3.1-flash-lite-preview`
- **Flow retrieval embeddings**: `gemini-embedding-001`

Para usar Ollama local, modificar `src/auditor.py` en FarmaRAG y configurar el provider correspondiente.
