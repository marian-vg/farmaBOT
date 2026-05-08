# ================================================
# FarmaRAG + Rasa System - Script de Servicios
# ================================================
# Requiere: farmaRAG/ como directorio hermano
#
# Uso:
#   .\run_services.ps1 start-all   - Levanta todos los servicios
#   .\run_services.ps1 stop        - Detiene todos los servicios
#   .\run_services.ps1 status      - Muestra estado de servicios
#   .\run_services.ps1 help       - Muestra esta ayuda
# ================================================

param([string]$Action = "help")

$FARMA_RAG_DIR = "..\farmaRAG"

# ---- HELP ----
function Show-Help {
    Write-Host "FarmaRAG + Rasa System"
    Write-Host "===================="
    Write-Host ""
    Write-Host "Servicios y puertos:"
    Write-Host "  FarmaRAG  - http://localhost:8000"
    Write-Host "  Rasa      - http://localhost:5005"
    Write-Host "  Actions   - http://localhost:5055"
    Write-Host "  History   - http://localhost:5056"
    Write-Host "  Frontend  - http://localhost:5174"
    Write-Host ""
    Write-Host "Comandos disponibles:"
    Write-Host "  .\run_services.ps1 start-all   - Levanta todos los servicios"
    Write-Host "  .\run_services.ps1 stop        - Detiene todos los servicios"
    Write-Host "  .\run_services.ps1 status      - Muestra estado de servicios"
    Write-Host "  .\run_services.ps1 help        - Muestra esta ayuda"
    Write-Host ""
    Write-Host "REQUISITO: ..\farmaRAG debe existir como directorio hermano"
}

# ---- START ALL ----
function Start-All {
    Write-Host "[*] Levantando todos los servicios..."

    # FarmaRAG (backend RAG)
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$FARMA_RAG_DIR'; python server.py" -WindowStyle Hidden

    # Rasa Actions
    Start-Process powershell -ArgumentList "-NoExit", "-Command", ".venv\Scripts\rasa run actions" -WindowStyle Hidden

    # Rasa Server
    Start-Process powershell -ArgumentList "-NoExit", "-Command", ".venv\Scripts\rasa run --enable-api --cors '*'" -WindowStyle Hidden

    # History API
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'backend'; python history_server.py" -WindowStyle Hidden

    # Frontend
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'frontend'; npm run dev" -WindowStyle Hidden

    Write-Host "[*] Todos los servicios iniciados en background"
    Write-Host "[*] Verificar estado con: .\run_services.ps1 status"
}

# ---- STOP ----
function Stop-All {
    Write-Host "[*] Deteniendo servicios..."

    Stop-Process -Name python -Force -ErrorAction SilentlyContinue
    Stop-Process -Name node -Force -ErrorAction SilentlyContinue
    Stop-Process -Name rasa -Force -ErrorAction SilentlyContinue

    Write-Host "[*] Servicios detenidos"
}

# ---- STATUS ----
function Status {
    Write-Host "[*] Estado de servicios:"
    Write-Host ""

    $ports = @{
        "8000" = "FarmaRAG"
        "5005" = "Rasa"
        "5055" = "Actions"
        "5056" = "History"
        "5174" = "Frontend"
    }

    $active = 0
    $stopped = 0

    foreach ($port in $ports.Keys) {
        $connection = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue | Where-Object { $_.State -eq "Listen" }
        if ($connection) {
            Write-Host "  [$port] $($ports[$port]) - ACTIVO" -ForegroundColor Green
            $active++
        } else {
            Write-Host "  [$port] $($ports[$port]) - DETENIDO" -ForegroundColor Red
            $stopped++
        }
    }

    Write-Host ""
    Write-Host "Resumen: $active activos, $stopped detenidos"
}

# ---- DISPATCH ----
switch ($Action) {
    "start-all" { Start-All }
    "stop" { Stop-All }
    "status" { Status }
    "help" { Show-Help }
    default {
        Write-Host "Comando no reconocido: $Action"
        Write-Host "Ejecuta .\run_services.ps1 help para ver los comandos disponibles"
    }
}