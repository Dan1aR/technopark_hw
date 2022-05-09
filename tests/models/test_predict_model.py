import os
import pickle
from turtle import shape
from sklearn.metrics import accuracy_score
from sklearn.utils.validation import check_is_fitted
from typing import Tuple

import pandas as pd
import pytest
from py._path.local import LocalPath
from xgboost import XGBClassifier
from src.models.predict_model import predict_model

from src.data.make_dataset import read_data
from src.enities import TrainingParams
from src.enities.feature_params import FeatureParams
from src.features.build_features import make_features, extract_target, build_transformer
from src.models.train_model import train_model
from src.models.serialize_model import serialize_model
from src.models.load_model import load_model
from typing import List


@pytest.fixture
def features_and_target(
    dataset_path: str, categorical_features: List[str], numerical_features: List[str]
) -> Tuple[pd.DataFrame, pd.Series]:
    params = FeatureParams(
        categorical_features=categorical_features,
        numerical_features=numerical_features,
        features_to_drop=[""],
        target_col="target",
    )
    data = read_data(dataset_path)
    transformer = build_transformer(params)
    transformer.fit(data)
    features = make_features(transformer, data)
    target = extract_target(data, params)
    return features, target


def test_predict_model(features_and_target: Tuple[pd.DataFrame, pd.Series]):
    features, target = features_and_target
    model = train_model(features, target, train_params=TrainingParams())
    pred_target = predict_model(model, features)
    assert pred_target.shape == target.shape
    assert accuracy_score(target, pred_target) > 0.5


def test_load_model(features_and_target: Tuple[pd.DataFrame, pd.Series], tmpdir: LocalPath):
    tmp_output = tmpdir.join("model.pkl")
    features, target = features_and_target
    model = train_model(features, target, train_params=TrainingParams())

    model_path = serialize_model(model, tmp_output)
    new_model = load_model(model_path)

    pred_target = predict_model(new_model, features)
    
    assert pred_target.shape == target.shape
    assert accuracy_score(target, pred_target) > 0.5
    assert type(new_model) == type(model)
    