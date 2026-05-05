"""
Deep trace: How prompt_template is loaded and used in model
"""
import json
import tarfile
import os

model_path = 'models/20260505-001524-sweet-condenser.tar.gz'

print('='*60)
print('DEEP TRACE: How prompt_template is loaded in model')
print('='*60)

with tarfile.open(model_path, 'r:gz') as tar:
    for member in tar.getmembers():
        if member.name.endswith('config.json'):
            content = tar.extractfile(member).read().decode('utf-8')
            config = json.loads(content)
            print(f'\nFile: {member.name}')
            if 'prompt_template' in content:
                pt = config.get('prompt_template', 'NOT FOUND')
                print(f'  prompt_template: {pt}')
                if 'llm' in config:
                    models = config.get('llm', {}).get('models', [])
                    print(f'  llm.models: {models}')

print()
print('='*60)
print('Checking if custom prompt template file exists')
print('='*60)
template_path = 'prompts/custom-command-template.jinja2'
print(f'Path: {template_path}')
print(f'Exists: {os.path.exists(template_path)}')
if os.path.exists(template_path):
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
        print(f'Size: {len(content)} chars')

print()
print('='*60)
print('Checking how model fingerprint relates to prompt')
print('='*60)

# Check fingerprint in model metadata
with tarfile.open(model_path, 'r:gz') as tar:
    for member in tar.getmembers():
        if 'fingerprint' in member.name.lower() or 'metadata' in member.name.lower():
            content = tar.extractfile(member).read().decode('utf-8', errors='replace')
            print(f'\nFile: {member.name}')
            print(f'Size: {len(content)} chars')
            if len(content) < 5000:
                print(content[:2000])