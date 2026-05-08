FROM rasa/rasa-sdk:3.16.0

WORKDIR /app

USER root

COPY actions/requirements-actions.txt /app/requirements-actions.txt

RUN pip install --no-cache-dir -r /app/requirements-actions.txt

COPY actions/ ./actions/

USER 1001

EXPOSE 5055

CMD ["start", "--actions", "actions", "--port", "5055"]
