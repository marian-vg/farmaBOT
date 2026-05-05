"""
Run rasa shell with direct print capture - capture ALL stdout/stderr
"""
import subprocess
import sys
import os
import time
import threading

# Environment with debug flags
env = os.environ.copy()
env['GEMINI_API_KEY'] = 'AIzaSyCx4H6k2WERyL3-j11udVl6slOjhnIPhaA'
env['LLM_API_HEALTH_CHECK'] = 'true'
env['RASALOG'] = 'DEBUG'
env['LOG_LEVEL_LLM_COMMAND_GENERATOR'] = 'DEBUG'
env['PYTHONIOENCODING'] = 'utf-8'

print("="*70)
print("RUNNING: rasa shell - capturing ALL output")
print("="*70)

# Start rasa shell
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

print("Waiting for model to load (30s)...")
time.sleep(30)

print("Sending 'Hola'...")
proc.stdin.write(b"Hola\n")
proc.stdin.flush()

time.sleep(25)

print("Sending 'salir'...")
proc.stdin.write(b"salir\n")
proc.stdin.flush()

time.sleep(5)

print("Terminating...")
proc.terminate()
try:
    stdout, _ = proc.communicate(timeout=5)
except:
    proc.kill()
    stdout, _ = proc.communicate()

print()
print("="*70)
print("ALL LINES WITH 'DEBUG' OR 'predict'")
print("="*70)

for line in stdout.decode('utf-8', errors='replace').split('\n'):
    lower = line.lower()
    if 'debug' in lower or 'predict' in lower or 'compactllm' in lower or 'startflow' in lower:
        print(f"  {line[:250]}")

print()
print("="*70)
print("LAST 50 LINES OF OUTPUT (to see what Rasa actually returned)")
print("="*70)
lines = stdout.decode('utf-8', errors='replace').split('\n')
for line in lines[-50:]:
    if line.strip():
        print(f"  {line[:250]}")