import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from receipt_review.core import fit_model,review
rows=json.loads(Path('evaluation/train.json').read_text());model=fit_model(rows);vec,clf=model.steps[0][1],model.steps[1][1]
x={'vocab':vec.vocabulary_,'idf':vec.idf_.tolist(),'weights':clf.coef_.tolist(),'bias':clf.intercept_.tolist(),'classes':clf.classes_.tolist()}
demo=[json.loads(s) for s in Path('data/demo.jsonl').read_text().splitlines()]
s=Path('web/template.html').read_text().replace('__MODEL__',json.dumps(x)).replace('__DEMO__',json.dumps(demo))
Path('web/receipt-review.html').write_text(s)
Path('results/ui-python-reference.json').write_text(json.dumps(review(model,demo),indent=2))

Path('docs').mkdir(exist_ok=True)
Path('docs/index.html').write_text(s)
