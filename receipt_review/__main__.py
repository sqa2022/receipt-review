import argparse
import json
from pathlib import Path
from .core import fit_model, review

p = argparse.ArgumentParser(description='Offline receipt suggestions and review queue; no network calls')
p.add_argument('--train', default='evaluation/train.json')
p.add_argument('--input', default='data/demo.jsonl')
p.add_argument('--output', default='results/review.json')
p.add_argument('--config', default='configs/default.json')
p.add_argument('--threshold', type=float)
a = p.parse_args()
def read(path):
    text = Path(path).read_text()
    return json.loads(text) if text.lstrip().startswith('[') else [json.loads(line) for line in text.splitlines() if line.strip()]
config = json.loads(Path(a.config).read_text())
threshold = a.threshold if a.threshold is not None else config['review_confidence_threshold']
if not 0 <= threshold <= 1:
    p.error('threshold must lie between 0 and 1')
rows = review(fit_model(read(a.train)), read(a.input), threshold)
Path(a.output).parent.mkdir(parents=True, exist_ok=True)
Path(a.output).write_text(json.dumps(rows, indent=2))
print(json.dumps({'records': len(rows), 'review_required': sum(r['review_required'] for r in rows), 'output': a.output}))
