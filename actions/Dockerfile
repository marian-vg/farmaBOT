FROM python:3.11-slim

WORKDIR /app

COPY requirements-test.txt .

RUN pip install --no-cache-dir -r requirements-test.txt

RUN pip install --no-cache-dir flask flask-cors

COPY actions/ ./actions/

COPY backend/ ./backend/

EXPOSE 5055 5056

CMD ["bash", "-c", "rasa run actions & python backend/history_server.py"]
