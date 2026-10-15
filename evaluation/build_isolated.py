import json
from pathlib import Path
train = {
 'software':['cloud hosting subscription','design software license','developer tool plan','online storage service','web server monthly bill','project management software'],
 'travel':['train ticket business trip','hotel room conference','airline ticket meeting','taxi ride airport','rail fare business travel','flight accommodation booking'],
 'office':['printer paper ink cartridges','office desk stationery','notebooks pens paper','desk chair supplies','printer toner purchase','stationery pencils order'],
 'meals':['restaurant lunch client','business dinner restaurant','cafe coffee discussion','catering team lunch','restaurant meal meeting','sandwiches work lunch'],
 'marketing':['advertising campaign social media','paid search advertisement','promotional flyer printing','sponsored post marketing','search promotion spend','advertising banner campaign'],
 'professional':['legal consultation contract','accounting service invoice','bookkeeping professional service','consultant strategy advice','lawyer legal review','accountant tax preparation']}
test = {
 'software':['usage charge for hosted server instances','renew the annual editing application entitlement','encrypted online backup storage renewal'],
 'travel':['return rail fare to visit customer','overnight accommodation for industry conference','cab transfer from terminal to hotel'],
 'office':['replacement ink for the printer','stationery pack containing pens and notebooks','ergonomic chair for workspace'],
 'meals':['client catch-up over coffee at cafe','team catering for midday meeting','restaurant bill after customer discussion'],
 'marketing':['sponsored search campaign placement','print promotional flyer batch','paid social media audience campaign'],
 'professional':['external accountant prepares monthly books','solicitor reviews a legal contract','independent strategy consultant session']}
unknown=['patient dental checkup','gym membership renewal','charity donation fundraiser','child school tuition','electricity household meter','personal wardrobe shoes','mortgage principal repayment','pet veterinary checkup','concert admission pass','parking fine penalty','passport visa processing','unclassified zxqv blorp']
def rows(d,split):
 return [{'description':s,'category':c,'vendor':f'{split}-vendor-{i}-{c}','template_id':f'{split}-phrase-{i}-{c}'} for c,ss in d.items() for i,s in enumerate(ss)]
for name,r in [('train',rows(train,'train')),('test',rows(test,'test')),('unknown',[{'description':s,'category':'UNKNOWN','vendor':f'unknown-vendor-{i}','template_id':f'unknown-phrase-{i}'} for i,s in enumerate(unknown)])]:
 Path(f'evaluation/{name}.json').write_text(json.dumps(r,indent=2))
