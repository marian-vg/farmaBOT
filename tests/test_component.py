"""
Rasa CALM Command Generator Component Test
Tests the CompactLLMCommandGenerator in isolation
"""
import os
import sys

for k, v in [
    ('GEMINI_API_KEY', 'AIzaSyCx4H6k2WERyL3-j11udVl6slOjhnIPhaA'),
    ('LLM_API_HEALTH_CHECK', 'true'),
    ('RASALOG', 'DEBUG'),
    ('LOG_LEVEL_LLM_COMMAND_GENERATOR', 'DEBUG'),
    ('PYTHONIOENCODING', 'utf-8'),
]:
    os.environ[k] = v

print("=" * 70)
print("COMPACT LLM COMMAND GENERATOR COMPONENT TEST")
print("=" * 70)

# Import the key components
print("\n[1] Importing components...")
try:
    from rasa.dialogue_understanding.generator.single_step.single_step_based_llm_command_generator import SingleStepBasedLLMCommandGenerator
    print("  SingleStepBasedLLMCommandGenerator imported")
except Exception as e:
    print(f"  ERROR importing: {e}")

try:
    from rasa.dialogue_understanding.generator.llm_based_command_generator import LLMBasedCommandGenerator
    print("  LLMBasedCommandGenerator imported")
except Exception as e:
    print(f"  ERROR importing: {e}")

# Check the source code for the process method
print("\n[2] Checking process method signature...")
import inspect
if 'SingleStepBasedLLMCommandGenerator' in dir():
    source = inspect.getsource(SingleStepBasedLLMCommandGenerator.process)
    print("process method found, checking for _should_skip_llm_call...")
    if '_should_skip_llm_call' in source:
        print("  YES - _should_skip_llm_call is used")
    else:
        print("  NO - _should_skip_llm_call not found")

# Test with minimal config
print("\n[3] Testing with mock tracker and message...")
try:
    from rasa.shared.core.trackers import DialogueStateTracker
    from rasa.shared.constants import TEXT
    from rasa.shared.nlu.training_data.message import Message
    from rasa.shared.core.domain import Domain
    import yaml

    # Load domain
    with open('domain.yml', 'r', encoding='utf-8') as f:
        domain_dict = yaml.safe_load(f)

    domain = Domain.from_dict(domain_dict)

    # Create minimal tracker
    tracker = DialogueStateTracker(
        sender_id='test',
        slots=domain.slots,
        max_event_history=None
    )

    # Create message
    message = Message(data={TEXT: 'Hola'})

    print(f"  Tracker events: {len(tracker.events)}")
    print(f"  Message: {message.get(TEXT)}")
    print(f"  Domain flows: {list(domain.flows.keys()) if hasattr(domain, 'flows') else 'N/A'}")

except Exception as e:
    print(f"  ERROR: {e}")
    import traceback
    traceback.print_exc()

# Check evaluate_message method
print("\n[4] Checking evaluate_message method...")
if 'SingleStepBasedLLMCommandGenerator' in dir():
    if hasattr(SingleStepBasedLLMCommandGenerator, 'evaluate_message'):
        print("  evaluate_message found")
        source = inspect.getsource(SingleStepBasedLLMCommandGenerator.evaluate_message)
        print("  Source preview:")
        print(source[:1000])
    else:
        print("  evaluate_message NOT found")

print("\n" + "=" * 70)
print("COMPONENT TEST COMPLETE")
print("=" * 70)