"""
Direct test of command generator via Python - bypasses shell issues
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

print("="*70)
print("DIRECT COMPONENT TEST - Full Pipeline Trace")
print("="*70)

async def test():
    # Import components
    from rasa.core.agent import Agent
    from pathlib import Path

    model_path = 'models/20260505-001524-sweet-condenser.tar.gz'

    print(f"[1] Loading agent from {model_path}...")

    try:
        agent = Agent.load(model_path)
        print("    Agent loaded successfully")
    except Exception as e:
        print(f"    ERROR loading agent: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return

    print("[2] Creating processor...")
    try:
        processor = agent.create_processor()
        print(f"    Processor: {type(processor).__name__}")
    except Exception as e:
        print(f"    ERROR creating processor: {type(e).__name__}: {e}")
        return

    print("[3] Creating test message...")
    from rasa.core.message import UserMessage
    message = UserMessage(text="Hola", sender_id="debug-test")
    print(f"    Message: '{message.text}'")

    print("[4] Handling message (this should trigger the full pipeline)...")
    print("    NOTE: handle_message is async and will call process() internally")
    print("    Expect DEBUG output from instrumented code...")

    try:
        result = await agent.handle_message(message)
        print(f"\n[5] Result: {result}")
    except Exception as e:
        print(f"    ERROR handling message: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()

asyncio.run(test())

print()
print("="*70)
print("COMPLETE - Check for DEBUG output above")
print("="*70)