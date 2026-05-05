"""Test like the actual server does - calling through the class method"""
import sys
sys.path.insert(0, '.venv/Lib/site-packages/rasa')

from rasa.dialogue_understanding.generator.single_step.single_step_based_llm_command_generator import SingleStepBasedLLMCommandGenerator as Gen

print("=== Testing through class method ===")

# Call the actual class method as the server would
class MockTracker:
    pass

tracker = MockTracker()

# Test 1: flows=None
print("\nTest 1: flows=None")
result = Gen.parse_commands("StartFlow(saludo)", tracker, None)
print(f"Result: {result}")
print(f"Count: {len(result)}")

# Check parse_commands_using_command_parsers
from rasa.dialogue_understanding.generator.command_parser import parse_commands as original_pc
print(f"\nOriginal parse_commands id: {id(original_pc)}")
print(f"Gen.parse_commands.__func__: {Gen.parse_commands.__func__}")

# Let's trace what happens inside parse_commands
print("\n=== Tracing parse_commands execution ===")
import structlog
structlogger = structlog.get_logger()

actions = "StartFlow(saludo)"
flows = None

print(f"actions: {actions}")
print(f"flows: {flows}")
print(f"flows is None: {flows is None}")

# Simulate what parse_commands does
if not actions:
    print("Early return: no actions")
else:
    print("Processing actions...")
    action = actions.strip()
    print(f"Processing action: '{action}'")

    # Get default commands
    from rasa.dialogue_understanding.generator.command_parser import DEFAULT_COMMANDS, _get_compiled_pattern, _get_additional_parsing_logic
    from rasa.dialogue_understanding.commands import StartFlowCommand

    standard_commands = DEFAULT_COMMANDS
    print(f"Standard commands: {[c.__name__ for c in standard_commands]}")

    for command_clz in standard_commands:
        pattern = _get_compiled_pattern(command_clz.regex_pattern())
        print(f"  Checking {command_clz.__name__} with pattern {pattern.pattern}")
        if match := pattern.search(action):
            print(f"    MATCH! Creating command...")
            parsed_command = command_clz.from_dsl(match)
            print(f"    parsed_command: {parsed_command}")
            if _additional_parsing_fn := _get_additional_parsing_logic(command_clz):
                print(f"    Calling additional parsing function: {_additional_parsing_fn.__name__}")
                parsed_command = _additional_parsing_fn(parsed_command, flows)
                print(f"    After additional parsing: {parsed_command}")
            if parsed_command:
                print(f"    Added to commands")
            else:
                print(f"    NOT added (parsed_command was None)")
        else:
            print(f"    No match")