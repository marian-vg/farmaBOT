"""Check which Python executable rasa run uses"""
import subprocess
import sys
import os

print("Current Python:", sys.executable)
print("Current process:", os.getpid())

# Check if there's a different Python in the venv
venv_python = ".venv\\Scripts\\python.exe"
print(f"Venv Python exists: {os.path.exists(venv_python)}")

# Run rasa run in a way that prints the Python it uses
env = os.environ.copy()
env['GEMINI_API_KEY'] = 'AIzaSyCx4H6k2WERyL3-j11udVl6slOjhnIPhaA'
env['PYTHONIOENCODING'] = 'utf-8'

# Use -c to trace what Python is being used
proc = subprocess.Popen(
    [sys.executable, '-c', '''
import sys
print(f"Python: {sys.executable}")
print(f"Version: {sys.version}")
import rasa
print(f"Rasa location: {rasa.__file__}")
import rasa.dialogue_understanding.generator.command_parser as cp
print(f"Command parser: {cp.__file__}")
'''],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    cwd=os.getcwd(),
    env=env,
)
stdout, stderr = proc.communicate(timeout=30)
print(stdout.decode('utf-8', errors='replace'))