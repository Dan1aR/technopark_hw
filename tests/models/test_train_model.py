import os
import pickle
from sklearn.utils.validation import check_is_fitted
from typing import Tuple

import pandas as pd
import pytest
from py._path.local import LocalPath
from xgboost import XGBClassifier

from src.data.make_dataset import read_data
from src.enities import TrainingParams
from src.enities.feature_params import FeatureParams
from src.features.build_features import make_features, extract_target, build_transformer
from src.models.train_model import train_model
from src.models.serialize_model import serialize_model
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


def test_train_model(features_and_target: Tuple[pd.DataFrame, pd.Series]):
    features, target = features_and_target
    model = train_model(features, target, train_params=TrainingParams())
    assert type(model) == XGBClassifier
    check_is_fitted(model)


def test_serialize_model(tmpdir: LocalPath):
    expected_output = tmpdir.join("model.pkl")
    n_estimators = 20
    model = XGBClassifier(n_estimators=n_estimators)
    real_output = serialize_model(model, expected_output)
    assert real_output == expected_output
    assert os.path.exists
    with open(real_output, "rb") as f:
        model = pickle.load(f)
    assert type(model) == XGBClassifier
