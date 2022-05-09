import sys
import logging
import pickle
import pandas as pd
import click
from src.data import read_data

import prettyprinter as pp

from src.enities.predict_pipeline_params import (
    PredictPipelineParams,
    read_predict_pipeline_params,
)

from src.features import make_features
from src.features.build_features import extract_target, build_transformer
from src.models import (
    train_model,
    serialize_model,
    predict_model,
    evaluate_model,
)
import mlflow

logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
logger.setLevel(logging.INFO)
logger.addHandler(handler)

def predict_pipeline(config_path: str):

    predict_pipeline_params = read_predict_pipeline_params(config_path)

    if predict_pipeline_params.use_mlflow:

        mlflow.set_tracking_uri(predict_pipeline_params.mlflow_uri)
        mlflow.set_experiment(predict_pipeline_params.mlflow_experiment)
        with mlflow.start_run():
            mlflow.log_artifact(config_path)
            model_path, metrics = run_predict_pipeline(predict_pipeline_params)
            mlflow.log_metrics(metrics)
            mlflow.log_artifact(model_path)
    else:
        return run_predict_pipeline(predict_pipeline_params)


def run_predict_pipeline(predict_pipeline_params):
    pp.install_extras(exclude=['ipython', 'django'])
    logger.info(pp.pformat(predict_pipeline_params))

    data = read_data(predict_pipeline_params.input_data_path)
    logger.info(f"Data: {data.shape}")

    model = pickle.load(open(predict_pipeline_params.model_path, 'rb'))

    predicts = predict_model(
        model,
        data,
    )

    pd.DataFrame(predicts).to_csv(predict_pipeline_params.output_predict_path, index=False)

    logger.info(f"Prediction is saved to: {predict_pipeline_params.output_predict_path}")

    return predict_pipeline_params.output_predict_path


@click.command(name="predict_pipeline")
@click.argument("config_path")
def predict_pipeline_command(config_path: str):
    predict_pipeline(config_path)


if __name__ == "__main__":
    predict_pipeline_command()