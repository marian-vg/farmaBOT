# Test parse_commands with 'StartFlow(saludo)'
from rasa.dialogue_understanding.generator.command_parser import parse_commands

# Create mock flows_list
class MockFlowsList:
    def __init__(self):
        self._flow_ids = ['saludo', 'ayuda', 'consulta_auditoria', 'fuera_tema']
    @property
    def user_flow_ids(self):
        return self._flow_ids

flows_list = MockFlowsList()

# Test parse_commands
action_list = 'StartFlow(saludo)'
result = parse_commands(action_list, flows_list)
print(f'parse_commands("{action_list}", flows_list) = {result}')
print(f'Count: {len(result)}')

# Also test with different formats
test_cases = [
    'StartFlow(saludo)',
    'StartFlow(saludo)\n',
    ' StartFlow(saludo) ',
    'StartFlow(saludo) ',
]

print()
print('Testing different formats:')
for test in test_cases:
    result = parse_commands(test, flows_list)
    print(f'  parse_commands({repr(test)}) = {result}, len={len(result)}')