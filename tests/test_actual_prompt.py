"""
Test: Verify what prompt is loaded from model
Simpler approach - just check if prompt loads correctly
"""
import os
import sys
import json
import tempfile
from pathlib import Path

for k, v in [
    ('GEMINI_API_KEY', 'AIzaSyCx4H6k2WERyL3-j11udVl6slOjhnIPhaA'),
    ('LLM_API_HEALTH_CHECK', 'true'),
    ('RASALOG', 'DEBUG'),
    ('LOG_LEVEL_LLM_COMMAND_GENERATOR', 'DEBUG'),
    ('PYTHONIOENCODING', 'utf-8'),
]:
    os.environ[k] = v

print("="*70)
print("TEST: Verify prompt loaded from model")
print("="*70)

try:
    import tarfile

    model_path = 'models/20260505-001524-sweet-condenser.tar.gz'

    # Extract model to temp dir
    with tempfile.TemporaryDirectory() as tmpdir:
        print(f"\n[1] Extracting model to temp dir...")
        with tarfile.open(model_path, 'r:gz') as tar:
            tar.extractall(tmpdir)

        tmpdir = Path(tmpdir)

        # Load config
        config_path = tmpdir / 'components' / 'train_CompactLLMCommandGenerator2' / 'config.json'
        with open(config_path, 'r') as f:
            config = json.load(f)
        print(f"Config prompt_template: {config.get('prompt_template')}")

        # Load the actual prompt from model
        prompt_path = tmpdir / 'components' / 'train_CompactLLMCommandGenerator2' / 'command_prompt.jinja2'
        with open(prompt_path, 'r', encoding='utf-8') as f:
            model_prompt = f.read()
        print(f"Model prompt length: {len(model_prompt)} chars")

        # Load the custom template
        custom_path = Path('prompts/custom-command-template.jinja2')
        with open(custom_path, 'r', encoding='utf-8') as f:
            custom_prompt = f.read()
        print(f"Custom prompt length: {len(custom_prompt)} chars")

        print(f"\n[2] Comparison:")
        print(f"  Same content: {model_prompt == custom_prompt}")
        print(f"  Model has extra: {len(model_prompt) - len(custom_prompt)} chars")

        # Test rendering with Jinja2
        print(f"\n[3] Testing Jinja2 rendering...")
        from jinja2 import Template

        template = Template(model_prompt)

        # Simulate inputs
        inputs = {
            'user_message': 'Hola',
            'current_conversation': 'USER: Hola',
            'current_flow': None,
            'current_slot': None,
            'current_slot_description': None,
            'available_flows': 'saludo, ayuda, consulta_auditoria, fuera_tema'
        }

        rendered = template.render(**inputs)
        print(f"Rendered prompt length: {len(rendered)} chars")

        # Write rendered to file
        with open('debug_actual_rendered.txt', 'w', encoding='utf-8') as f:
            f.write(rendered)
        print("Written to debug_actual_rendered.txt")

        # Test with Gemini
        print(f"\n[4] Testing with Gemini...")
        from rasa.shared.providers.llm.default_litellm_llm_client import DefaultLiteLLMClient

        client = DefaultLiteLLMClient.from_config({
            'provider': 'gemini',
            'model': 'gemini-2.5-flash',
            'api_key': os.environ['GEMINI_API_KEY']
        })

        response = client.completion(rendered)

        if hasattr(response, 'choices') and response.choices:
            choice = response.choices[0]
            if isinstance(choice, dict):
                llm_output = choice.get('message', {}).get('content', '')
            else:
                llm_output = str(choice)
            print(f"LLM Output: {repr(llm_output)}")

            # Parse the output
            print(f"\n[5] Parsing LLM output...")
            from rasa.dialogue_understanding.generator.command_parser import parse_commands

            class MockFlowsList:
                def __init__(self, flow_ids):
                    self._flow_ids = flow_ids
                @property
                def user_flow_ids(self):
                    return self._flow_ids

            flows_list = MockFlowsList(['saludo', 'ayuda', 'consulta_auditoria', 'fuera_tema'])
            parsed = parse_commands(llm_output, flows_list)
            print(f"Parsed: {parsed}")

            if parsed:
                print("\n✅ SUCCESS! Command was parsed correctly!")
            else:
                print("\n❌ FAILURE! No commands parsed!")

except Exception as e:
    print(f"ERROR: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*70)
print("TEST COMPLETE")
print("="*70)