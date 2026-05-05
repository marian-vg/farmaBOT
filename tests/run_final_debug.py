import subprocess, sys, os, time

env = os.environ.copy()
env['GEMINI_API_KEY'] = 'AIzaSyCx4H6k2WERyL3-j11udVl6slOjhnIPhaA'
env['LLM_API_HEALTH_CHECK'] = 'true'
env['RASALOG'] = 'DEBUG'
env['PYTHONIOENCODING'] = 'utf-8'

DEBUG_LOG = 'C:/Users/Administrador/Herd/farmarag-rasa/debug_predict.log'
if os.path.exists(DEBUG_LOG):
    os.remove(DEBUG_LOG)

print('Starting rasa shell...')
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

print('Waiting 35s...')
time.sleep(35)

print('Sending Hola...')
try:
    proc.stdin.write(b'Hola\n')
    proc.stdin.flush()
except Exception as e:
    print(f'Error: {e}')

time.sleep(20)

# Check debug log
if os.path.exists(DEBUG_LOG):
    print('DEBUG LOG EXISTS!')
    with open(DEBUG_LOG, 'r', encoding='utf-8') as f:
        print(f.read())
else:
    print('DEBUG LOG NOT CREATED')

proc.terminate()
stdout, _ = proc.communicate(timeout=5)