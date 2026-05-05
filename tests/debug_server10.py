"""
Run rasa directly as module subprocess to test
"""
import subprocess
import sys
import os
import time

env = os.environ.copy()
env['GEMINI_API_KEY'] = 'AIzaSyCx4H6k2WERyL3-j11udVl6slOjhnIPhaA'
env['PYTHONIOENCODING'] = 'utf-8'

print('Starting rasa server as subprocess...')

proc = subprocess.Popen(
    [sys.executable, '-m', 'rasa', 'run',
     '--model', 'models/20260505-001524-sweet-condenser.tar.gz',
     '--port', '5005',
     '--enable-api'],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    cwd=os.getcwd(),
    env=env,
)

# Wait for startup
time.sleep(55)

# Check process
if proc.poll() is not None:
    out, err = proc.communicate(timeout=5)
    print('Process exited!')
    print(out.decode('utf-8', errors='replace')[:3000])
else:
    print('Process still running')

    # Send test request
    import requests
    try:
        resp = requests.post(
            'http://localhost:5005/webhooks/rest/webhook',
            json={'sender': 'test', 'message': 'Hola'},
            timeout=30
        )
        print(f'Webhook response: {resp.status_code}')
        print(f'Body: {resp.text[:300]}')
    except Exception as e:
        print(f'Webhook error: {e}')

    time.sleep(5)

    # Read output
    try:
        import select
        if select.select([proc.stdout], [], [], 0)[0]:
            lines = proc.stdout.read().decode('utf-8', errors='replace')
            print('Output:')
            print(lines[:2000])
    except:
        pass

    proc.terminate()
    proc.communicate(timeout=5)