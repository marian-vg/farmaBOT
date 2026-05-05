"""
Direct test of command parser as Rasa server would use it
"""
import subprocess
import sys
import os

env = os.environ.copy()
env['GEMINI_API_KEY'] = 'AIzaSyCx4H6k2WERyL3-j11udVl6slOjhnIPhaA'
env['PYTHONIOENCODING'] = 'utf-8'

# Create a simple test script that imports and tests the command parser
test_code = '''
import sys
sys.path.insert(0, 'C:/Users/Administrador/Herd/farmarag-rasa/.venv/Lib/site-packages/rasa')

# Import like Rasa does
from rasa.dialogue_understanding.generator.single_step.single_step_based_llm_command_generator import SingleStepBasedLLMCommandGenerator as Gen

class FakeTracker:
    pass

tracker = FakeTracker()
flows = None

# Call parse_commands directly
result = Gen.parse_commands.__func__(Gen, 'StartFlow(saludo)', tracker, flows)
print(f'RESULT: {result}')
print(f'COUNT: {len(result)}')
'''

proc = subprocess.Popen(
    [sys.executable, '-c', test_code],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    cwd='C:/Users/Administrador/Herd/farmarag-rasa',
    env=env,
)

stdout, stderr = proc.communicate(timeout=30)
print('Output:')
print(stdout.decode('utf-8', errors='replace'))