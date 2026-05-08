# ================================================
# FarmaRAG + Rasa System - Windows Makefile
# ================================================
# Requiere: farmaRAG/ como directorio hermano de farmarag-rasa/
#
# Uso:
#   make help        - Muestra esta ayuda
#   make start-all   - Levanta todos los servicios
#   make start-farmarag  - Levanta solo FarmaRAG (backend RAG)
#   make start-rasa     - Levanta Rasa server con API y CORS
#   make start-actions  - Levanta Action server
#   make start-history  - Levanta History API
#   make start-frontend - Levanta Frontend Svelte
#   make stop           - Detiene todos los servicios
# ================================================

.PHONY: help start-all start-farmarag start-actions start-rasa start-history start-frontend stop

# Ruta a FarmaRAG (directorio hermano)
FARMA_RAG_DIR = ../farmaRAG

# ---- HELP ----
help:
	@echo FarmaRAG + Rasa System
	@echo =======================
	@echo.
	@echo Servicios y puertos:
	@echo   FarmaRAG  - http://localhost:8000
	@echo   Rasa      - http://localhost:5005
	@echo   Actions   - http://localhost:5055
	@echo   History   - http://localhost:5056
	@echo   Frontend  - http://localhost:5174
	@echo.
	@echo Targets disponibles:
	@echo   make start-all       - Levanta todos los servicios
	@echo   make start-farmarag  - Levanta solo FarmaRAG (port 8000)
	@echo   make start-rasa      - Levanta Rasa server (port 5005)
	@echo   make start-actions   - Levanta Action server (port 5055)
	@echo   make start-history   - Levanta History API (port 5056)
	@echo   make start-frontend  - Levanta Frontend (port 5174)
	@echo   make stop            - Detiene todos los servicios
	@echo.
	@echo REQUISITO: ../farmaRAG debe existir como directorio hermano

# ---- LEVANTAR SERVICIOS ----
start-farmarag:
	@echo [*] Levantando FarmaRAG (port 8000)...
	cd $(FARMA_RAG_DIR) && python server.py

start-actions:
	@echo [*] Levantando Rasa Actions (port 5055)...
	rasa run actions

start-rasa:
	@echo [*] Levantando Rasa Server (port 5005)...
	rasa run --enable-api --cors "*"

start-history:
	@echo [*] Levantando History API (port 5056)...
	cd backend && python history_server.py

start-frontend:
	@echo [*] Levantando Frontend (port 5174)...
	cd frontend && npm run dev

start-all: start-farmarag start-actions start-rasa start-history start-frontend

# ---- DETENER SERVICIOS ----
stop:
	@echo [*] Deteniendo servicios...
	taskkill /F /IM python.exe 2>nul
	taskkill /F /IM node.exe 2>nul
	taskkill /F /IM rasa.exe 2>nul
	@echo [*] Servicios detenidos