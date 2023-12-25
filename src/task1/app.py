import os
from pathlib import Path
from typing import Any, Dict, List

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Response, status
from fastapi.concurrency import asynccontextmanager
from fastapi.responses import RedirectResponse
from pandas import DataFrame as DF
from tools.logger import service_logger as logger
from tools.state import State

from task1 import Predictor

load_dotenv()

MODEL_FILENAME = os.getenv("MODEL_FILENAME")
FASTAPI_PORT = int(os.getenv("FASTAPI_PORT"))
DATASET_PATH = os.getenv("DATASET_PATH")

state = State()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # executed prior requests handling: load the model
    predictor = Predictor(Path(Path(__file__).parent, "models", MODEL_FILENAME), store_as_csv=False)
    yield
    # Executed on shutdown: cleaning up
    state.set_ready_status(False)
    state.set_live_status(False)
    logger.info("Service shuted down !")


app = FastAPI(debug=True, lifespan=lifespan)
state.set_live_status(True)
state.set_ready_status(True)


# TODO: implement Pydantic models and data quality checks
# TODO: prettify docstrings


@app.post("/test")
def test(data: List[Dict[Any, Any]] = [dict(one=1, two=2), dict(three=3, four=4)]) -> List[Dict]:
    """Dummy endpoint returning the inputs, easy testing from the FastAPI docs GUI

    Args:
        data (List[Dict[Any, Any]], optional): _description_. Defaults to [dict(one=1,two=2),dict(three=3,four=4)].

    Returns:
        Dict: _description_
    """
    return data


@app.post("/predict")
async def predict(data: Dict[str, Any]) -> Dict:
    """!NotImplemented! Predict a single datapoint

    Args:
        data (Dict[str, Any]): _description_

    Raises:
        HTTPException: _description_
        HTTPException: _description_

    Returns:
        Dict: _description_
    """
    raise HTTPException(
        status_code=501,
        detail="/predict endpoint to process a single datapoint is not implemented.\
                         Preprocessing fails, if no non-NaN values in any of the columns",
    )
    try:
        df = DF(data, index=[0])
        predictor = Predictor(
            Path(Path(__file__).parent, "models", MODEL_FILENAME), store_as_csv=False
        )
        df_output = predictor.process_dataset(df)
        df_output = df_output.to_dict(orient="records")
        return {"result": df_output}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/predict_batch")
async def predict_batch(data: List[Dict[str, Any]]) -> Dict:
    """Make a batch-prediction. See test_app.py/predict_batch() for example

    Args:
        data (List[Dict[str, Any]]): DF serialized to a list of dict, row by row

    Raises:
        HTTPException: _description_

    Returns:
        Dict: _description_
    """
    try:
        df = DF(data)
        predictor = Predictor(
            Path(Path(__file__).parent, "models", MODEL_FILENAME), store_as_csv=False
        )
        df_output = predictor.process_dataset(df)
        df_output = df_output.to_dict(orient="records")
        return {"result": df_output}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Service-side endpoints
@app.get("/health/liveness", tags=["observability"])
def liveness(response: Response) -> Dict:
    """Liveness probe endpoint."""
    _status = state.get_live_status()
    if _status:
        response.status_code = status.HTTP_200_OK
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
    return {"liveness": _status}


@app.get("/health/readiness", tags=["observability"])
def readiness(response: Response) -> Dict:
    """Readiness probe endpoint."""
    _status = state.get_ready_status()
    if _status:
        response.status_code = status.HTTP_200_OK
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
    return {"readiness": _status}


@app.get("/", tags=["redirect"])
def redirect_docs():
    """Redirect on SwaggerUI."""
    logger.info("Request to docs.")
    return RedirectResponse(url="/docs")


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=FASTAPI_PORT, log_level="info")
