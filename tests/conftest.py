"""Pytest configuration and fixtures for farmarag-rasa tests."""
import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

RASA_LICENSE = os.getenv(
    "RASA_LICENSE",
    "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiJiOTZiNjYyYS0xMDFiLTRjNjktODM0My1lNmZiNWIwNDkwZWQiLCJpYXQiOjE3Nzc4MDc5NTksIm5iZiI6MTc3NzgwNzk1NSwic2NvcGUiOiJyYXNhOnBybyByYXNhOnBybzpjaGFtcGlvbiByYXNhOnZvaWNlIiwiZXhwIjoxODcyNTAyMzU1LCJlbWFpbCI6ImNhbWlub3NtYXJpYW5vMUBnbWFpbC5jb20iLCJjb21wYW55IjoiUmFzYSBDaGFtcGlvbnMifQ.OrF269VycVAxTzLp_8A79lDHWzlvnie2I8frkig9jVs4qiBk45QbAs-DZkRg5hEkh-8GJsbmRcKkJLZsp6sLoqum9FWV1REQgg3XFnkO5lJIUv0syHUUgEJERiPzZtlUGF3gEaZJ7pLkAFz4HCuHGF3KyVyLUhG8Ph1_duzNDv8nh4TBLg2iuUGTNx87darQXv2tJ7N24_y_RMoytqqfwocx_YqDc0-CCcQg2Vgh2g3Z1gZTSYcCGRdAg6wHfX2JnDPewpmG_4xej9FKUpcLWMjERE6otDfdoRuUxo2ZcdV4eBEuXYjbUxYWb0XncRxBktVpaL4EcRJBDQeQJI6STg"
)
GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY",
    "AIzaSyCx4H6k2WERyL3-j11udVl6slOjhnIPhaA"
)


@pytest.fixture(scope="session")
def rasa_env():
    """Set up Rasa environment variables for all tests."""
    original_license = os.getenv("RASA_LICENSE")
    original_gemini = os.getenv("GEMINI_API_KEY")

    os.environ["RASA_LICENSE"] = RASA_LICENSE
    os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY
    os.environ["LLM_API_HEALTH_CHECK"] = "false"
    os.environ["EMBEDDINGS_API_HEALTH_CHECK"] = "false"

    yield {
        "RASA_LICENSE": RASA_LICENSE,
        "GEMINI_API_KEY": GEMINI_API_KEY,
    }

    if original_license is not None:
        os.environ["RASA_LICENSE"] = original_license
    if original_gemini is not None:
        os.environ["GEMINI_API_KEY"] = original_gemini


@pytest.fixture(scope="session")
def farmarag_url():
    """Return the FarmaRAG backend URL."""
    return "http://127.0.0.1:8000"


@pytest.fixture(scope="session")
def farmarag_health_url():
    """Return the FarmaRAG health check URL."""
    return "http://127.0.0.1:8000/health"


TEST_MESSAGES = {
    "saludo": [
        "Hola",
        "Buen día",
        "Buenos días",
        "Buenas tardes",
    ],
    "ayuda": [
        "Qué puedes hacer?",
        "Necesito ayuda",
        "Cómo me puedes ayudar?",
    ],
    "consulta_auditoria": [
        "Cuáles son los requisitos de PAMI para una receta",
        "Qué dice COFAER sobre validación de recetas",
        "Necesito saber los requisitos de auditoría",
    ],
    "fuera_tema": [
        "Qué hora es?",
        "Cuánto mide el monte Everest?",
        "Quién descubrió América?",
        "Cuéntame un chiste",
    ],
}

EXPECTED_RESPONSES = {
    "saludo": ["Buenos días", "Hola", "asistente", "auditoría"],
    "ayuda": ["Puedo ayudarle", "consultas", "auditoría", "PAMI", "DIM", "COFAER"],
    "consulta_auditoria": [],  # Depends on FarmaRAG response
    "fuera_tema": ["alcance", "limitado", "auditoría farmacéutica", "PAMI", "DIM", "COFAER", "OSER"],
}