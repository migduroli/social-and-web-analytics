import uvicorn

from datetime import datetime
from typing import NoReturn, List, Dict
from fastapi import FastAPI
from pydantic import BaseModel, Field

from mlapi.utils import models, salute


class XLogReg(BaseModel):
    x: List[Dict]


app = FastAPI(
    title="My first API",
    docs_url="/",
)


@app.get(path="/salute")
def hello_world(name: str = None) -> dict:
    """Returns a "Hello World" message with World replaced
    by a name if this exists
    """
    return {
        "metadata": {
            "date": datetime.now(),
        },
        "response": {
            "status": 202,
            "text": salute.hello_world(name)
        }
    }


@app.get(path="/model/logreg/info")
def get_logreg_model_info() -> dict:
    return {
        "metadata": None,
        "response": models.get_logreg_model_info(),
    }


@app.get(path="/model/logreg/predict")
def get_logreg_predict(
        gmat: float,
        gpa: float,
        work_experience: int
):
    return {
        "metadata": {
            "model": "logreg",
            "params":  models.get_logreg_model_info(),
        },
        "response": {
            "predict": models.get_logreg_predict(
                gmat=gmat,
                gpa=gpa,
                work_experience=work_experience,
            )
        }
    }


@app.post(path="/model/logreg/batch_predict")
def get_logreg_batch_predict(data: XLogReg):
    return {
        "metadata": {
            "model": "logreg",
            "params":  models.get_logreg_model_info(),
        },
        "response": {
            "predict": models.get_logreg_batch_predict(
                data=data.x
            )
        }
    }


def main():
    uvicorn.run(
        "mlapi.main:app",
        debug=False,
        reload=True,
        port=8080,
        log_level="debug",
    )


if __name__ == "__main__":
    main()
