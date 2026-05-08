FROM python:3.11-slim

WORKDIR /app

COPY backend/requirements-history.txt /app/requirements-history.txt

RUN pip install --no-cache-dir -r /app/requirements-history.txt

COPY backend/ /app/backend/

WORKDIR /app/backend

EXPOSE 5056

CMD ["python", "history_server.py"]
