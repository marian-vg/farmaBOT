"""
Run rasa server and test via HTTP webhook
Simpler approach to verify command generation
"""
import subprocess
import sys
import os
import time
import requests

# Environment
env = os.environ.copy()
env['GEMINI_API_KEY'] = 'AIzaSyCx4H6k2WERyL3-j11udVl6slOjhnIPhaA'
env['LLM_API_HEALTH_CHECK'] = 'true'
env['RASALOG'] = 'DEBUG'
env['LOG_LEVEL_LLM_COMMAND_GENERATOR'] = 'DEBUG'
env['PYTHONIOENCODING'] = 'utf-8'

print("="*70)
print("TESTING VIA HTTP WEBHOOK")
print("="*70)

# Start rasa server in background
print("[1] Starting Rasa server...")
proc = subprocess.Popen(
    [sys.executable, '-m', 'rasa', 'run',
     '--model', 'models/20260505-001524-sweet-condenser.tar.gz',
     '--port', '5005',
     '--credentials', 'credentials.yml'],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    cwd=os.getcwd(),
    env=env,
)

print("  Waiting for server startup (20s)...")
time.sleep(20)

print("[2] Checking if server is up...")
try:
    resp = requests.get('http://localhost:5005/', timeout=5)
    print(f"  Server responded: {resp.status_code}")
except Exception as e:
    print(f"  Server not responding: {e}")

# Give more time for model loading
time.sleep(10)

print("[3] Sending test message via webhook...")
payload = {
    "sender": "test-user",
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

# Wait for logs
time.sleep(5)

print("[4] Terminating server...")
proc.terminate()
try:
    stdout, _ = proc.communicate(timeout=5)
except:
    proc.kill()
    stdout, _ = proc.communicate()

# Check for key debug lines
print()
print("="*70)
print("DEBUG LINES FOUND")
print("="*70)

keywords = ['prompt_rendered', 'actions_generated', 'StartFlow',
            'llm_command_generator', 'command_generated', 'parse_commands',
            'ERROR', 'exception']

for line in stdout.decode('utf-8', errors='replace').split('\n'):
    for kw in keywords:
        if kw.lower() in line.lower():
            print(f"  {line[:250]}")

print()
print("="*70)
print("TEST COMPLETE")
print("="*70)