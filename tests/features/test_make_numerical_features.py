import numpy as np
import pandas as pd
import pytest
from typing import List

from src.features.build_features import process_numerical_features


@pytest.fixture()
def numerical_feature() -> str:
    return "numerical_feature"


@pytest.fixture()
def numerical_values() -> List[str]:
    return [1, 2, 3, np.nan]

@pytest.fixture
def fake_numerical_data(
    numerical_feature: str, numerical_values: List[str]
) -> pd.DataFrame:
    return pd.DataFrame({numerical_feature: numerical_values})


def test_process_numerical_features(
    fake_numerical_data: pd.DataFrame,
    numerical_feature: str,
    numerical_values: List[str],
):
    transformed = process_numerical_features(fake_numerical_data)
    assert transformed.shape[0] == 4
    assert transformed.notna().to_numpy().all()
