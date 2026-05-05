"""
Run rasa shell and check for debug log file
"""
import subprocess
import sys
import os
import time

# Environment
env = os.environ.copy()
env['GEMINI_API_KEY'] = 'AIzaSyCx4H6k2WERyL3-j11udVl6slOjhnIPhaA'
env['LLM_API_HEALTH_CHECK'] = 'true'
env['RASALOG'] = 'DEBUG'
env['PYTHONIOENCODING'] = 'utf-8'

DEBUG_LOG = "C:/Users/Administrador/Herd/farmarag-rasa/debug_predict.log"

# Delete old log
if os.path.exists(DEBUG_LOG):
    os.remove(DEBUG_LOG)
    print(f"Deleted old {DEBUG_LOG}")

print("="*70)
print("RUNNING: rasa shell with file-based debug logging")
print("="*70)

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

print("Waiting for model load (30s)...")
time.sleep(30)

print("Sending 'Hola'...")
proc.stdin.write(b"Hola\n")
proc.stdin.flush()

time.sleep(20)

print("Sending 'salir'...")
proc.stdin.write(b"salir\n")
proc.stdin.flush()

time.sleep(5)

proc.terminate()
try:
    stdout, _ = proc.communicate(timeout=5)
except:
    proc.kill()
    stdout, _ = proc.communicate()

print()
print("="*70)
print("CHECKING DEBUG LOG FILE")
print("="*70)

if os.path.exists(DEBUG_LOG):
    print(f"{DEBUG_LOG} EXISTS!")
    with open(DEBUG_LOG, 'r', encoding='utf-8') as f:
        content = f.read()
    print(f"Content ({len(content)} chars):")
    print('-'*60)
    print(content[:3000])
    print('-'*60)
else:
    print(f"{DEBUG_LOG} does not exist - predict_commands was never called!")

print()
print("LAST 30 LINES OF Rasa OUTPUT:")
print('='*60)
lines = stdout.decode('utf-8', errors='replace').split('\n')
for line in lines[-30:]:
    if line.strip():
        print(f"  {line[:200]}")