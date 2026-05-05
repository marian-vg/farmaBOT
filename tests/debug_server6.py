"""
Run rasa RUN (server mode) with longer wait and process check
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

print('Starting rasa run (server mode)...')
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

print('Waiting 60s for server to start...')
time.sleep(60)

print('Checking if process is still running...')
if proc.poll() is not None:
    print(f'  Process has exited with code: {proc.returncode}')
    stdout, stderr = proc.communicate(timeout=5)
    print('STDOUT:')
    print(stdout.decode('utf-8', errors='replace')[:2000])
else:
    print('  Process is still running')

print('Checking if server is up (3 attempts)...')
for i in range(3):
    try:
        resp = requests.get('http://localhost:5005/', timeout=10)
        print(f'  Attempt {i+1}: Server responded: {resp.status_code}')
        break
    except Exception as e:
        print(f'  Attempt {i+1}: {e}')
    time.sleep(5)

print('Sending webhook request...')
try:
    resp = requests.post(
        'http://localhost:5005/webhooks/rest/webhook',
        json={'sender': 'test', 'message': 'Hola'},
        timeout=30
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
try:
    stdout, stderr = proc.communicate(timeout=5)
except:
    pass