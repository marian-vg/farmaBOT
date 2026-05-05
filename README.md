# FarmaRAG Rasa Orchestrator

Minimal Rasa CALM assistant in Spanish that routes pharmacy-auditing queries to the existing FarmaRAG FastAPI backend.

## Architecture

- Rasa server: `http://localhost:5005`
- Rasa action server: `http://localhost:5055`
- FarmaRAG backend: `http://localhost:8000`

## Required Environment

Before training or running the assistant, set:

- `RASA_LICENSE`: required by the installed Rasa Pro build

## Files

- `config.yml` - CALM + NLU pipeline
- `domain.yml` - responses, slots, actions
- `flows.yml` - flow definitions and NLU triggers
- `data/nlu.yml` - Spanish intent examples
- `actions/actions.py` - FarmaRAG integration
- `credentials.yml` - REST channel
- `endpoints.yml` - action server and LLM model group

## Run Sequence

1. Start FarmaRAG on port `8000`.
2. Export `RASA_LICENSE` and make sure `GEMINI_API_KEY` is available (for example through `.env`).
3. Train: `rasa train`
4. Start action server: `rasa run actions`
5. Start Rasa: `rasa run --enable-api --cors "*" --inspect`

The current configuration uses Gemini models already aligned with the FarmaRAG backend:

- command generator: `models/gemini-3.1-flash-lite-preview`
- flow retrieval embeddings: `models/gemini-embedding-001`

## Current Status

The project scaffold is in place, but runtime validation is blocked until:

1. `RASA_LICENSE` is available.
2. FarmaRAG is running locally.

## Validation Completed

- YAML syntax for all assistant files is valid.
- The custom action module imports successfully in the current virtual environment.

## Critical Runtime Blocker

Running `rasa train` currently stops immediately with:

```text
license.not_found.error
A Rasa license is required. Please set the environment variable `RASA_LICENSE` to a valid license string.
```
