FROM python:3.10-slim

WORKDIR /app

# Instalamos dependencias
COPY requirements-test.txt .
RUN pip install --no-cache-dir -r requirements-test.txt && \
    pip install --no-cache-dir flask flask-cors

# Copiamos el código
COPY actions/ ./actions/
COPY backend/ ./backend/

# Variable de entorno para que Python encuentre las acciones
ENV PYTHONPATH="${PYTHONPATH}:/app"

EXPOSE 5055 5056

# COMANDO CORREGIDO: Eliminamos el 'run' innecesario
CMD ["bash", "-c", "python -m rasa_sdk --actions actions --port 5055 & python backend/history_server.py"]