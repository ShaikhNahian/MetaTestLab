"""
Author: Shaikh Nahian
Since: Dec 2025
"""
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_classification


# INTERNAL: model training

def _train_model():
    X, y = make_classification(
        n_samples=500,
        n_features=3,
        n_informative=3,
        n_redundant=0,
        random_state=42
    )

    model = LogisticRegression()
    model.fit(X, y)
    return model


_MODEL = _train_model()


# PREPROCESSING


def _normalize_copy(features):
    """Correct preprocessing (no mutation)."""
    features = np.array(features, dtype=float)
    return (features - features.mean()) / (features.std() + 1e-8)


def _normalize_in_place(features):
    """BUGGY preprocessing: mutates input."""
    mean = sum(features) / len(features)
    std = (sum((x - mean) ** 2 for x in features) / len(features)) ** 0.5 + 1e-8

    for i in range(len(features)):
        features[i] = (features[i] - mean) / std

    return features


# SYSTEMS UNDER TEST


def predict_clean(features):
    processed = _normalize_copy(features)
    processed = processed.reshape(1, -1)
    return int(_MODEL.predict(processed)[0])


def predict_with_buggy_preprocessing(features):
    processed = _normalize_in_place(features)  # mutates input!
    processed = np.array(processed).reshape(1, -1)
    return int(_MODEL.predict(processed)[0])

def predict_proba_clean(features):
    """
    Returns probability of class 1 (float in [0,1]).
    Uses correct preprocessing.
    """
    processed = _normalize_copy(features)
    processed = processed.reshape(1, -1)
    return float(_MODEL.predict_proba(processed)[0][1])


def predict_proba_buggy(features):
    """
    Returns probability of class 1.
    Uses buggy preprocessing (mutates input).
    """
    processed = _normalize_in_place(features)
    processed = np.array(processed).reshape(1, -1)
    return float(_MODEL.predict_proba(processed)[0][1])


predict = predict_clean
predict_buggy = predict_with_buggy_preprocessing