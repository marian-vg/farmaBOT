"""
Run rasa shell - just wait and check debug log
"""
import subprocess
import sys
import os
import time

env = os.environ.copy()
env['GEMINI_API_KEY'] = 'AIzaSyCx4H6k2WERyL3-j11udVl6slOjhnIPhaA'
env['LLM_API_HEALTH_CHECK'] = 'true'
env['RASALOG'] = 'DEBUG'
env['PYTHONIOENCODING'] = 'utf-8'

DEBUG_LOG = "C:/Users/Administrador/Herd/farmarag-rasa/debug_predict.log"

if os.path.exists(DEBUG_LOG):
    os.remove(DEBUG_LOG)

print("Starting rasa shell...")
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

print("Waiting 35s for model to load...")
time.sleep(35)

print("Sending 'Hola' via stdin...")
try:
    proc.stdin.write(b"Hola\n")
    proc.stdin.flush()
    print("  Sent 'Hola'")
except Exception as e:
    print(f"  Error sending: {e}")

time.sleep(20)

# Check if debug log was created
print()
if os.path.exists(DEBUG_LOG):
    print(f"DEBUG LOG CREATED!")
    with open(DEBUG_LOG, 'r', encoding='utf-8') as f:
        content = f.read()
    print(f"Content ({len(content)} chars):")
    print('-'*60)
    print(content)
    print('-'*60)
else:
    print("DEBUG LOG NOT CREATED - predict_commands may not have been called")

# Terminate
try:
    proc.stdin.write(b"salir\n")
    proc.stdin.flush()
except:
    pass

time.sleep(3)
proc.terminate()
stdout, _ = proc.communicate(timeout=5)

print()
print("RASA OUTPUT (last 20 lines):")
lines = stdout.decode('utf-8', errors='replace').split('\n')
for line in lines[-20:]:
    if line.strip():
        print(f"  {line[:200]}")