import pytest


def test_rasa_installed():
    import rasa
    assert rasa.__version__ is not None


def test_llm_configured():
    import yaml
    with open("config.yml", "r") as f:
        config = yaml.safe_load(f)
    llm_component = next(
        (c for c in config["pipeline"] if c.get("name") == "CompactLLMCommandGenerator"),
        None
    )
    assert llm_component is not None
    assert llm_component["llm"]["model_group"] == "gemini_llm"
    assert "flow_retrieval" in llm_component
    assert llm_component["flow_retrieval"]["active"] is False
    assert llm_component.get("prompt_template") == "prompts/custom-command-template.jinja2"

    import yaml
    with open("endpoints.yml", "r") as f:
        endpoints = yaml.safe_load(f)
    model_groups = {mg["id"] for mg in endpoints.get("model_groups", [])}
    assert "gemini_llm" in model_groups


def test_farmarag_agent_configured():
    import yaml
    with open("credentials.yml", "r") as f:
        creds = yaml.safe_load(f)
    assert creds["farmarag_agent"]["url"] == "http://localhost:8000"


def test_domain_flows():
    import yaml
    with open("domain.yml", "r") as f:
        domain = yaml.safe_load(f)
    assert "saludo" in domain["flows"]
    assert "ayuda" in domain["flows"]
    assert "consulta_auditoria" in domain["flows"]
    assert "fuera_tema" in domain["flows"]


def test_nlu_intents():
    import yaml
    with open("data/nlu.yml", "r") as f:
        nlu = yaml.safe_load(f)
    intents = [item["intent"] for item in nlu["nlu"]]
    assert "saludo" in intents
    assert "ayuda" in intents
    assert "consulta_auditoria" in intents
    assert "fuera_tema" in intents