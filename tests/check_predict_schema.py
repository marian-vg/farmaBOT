import tarfile
import json

model_path = 'models/20260505-001524-sweet-condenser.tar.gz'

with tarfile.open(model_path, 'r:gz') as tar:
    for member in tar.getmembers():
        if member.name == 'metadata.json':
            content = tar.extractfile(member).read().decode('utf-8')
            metadata = json.loads(content)

            print('Predict schema:')
            predict_schema = metadata.get('predict_schema', {})
            print(json.dumps(predict_schema, indent=2)[:3000])