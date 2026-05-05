# Implementation Checklist

## Phase 0 - Preparation
- [x] Confirmed `farmarag-rasa` is a clean workspace.
- [x] Confirmed the current Rasa install requires `RASA_LICENSE`.
- [x] Confirmed FarmaRAG health is currently unavailable locally.

## Phase 1 - Minimal Rasa Foundation
- [x] Create `config.yml` with CALM + NLU pipeline.
- [x] Create `domain.yml` with slots, responses, and actions.
- [x] Create `flows.yml` with four initial flows.
- [x] Create `credentials.yml` for REST channel.
- [x] Create `endpoints.yml` for action server and LLM model group.

## Phase 2 - Domain and NLU
- [x] Add Spanish NLU examples for `saludo`, `ayuda`, `consulta_auditoria`, and `fuera_tema`.
- [x] Keep the first domain intentionally small and deterministic.

## Phase 3 - FarmaRAG Integration
- [x] Add standalone action server entrypoint in `actions/actions.py`.
- [x] Implement request timeout and HTTP error handling.
- [x] Store FarmaRAG metadata in slots for future frontend/debug use.

## Phase 4 - Validation
- [x] Validate YAML syntax for all configuration files.
- [x] Import the custom action module successfully.
- [ ] Run `rasa train` successfully.
- [ ] Run `rasa inspect` / REST checks successfully.
- [ ] Validate end-to-end call into FarmaRAG.

## Current Critical Blockers
- [ ] Provide `RASA_LICENSE` in the shell environment so Rasa Pro can train/run. Current error: `license.not_found.error`.
- [ ] Start FarmaRAG on `http://localhost:8000` so the custom action can be exercised.

## After Blockers Are Cleared
- [ ] Train the assistant.
- [ ] Validate each flow in Inspector.
- [ ] Validate REST webhook behavior.
- [ ] Refine NLU examples using misclassifications from manual tests.
