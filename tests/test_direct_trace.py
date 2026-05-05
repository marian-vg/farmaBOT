"""
Direct trace - write debug to file instead of stdout
"""
import os
import sys
import asyncio
import json
import tempfile
from pathlib import Path

# Environment
os.environ['GEMINI_API_KEY'] = 'AIzaSyCx4H6k2WERyL3-j11udVl6slOjhnIPhaA'
os.environ['LLM_API_HEALTH_CHECK'] = 'true'
os.environ['RASALOG'] = 'DEBUG'
os.environ['PYTHONIOENCODING'] = 'utf-8'

DEBUG_FILE = 'debug_trace_output.txt'

def debug_write(msg):
    """Write debug message to file"""
    with open(DEBUG_FILE, 'a', encoding='utf-8') as f:
        f.write(f"{msg}\n")

print("="*70)
print("DIRECT COMPONENT TEST - Writing to debug file")
print("="*70)

debug_write("STARTING DIRECT TEST")

async def test():
    # Import components
    from rasa.core.agent import Agent
    from pathlib import Path

    model_path = 'models/20260505-001524-sweet-condenser.tar.gz'

    debug_write(f"[1] Loading agent from {model_path}...")
    print(f"[1] Loading agent...")

    try:
        agent = Agent.load(model_path)
        debug_write("    Agent loaded successfully")
        print("    Agent loaded successfully")
    except Exception as e:
        debug_write(f"    ERROR: {type(e).__name__}: {e}")
        print(f"    ERROR: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        debug_write(str(traceback.format_exc()))
        return

    debug_write("[2] Creating processor...")
    print("[2] Creating processor...")

    try:
        processor = agent.create_processor()
        debug_write(f"    Processor: {type(processor).__name__}")
        print(f"    Processor: {type(processor).__name__}")
    except Exception as e:
        debug_write(f"    ERROR: {type(e).__name__}: {e}")
        print(f"    ERROR: {type(e).__name__}: {e}")
        return

    debug_write("[3] Creating message...")
    print("[3] Creating message...")

    from rasa.core.message import UserMessage
    message = UserMessage(text="Hola", sender_id="debug-test")
    debug_write(f"    Message: '{message.text}'")
    print(f"    Message: '{message.text}'")

    debug_write("[4] Calling agent.handle_message...")
    print("[4] Calling agent.handle_message...")

    try:
        result = await agent.handle_message(message)
        debug_write(f"[5] Result received: {result}")
        print(f"\n[5] Result: {result}")
    except Exception as e:
        debug_write(f"    ERROR: {type(e).__name__}: {e}")
        print(f"    ERROR: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        debug_write(str(traceback.format_exc()))

asyncio.run(test())

debug_write("TEST COMPLETE")
print()
print("="*70)
print(f"COMPLETE - Check {DEBUG_FILE} for debug output")
print("="*70)