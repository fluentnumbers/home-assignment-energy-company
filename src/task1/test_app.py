"""This script can be used to test the FastAPi endpoints from app.py (running locally or in a container)
"""
import os

import numpy as np
import pandas as pd
import requests
from dotenv import load_dotenv
from pandas import DataFrame as DF

load_dotenv()

DATASET_PATH = os.getenv("DATASET_PATH")
FASTAPI_PORT = os.getenv("FASTAPI_PORT")


def predict_batch():
    """Run predictive model on data from a csv file (batch)"""
    data = pd.read_csv(DATASET_PATH)
    # TODO: fix the issue with nan-serialization INSIDE the app or INSIDE the Predictor class
    data = data.fillna(np.nan).replace([np.nan], [None])
    data = data.to_dict(orient="records")

    response = requests.post(
        f"http://127.0.0.1:{FASTAPI_PORT}/predict_batch",
        timeout=30,
        json=data,
    )
    if response.status_code == 200:
        print(
            f"-----Returned {response.status_code}-----\n \
                {DF(response.json()['result'])}"
        )
    else:
        print(
            f"-----Returned {response.status_code}-----\n \
            {response.reason}: {response.json()['detail']}"
        )
    return response.status_code


def predict():
    """Run predictive model on data from a csv file (batch) line by line (single datapoint each time)"""
    data = pd.read_csv(DATASET_PATH)
    data = data.fillna(np.nan).replace([np.nan], [None])
    data = data.to_dict(orient="records")

    for row in data:
        response = requests.post(
            f"http://127.0.0.1:{FASTAPI_PORT}/predict",
            timeout=30,
            json=row,
        )
        if response.status_code == 200:
            print(
                f"-----Returned {response.status_code}-----\n \
                  {DF(response.json()['result'])}"
            )
        else:
            print(
                f"-----Returned {response.status_code}-----\n \
                {response.reason}: {response.json()['detail']}"
            )
    return response.status_code


if __name__ == "__main__":
    predict_batch()
