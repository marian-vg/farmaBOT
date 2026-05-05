"""
Check what RegexMessageHandler does and why it's the nlu_target
"""
import tarfile, json

model_path = 'models/20260505-001524-sweet-condenser.tar.gz'

with tarfile.open(model_path, 'r:gz') as tar:
    for member in tar.getmembers():
        if member.name == 'metadata.json':
            content = tar.extractfile(member).read().decode('utf-8')
            metadata = json.loads(content)

            print('nlu_target:', metadata.get('nlu_target'))
            print('core_target:', metadata.get('core_target'))

            # Check if there's a target that includes command_processor
            predict_schema = metadata.get('predict_schema', {})
            nodes = predict_schema.get('nodes', {})

            # Check run_RegexMessageHandler config
            if 'run_RegexMessageHandler' in nodes:
                print()
                print('run_RegexMessageHandler config:')
                print(json.dumps(nodes['run_RegexMessageHandler'], indent=2))

            # Check command_processor
            if 'command_processor' in nodes:
                print()
                print('command_processor config:')
                print(json.dumps(nodes['command_processor'], indent=2))

            # Check if there's something different in trained_at
            print()
            print('trained_at:', metadata.get('trained_at'))
            print('training_type:', metadata.get('training_type'))