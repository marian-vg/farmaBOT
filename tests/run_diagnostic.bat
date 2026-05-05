@echo off
REM Rasa CALM Diagnostic - Run with debug logging
set GEMINI_API_KEY=AIzaSyCx4H6k2WERyL3-j11udVl6slOjhnIPhaA
set LLM_API_HEALTH_CHECK=true
set RASALOG=DEBUG
set LOG_LEVEL_LLM_COMMAND_GENERATOR=DEBUG
set PYTHONIOENCODING=utf-8

echo Starting rasa shell with debug logging...
echo Watch for lines containing: prompt_rendered, predict_commands, parse_commands
echo.

.venv\Scripts\python.exe -m rasa shell --model models/20260505-001524-sweet-condenser.tar.gz --port 5005 2>&1 | findstr /I "prompt_rendered predict_commands parse_commands StartFlow command DEBUG ERROR"