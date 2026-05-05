"""
Run rasa shell and capture output - Python implementation
"""
import subprocess
import sys
import os
import time
import signal

# Environment
env = os.environ.copy()
env['GEMINI_API_KEY'] = 'AIzaSyCx4H6k2WERyL3-j11udVl6slOjhnIPhaA'
env['LLM_API_HEALTH_CHECK'] = 'true'
env['RASALOG'] = 'DEBUG'
env['LOG_LEVEL_LLM_COMMAND_GENERATOR'] = 'DEBUG'
env['PYTHONIOENCODING'] = 'utf-8'

print("="*70)
print("RUNNING: rasa shell with debug logging")
print("="*70)
print("Waiting for model to load (30 seconds)...")

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

print("Waiting for startup...")
time.sleep(20)

print("Sending 'Hola'...")
proc.stdin.write(b"Hola\n")
proc.stdin.flush()

time.sleep(15)

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
print("FILTERED DEBUG OUTPUT")
print("="*70)

keywords = ['prompt_rendered', 'actions_generated', 'StartFlow',
            'llm_command_generator', 'command_generated', 'parse_commands',
            'ERROR', 'exception', 'DEBUG']

found_lines = []
for line in stdout.decode('utf-8', errors='replace').split('\n'):
    line_lower = line.lower()
    for kw in keywords:
        if kw in line_lower:
            found_lines.append(line)
            break

if found_lines:
    for l in found_lines[:60]:
        print(f"  {l[:250]}")
else:
    print("  [NO KEY LINES FOUND - checking raw output instead]")
    # Show last 50 lines anyway
    lines = stdout.decode('utf-8', errors='replace').split('\n')
    for l in lines[-50:]:
        if l.strip():
            print(f"  {l[:250]}")

print()
print("="*70)
print("COMPLETE - Check if StartFlow appears above")
print("="*70)