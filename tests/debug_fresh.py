"""Fresh test - no cache, exact simulation"""
import subprocess
import sys
import os
import time

env = os.environ.copy()
env['GEMINI_API_KEY'] = 'AIzaSyCx4H6k2WERyL3-j11udVl6slOjhnIPhaA'
env['PYTHONIOENCODING'] = 'utf-8'

# First, clear all pycache
for root, dirs, files in os.walk('.venv'):
    for d in dirs:
        if d == '__pycache__':
            try:
                os.remove(os.path.join(root, d, '*.pyc'))
            except:
                pass
    for f in files:
        if f.endswith('.pyc'):
            try:
                os.remove(os.path.join(root, f))
            except:
                pass

print('Starting fresh rasa server...')

proc = subprocess.Popen(
    [sys.executable, '-m', 'rasa', 'run',
     '--model', 'models/20260505-001524-sweet-condenser.tar.gz',
     '--port', '5005',
     '--enable-api'],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    cwd=os.getcwd(),
    env=env,
)

print('Waiting 55s for startup...')
time.sleep(55)

print('Sending webhook...')
import requests
try:
    resp = requests.post(
        'http://localhost:5005/webhooks/rest/webhook',
        json={'sender': 'test', 'message': 'Hola'},
        timeout=30
    )
    print(f'Response: {resp.status_code}')
    print(f'Body: {resp.text[:500]}')
except Exception as e:
    print(f'Error: {e}')

time.sleep(5)

# Check if debug_predict.log exists and read it
if os.path.exists('debug_predict.log'):
    with open('debug_predict.log', 'r', encoding='utf-8') as f:
        content = f.read()
    print('\n=== DEBUG LOG ===')
    print(content)
    print('=== END DEBUG LOG ===')
else:
    print('debug_predict.log not found')

proc.terminate()
proc.communicate(timeout(5))