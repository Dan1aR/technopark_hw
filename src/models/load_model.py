import pickle
from typing import Union

from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier

SklearnClassificationModel = Union[RandomForestClassifier, XGBClassifier]

def load_model(
    model_path: str
) -> SklearnClassificationModel:
    model = pickle.load(open(model_path, 'rb'))
    return model
