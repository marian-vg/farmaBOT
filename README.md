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
                                 │
                                 ▼
                        ┌─────────────────┐
                        │  History API    │
                        │  (:5056)        │
                        └─────────────────┘
```

| Servicio | Puerto | Descripción |
|----------|--------|-------------|
| Frontend | `5174` | Interfaz web del chatbot (Svelte 5) |
| Rasa server | `5005` | Orquestador CALM + API REST |
| Action server | `5055` | Ejecuta `action_call_farmarag` |
| FarmaRAG | `8000` | Backend RAG (FastAPI + Chroma + LLM) |
| History API | `5056` | SQLite para guardar/cargar conversaciones |

## Requisitos

- Python 3.10+
- Node.js 20+
- Rasa Pro license (`RASA_LICENSE`)
- API key de Gemini (`GEMINI_API_KEY`) — o modelo Ollama local
- Clonar el repositorio del RAG ("git clone https://github.com/marian-vg/RAG-project.git")

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

## Levantar el sistema (manual)

Se necesitan **5 servicios** corriendo simultáneamente:

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
rasa run --enable-api --cors "*"
```

### Terminal 4 — History API

```bash
cd backend
python history_server.py
```

### Terminal 5 — Frontend

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
rasa run --enable-api --cors "*"
```

### Rasa no responde

1. Verificar que el action server esté corriendo en `:5055`
2. Verificar que el modelo esté entrenado: `rasa train`
3. Revisar logs en `rasa_err.log`

## Docker

Es posible levantar todo el sistema con Docker Compose. Esto levanta **5 servicios** automáticamente:

- **Frontend** (Svelte)
- **Rasa Server** (con entrenamiento automático del modelo)
- **Action Server** (Rasa actions + History API)
- **FarmaRAG** (Backend RAG)
- **History API** (SQLite para conversaciones)

### Requisitos

- Docker Engine 20.10+
- Docker Compose 2.0+
- Credenciales (RASA_LICENSE, GEMINI_API_KEY, GOOGLE_API_KEY)

### Configuración

1. Crear archivo `.env` en la raíz del proyecto:

```bash
cp .env.example .env
```

2. Editar `.env` con las credenciales:
- `RASA_LICENSE`: Licencia de Rasa Pro
- `GEMINI_API_KEY`: API key de Google Gemini
- `GOOGLE_API_KEY`: API key de Google (para FarmaRAG)

### Sobre las credenciales

Solo se necesita un archivo `.env` en la raíz de `farmarag-rasa/`.

Docker Compose lee las variables del `.env` y las pasa automáticamente a cada servicio que las necesite:

| Variable | Consumida por |
|----------|---------------|
| `RASA_LICENSE` | Rasa, Actions, FarmaRAG |
| `GEMINI_API_KEY` | Rasa (orchestrator) |
| `GOOGLE_API_KEY` | FarmaRAG (RAG + Chroma) |

**Si usás la misma API key para ambos servicios**, simplemente poné el mismo valor en `GEMINI_API_KEY` y `GOOGLE_API_KEY`. No es necesario que sean keys separadas.

### Levantar el sistema

```bash
docker compose up --build
```

**Primera vez:** El servicio `rasa` ejecutará `rasa train` automáticamente.

**Veces siguientes:** El modelo persistido en el volumen `rasa_models` se reutiliza — el entrenamiento se omite.

### Acceder al chatbot

Una vez todos los servicios estén levantados:

| Servicio | URL |
|----------|-----|
| Chatbot | http://localhost:5174 |
| Rasa API | http://localhost:5005 |
| History API | http://localhost:5056/api |

### Detener el sistema

```bash
docker compose down
```

Para eliminar también los volúmenes (incluyendo el modelo entrenado):

```bash
docker compose down -v
```

### Estructura del proyecto

```
farmarag-rasa/
├── frontend/                 # Chatbot frontend (Svelte 5)
│   ├── src/
│   │   ├── App.svelte
│   │   ├── components/       # ChatWindow, NavigationSidebar, etc.
│   │   └── lib/             # rasaClient, historyClient, types
│   └── Dockerfile
├── actions/
│   ├── actions.py            # ActionCallFarmaRAG
│   ├── Dockerfile            # Actions + History API
│   └── backend/             # History API (Flask + SQLite)
│       ├── history_server.py
│       └── history.db
├── data/
│   └── nlu.yml              # Training data (intents en español)
├── models/                   # Modelo entrenado de Rasa
├── config.yml               # Pipeline CALM + NLU
├── domain.yml               # Intents, responses, slots, flows
├── endpoints.yml            # Action server + LLM config
├── credentials.yml           # REST channel
├── docker-compose.yml        # Docker Compose principal
├── .env.example             # Template de variables
└── README.md
```

## Configuración de modelos

El orchestrator usa modelos Gemini configurados en `endpoints.yml`:

- **Command generator**: `gemini-2.5-flash-preview`
- **Flow retrieval embeddings**: `gemini-embedding-001`

Para usar Ollama local, modificar `src/auditor.py` en FarmaRAG y configurar el provider correspondiente.
