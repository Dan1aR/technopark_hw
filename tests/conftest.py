import os

import pytest
from typing import List


@pytest.fixture()
def dataset_path():
    curdir = os.path.dirname(__file__)
    return os.path.join(curdir, "train_data_sample.csv")


@pytest.fixture()
def target_col():
    return "target"


@pytest.fixture()
def categorical_features() -> List[str]:
    return [
        "col_5",
        "col_6",
        "col_7",
        "col_8",
        "col_9",
        "col_10",
    ]


@pytest.fixture
def numerical_features() -> List[str]:
    return [
        "col_0",
        "col_1",
        "col_2",
        "col_3",
        "col_4",
    ]


@pytest.fixture()
def features_to_drop() -> List[str]:
    return []
    