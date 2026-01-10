import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_classification

# Train once, reuse as black-box
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


def predict(features):
    """
    Black-box ML system under test.
    features: list or np.array of shape (n_features,)
    """
    features = np.array(features).reshape(1, -1)
    return _MODEL.predict(features)[0]
