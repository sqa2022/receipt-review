---
title: Receipt Review: keep the decision, not just the category
published: false
tags: devchallenge, hf26challenge
---

*This is a submission for the [Hacktoberfest Open-Source AI Challenge Week 2: Side Hustle](https://dev.to/challenges/hacktoberfest-week2-2026-10-12).*

## What I Built

Receipt Review is a local review desk for a freelancer getting expenses ready for a bookkeeper. It brings the awkward cases into one place: totals that do not add up, records that might be duplicates, and descriptions that need a human category choice.

A category label alone is not enough to resolve those cases. If a receipt says 15.00 while its subtotal and tax add up to 11.00, the reviewer needs to see the four-unit difference. If two hosting charges match, deleting one may erase a legitimate expense. The desk explains the amount check, groups the duplicate candidates, and lets the reviewer keep a note and a decision alongside the original record.

The side-hustle opportunity is a focused expense-preparation tool for freelancers and small bookkeeping practices: fewer unexplained rows to chase, with client descriptions kept on the reviewer's own computer.

## Demo

[Open the live demo](https://receipt-review.flowypanda.chatgpt.site/) — load the six sample receipts and try the review workflow in your browser.

The demo is one self-contained HTML file: `docs/index.html` in the [public repository](https://github.com/sqa2022/receipt-review). Download and open it, or serve the `docs` directory as a static page. The model, interface and six synthetic example receipts are included.

Try this short review:

1. Load the six demo receipts, or import the supplied CSV or JSONL.
2. Inspect S1 and S4 in the duplicate group. Both remain in the file.
3. Open S3's amount explanation: 10.00 + 1.00 versus a stated 15.00. S6 demonstrates invalid decimal input.
4. Change S5 to “other / unknown,” add a note and confirm the review.
5. Export the reviewed CSV and the separate audit JSON.

The exported table preserves source amounts, suggested and final categories, confirmation status and notes. CSV fields are quoted and spreadsheet-formula prefixes are neutralized. Decisions remain in the tab until exported.

## Code

[Source code and reproducible examples](https://github.com/sqa2022/receipt-review)

The repository includes the standalone browser desk, Python implementation, model-export script, synthetic training and evaluation data, pinned dependencies and tests. The source is MIT licensed; the original synthetic records are CC0.

## How I Built It

The open-source AI component is scikit-learn: TF-IDF features and logistic regression suggest six expense categories. I export the vocabulary, IDF values and classifier weights to JavaScript, so inference runs inside the browser. No API key or inference server is involved. On the six demo descriptions, the largest score difference between Python and JavaScript was 2.22 × 10⁻¹⁶.

The arithmetic and review rules stay deterministic. Python uses Decimal; the browser uses integer cents. Matching vendor, date, currency and total creates a duplicate candidate, while a shared receipt ID creates another reason to inspect. Category changes and confirmations are recorded separately from the original inputs.

I compared the classifier with a keyword baseline on 18 synthetic descriptions held apart from the 36 training descriptions by merchant identifier and exact phrase template. Before rejection, the classifier matched 18/18 category labels and keywords matched 17/18. A separate 12-description unknown-category set checks rejection. Shared category vocabulary makes these integration checks rather than a measure of real receipt accuracy.

The rejection check informed the interaction design. The uncalibrated 0.65 heuristic rejected all 18 known examples as well as all 12 unknown examples. Instead of treating that score as permission to approve an expense, the interface keeps a suggestion visible and asks for a review decision. Exact totals, duplicate candidates and notes provide the explanation the score cannot supply.

Thirteen JavaScript check groups and nine Python tests cover model agreement, decimal arithmetic, duplicate detection, invalid input and reviewed CSV export. CSV validation also rejects malformed quotes, extra fields and duplicate column names after BOM normalization.

## Why Does Open Innovation Matter?

For this workflow, the open model makes the cost and data path simple. The features and weights ship with the application. A reviewer can inspect a suggestion, replace the training examples and rebuild the same desk without sending receipt descriptions to a third party or paying for each inference.

That makes the tool practical to distribute as a single file. The model helps organize the queue; the reviewer keeps the decision and its explanation.

## Prize Categories

Overall prize.
