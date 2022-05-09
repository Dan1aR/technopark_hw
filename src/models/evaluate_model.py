import numpy as np
import pandas as pd
from typing import Dict
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

def evaluate_model(
    predicts: np.ndarray, target: pd.Series, model_type: str,
) -> Dict[str, float]:
    return {
        "model": model_type, 
        "accuracy_score": accuracy_score(target, predicts),
        "precision_score": precision_score(target, predicts),
        "recall_score": recall_score(target, predicts),
        "f1_score": f1_score(target, predicts),
    }

