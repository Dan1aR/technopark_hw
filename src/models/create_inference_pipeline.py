from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from typing import Union
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier

SklearClassificationModel = Union[RandomForestClassifier, XGBClassifier]

def create_inference_pipeline(
    model: SklearClassificationModel, transformer: ColumnTransformer
) -> Pipeline:
    return Pipeline([("feature_part", transformer), ("model_part", model)])
