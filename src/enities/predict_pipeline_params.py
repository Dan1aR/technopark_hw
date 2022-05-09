from dataclasses import dataclass
from .feature_params import FeatureParams
from marshmallow_dataclass import class_schema
import yaml


@dataclass()
class PredictPipelineParams:
    input_data_path: str
    model_path: str
    output_predict_path: str
    use_mlflow: bool = False
    mlflow_uri: str = "http://127.0.0.0/"
    mlflow_experiment: str = "inference_demo"

PredictPipelineParamsSchema = class_schema(PredictPipelineParams)


def read_predict_pipeline_params(path: str) -> PredictPipelineParams:
    with open(path, "r") as file:
        schema = PredictPipelineParamsSchema()
        return schema.load(yaml.safe_load(file))
        