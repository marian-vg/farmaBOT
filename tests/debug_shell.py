"""
Simple test to see if rasa shell starts and loads model
"""
import subprocess
import sys
import os
import time

env = os.environ.copy()
env['GEMINI_API_KEY'] = 'AIzaSyCx4H6k2WERyL3-j11udVl6slOjhnIPhaA'
env['LLM_API_HEALTH_CHECK'] = 'true'
env['PYTHONIOENCODING'] = 'utf-8'

DEBUG_LOG = 'C:/Users/Administrador/Herd/farmarag-rasa/debug_predict.log'
if os.path.exists(DEBUG_LOG):
    os.remove(DEBUG_LOG)

print('Starting rasa shell...')
proc = subprocess.Popen(
    [sys.executable, '-m', 'rasa', 'shell',
     '--model', 'models/20260505-001524-sweet-condenser.tar.gz',
     '--port', '5005'],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    stdin=subprocess.PIPE,
    cwd=os.getcwd(),
    env=env,
)

print('Waiting 40s...')
time.sleep(40)

# Try to send input
print('Sending Hola...')
try:
    proc.stdin.write(b'Hola\n')
    proc.stdin.flush()
    print('  Input sent')
except Exception as e:
    print(f'  Error sending: {e}')

time.sleep(15)

# Check debug log
print()
if os.path.exists(DEBUG_LOG):
    print('DEBUG LOG EXISTS! Contents:')
    print('='*60)
    with open(DEBUG_LOG, 'r', encoding='utf-8') as f:
        print(f.read())
    print('='*60)
else:
    print('DEBUG LOG NOT CREATED')

# Terminate
try:
    proc.terminate()
except:
    pass
stdout, stderr = proc.communicate(timeout=5)

print()
print('RASA OUTPUT (last 30 lines):')
print('='*60)
lines = stdout.decode('utf-8', errors='replace').split('\n')
for line in lines[-30:]:
    if line.strip():
        print(f'  {line[:200]}')