"""
Rasa CALM Full Flow Test - Server + HTTP Request
Starts Rasa server and sends test message to trace command generation
"""
import os
import sys
import time
import json
import subprocess
import threading
import requests

for k, v in [
    ('GEMINI_API_KEY', 'AIzaSyCx4H6k2WERyL3-j11udVl6slOjhnIPhaA'),
    ('LLM_API_HEALTH_CHECK', 'true'),
    ('RASALOG', 'DEBUG'),
    ('LOG_LEVEL_LLM_COMMAND_GENERATOR', 'DEBUG'),
    ('PYTHONIOENCODING', 'utf-8'),
]:
    os.environ[k] = v

print("=" * 70)
print("RASA CALM FULL FLOW TEST")
print("=" * 70)

# Start Rasa server in background
print("\n[1] Starting Rasa server...")
server_process = subprocess.Popen(
    [
        sys.executable, '-m', 'rasa', 'run',
        '--model', 'models/20260505-001524-sweet-condenser.tar.gz',
        '--port', '5005',
        '--credentials', 'credentials.yml',
    ],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    cwd=os.getcwd(),
    env=dict(os.environ, PYTHONIOENCODING='utf-8', RASALOG='DEBUG'),
)

print("  Server PID:", server_process.pid)
print("  Waiting for server to start...")

# Wait for server to be ready
max_wait = 30
for i in range(max_wait):
    try:
        response = requests.get('http://localhost:5005/', timeout=2)
        print(f"  Server ready after {i+1} seconds")
        break
    except:
        time.sleep(1)
else:
    print("  WARNING: Server may not be ready")

# Give extra time for model loading
time.sleep(5)

# Send test message
print("\n[2] Sending test message to webhook...")
payload = {
    "sender": "diagnostic-test",
    "message": "Hola"
}

try:
    response = requests.post(
        'http://localhost:5005/webhooks/rest/webhook',
        json=payload,
        timeout=30
    )
    print(f"  Status: {response.status_code}")
    print(f"  Response: {response.text[:500]}")
except Exception as e:
    print(f"  Error: {type(e).__name__}: {e}")

# Wait a bit more for any async logs
time.sleep(5)

# Terminate server
print("\n[3] Stopping server...")
server_process.terminate()
stdout, _ = server_process.communicate(timeout=5)

# Print last lines of output that contain DEBUG info
print("\n[4] Relevant server output (DEBUG lines with command/prompt/llm):")
lines = stdout.decode('utf-8', errors='replace').split('\n')
debug_keywords = ['prompt', 'llm', 'command', 'StartFlow', 'parse', 'predict', 'DEBUG']
for line in lines:
    for kw in debug_keywords:
        if kw.lower() in line.lower():
            print(f"  {line[:200]}")
            break

print("\n" + "=" * 70)
print("TEST COMPLETE")
print("=" * 70)