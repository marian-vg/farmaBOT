"""
Run rasa RUN (server mode) - use stderr for debugging
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

print(f'Starting rasa run (server mode)...', flush=True)

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
    bufsize=1,
    universal_newlines=True,
)

print('Waiting 50s for server to start...', flush=True)
time.sleep(50)

print('Checking if process is still running...', flush=True)
if proc.poll() is not None:
    print(f'  Process has exited with code: {proc.returncode}', flush=True)
    out, err = proc.communicate()
    print('STDOUT:', flush=True)
    print(out[:2000], flush=True)
else:
    print('  Process is still running', flush=True)

print('Checking if server is up (3 attempts)...', flush=True)
for i in range(3):
    try:
        resp = requests.get('http://localhost:5005/', timeout=10)
        print(f'  Attempt {i+1}: Server responded: {resp.status_code}', flush=True)
        break
    except Exception as e:
        print(f'  Attempt {i+1}: {e}', flush=True)
    time.sleep(5)

print('Sending webhook request...', flush=True)
try:
    resp = requests.post(
        'http://localhost:5005/webhooks/rest/webhook',
        json={'sender': 'test', 'message': 'Hola'},
        timeout=30
    )
    print(f'  Response: {resp.status_code}', flush=True)
    print(f'  Body: {resp.text[:500]}', flush=True)
except Exception as e:
    print(f'  Error: {e}', flush=True)

time.sleep(5)

# Check debug log
print()
if os.path.exists(DEBUG_LOG):
    print('DEBUG LOG:', flush=True)
    with open(DEBUG_LOG, 'r', encoding='utf-8') as f:
        content = f.read()
    print(content, flush=True)
else:
    print('DEBUG LOG NOT CREATED', flush=True)

# Try to read some output from the process
print('\nReading process output...', flush=True)
try:
    import select
    if select.select([proc.stdout], [], [], 1)[0]:
        line = proc.stdout.read(2000)
        if line:
            print(f'Process output: {line}', flush=True)
except:
    pass

try:
    proc.terminate()
except:
    pass
try:
    proc.communicate(timeout=5)
except:
    pass