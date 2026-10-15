# Receipt Review

An offline expense-review desk for freelancers and bookkeepers. Import structured receipts, inspect amount discrepancies and candidate duplicates, choose categories, and export the reviewed records with a decision trail.

## Open the demo

[Try the live review desk](https://receipt-review.flowypanda.chatgpt.site/)

Open `docs/index.html` in a browser. The complete interface, synthetic six-receipt demo and fitted classifier are embedded in that file. No installation, account, API key or inference service is required. The file makes no external requests.

To serve it locally: `python -m http.server 8000 --directory docs`, then open http://localhost:8000 . For GitHub Pages, select the repository's default branch and `/docs` directory in Settings → Pages.

1. Load or import `data/demo.csv` or `data/demo.jsonl`.
2. Inspect S1/S4's duplicate candidate, S3's four-unit discrepancy and S6's invalid amount.
3. Change S5 to `other / unknown`, add a review note and confirm the records.
4. Export reviewed CSV and audit JSON before closing the tab.

## How it works

A scikit-learn TF-IDF + logistic-regression model suggests six expense categories. Its vocabulary, IDF values and classifier weights are exported into the standalone browser file. Amount validation uses integer cents in JavaScript and Decimal in Python. Category suggestions remain separate from the reviewer's final decision; duplicate candidates are never deleted automatically.

CSV/JSONL fields are strings: `receipt_id`, `description`, `vendor`, `date`, `currency`, `subtotal`, `tax`, `total`. Amounts must be nonnegative decimal strings with at most two fractional digits. The app accepts up to 5 MB and 10,000 rows, supports quoted CSV and neutralizes spreadsheet-formula prefixes on export. Review decisions stay in tab memory until export. Input is structured data; receipt-image OCR and currency conversion are outside the current workflow.

## Reproduce the model and checks

Use Python 3.12 and Node.js. Install the pinned Python packages with `python -m pip install -r requirements.lock`.

```sh
python evaluation/build_isolated.py
python evaluation/run.py
python web/build.py
node web/test.cjs
python -m unittest discover -s tests -v
python -m receipt_review --input data/demo.jsonl --output results/review.json
```

`web/build.py` regenerates `web/receipt-review.html` and `docs/index.html`. Model weights are embedded in both files; no binary model download is needed. `evaluation/train.json` is the current 36-description training set; `data/train.jsonl` is retained for the original core regression tests.

## Evaluation

The current model and keyword baseline use 36 synthetic training descriptions, 18 known-category test descriptions and 12 unknown-category descriptions. Vendor identifiers and exact templates are disjoint between training and evaluation; category vocabulary overlaps. Known-category predictions before rejection were 18/18 for the classifier and 17/18 for keywords.

The uncalibrated 0.65 review heuristic rejected all 18 known examples and all 12 unknown examples. The keyword rule rejected five known examples and all unknown examples. Every record therefore remains a human review decision; the score is not an automatic approval policy. These checks describe synthetic examples, not measured performance on customer receipts.

13 JavaScript check groups and nine Python tests pass. JavaScript checks cover model agreement with Python, exact cents, duplicate groups, amount errors, review/export roundtrip, CSV formula safety and malformed CSV rejection. Browser/Python model-score disagreement on the six demo descriptions is at most 2.22e-16.

## License

Source: MIT. Original synthetic data: CC0-1.0. See `THIRD_PARTY.md` for dependency licenses and data provenance.
