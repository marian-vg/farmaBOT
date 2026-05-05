"""
Deep trace test - captures complete flow through logging
Sets up debug to see every step
"""
import os
import sys
import logging

# Set environment
for k, v in [
    ('GEMINI_API_KEY', 'AIzaSyCx4H6k2WERyL3-j11udVl6slOjhnIPhaA'),
    ('LLM_API_HEALTH_CHECK', 'true'),
    ('RASALOG', 'DEBUG'),
    ('LOG_LEVEL_LLM_COMMAND_GENERATOR', 'DEBUG'),
    ('PYTHONIOENCODING', 'utf-8'),
]:
    os.environ[k] = v

# Configure logging to capture everything
logging.basicConfig(
    level=logging.DEBUG,
    format='%(name)-50s %(levelname)-8s %(message)s',
    handlers=[
        logging.FileHandler('debug_deep_trace.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

# Set specific loggers
logging.getLogger('rasa.dialogue_understanding.generator.single_step.single_step_based_llm_command_generator').setLevel(logging.DEBUG)
logging.getLogger('rasa.core.processor').setLevel(logging.DEBUG)
logging.getLogger('rasa.dialogue_understanding.generator').setLevel(logging.DEBUG)

print("="*70)
print("DEEP TRACE - Capturing all debug logs")
print("="*70)
print("Run this and check debug_deep_trace.log for full flow")
print()

# Now import and try to run a simple test
try:
    from rasa.core.agent import Agent
    from rasa.core.processor import MessageProcessor
    from rasa.core.graph import MessageGraphRunner
    from pathlib import Path

    model_path = 'models/20260505-001524-sweet-condenser.tar.gz'

    print(f"Loading agent from {model_path}...")

    agent = Agent.load(model_path)
    print("Agent loaded")

    # Create a simple test message
    from rasa.core.message import UserMessage

    message = UserMessage(text="Hola", sender_id="trace-test")
    print(f"Message created: '{message.text}'")

    print("\nHandling message (watch debug_deep_trace.log for details)...")
    result = agent.handle_message(message)

    print(f"\nResult: {result}")

except Exception as e:
    print(f"Error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*70)
print("Check debug_deep_trace.log for full debug output")
print("="*70)