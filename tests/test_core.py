import json
from pathlib import Path
import unittest
from decimal import Decimal
from receipt_review.core import fit_model, review, money
class CoreTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.train=[json.loads(x) for x in Path('data/train.jsonl').read_text().splitlines()]
  cls.model=fit_model(cls.train)
  cls.rows=[json.loads(x) for x in Path('data/demo.jsonl').read_text().splitlines()]
 def test_decimal_exact(self): self.assertEqual(money('0.10')+money('0.20'),Decimal('0.30'))
 def test_invalid_money(self):
  for s in ['NaN','Infinity','-1.00','0.001',1.2]:
   with self.subTest(s=s),self.assertRaises(ValueError): money(s)
 def test_clean_receipt(self): self.assertFalse(review(self.model,[self.rows[1]])[0]['review_required'])
 def test_mismatch(self): self.assertIn('total_mismatch',review(self.model,[self.rows[2]])[0]['flags'])
 def test_duplicates(self):
  x=review(self.model,[self.rows[0],self.rows[3]])
  self.assertTrue(all('possible_duplicate' in r['flags'] for r in x))
 def test_unknown_text(self): self.assertIn('unseen_vocabulary',review(self.model,[self.rows[4]])[0]['flags'])
 def test_bad_amount(self): self.assertIn('invalid_amount',review(self.model,[self.rows[5]])[0]['flags'])
 def test_deterministic_fit(self): self.assertEqual(review(self.model,self.rows),review(fit_model(self.train),self.rows))
 def test_duplicate_id(self): self.assertIn('duplicate_id',review(self.model,[self.rows[1],self.rows[1]])[0]['flags'])
if __name__=='__main__':unittest.main()
