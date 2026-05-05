"""
Direct test via Agent - loads properly and accesses command generator
"""
import os
import sys
import asyncio
import yaml

for k, v in [
    ('GEMINI_API_KEY', 'AIzaSyCx4H6k2WERyL3-j11udVl6slOjhnIPhaA'),
    ('LLM_API_HEALTH_CHECK', 'true'),
    ('RASALOG', 'DEBUG'),
    ('LOG_LEVEL_LLM_COMMAND_GENERATOR', 'DEBUG'),
    ('PYTHONIOENCODING', 'utf-8'),
]:
    os.environ[k] = v

print("="*70)
print("DIRECT AGENT TEST")
print("="*70)

async def test_agent():
    try:
        from rasa.core.agent import Agent
        from rasa.shared.core.trackers import DialogueStateTracker
        from rasa.shared.core.domain import Domain
        from rasa.shared.nlu.training_data.message import Message
        from rasa.shared.constants import TEXT
        from pathlib import Path

        model_path = 'models/20260505-001524-sweet-condenser.tar.gz'

        print("[1] Loading agent...")
        agent = Agent.load(model_path)
        print("    Agent loaded")

        print("[2] Creating processor...")
        processor = agent.create_processor()
        print(f"    Processor: {type(processor).__name__}")

        # Get domain
        print("[3] Getting domain...")
        rasa_domain = processor.domain
        print(f"    Domain loaded: {len(list(rasa_domain.flows))} flows")

        # Create tracker
        print("[4] Creating tracker...")
        tracker = DialogueStateTracker(
            sender_id='test-agent',
            slots=rasa_domain.slots,
            max_event_history=None
        )
        print(f"    Tracker events: {len(tracker.events)}")

        # Create message
        print("[5] Creating message...")
        message = Message(data={TEXT: 'Hola'})
        print(f"    Message: {message.get(TEXT)}")

        # Check if we can access command generator
        print("[6] Checking graph nodes...")
        if hasattr(processor, 'graph_runner'):
            print(f"    Graph runner: {type(processor.graph_runner).__name__}")
            if hasattr(processor.graph_runner, 'graph'):
                graph = processor.graph_runner.graph
                print(f"    Graph: {type(graph).__name__}")
                if hasattr(graph, 'nodes'):
                    print(f"    Nodes: {list(graph.nodes.keys())[:10]}")

        # Try predict
        print("[7] Running prediction...")
        parse_data = await processor.parse_message(
            rasa.core.message.UserMessage(text="Hola", sender_id="test")
        )
        print(f"    Parse data intent: {parse_data.get('intent', {})}")
        print(f"    Parse data commands: {parse_data.get('commands', [])}")

    except Exception as e:
        print(f"ERROR: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()

asyncio.run(test_agent())

print()
print("="*70)
print("AGENT TEST COMPLETE")
print("="*70)