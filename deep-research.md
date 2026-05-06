# Deep Research: FarmaRAG + Rasa CALM Integration

> **Fecha**: 2026-05-06
> **Proyecto**: FarmaRAG (farmacología auditora RAG chatbot)
> **Directorio**: `C:\Users\Administrador\Herd\farmarag-rasa`

---

## Tabla de Contenidos

1. [Arquitectura del Sistema](#1-arquitectura-del-sistema)
2. [Pipeline NLU de Rasa CALM](#2-pipeline-nlu-de-rasa-calm)
3. [Análisis de Clasificación de Intentos](#3-análisis-de-clasificación-de-intentos)
4. [Flujo de Decisión de Flows](#4-flujo-de-decisión-de-flows)
5. [Investigación de Errores](#5-investigación-de-errores)
6. [Modelo LLM y Proveedores](#6-modelo-llm-y-proveedores)
7. [Fallback y Robustez](#7-fallback-y-robustez)
8. [Configuración de Componentes](#8-configuración-de-componentes)
9. [Plan de Testing](#9-plan-de-testing)
10. [Próximos Pasos](#10-próximos-pasos)

---

## 1. Arquitectura del Sistema

### 1.1 Componentes Principales

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    ARQUITECTURA FARMAUDITOR RAG                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   ┌─────────────┐      ┌──────────────────┐      ┌─────────────────┐  │
│   │   Usuario   │ ───► │  Rasa CALM      │ ───► │   FarmaRAG      │  │
│   │   Input    │      │  (Orchestrator) │      │   Backend       │  │
│   └─────────────┘      └────────┬─────────┘      │   :8000        │  │
│                                 │                └────────┬────────┘  │
│                    ┌────────────┴────────────┐               │         │
│                    │     Action Server      │               │         │
│                    │     :5055             │               ▼         │
│                    │  action_call_farmarag │      ┌─────────────────┐ │
│                    └───────────────────────┘      │   Chroma DB      │ │
│                                                  │   (Vector Store) │ │
│                                                  └─────────────────┘ │
│                                                                     │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 1.2 Puertos y Servicios

| Servicio | Puerto | Descripción |
|----------|--------|-------------|
| Rasa Server | 5005 | REST API + shell interactivo |
| Action Server | 5055 | Webhook para acciones custom |
| FarmaRAG Backend | 8000 | FastAPI + RAG engine |
| Ollama | 11434 | Embeddings (nomic-embed-text) |

### 1.3 Archivos Estructurales

```
farmarag-rasa/
├── actions/
│   └── actions.py          # action_call_farmarag
├── data/
│   ├── nlu.yml            # Training data (intents)
│   └── flows.yml          # Flow definitions
├── models/
│   └── *.tar.gz           # Trained Rasa models
├── config.yml             # Pipeline NLU + policies
├── domain.yml            # Intents, responses, slots, actions
├── endpoints.yml         # Action server + LLM model groups
├── credentials.yml      # REST channel
└── .env                  # Environment variables (API keys)
```

---

## 2. Pipeline NLU de Rasa CALM

### 2.1 Componentes del Pipeline

```yaml
pipeline:
  - name: WhitespaceTokenizer    # Tokeniza input en palabras
  - name: RegexFeaturizer         # Extrae features regex
  - name: KeywordIntentClassifier  # Clasificación por keywords
    case_sensitive: false
  - name: NLUCommandAdapter      # Adapta comandos NLU
    user_input:
      max_characters: 420
  - name: CompactLLMCommandGenerator  # Genera comandos via LLM
    llm:
      model_group: default_llm
    flow_retrieval:
      embeddings:
        model_group: default_embeddings
```

### 2.2 Flujo del Pipeline

```
User Input
    │
    ▼
┌─────────────────────────────────┐
│  WhitespaceTokenizer            │
│  "Que es pami" → [Token]       │
└─────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────┐
│  RegexFeaturizer                 │
│  Convierte tokens a features    │
└─────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────┐
│  KeywordIntentClassifier         │◄── Solo match EXACTO
│  Busca keywords en ejemplos     │
│  Si encuentra → intent con      │
│  confidence alta                │
│  Si NO encuentra → confidence:0 │
└─────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────┐
│  NLUCommandAdapter              │
│  Adapta comandos del NLU         │
└─────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────┐
│  CompactLLMCommandGenerator     │◄── USA LLM (Gemini)
│  Decide qué flow ejecutar       │
│  Basado en semantic search      │
└─────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────┐
│  FlowPolicy                     │
│  Ejecuta el flow decidido       │
└─────────────────────────────────┘
```

### 2.3 KeywordIntentClassifier vs Semantic Search

| Aspecto | KeywordIntentClassifier | CompactLLMCommandGenerator (Semantic) |
|---------|----------------------|----------------------------------------|
| **Método** | Match exacto palabra por palabra | Búsqueda vectorial (embeddings) |
| **Dependencias** | Ninguna | Ollama embeddings API |
| **Velocidad** | Muy rápido | Más lento |
| **Confianza si no match** | 0.0 | Scores 0.63-0.68 |
| **Fallback** | Va a Semantic Search | N/A |

---

## 3. Análisis de Clasificación de Intentos

### 3.1 Los 4 Intents Principales

| Intent | Descripción | Keywords Típicas |
|--------|-------------|------------------|
| `saludo` | Saludar e iniciar conversación | hola, buen, buenos, buenas, qué tal |
| `ayuda` | Explicar capacidades | ayuda, puedo, podes, saber |
| `consulta_auditoria` | Consulta normativa pharmacy | PAMI, DIM, COFAER, OSER, receta, auditoría |
| `fuera_tema` | Off-topic, no dominio pharmacy | hora, clima, chiste, quién, dólar |

### 3.2 Ejemplos por Intent (conteo)

| Intent | Ejemplos Originales | Ejemplos Actualizados |
|--------|-------------------|----------------------|
| `saludo` | 17 | 27 |
| `ayuda` | 16 | 27 |
| `consulta_auditoria` | 36 | 48 |
| `fuera_tema` | 17 | 28 |

### 3.3 Análisis de Cobertura

**Saludo**: ✅ Diverso (formal/informal, voseo/tuteo, regional)
**Ayuda**: ✅ Bueno, incluye variaciones gramaticales
**Consulta_Auditoria**: ✅ Excelente, incluye entidades específicas
**Fuera_Tema**: ⚠️ Falta diversidad en ejemplos comunes (noticias, clima, deportes)

---

## 4. Flujo de Decisión de Flows

### 4.1 Arquitectura de Flows

```yaml
flows:
  saludo:
    description: "Saludar al usuario e iniciar..."
    nlu_trigger:
      - intent:
          name: saludo
          confidence_threshold: 0.5
    steps:
      - action: utter_greeting

  ayuda:
    description: "Explicar capacidades..."
    nlu_trigger:
      - intent:
          name: ayuda
          confidence_threshold: 0.5
    steps:
      - action: utter_help

  fuera_tema:
    description: "Responder cortésmente..."
    nlu_trigger:
      - intent:
          name: fuera_tema
          confidence_threshold: 0.5
    steps:
      - action: utter_fuera_tema

  consulta_auditoria:
    description: "Delegar a FarmaRAG..."
    nlu_trigger:
      - intent:
          name: consulta_auditoria
          confidence_threshold: 0.5
    steps:
      - action: action_call_farmarag
```

### 4.2 Decisión Flow - Ejemplo "Que es pami"

```
Input: "Que es pami"

1. KeywordIntentClassifier
   → "pami" no es keyword exacta en ningún intent
   → Confidence: 0.0
   → Resultado: NO MATCH

2. CompactLLMCommandGenerator (Semantic Search)
   → Query embedding: "Que es pami"
   → Vector search en flows store
   → Resultados:
      - ayuda: 0.62
      - saludo: 0.59
      - fuera_tema: 0.58
      - consulta_auditoria: 0.57

3. LLM decide basándose en el contexto:
   → "Que es pami" → consulta_auditoria (porque menciona PAMI)

4. FlowPolicy ejecuta:
   → action_call_farmarag
   → slots: {audit_question: "Que es pami"}
   → FarmaRAG recibe la query
```

### 4.3 Caso "Hola" - Flujo Exitoso

```
Input: "Hola"

1. KeywordIntentClassifier
   → Encuentra "hola" en ejemplos de saludo
   → Confidence: ALTA
   → Resultado: INTENT = saludo

2. FlowPolicy ejecuta directamente:
   → flow: saludo
   → action: utter_greeting
   → "Buenos días. Soy el asistente de auditoría..."
```

### 4.4 Caso "Que hora es?" - Flujo Exitoso

```
Input: "Que hora es?"

1. KeywordIntentClassifier
   → Encuentra "hora" en ejemplos de fuera_tema
   → Confidence: ALTA
   → Resultado: INTENT = fuera_tema

2. FlowPolicy ejecuta directamente:
   → flow: fuera_tema
   → action: utter_fuera_tema
   → "Mi alcance está limitado a auditoría farmacéutica..."
```

---

## 5. Investigación de Errores

### 5.1 Error: pattern_internal_error

**Síntoma**: El sistema devuelve "Sorry, I am having trouble with that..."

**Causa Raíz**: `CompactLLMCommandGenerator` falla con `litellm.NotFoundError: GeminiException`

**Flujo del Error**:
```
1. KeywordIntentClassifier → NO MATCH (confidence: 0.0)
2. Semantic Search → Encuentra flows (scores 0.63-0.68)
3. CompactLLMCommandGenerator → USA GEMINI para decidir
4. GEMINI FALLA (modelo no disponible o timeout)
5. ErrorCommand → pattern_internal_error
6. utter_internal_error_rasa → "Sorry, I am having trouble..."
```

### 5.2 Error: ProviderClientAPIException

**Mensaje**:
```
ProviderClientAPIException('
Original error: litellm.NotFoundError: GeminiException - )')
```

**Causa**: El modelo `models/gemini-3.1-flash-lite-preview` no está disponible en la API

### 5.3 Modelo Timeout

**Test Directo a la API**:
```powershell
POST https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-lite-preview:generateContent
→ TIMEOUT ❌
```

### 5.4 Modelos Disponibles y su Estado

| Modelo | Status | Notes |
|--------|--------|-------|
| `gemini-2.5-flash` | ✅ Works | 200 OK |
| `gemini-flash-latest` | ✅ Works | Alias funcional |
| `gemini-2.0-flash` | ❌ 429 | Rate limit |
| `gemini-3.1-flash-lite-preview` | ❌ TIMEOUT | No disponible |

### 5.5 Cambio Realizado

**Antes** (endpoints.yml):
```yaml
model: models/gemini-3.1-flash-lite-preview
timeout: 10
```

**Después**:
```yaml
model: models/gemini-2.5-flash
timeout: 15
```

---

## 6. Modelo LLM y Proveedores

### 6.1 Configuración de Model Groups

```yaml
model_groups:
  - id: default_llm
    models:
      - provider: gemini
        model: models/gemini-2.5-flash
        api_key: ${GEMINI_API_KEY}
        timeout: 15

  - id: default_embeddings
    models:
      - provider: ollama
        model: nomic-embed-text:latest
        api_base: http://localhost:11434
        timeout: 10
```

### 6.2 LiteLLM y Provider List

El error muestra:
```
Provider List: https://docs.litellm.ai/docs/providers
```

**LiteLLM** es la biblioteca que usa Rasa para comunicarse con múltiples proveedores LLM (Gemini, OpenAI, Ollama, etc.)

### 6.3 Flujo: LiteLLM → Gemini API

```
Rasa → LiteLLM → Gemini API → Response
           │
           └── Wrapper unificado para múltiples providers
```

### 6.4 API Key y Authentication

```bash
GEMINI_API_KEY=AIzaSyCx4H6k2WERyL3-j11udVl6slOjhnIPhaA
```

La API key está configurada en `.env` y se pasa como variable de entorno.

---

## 7. Fallback y Robustez

### 7.1 Arquitectura de Fallback Actual

```
Input
  │
  ▼
┌─────────────────────────┐
│ KeywordIntentClassifier │
│ (Match exacto)           │
└───────────┬─────────────┘
            │ No match
            ▼
┌─────────────────────────┐
│ Semantic Search          │
│ (Embeddings vectoriales) │
└───────────┬─────────────┘
            │ LLM decide
            ▼
┌─────────────────────────┐
│ CompactLLMCommandGenerator │ ← DEPENDE DE GEMINI
└───────────┬─────────────┘
            │ Falla
            ▼
┌─────────────────────────┐
│ pattern_internal_error   │ ← NO HAY FALLBACK
└─────────────────────────┘
```

### 7.2 El Problema: Sin Fallback a Semantic Scores

Cuando el LLM falla, el sistema debería:
1. Tomar los flows encontrados por semantic search
2. Usar el flow con mayor score directamente
3. O ejecutar `utter_fuera_tema` como respuesta segura

**Actualmente**: No hace esto → activa `pattern_internal_error`

### 7.3 Próxima Iteración: Implementar Fallback

```
Input
  │
  ▼
┌─────────────────────────┐
│ KeywordIntentClassifier │
└───────────┬─────────────┘
            │ No match
            ▼
┌─────────────────────────┐
│ Semantic Search          │
│ (Embeddings)             │
└───────────┬─────────────┘
            │
            ▼
    ┌───────────────┐
    │ LLM decide     │ ← CompactLLMCommandGenerator
    └───────┬────────┘
            │ Falla
            ▼
┌─────────────────────────────────┐
│ FALLBACK: Usar semantic scores  │
│ - Si ayuda > 0.6 → ayuda       │
│ - Si fuera_tema > 0.6 → fuera  │
│ - Si no → utter_fuera_tema      │
└─────────────────────────────────┘
```

---

## 8. Configuración de Componentes

### 8.1 Domain.yml - Estructura

```yaml
version: "3.1"

intents:
  - saludo
  - ayuda
  - consulta_auditoria
  - fuera_tema

responses:
  utter_greeting:        # respuestas para saludo
  utter_help:            # respuestas para ayuda
  utter_fuera_tema:      # respuestas para fuera_tema
  utter_consulta_auditoria_error  # error handling
  utter_backend_unavailable       # FarmaRAG down
  utter_timeout:                  # timeout

slots:
  audit_question:        # query del usuario
  farmarag_response:     # respuesta de RAG
  provider_used:        # ollama/gemini
  fallback_triggered:    # boolean
  correlation_id:       # tracking
  last_error_code:       # código de error

actions:
  - action_call_farmarag
```

### 8.2 Slots y su Propósito

| Slot | Tipo | Uso |
|------|------|-----|
| `audit_question` | text | Almacena la pregunta del usuario |
| `farmarag_response` | text | Almacena respuesta de FarmaRAG |
| `provider_used` | text | Ollama o Gemini |
| `fallback_triggered` | bool | Si hubo fallback |
| `correlation_id` | text | UUID para tracking |
| `last_error_code` | text | Código de error si falla |

### 8.3 Action: action_call_farmarag

**Responsabilidades**:
1. Recibir el mensaje del usuario
2. POST a `http://127.0.0.1:8000/ask`
3. Retry con exponential backoff (3 intentos)
4. Manejar timeouts, connection errors
5. Almacenar respuesta en slots
6. Devolver respuesta al usuario

**Errores Manejados**:
- `requests.exceptions.Timeout`
- `requests.exceptions.ConnectionError`
- HTTP 429 (rate limit)
- HTTP 500/502/503/504 (server errors)
- JSON inválido
- Respuesta vacía

---

## 9. Plan de Testing

### 9.1 Tests Manuales - Validación de Flows

| # | Input | Flow Esperado | Respuesta Esperada |
|---|-------|--------------|-------------------|
| 1 | `Hola` | saludo | utter_greeting |
| 2 | `Buen día` | saludo | utter_greeting |
| 3 | `Qué puedes hacer?` | ayuda | utter_help |
| 4 | `Necesito ayuda` | ayuda | utter_help |
| 5 | `Cuáles son los requisitos de PAMI?` | consulta_auditoria | FarmaRAG response |
| 6 | `Qué dice COFAER?` | consulta_auditoria | FarmaRAG response |
| 7 | `Qué hora es?` | fuera_tema | utter_fuera_tema |
| 8 | `Cuéntame un chiste` | fuera_tema | utter_fuera_tema |
| 9 | `Cuánto mide el Everest?` | fuera_tema | utter_fuera_tema (sin error) |
| 10 | `Tu nariz contra mis bolas` | fuera_tema | utter_fuera_tema (sin error) |

### 9.2 Tests de Integración

**Test FarmaRAG Backend**:
```powershell
# Health check
Invoke-WebRequest http://localhost:8000/health

# Query test
Invoke-WebRequest http://localhost:8000/ask -Method POST -Body (@{question="Qué es PAMI"} | ConvertTo-Json)
```

**Test Rasa REST API**:
```powershell
# Test saludo
Invoke-WebRequest http://localhost:5005/webhooks/rest/webhook -Method POST -Body (@{sender="test"; message="Hola"} | ConvertTo-Json)

# Test consulta_auditoria
Invoke-WebRequest http://localhost:5005/webhooks/rest/webhook -Method POST -Body (@{sender="test"; message="Cuáles son losrequisitos de PAMI?"} | ConvertTo-Json)
```

### 9.3 Tests de Error - Escenarios

| Escenario | Condición | Respuesta Esperada |
|-----------|-----------|---------------------|
| FarmaRAG down | `localhost:8000` no responde | `utter_backend_unavailable` |
| Timeout | FarmaRAG tarda > 25s | `utter_timeout` |
| Rate limit | HTTP 429 | "Límite temporal de consultas" |
| Invalid JSON | Response no es JSON | `utter_consulta_auditoria_error` |

---

## 10. Próximos Pasos

### 10.1 Iteración Actual (Completada)

- [x] Cambio de modelo `gemini-3.1-flash-lite-preview` → `gemini-2.5-flash`
- [x] Reentrenamiento del modelo
- [x] Documentación de investigación

### 10.2 Verificación Post-Cambio

**Para el usuario**:
1. Asegurarse que FarmaRAG está corriendo en `:8000`
2. Asegurarse que Action Server está corriendo en `:5055`
3. Reiniciar Rasa server
4. Probar los 10 flujos de la tabla 9.1

**Para verificar**:
```bash
# Terminal 1: FarmaRAG
python server.py

# Terminal 2: Action Server
rasa run actions

# Terminal 3: Rasa Server
rasa run --enable-api --cors "*"

# Terminal 4: Shell interactivo
rasa shell
```

### 10.3 Próxima Iteración (Planificada)

**Fallback Semántico**:
- Investigar por qué semantic search no se usa como fallback
- Implementar lógica de fallback basada en scores
- Agregar threshold configurable

**Edge Cases**:
- Inputs muy largos (> 420 chars)
- Inputs con caracteres especiales
- Inputs en otros idiomas
- Inputs con emojis

**Testing**:
- Suite de tests automáticos (pytest)
- Tests de integración Rasa ↔ FarmaRAG
- Tests de stress con rate limiting

### 10.4 Mejoras Futuras

1. **Modelo de Embeddings**: Cambiar de Ollama a Gemini Embeddings para consistencia
2. **NLG Endpoint**: Configurar endpoint de NLG para rephrasing
3. **Multi-tenant**: Soporte para múltiples farmacias
4. **Logging**: Integración con sistema de logging centralizado
5. **Monitoring**: Métricas Prometheus/ Grafana

---

## Anexo: Comandos Útiles

### Entrenamiento
```bash
rasa train
```

### Validación de Configuración
```bash
rasa data validate
```

### Iniciar Servicios
```bash
# FarmaRAG (desde farmarag/)
python server.py

# Action Server
rasa run actions

# Rasa Server
rasa run --enable-api --cors "*"

# Shell interactivo
rasa shell
```

### Testing via REST
```bash
# Webhook test
curl -X POST http://localhost:5005/webhooks/rest/webhook \
  -H "Content-Type: application/json" \
  -d '{"sender": "test", "message": "Hola"}'
```

### Debug Mode
```bash
rasa shell --debug
```

---

*Documento generado: 2026-05-06*
*Proyecto: FarmaRAG + Rasa CALM Integration*
