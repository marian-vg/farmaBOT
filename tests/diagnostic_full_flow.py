"""
Rasa CALM Command Generator Diagnostic Script
Captures full flow from message to command generation
"""
import os
import sys
import tempfile
import tarfile
from pathlib import Path

# Environment setup
for k, v in [
    ('GEMINI_API_KEY', 'AIzaSyCx4H6k2WERyL3-j11udVl6slOjhnIPhaA'),
    ('LLM_API_HEALTH_CHECK', 'true'),
    ('RASALOG', 'DEBUG'),
    ('LOG_LEVEL_LLM_COMMAND_GENERATOR', 'DEBUG'),
    ('PYTHONIOENCODING', 'utf-8'),
]:
    os.environ[k] = v

print("=" * 70)
print("DIAGNOSTIC: Rasa CALM Command Generator Full Flow")
print("=" * 70)

# STEP 1: Extract custom prompt from model
print("\n[STEP 1] Extracting custom prompt from model...")
model_path = 'models/20260505-001524-sweet-condenser.tar.gz'

with tarfile.open(model_path, 'r:gz') as tar:
    for member in tar.getmembers():
        if 'command' in member.name.lower() and member.isfile():
            content = tar.extractfile(member).read().decode('utf-8')
            print(f"  Found: {member.name}")
            print(f"  Size: {len(content)} chars")
            with open('debug_prompt_from_model.txt', 'w', encoding='utf-8') as f:
                f.write(content)

# STEP 2: Initialize Rasa configuration properly
print("\n[STEP 2] Initializing Rasa configuration...")
from rasa.core.config import Configuration

config = Configuration()
Configuration.set_instance(config)

# Initialize endpoints
from rasa.core.config import initialise_endpoints, initialise_sub_agents, initialise_credentials, initialise_message_processing

# Load credentials and endpoints
try:
    initialise_credentials('credentials.yml')
    print("  Credentials initialized")
except Exception as e:
    print(f"  Credentials init warning: {e}")

try:
    initialise_endpoints('endpoints.yml')
    print("  Endpoints initialized")
except Exception as e:
    print(f"  Endpoints init warning: {e}")

try:
    initialise_message_processing()
    print("  Message processing initialized")
except Exception as e:
    print(f"  Message processing init warning: {e}")

# STEP 3: Load agent
print("\n[STEP 3] Loading agent...")
from rasa.core.agent import Agent

agent = Agent.load(model_path)
print(f"  Agent loaded: {type(agent).__name__}")

processor = agent.create_processor()
print(f"  Processor: {type(processor).__name__}")

# STEP 4: Create tracker and message
print("\n[STEP 4] Creating test tracker and message...")
from rasa.shared.core.trackers import DialogueStateTracker
from rasa.shared.core.domain import Domain
from rasa.shared.constants import TEXT
from rasa.shared.nlu.training_data.message import Message
import yaml

with open('domain.yml', 'r', encoding='utf-8') as f:
    domain_dict = yaml.safe_load(f)

rasa_domain = Domain.from_dict(domain_dict)
tracker = DialogueStateTracker(
    sender_id='diagnostic-test',
    slots=rasa_domain.slots,
    max_event_history=None
)

message = Message(data={TEXT: 'Hola'})
print(f"  Message: '{message.get(TEXT)}'")

# STEP 5: Trace the prediction flow
print("\n[STEP 5] Tracing prediction flow...")
print("-" * 70)

# Enable debug logging for LLM command generator
import logging
logging.getLogger('rasa.dialogue_understanding.generator.single_step.single_step_based_llm_command_generator').setLevel(logging.DEBUG)
logging.getLogger('rasa.core.processor').setLevel(logging.DEBUG)

# Capture logs to file
log_file = open('debug_rasa_flow.log', 'w', encoding='utf-8')

# Run prediction with log capture
import io
old_stderr = sys.stderr
sys.stderr = io.StringIO()

try:
    result = agent.handle_message(message, tracker)
except Exception as e:
    result = None
    print(f"  Error during handle_message: {type(e).__name__}: {e}")

# Get stderr output
stderr_output = sys.stderr.getvalue()
sys.stderr = old_stderr

# STEP 6: Parse results
print("\n[STEP 6] Parsing results...")

# Get tracker events
print(f"  Tracker events: {len(tracker.events)}")
for event in tracker.events[-5:]:
    event_dict = event.as_dict()
    print(f"    {type(event).__name__}: {event_dict}")

# Check log file for key patterns
with open('debug_rasa_flow.log', 'r', encoding='utf-8') as f:
    log_content = f.read()

print("\n[KEY LOG ENTRIES]")
key_patterns = ['prompt_rendered', 'llm_command_generator', 'StartFlow', 'parse_commands', 'predict_commands', 'DEBUG']
for line in log_content.split('\n'):
    for pattern in key_patterns:
        if pattern in line:
            print(f"  {line[:200]}")
            break

print("\n" + "=" * 70)
print("DIAGNOSTIC COMPLETE")
print("=" * 70)
print("\nCheck files:")
print("  - debug_prompt_from_model.txt: Custom prompt inside model")
print("  - debug_rasa_flow.log: Full debug log from Rasa flow")