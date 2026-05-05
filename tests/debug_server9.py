"""
Run rasa RUN (server mode) - read process output
"""
import subprocess
import sys
import os
import time
import requests
import threading

env = os.environ.copy()
env['GEMINI_API_KEY'] = 'AIzaSyCx4H6k2WERyL3-j11udVl6slOjhnIPhaA'
env['LLM_API_HEALTH_CHECK'] = 'true'
env['PYTHONIOENCODING'] = 'utf-8'

DEBUG_LOG = 'C:/Users/Administrador/Herd/farmarag-rasa/debug_predict.log'
if os.path.exists(DEBUG_LOG):
    os.remove(DEBUG_LOG)

proc_output = []
output_lock = threading.Lock()

def read_output(pipe, prefix):
    try:
        for line in pipe:
            with output_lock:
                proc_output.append(f'{prefix}: {line.rstrip()}')
    except:
        pass

print('Starting rasa run...', flush=True)

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

# Start reader threads
import threading
t = threading.Thread(target=read_output, args=(proc.stdout, 'OUT'))
t.daemon = True
t.start()

print('Waiting 60s...', flush=True)
time.sleep(60)

print(f'Process running: {proc.poll() is None}', flush=True)

# Try requests
for i in range(3):
    try:
        resp = requests.get('http://localhost:5005/', timeout=10)
        print(f'Request {i+1}: {resp.status_code}', flush=True)
        break
    except Exception as e:
        print(f'Request {i+1}: {e}', flush=True)
    time.sleep(5)

# Send webhook
print('Sending webhook...', flush=True)
try:
    resp = requests.post('http://localhost:5005/webhooks/rest/webhook',
                        json={'sender': 'test', 'message': 'Hola'}, timeout=30)
    print(f'Webhook response: {resp.status_code}', flush=True)
except Exception as e:
    print(f'Webhook error: {e}', flush=True)

time.sleep(5)

print('Process output so far:', flush=True)
with output_lock:
    for line in proc_output[-30:]:
        print(line, flush=True)

if os.path.exists(DEBUG_LOG):
    print('DEBUG LOG:')
    with open(DEBUG_LOG, 'r', encoding='utf-8') as f:
        print(f.read())

proc.terminate()
proc.communicate(timeout=5)