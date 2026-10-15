import json,re,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import numpy as np
from sklearn.metrics import accuracy_score,f1_score
from receipt_review.core import fit_model
read=lambda n: json.loads(Path('evaluation/'+n+'.json').read_text())
train,test,unknown=read('train'),read('test'),read('unknown')
assert not set(r['vendor'] for r in train)&set(r['vendor'] for r in test+unknown)
assert not set(r['template_id'] for r in train)&set(r['template_id'] for r in test+unknown)
assert not set(r['description'] for r in train)&set(r['description'] for r in test+unknown)
model=fit_model(train)
classes=model.classes_.tolist()
keywords={c:set(w for r in train if r['category']==c for w in re.findall(r'(?u)\b\w\w+\b',r['description'].lower())) for c in classes}
def predict(rows,kind):
 desc=[r['description'] for r in rows]
 if kind=='model':
  prob=model.predict_proba(desc);labels=model.classes_[prob.argmax(axis=1)].tolist();scores=prob.max(axis=1)
  reject=(scores<0.65)|(model.steps[0][1].transform(desc).getnnz(axis=1)==0)
 else:
  counts=np.array([[len(set(re.findall(r'(?u)\b\w\w+\b',d.lower()))&keywords[c]) for c in classes] for d in desc])
  labels=[classes[i] for i in counts.argmax(axis=1)]
  reject=(counts.max(axis=1)<2)|((counts==counts.max(axis=1)[:,None]).sum(axis=1)>1)
 return labels,reject
report={'data_kind':'authored synthetic; merchant IDs and exact phrase templates disjoint; shared vocabulary remains; no real-world claim','train_n':len(train),'known_test_n':len(test),'unknown_test_n':len(unknown),'threshold_policy':'0.65 heuristic selected before this split; uncalibrated score; no tuning on test','vendor_overlap':0,'template_overlap':0,'methods':{}}
for kind in ['model','keywords']:
 y,rej=predict(test,kind);uy,ur=predict(unknown,kind);truth=[r['category'] for r in test]
 report['methods'][kind]={'known_accuracy_before_rejection':accuracy_score(truth,y),'known_macro_f1_before_rejection':f1_score(truth,y,average='macro'),'known_rejection_rate':float(rej.mean()),'accepted_known_count':int((~rej).sum()),'accepted_known_accuracy':accuracy_score(np.array(truth)[~rej],np.array(y)[~rej]) if (~rej).any() else None,'unknown_false_acceptance_count':int((~ur).sum()),'unknown_false_acceptance_rate':float((~ur).mean()),'unknown_rejection_rate':float(ur.mean()),'known_details':[dict(r,prediction=v,rejected=bool(b)) for r,v,b in zip(test,y,rej)],'unknown_details':[dict(r,prediction=v,rejected=bool(b)) for r,v,b in zip(unknown,uy,ur)]}
Path('results/isolated-evaluation.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:v for k,v in report.items() if k!='methods'}));print(json.dumps({k:{a:b for a,b in v.items() if not a.endswith('_details')} for k,v in report['methods'].items()}))
