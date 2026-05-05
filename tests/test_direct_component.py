"""
Minimal test: Directly call command generator's process method
This bypasses all the Rasa infrastructure and tests the component directly
"""
import os
import sys
import asyncio
import tempfile
from pathlib import Path
import json

for k, v in [
    ('GEMINI_API_KEY', 'AIzaSyCx4H6k2WERyL3-j11udVl6slOjhnIPhaA'),
    ('LLM_API_HEALTH_CHECK', 'true'),
    ('RASALOG', 'DEBUG'),
    ('LOG_LEVEL_LLM_COMMAND_GENERATOR', 'DEBUG'),
    ('PYTHONIOENCODING', 'utf-8'),
]:
    os.environ[k] = v

print("="*70)
print("DIRECT COMPONENT TEST")
print("="*70)

async def test_direct():
    try:
        # Extract model to temp dir
        import tarfile
        model_path = 'models/20260505-001524-sweet-condenser.tar.gz'

        with tempfile.TemporaryDirectory() as tmpdir:
            print("[1] Extracting model...")
            with tarfile.open(model_path, 'r:gz') as tar:
                tar.extractall(tmpdir)

            tmpdir = Path(tmpdir)

            # Load config
            config_path = tmpdir / 'components' / 'train_CompactLLMCommandGenerator2' / 'config.json'
            with open(config_path, 'r') as f:
                config = json.load(f)
            print(f"    Config loaded: {config.get('llm', {}).get('models', [])}")

            # Load prompt
            prompt_path = tmpdir / 'components' / 'train_CompactLLMCommandGenerator2' / 'command_prompt.jinja2'
            with open(prompt_path, 'r', encoding='utf-8') as f:
                prompt_template = f.read()
            print(f"    Prompt loaded: {len(prompt_template)} chars")

            # Create model storage and resource
            from rasa.engine.storage.storage import ModelStorage
            from rasa.engine.storage.resource import Resource
            from rasa.engine.graph import ExecutionContext

            model_storage = ModelStorage.from_model_archive(tmpdir)
            resource = Resource('train_CompactLLMCommandGenerator2')
            execution_context = ExecutionContext(resource=resource, model_package=tmpdir)

            print("[2] Loading command generator...")
            from rasa.dialogue_understanding.generator.single_step.single_step_based_llm_command_generator import SingleStepBasedLLMCommandGenerator

            cg = SingleStepBasedLLMCommandGenerator.load(
                config=config,
                model_storage=model_storage,
                resource=resource,
                execution_context=execution_context
            )
            print(f"    Loaded: {type(cg).__name__}")
            print(f"    Prompt template: {cg.prompt_template[:50]}...")

            # Create test message
            print("[3] Creating test message...")
            from rasa.shared.nlu.training_data.message import Message
            from rasa.shared.constants import TEXT

            message = Message(data={TEXT: 'Hola'})
            print(f"    Message: {message.get(TEXT)}")

            # Create test flows
            print("[4] Creating test flows...")
            from rasa.shared.core.flows import FlowsList, Flow
            import yaml

            with open('domain.yml', 'r', encoding='utf-8') as f:
                domain = yaml.safe_load(f)

            flows_dict = domain.get('flows', {})
            flows_list = FlowsList.from_flows([
                Flow.from_dict(name, fd) for name, fd in flows_dict.items()
            ])
            print(f"    Flows: {flows_list.user_flow_ids}")

            # Create empty tracker
            print("[5] Creating tracker...")
            from rasa.shared.core.trackers import DialogueStateTracker
            from rasa.shared.core.domain import Domain

            rasa_domain = Domain.from_dict(domain)
            tracker = DialogueStateTracker(
                sender_id='test-direct',
                slots=rasa_domain.slots,
                max_event_history=None
            )
            print(f"    Tracker events: {len(tracker.events)}")

            # Call predict_commands directly
            print("[6] Calling predict_commands directly...")
            print("    This should invoke the LLM with the custom prompt")

            commands = await cg.predict_commands(message, flows_list, tracker)

            print()
            print("="*70)
            print(f"RESULT: {len(commands)} commands")
            print("="*70)

            for cmd in commands:
                print(f"  {type(cmd).__name__}: {cmd.as_dict()}")

            if commands:
                print()
                print("SUCCESS! Commands were generated!")
            else:
                print()
                print("FAILURE! No commands generated!")
                print("This means the LLM was either not called or returned empty")

    except Exception as e:
        print(f"ERROR: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()

asyncio.run(test_direct())

print()
print("="*70)
print("DIRECT TEST COMPLETE")
print("="*70)