from typing import Optional

from dataclasses import dataclass

from .download_params import DownloadParams
from .split_params import SplittingParams
from .feature_params import FeatureParams
from .train_params import TrainingParams
from marshmallow_dataclass import class_schema
import yaml


@dataclass()
class TrainingPipelineParams:
    input_data_path: str
    output_model_path: str
    metric_path: str
    splitting_params: SplittingParams
    feature_params: FeatureParams
    train_params: TrainingParams
    downloading_params: Optional[DownloadParams] = None
    use_mlflow: bool = False
    mlflow_uri: str = "http://127.0.0.0/"
    mlflow_experiment: str = "inference_demo"


TrainingPipelineParamsSchema = class_schema(TrainingPipelineParams)


def read_training_pipeline_params(path: str) -> TrainingPipelineParams:
    with open(path, "r") as file:
        schema = TrainingPipelineParamsSchema()
        return schema.load(yaml.safe_load(file))
        
        