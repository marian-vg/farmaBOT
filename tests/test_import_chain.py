"""Test parse_commands with actual rasa Core imports - as used by server"""
import sys
sys.path.insert(0, '.venv/Lib/site-packages/rasa')

print("=== Testing parse_commands through full import chain ===")

# Simulate how rasa server imports it
from rasa.dialogue_understanding.generator.single_step.single_step_based_llm_command_generator import (
    SingleStepBasedLLMCommandGenerator as Generator
)

# Get the parse_commands function as imported
from rasa.dialogue_understanding.generator.command_parser import parse_commands as pc

print(f"parse_commands function id: {id(pc)}")
print(f"parse_commands source file: {pc.__module__}")

# Check if the source has our fix
import inspect
src = inspect.getsource(pc)
print("\nFirst 500 chars of parse_commands source:")
print(src[:500])

# Test
print("\n=== Testing with flows=None ===")
result = pc("StartFlow(saludo)", flows=None)
print(f"Result: {result}")
print(f"Count: {len(result)}")