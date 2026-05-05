"""
Run rasa shell with DEBUG logging to capture instrumented output
"""
import subprocess
import sys
import os
import time

# Environment with debug flags
env = os.environ.copy()
env['GEMINI_API_KEY'] = 'AIzaSyCx4H6k2WERyL3-j11udVl6slOjhnIPhaA'
env['LLM_API_HEALTH_CHECK'] = 'true'
env['RASALOG'] = 'DEBUG'
env['LOG_LEVEL_LLM_COMMAND_GENERATOR'] = 'DEBUG'
env['PYTHONIOENCODING'] = 'utf-8'

print("="*70)
print("RUNNING: rasa shell with DEBUG instrumentation")
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

print("Waiting for model to load (25s)...")
time.sleep(25)

print("Sending 'Hola'...")
proc.stdin.write(b"Hola\n")
proc.stdin.flush()

time.sleep(20)

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
print("FILTERED DEBUG OUTPUT (DEBUG_ lines)")
print("="*70)

for line in stdout.decode('utf-8', errors='replace').split('\n'):
    if 'DEBUG_' in line or 'DEBUG predict' in line.lower() or 'DEBUG should' in line.lower():
        print(f"  {line[:300]}")

print()
print("="*70)
print("CHECK ABOVE FOR:")
print("  - DEBUG_predict_commands.enter")
print("  - DEBUG_should_skip_llm_call")
print("  - DEBUG_predict_commands.filtered_flows")
print("  - DEBUG_predict_commands.prompt_rendered")
print("  - DEBUG_predict_commands.calling_llm")
print("  - DEBUG_predict_commands.llm_response")
print("="*70)