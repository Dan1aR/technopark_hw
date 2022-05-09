from src.data.make_dataset import read_data, split_train_val_data
from src.enities import SplittingParams

def test_load_dataset(dataset_path: str, target_col: str):
    data = read_data(dataset_path)
    assert len(data) == 10000
    assert target_col in data.keys()


def test_split_dataset(dataset_path: str):
    val_size = 0.3
    splitting_params = SplittingParams(random_state=42, val_size=val_size)
    data = read_data(dataset_path)
    train, val = split_train_val_data(data, splitting_params)
    assert train.shape[0] == 7000
    assert val.shape[0] == 3000
