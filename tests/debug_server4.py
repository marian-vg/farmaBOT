"""
Run rasa RUN (server mode) NO credentials file - just REST
"""
import subprocess
import sys
import os
import time
import requests

env = os.environ.copy()
env['GEMINI_API_KEY'] = 'AIzaSyCx4H6k2WERyL3-j11udVl6slOjhnIPhaA'
env['LLM_API_HEALTH_CHECK'] = 'true'
env['PYTHONIOENCODING'] = 'utf-8'

DEBUG_LOG = 'C:/Users/Administrador/Herd/farmarag-rasa/debug_predict.log'
if os.path.exists(DEBUG_LOG):
    os.remove(DEBUG_LOG)

print('Starting rasa run (server mode) - NO credentials file...')
proc = subprocess.Popen(
    [sys.executable, '-m', 'rasa', 'run',
     '--model', 'models/20260505-001524-sweet-condenser.tar.gz',
     '--port', '5005',
     '--enable-api'],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    stdin=subprocess.PIPE,
    cwd=os.getcwd(),
    env=env,
)

print('Waiting 45s for server to start...')
time.sleep(45)

print('Checking if server is up...')
try:
    resp = requests.get('http://localhost:5005/', timeout=5)
    print(f'  Server responded: {resp.status_code}')
except Exception as e:
    print(f'  Server not responding: {e}')

print('Sending webhook request...')
try:
    resp = requests.post(
        'http://localhost:5005/webhooks/rest/webhook',
        json={'sender': 'test', 'message': 'Hola'},
        timeout=20
    )
    print(f'  Response: {resp.status_code}')
    print(f'  Body: {resp.text[:500]}')
except Exception as e:
    print(f'  Error: {e}')

time.sleep(5)

# Check debug log
print()
if os.path.exists(DEBUG_LOG):
    print('DEBUG LOG CONTENTS:')
    print('='*60)
    with open(DEBUG_LOG, 'r', encoding='utf-8') as f:
        content = f.read()
    print(content)
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
print('RASA OUTPUT (last 20 lines):')
print('='*60)
lines = stdout.decode('utf-8', errors='replace').split('\n')
for line in lines[-20:]:
    if line.strip():
        print(f'  {line[:200]}')