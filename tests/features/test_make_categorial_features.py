import numpy as np
from typing import List
import pandas as pd
import pytest

from src.features.build_features import process_categorical_features


@pytest.fixture()
def categorical_feature() -> str:
    return "categorical_feature"


@pytest.fixture()
def categorical_values() -> List[str]:
    return ["1", "2", "3", np.nan]

@pytest.fixture
def fake_categorical_data(
    categorical_feature: str, categorical_values: List[str]
) -> pd.DataFrame:
    return pd.DataFrame({categorical_feature: categorical_values})


def test_process_categorical_features(
    fake_categorical_data: pd.DataFrame,
    categorical_feature: str,
    categorical_values: List[str],
):
    transformed = process_categorical_features(fake_categorical_data)
    assert transformed.shape[0] == 4
    assert transformed.notna().to_numpy().all()
