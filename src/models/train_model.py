from typing import Dict, Union

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier

from src.enities.train_params import TrainingParams

SklearnRegressionModel = Union[RandomForestClassifier, XGBClassifier]


def train_model(
    features: pd.DataFrame, target: pd.Series, train_params: TrainingParams
) -> SklearnRegressionModel:
    if train_params.model_type == "XGBClassifier":
        model = XGBClassifier(eval_metric="auc", seed=train_params.random_state)
    elif train_params.model_type == "RandomForestClassifier":
        model = RandomForestClassifier(n_estimators=100, random_state=train_params.random_state)
    else:
        raise NotImplementedError()
    model.fit(features, target)
    return model

