"""Test command_parser with direct imports"""
import sys
sys.path.insert(0, '.venv/Lib/site-packages/rasa')

# Import fresh - bypass module caching
import importlib
import rasa.dialogue_understanding.generator.command_parser as cp_module
importlib.reload(cp_module)

from rasa.dialogue_understanding.generator.command_parser import parse_commands

# Verify the fix is in place
print("Checking _parse_start_flow_command source...")
import inspect
src = inspect.getsource(cp_module._parse_start_flow_command)
print(src[:300])

# Test with flows=None
print("\n=== Testing with flows=None ===")
result = parse_commands("StartFlow(saludo)", flows=None)
print(f"Result: {result}")
print(f"Count: {len(result)}")

# Test with flows being a proper FlowsList
print("\n=== Testing with empty FlowsList ===")
from rasa.shared.core.flows import FlowsList
empty_flows = FlowsList(underlying_flows=[])
result2 = parse_commands("StartFlow(saludo)", flows=empty_flows)
print(f"Result: {result2}")
print(f"Count: {len(result2)}")