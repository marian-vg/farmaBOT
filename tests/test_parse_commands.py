"""Direct test of command_parser.parse_commands with flows=None"""
import sys
sys.path.insert(0, '.venv/Lib/site-packages/rasa')

from rasa.dialogue_understanding.generator.command_parser import parse_commands

# Test 1: flows=None
print("TEST 1: flows=None")
result = parse_commands("StartFlow(saludo)", flows=None)
print(f"  Result: {result}, count={len(result)}")

# Test 2: flows=[] (empty list converted to FlowsList)
print("\nTEST 2: flows=[]")
from rasa.shared.core.flows import FlowsList
empty_flows = FlowsList(underlying_flows=[])
result2 = parse_commands("StartFlow(saludo)", flows=empty_flows)
print(f"  Result: {result2}, count={len(result2)}")

# Test 3: flows=[] with another command
print("\nTEST 3: flows=[] with SetSlot command")
result3 = parse_commands("SetSlot(slot_name=value)", flows=empty_flows)
print(f"  Result: {result3}, count={len(result3)}")

print("\nDone")