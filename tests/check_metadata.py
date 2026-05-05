import tarfile, json

model_path = 'models/20260505-001524-sweet-condenser.tar.gz'

with tarfile.open(model_path, 'r:gz') as tar:
    for member in tar.getmembers():
        if member.name == 'metadata.json':
            content = tar.extractfile(member).read().decode('utf-8')
            metadata = json.loads(content)

            print('predict_schema keys:', list(metadata.get('predict_schema', {}).keys()))
            
            predict_schema = metadata.get('predict_schema', {})
            
            if 'targets' in predict_schema:
                print('predict_schema targets:', predict_schema['targets'])
            
            if 'graph' in predict_schema:
                graph = predict_schema['graph']
                print('graph keys:', list(graph.keys()) if isinstance(graph, dict) else graph)

            # Check core_target
            print()
            print('core_target:', metadata.get('core_target'))
            
            # List all files in components
            print()
            print('Components in model:')
            for m in tar.getmembers():
                if m.name.startswith('components/') and 'train_' in m.name:
                    parts = m.name.split('/')
                    if len(parts) >= 2:
                        print(f'  {parts[1]}')