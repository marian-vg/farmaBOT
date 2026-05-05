"""Verify which parse_commands is being called"""
import sys
sys.path.insert(0, '.venv/Lib/site-packages/rasa')

# Import the actual module
import rasa.dialogue_understanding.generator.single_step.single_step_based_llm_command_generator as gen_module

# Check what parse_commands_using_command_parsers points to
print("parse_commands_using_command_parsers from generator module:")
import inspect
print(f"  Module: {gen_module.parse_commands_using_command_parsers.__module__}")
print(f"  Function: {gen_module.parse_commands_using_command_parsers.__name__}")
print(f"  ID: {id(gen_module.parse_commands_using_command_parsers)}")

# Get the original
from rasa.dialogue_understanding.generator.command_parser import parse_commands
print("\nOriginal parse_commands from command_parser:")
print(f"  Module: {parse_commands.__module__}")
print(f"  Function: {parse_commands.__name__}")
print(f"  ID: {id(parse_commands)}")

print(f"\nSame? {gen_module.parse_commands_using_command_parsers is parse_commands}")

# Check source of the imported function
print("\nSource of parse_commands_using_command_parsers:")
src = inspect.getsource(gen_module.parse_commands_using_command_parsers)
print(src[:400])