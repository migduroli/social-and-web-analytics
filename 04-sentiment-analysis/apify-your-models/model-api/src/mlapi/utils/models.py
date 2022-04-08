import pickle

import pandas as pd
from typing import List, Dict


class ModelPaths:
    _root = "models"
    logreg = f"{_root}/logreg/model.pkl"


def load_model(path: str):
    with open(path, "rb") as file:
        return pickle.load(file)


def get_logreg_model_info():
    model = load_model(path=ModelPaths.logreg)
    return model.get_params()


def get_logreg_predict(
        gmat: float,
        gpa: float,
        work_experience: int,
) -> list:
    model = load_model(path=ModelPaths.logreg)
    x = pd.DataFrame(
        {
            "gmat": [gmat],
            "gpa": [gpa],
            "work_experience": [work_experience]
        }
    )
    return model.predict(x).astype(bool).tolist()


def get_logreg_batch_predict(
        data: List[Dict]
) -> list:
    x = pd.DataFrame(data)
    model = load_model(path=ModelPaths.logreg)
    return model.predict(x).astype(bool).tolist()
