"""
Rasa CALM - Full Prompt Rendering and LLM Test
Simulates exactly what happens during command generation
"""
import os
import sys
import yaml
from pathlib import Path

for k, v in [
    ('GEMINI_API_KEY', 'AIzaSyCx4H6k2WERyL3-j11udVl6slOjhnIPhaA'),
    ('LLM_API_HEALTH_CHECK', 'true'),
    ('RASALOG', 'DEBUG'),
    ('LOG_LEVEL_LLM_COMMAND_GENERATOR', 'DEBUG'),
    ('PYTHONIOENCODING', 'utf-8'),
]:
    os.environ[k] = v

print("=" * 70)
print("FULL PROMPT RENDERING TEST")
print("=" * 70)

# Load the custom prompt template
print("\n[STEP 1] Loading custom prompt template...")
template_path = 'prompts/custom-command-template.jinja2'
with open(template_path, 'r', encoding='utf-8') as f:
    template_content = f.read()
print(f"Template loaded: {len(template_content)} chars")

# Load domain for flows
print("\n[STEP 2] Loading domain for flow information...")
with open('domain.yml', 'r', encoding='utf-8') as f:
    domain = yaml.safe_load(f)
flows_dict = domain.get('flows', {})
print(f"Flows in domain: {list(flows_dict.keys())}")

# Simulate what render_template does
print("\n[STEP 3] Simulating render_template inputs...")

user_message = "Hola"
current_conversation = "\nUSER: Hola"
current_flow = None
current_slot = None
current_slot_description = None
available_flows_str = "saludo, ayuda, consulta_auditoria, fuera_tema"

inputs = {
    "user_message": user_message,
    "current_conversation": current_conversation,
    "current_flow": current_flow,
    "current_slot": current_slot,
    "current_slot_description": current_slot_description,
    "available_flows": available_flows_str,
}

print("Template inputs:")
for k, v in inputs.items():
    print(f"  {k}: {repr(v)}")

# Render the template
print("\n[STEP 4] Rendering template...")
from jinja2 import Template

template = Template(template_content)
rendered_prompt = template.render(**inputs)

# Write to file instead of printing
with open('debug_rendered_prompt.txt', 'w', encoding='utf-8') as f:
    f.write(rendered_prompt)
print(f"Rendered prompt written to debug_rendered_prompt.txt ({len(rendered_prompt)} chars)")

# Send to LLM
print("\n[STEP 5] Sending rendered prompt to Gemini...")
from rasa.shared.providers.llm.default_litellm_llm_client import DefaultLiteLLMClient

client = DefaultLiteLLMClient.from_config({
    'provider': 'gemini',
    'model': 'gemini-2.5-flash',
    'api_key': os.environ['GEMINI_API_KEY']
})

response = client.completion(rendered_prompt)

if hasattr(response, 'choices') and response.choices:
    choice = response.choices[0]
    if isinstance(choice, dict):
        llm_output = choice.get('message', {}).get('content', '')
    else:
        llm_output = str(choice)
else:
    llm_output = str(response)

# Write LLM output to file
with open('debug_llm_output.txt', 'w', encoding='utf-8') as f:
    f.write(llm_output)
print(f"LLM output written to debug_llm_output.txt ({len(llm_output)} chars)")
print(f"LLM output preview: {repr(llm_output[:300])}")

# Parse the LLM output
print("\n[STEP 6] Parsing LLM output...")
from rasa.dialogue_understanding.generator.command_parser import parse_commands

class MockFlowsList:
    def __init__(self, flow_ids):
        self._flow_ids = flow_ids
    @property
    def user_flow_ids(self):
        return self._flow_ids
    def flow_by_id(self, fid):
        return type('F', (), {'id': fid})()

flows_list = MockFlowsList(['saludo', 'ayuda', 'consulta_auditoria', 'fuera_tema'])

parsed = parse_commands(llm_output, flows_list)
print(f"Parsed commands: {parsed}")

if not parsed:
    print("\n[FAILURE] No commands parsed!")
    print("Analyzing why parse_commands failed...")
    
    import re
    
    patterns_to_test = [
        (r'StartFlow\s*\(\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*\)', 'StartFlow pattern'),
        (r'start\s+flow\s*\(\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*\)', 'start flow pattern'),
        (r'([a-zA-Z_][a-zA-Z0-9_]*)', 'Generic flow name'),
    ]
    
    for pattern, desc in patterns_to_test:
        matches = re.findall(pattern, llm_output, re.IGNORECASE)
        print(f"  {desc}: {matches}")
        
    # Check for common issues
    print("\nDiagnostic checks:")
    print(f"  - Output is empty: {not llm_output}")
    print(f"  - Output length: {len(llm_output)}")
    print(f"  - Contains 'StartFlow': {'StartFlow' in llm_output}")
    print(f"  - Contains 'start': {'start' in llm_output.lower()}")
    print(f"  - Contains 'flow': {'flow' in llm_output.lower()}")
else:
    print("\n[SUCCESS] Commands were parsed!")

print("\n" + "=" * 70)
print("TEST COMPLETE")
print("=" * 70)