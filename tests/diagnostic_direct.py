"""
Rasa CALM Command Generator Diagnostic - Direct Test
Tests LLM prompt and parse_commands without full agent initialization
"""
import os
import sys
import yaml

for k, v in [
    ('GEMINI_API_KEY', 'AIzaSyCx4H6k2WERyL3-j11udVl6slOjhnIPhaA'),
    ('LLM_API_HEALTH_CHECK', 'true'),
    ('RASALOG', 'DEBUG'),
    ('LOG_LEVEL_LLM_COMMAND_GENERATOR', 'DEBUG'),
    ('PYTHONIOENCODING', 'utf-8'),
]:
    os.environ[k] = v

print("=" * 70)
print("DIAGNOSTIC: LLM Prompt vs Parser Compatibility Test")
print("=" * 70)

# Load custom prompt from model
print("\n[STEP 1] Loading custom prompt from model...")
with open('debug_prompt_from_model.txt', 'r', encoding='utf-8') as f:
    custom_prompt = f.read()

print(f"Custom prompt ({len(custom_prompt)} chars):")
print("-" * 70)
print(custom_prompt[:1000])
print("...")
print("-" * 70)

# Extract the expected command format from prompt
print("\n[STEP 2] Extracting command format from prompt...")
import re

# Find the flow name examples in the prompt
flow_names_in_prompt = re.findall(r'Valid flow names:\s*([^.\n]+)', custom_prompt)
print(f"Flow names in prompt: {flow_names_in_prompt}")

# Find examples of commands
examples = re.findall(r'(?:->|=>)\s*`(.*?)`', custom_prompt)
print(f"Example commands in prompt: {examples}")

# Check what format the prompt instructs
instruction_patterns = [
    (r'output.*?commands?.*?format', 'has format instruction'),
    (r'StartFlow\s*\(', 'uses StartFlow'),
    (r'start\s*flow', 'uses "start flow"'),
    (r'startflow', 'uses "startflow"'),
]
print("\nPrompt contains:")
for pattern, desc in instruction_patterns:
    if re.search(pattern, custom_prompt, re.IGNORECASE):
        print(f"  [YES] {desc}")
    else:
        print(f"  [NO]  {desc}")

# Test parse_commands with actual prompt content
print("\n[STEP 3] Testing parse_commands with various inputs...")
from rasa.dialogue_understanding.generator.command_parser import parse_commands

# Create a minimal FlowsList-like object
class MockFlowsList:
    def __init__(self, flow_ids):
        self._flow_ids = flow_ids
    def flow_by_id(self, flow_id):
        return type('Flow', (), {'id': flow_id})()

flows_list = MockFlowsList(['saludo', 'ayuda', 'consulta_auditoria', 'fuera_tema'])

test_cases = [
    # From custom prompt examples
    ('StartFlow(saludo)', 'From prompt example'),
    # Common variations
    ('StartFlow(saludo)\n', 'With newline'),
    ('StartFlow( saludo )', 'With spaces'),
    ('start flow(saludo)', 'Lowercase "start flow"'),
    ('startflow(saludo)', 'No space'),
    # What LLM might return
    ('StartFlow(saludo)\nStartFlow(ayuda)', 'Two commands'),
    ('  StartFlow(saludo)', 'Leading spaces'),
    # Edge cases
    ('start flow (saludo)', 'Space before paren'),
    ('Starting flow: saludo', 'Natural language'),
    ('I should start the saludo flow', 'Sentence'),
    ('`StartFlow(saludo)`', 'With backticks'),
]

print("\nParsing test cases:")
for test_input, desc in test_cases:
    try:
        result = parse_commands(test_input, flows_list)
        status = "OK" if result else "EMPTY"
        print(f"  [{status}] {desc}: {repr(test_input)} -> {result}")
    except Exception as e:
        print(f"  [ERR] {desc}: {repr(test_input)} -> {type(e).__name__}: {e}")

# Test actual LLM response
print("\n[STEP 4] Testing actual LLM response...")
from rasa.shared.providers.llm.default_litellm_llm_client import DefaultLiteLLMClient

client = DefaultLiteLLMClient.from_config({
    'provider': 'gemini',
    'model': 'gemini-2.5-flash',
    'api_key': os.environ['GEMINI_API_KEY']
})

# Send the actual prompt from model
print("Sending custom prompt to Gemini...")
response = client.completion(custom_prompt)

if hasattr(response, 'choices') and response.choices:
    choice = response.choices[0]
    if isinstance(choice, dict):
        llm_output = choice.get('message', {}).get('content', '')
    else:
        llm_output = str(choice)
    print(f"LLM Output: {repr(llm_output)}")

    # Now parse the LLM output
    print("\nParsing LLM output...")
    parsed = parse_commands(llm_output, flows_list)
    print(f"Parsed result: {parsed}")
else:
    print(f"Response: {response}")

print("\n" + "=" * 70)
print("DIAGNOSTIC COMPLETE")
print("=" * 70)