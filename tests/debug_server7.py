"""
Run rasa RUN (server mode) - print Python info
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

print(f'Starting rasa run (server mode)...')
print(f'Python executable: {sys.executable}')

proc = subprocess.Popen(
    [sys.executable, '-c', '''
import sys
print(f"Subprocess Python: {sys.executable}", flush=True)
import rasa
print(f"Rasa file: {rasa.__file__}", flush=True)
import rasa.dialogue_understanding.generator.command_parser as cp
print(f"Command parser file: {cp.__file__}", flush=True)
with open("C:/Users/Administrador/Herd/farmarag-rasa/debug_python.log", "w") as f:
    f.write(f"Python: {sys.executable}\\n")
    f.write(f"Rasa: {rasa.__file__}\\n")
    f.write(f"Command parser: {cp.__file__}\\n")
'''],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    stdin=subprocess.PIPE,
    cwd=os.getcwd(),
    env=env,
)

print('Running subprocess to get Python info...')
stdout, stderr = proc.communicate(timeout=30)
print(stdout.decode('utf-8', errors='replace'))

print(f'\n--- Starting actual rasa server ---')
proc2 = subprocess.Popen(
    [sys.executable, '-m', 'rasa', 'run',
     '--model', 'models/20260505-001524-sweet-condenser.tar.gz',
     '--port', '5005',
     '--enable-api'],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    cwd=os.getcwd(),
    env=env,
)

print('Waiting 60s for server to start...')
time.sleep(60)

print('Checking if server is up...')
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
    print('DEBUG LOG:')
    with open(DEBUG_LOG, 'r', encoding='utf-8') as f:
        print(f.read())

try:
    proc2.terminate()
except:
    pass
try:
    proc2.communicate(timeout=5)
except:
    pass