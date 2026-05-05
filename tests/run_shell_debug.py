"""
Simple test: Run rasa shell and capture output for "Hola"
This is the most direct test of the actual behavior
"""
import subprocess
import sys
import os
import time
import signal

for k, v in [
    ('GEMINI_API_KEY', 'AIzaSyCx4H6k2WERyL3-j11udVl6slOjhnIPhaA'),
    ('LLM_API_HEALTH_CHECK', 'true'),
    ('RASALOG', 'DEBUG'),
    ('LOG_LEVEL_LLM_COMMAND_GENERATOR', 'DEBUG'),
    ('PYTHONIOENCODING', 'utf-8'),
]:
    os.environ[k] = v

print("="*70)
print("RUNNING: rasa shell with debug logging")
print("="*70)
print("Waiting for model to load (约30秒)...")
print("Type 'Hola' and press Enter")
print("Check for lines with: prompt_rendered, actions_generated, StartFlow")
print("="*70)
print()

# Start rasa shell
proc = subprocess.Popen(
    [sys.executable, '-m', 'rasa', 'shell',
     '--model', 'models/20260505-001524-sweet-condenser.tar.gz',
     '--port', '5005'],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    stdin=subprocess.PIPE,
    cwd=os.getcwd(),
    env=dict(os.environ),
)

# Wait for startup
time.sleep(25)

# Send test message
test_input = "Hola\n"
proc.stdin.write(test_input.encode('utf-8'))
proc.stdin.flush()

# Wait for response
time.sleep(15)

# Send exit command
proc.stdin.write(b"salir\n")
proc.stdin.flush()

time.sleep(3)

# Terminate
proc.terminate()
stdout, _ = proc.communicate(timeout=5)

# Filter and print relevant lines
print()
print("="*70)
print("FILTERED DEBUG OUTPUT (lines with key terms)")
print("="*70)

keywords = ['prompt_rendered', 'actions_generated', 'StartFlow', 'llm_command_generator', 'command_generated', 'parse_commands', 'ERROR', 'exception']

for line in stdout.decode('utf-8', errors='replace').split('\n'):
    for kw in keywords:
        if kw.lower() in line.lower():
            print(f"  {line[:200]}")
            break

print()
print("="*70)
print("Check if you see 'StartFlow' in the output above")
print("="*70)