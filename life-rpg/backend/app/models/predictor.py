# lightweight wrapper over a joblib model to keep example code simple
from joblib import load
import os


class LifeModel:
def __init__(self, model):
self.model = model


@classmethod
def load(cls, path: str):
# path should point to a .joblib file. If missing, use a trivial fallback.
if not os.path.exists(path):
# fallback dummy model
class Dummy:
def predict(self, X):
return [0 for _ in X]
def predict_proba(self, X):
return [[0.7, 0.3] for _ in X]
return cls(Dummy())
m = load(path)
return cls(m)


def predict_single(self, features: list):
# features: list of numeric values -> returns prediction or probability
X = [features]
if hasattr(self.model, "predict_proba"):
proba = self.model.predict_proba(X)
return {"probability": proba[0]}
pred = self.model.predict(X)
return {"prediction": pred[0]}