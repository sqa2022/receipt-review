from collections import Counter
from decimal import Decimal, InvalidOperation
import re
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


def fit_model(rows):
    model = make_pipeline(TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True),
                          LogisticRegression(C=4, random_state=17, max_iter=500))
    model.fit([r['description'] for r in rows], [r['category'] for r in rows])
    return model


def money(value):
    if not isinstance(value, str) or not re.fullmatch(r'-?\d+(\.\d{1,2})?', value):
        raise ValueError('Amount must be a decimal string with at most two fractional digits')
    try:
        v = Decimal(value)
    except InvalidOperation as e:
        raise ValueError('Invalid amount') from e
    if v < 0:
        raise ValueError('Negative receipt requires a separate credit-note workflow')
    return v


def review(model, rows, threshold=0.65):
    ids = Counter(r.get('receipt_id', '') for r in rows)
    fingerprints = Counter((str(r.get('vendor', '')).casefold().strip(),
                            r.get('date'), r.get('currency'), r.get('total')) for r in rows)
    output = []
    vectorizer = model.steps[0][1]
    for row in rows:
        description = row.get('description', '')
        flags = []
        if not isinstance(description, str) or not description.strip():
            flags.append('missing_description')
            description = ''
        probabilities = model.predict_proba([description])[0]
        index = int(probabilities.argmax())
        category = str(model.classes_[index])
        confidence = float(probabilities[index])
        if confidence < threshold:
            flags.append('low_model_confidence')
        if vectorizer.transform([description]).nnz == 0:
            flags.append('unseen_vocabulary')
        if not row.get('receipt_id'):
            flags.append('missing_receipt_id')
        elif ids[row['receipt_id']] > 1:
            flags.append('duplicate_id')
        fingerprint = (str(row.get('vendor', '')).casefold().strip(), row.get('date'),
                       row.get('currency'), row.get('total'))
        if fingerprints[fingerprint] > 1:
            flags.append('possible_duplicate')
        if row.get('currency') not in ('USD', 'EUR', 'GBP', 'CNY'):
            flags.append('unsupported_currency')
        try:
            subtotal, tax, total = (money(row[k]) for k in ('subtotal', 'tax', 'total'))
            if subtotal + tax != total:
                flags.append('total_mismatch')
        except (ValueError, KeyError, TypeError):
            flags.append('invalid_amount')
        output.append({**row, 'suggested_category': category, 'model_confidence': confidence,
                       'review_required': bool(flags), 'flags': flags})
    return output
