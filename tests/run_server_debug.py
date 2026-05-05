"""
Run rasa run (not shell) and test via HTTP webhook
This tests the actual prediction pipeline
"""
import subprocess
import sys
import os
import time
import requests

# Environment with debug flags
env = os.environ.copy()
env['GEMINI_API_KEY'] = 'AIzaSyCx4H6k2WERyL3-j11udVl6slOjhnIPhaA'
env['LLM_API_HEALTH_CHECK'] = 'true'
env['RASALOG'] = 'DEBUG'
env['LOG_LEVEL_LLM_COMMAND_GENERATOR'] = 'DEBUG'
env['PYTHONIOENCODING'] = 'utf-8'

print("="*70)
print("RUNNING: rasa run with HTTP webhook test")
print("="*70)

# Start rasa server
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

print("Waiting for server startup (35s)...")
time.sleep(35)

print("Checking if server is up...")
try:
    resp = requests.get('http://localhost:5005/', timeout=5)
    print(f"  Server responded: {resp.status_code}")
except Exception as e:
    print(f"  Server not responding: {e}")
    print("  Continuing anyway...")

time.sleep(5)

print("Sending webhook request...")
payload = {
    "sender": "debug-test",
    "message": "Hola"
}

try:
    resp = requests.post(
        'http://localhost:5005/webhooks/rest/webhook',
        json=payload,
        timeout=30
    )
    print(f"  Status: {resp.status_code}")
    print(f"  Response: {resp.text[:500]}")
except Exception as e:
    print(f"  Error: {type(e).__name__}: {e}")

time.sleep(10)

print("Terminating server...")
proc.terminate()
try:
    stdout, _ = proc.communicate(timeout=5)
except:
    proc.kill()
    stdout, _ = proc.communicate()

print()
print("="*70)
print("DEBUG LINES IN OUTPUT")
print("="*70)

for line in stdout.decode('utf-8', errors='replace').split('\n'):
    lower = line.lower()
    if 'debug' in lower or 'compactllm' in lower or 'startflow' in lower or 'predict_commands' in lower:
        print(f"  {line[:250]}")

print()
print("="*70)
print("SERVER STDERR (last 50 lines)")
print("="*70)
lines = stdout.decode('utf-8', errors='replace').split('\n')
for line in lines[-50:]:
    if line.strip():
        print(f"  {line[:250]}")