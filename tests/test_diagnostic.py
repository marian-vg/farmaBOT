"""
Diagnostic test script for Rasa CALM CompactLLMCommandGenerator.
Traces the entire flow from user message to command generation.
"""
import os
import sys
import asyncio
import tempfile
import tarfile
import json
from pathlib import Path

# Set environment variables
os.environ['GEMINI_API_KEY'] = 'AIzaSyCx4H6k2WERyL3-j11udVl6slOjhnIPhaA'
os.environ['LLM_API_HEALTH_CHECK'] = 'true'
os.environ['RASALOG'] = 'DEBUG'
os.environ['LOG_LEVEL_LLM_COMMAND_GENERATOR'] = 'DEBUG'
os.environ['PYTHONIOENCODING'] = 'utf-8'

print("=" * 80)
print("RASA CALM DIAGNOSTIC TEST")
print("=" * 80)

# Step 1: Verify model and extract custom prompt
print("\n[STEP 1] Verifying model and custom prompt...")
print("-" * 40)

MODEL_PATH = 'models/20260505-001524-sweet-condenser.tar.gz'

with tarfile.open(MODEL_PATH, 'r:gz') as tar:
    # List all files
    print("Files in model:")
    for member in tar.getmembers():
        if 'command_prompt' in member.name.lower():
            content = tar.extractfile(member).read().decode('utf-8')
            print(f"  Found: {member.name}")
            print(f"  Size: {len(content)} chars")
            # Write to debug file
            with open('debug_prompt_from_model.txt', 'w', encoding='utf-8') as f:
                f.write(content)
            print("  -> Written to debug_prompt_from_model.txt")

# Step 2: Load Rasa components
print("\n[STEP 2] Loading Rasa components...")
print("-" * 40)

from rasa.model_training import train
from rasa.shared.constants import TEXT, INTENT, COMMANDS
from rasa.shared.nlu.training_data.message import Message
from rasa.shared.core.flows import FlowsList, Flow
from rasa.shared.core.trackers import DialogueStateTracker
from rasa.dialogue_understanding.generator.single_step.single_step_based_llm_command_generator import SingleStepBasedLLMCommandGenerator
from rasa.dialogue_understanding.generator.llm_based_command_generator import LLMBasedCommandGenerator
from rasa.dialogue_understanding.generator.command_parser import parse_commands
import rasa.shared.core.domain as domain_module

# Load domain
print("Loading domain...")
with open('domain.yml', 'r', encoding='utf-8') as f:
    import yaml
    domain_dict = yaml.safe_load(f)

print(f"  Intents: {domain_dict.get('intents', [])}")
print(f"  Flows: {list(domain_dict.get('flows', {}).keys())}")

# Step 3: Create a test message
print("\n[STEP 3] Creating test message...")
print("-" * 40)

test_message_text = "Hola"
message = Message(data={TEXT: test_message_text})
print(f"  Message created: '{test_message_text}'")
print(f"  Message data: {message.data}")

# Step 4: Create empty tracker (new conversation)
print("\n[STEP 4] Creating empty tracker...")
print("-" * 40)

tracker = DialogueStateTracker(
    sender_id="test-conversation",
    slots=domain_module.Domain.from_dict(domain_dict).slots,
    max_event_history=None
)
print(f"  Tracker created with {len(tracker.events)} events")
print(f"  Stack: {tracker.stack}")

# Step 5: Check startable flows
print("\n[STEP 5] Checking startable flows...")
print("-" * 40)

from rasa.graph_components.providers.flows_provider import FlowsProvider
from rasa.engine.storage.storage import ModelStorage
from rasa.engine.storage.resource import Resource
from rasa.engine.graph import ExecutionContext

# We need to load flows from the model
print("  Flows from domain.yml:")
flows_dict = domain_dict.get('flows', {})
for flow_name, flow_def in flows_dict.items():
    print(f"    - {flow_name}: {flow_def.get('description', 'No description')}")

# Create FlowsList manually for testing
print("\n  Creating FlowsList from domain...")
# The FlowsList needs to be constructed properly
flows_list = FlowsList.from_flows([
    Flow.from_dict(flow_name, flow_def)
    for flow_name, flow_def in flows_dict.items()
])
print(f"  FlowsList created with {len(list(flows_list.user_flows))} user flows")
print(f"  User flow IDs: {flows_list.user_flow_ids}")

# Step 6: Test render_template with actual components
print("\n[STEP 6] Testing template rendering...")
print("-" * 40)

# We need to actually load the model to get the command generator
# But for now, let's simulate what render_template would do
print("  Simulating template variables:")

# This is what render_template would build:
template_inputs = {
    "available_flows": "Flows will be listed here",  # Would come from prepare_flows_for_template
    "current_conversation": "",  # Empty for new conversation
    "flow_slots": [],
    "current_flow": None,  # No active flow for new conversation
    "current_slot": None,
    "current_slot_description": None,
    "current_slot_type": None,
    "current_slot_allowed_values": None,
    "user_message": test_message_text,
}

for key, value in template_inputs.items():
    print(f"    {key}: {value}")

# Step 7: Test the actual LLM call
print("\n[STEP 7] Testing LLM call with Gemini...")
print("-" * 40)

from rasa.shared.providers.llm.default_litellm_llm_client import DefaultLiteLLMClient

# Create LLM client
llm_config = {
    'provider': 'gemini',
    'model': 'gemini-2.5-flash',
    'api_key': os.environ['GEMINI_API_KEY']
}

print(f"  Config: {llm_config}")

client = DefaultLiteLLMClient.from_config(llm_config)
print(f"  Client created: {type(client).__name__}")
print(f"  LiteLLM model name: {client._litellm_model_name}")

# Build a test prompt (simulating what the template would generate)
test_prompt = """## Task
Analyze the conversation and output commands. One command per line. Use ONLY the formats specified below.

## Supported Command Formats
- `StartFlow(flow_name)` - Start a flow. Valid flow names: saludo, ayuda, consulta_auditoria, fuera_tema

## Examples
- User: "Hola" -> `StartFlow(saludo)`

## User Message
Hola

## Your Response (one command per line):
"""

print(f"  Prompt to send ({len(test_prompt)} chars):")
print("-" * 40)
print(test_prompt)
print("-" * 40)

# Make the actual LLM call
print("\n  Calling Gemini API...")
try:
    response = client.completion(test_prompt)
    print(f"  Response type: {type(response)}")
    print(f"  Response: {response}")

    if hasattr(response, 'choices') and response.choices:
        llm_output = response.choices[0] if isinstance(response.choices[0], str) else response.choices[0].get('message', {}).get('content', str(response.choices[0]))
        print(f"  LLM Output: '{llm_output}'")
    else:
        llm_output = str(response.choices) if response.choices else ""
        print(f"  LLM Choices: {response.choices}")
        print(f"  LLM Output: '{llm_output}'")
except Exception as e:
    print(f"  ERROR calling LLM: {type(e).__name__}: {e}")
    llm_output = ""

# Step 8: Test parse_commands
print("\n[STEP 8] Testing parse_commands...")
print("-" * 40)

if llm_output:
    print(f"  Input to parse_commands: '{llm_output}'")
    try:
        parsed_commands = parse_commands(llm_output, flows_list)
        print(f"  Parsed commands: {parsed_commands}")
        print(f"  Number of commands: {len(parsed_commands)}")

        for i, cmd in enumerate(parsed_commands):
            print(f"    [{i}] {type(cmd).__name__}: {cmd.as_dict() if hasattr(cmd, 'as_dict') else cmd}")
    except Exception as e:
        print(f"  ERROR parsing commands: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
else:
    print("  Skipped - no LLM output")

# Step 9: Full CompactLLMCommandGenerator test
print("\n[STEP 9] Testing CompactLLMCommandGenerator.process()...")
print("-" * 40)

try:
    # We need to load the actual model to test this
    # For now, let's try importing and using the SingleStepBasedLLMCommandGenerator

    print("  This step requires loading the full model graph.")
    print("  Skipping for now - run 'rasa shell --debug' to see full flow.")
except Exception as e:
    print(f"  Error: {type(e).__name__}: {e}")

# Summary
print("\n" + "=" * 80)
print("DIAGNOSTIC TEST COMPLETE")
print("=" * 80)
print("""
Next steps:
1. Check debug_prompt_from_model.txt - the custom prompt in the model
2. Check if LLM output matches expected format (StartFlow(saludo))
3. If parse_commands returns [], the regex patterns aren't matching

Key files created:
- debug_prompt_from_model.txt - Custom prompt extracted from model
""")
