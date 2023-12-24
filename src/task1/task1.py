import logging
import os
import pickle
from datetime import datetime
from pathlib import Path
from typing import Any, List, Dict

import pathlib as pl
from pandas import DataFrame as DF
from dotenv import load_dotenv

import pandas as pd
from pandas import DataFrame

from nptyping import NDArray
from nptyping.shape import Shape

np1d = NDArray[Shape["*"], Any]


load_dotenv()

# DATASET_PATH = Path(Path(__file__).parent,'data', f'data_set.csv').as_posix()
DATASET_PATH = os.getenv('DATASET_PATH')
COLUMN_RESPONSE = os.getenv('COLUMN_RESPONSE')
COLUMN_ID = os.getenv('COLUMN_ID')
MODEL_FILENAME = os.getenv('MODEL_FILENAME')


logger_task1 = logging.getLogger()
logger_task1.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s - [%(filename)s:%(funcName)s]')
handler.setFormatter(formatter)
logger_task1.addHandler(handler)

handler = logging.FileHandler(filename=f'{__file__}.log')
handler.setLevel(logging.INFO)
handler.setFormatter(formatter)
logger_task1.addHandler(handler)



class Predictor:
    def __init__(self, model_path: Path,)->None:
        assert model_path.exists(), f"Model object file {model_path} not found"
        with open(model_path.as_posix(), 'rb') as file:
            self.model = pickle.load(file)
        self.predictors = self.model.feature_names_in_

        self.response_col = COLUMN_RESPONSE 
        self.id_col = COLUMN_ID
        self.processing_time = None  # redefined at self.run()
        
    def preprocess_data(self, df_raw: DF) -> DF:
        ##### INTERNAL FUNCTIONS ####################
        def fill_na_with_median(df:DF, cols: list) -> DF:
            for col in cols:
                if col in df.columns:
                    fill_val = df[col].median()
                    df[col].fillna(fill_val, inplace=True)
            return df

        def fill_na_with_unknown(df:DF, cols: list) -> DF:
            df[cols] = df[cols].fillna("onbekend")
            return df

        def fill_na_with_mode(df:DF, cols: list) -> DF:
            for col in cols:
                if col in df.columns:
                    fill_val = df[col].mode().values[0]
                    df[col].fillna(fill_val, inplace=True)
            return df
        ##### INTERNAL FUNCTIONS ####################

        cols_numeric = [
            'BOUWJAAR_PAND',
            'VLOEROPPERVLAK_VERBLIJFSOBJECT',
            'age',
            'electricity_annual_consumption_estimated_offpeak',
            'electricity_annual_consumption_estimated_peak',
            'electricity_annual_consumption_estimated_total',
            'electricity_last_contract_annual_consumption_estimated_offpeak',
            'electricity_last_contract_annual_consumption_estimated_peak',
            'electricity_last_contract_annual_consumption_estimated_total',
            'gas_annual_consumption_estimated',
            'gas_last_contract_annual_consumption_estimated'
        ]
        df_preprocessed = fill_na_with_median(df_raw, cols_numeric)

        cols_string = ['electricity_last_contract_term','province']
        df_preprocessed = fill_na_with_unknown(df_preprocessed, cols_string)

        cols_bool = ['bought_toon', 'has_active_boiler_rent_contract', 'has_active_electricity_contract', 'has_phone_number']
        df_preprocessed = fill_na_with_mode(df_preprocessed, cols_bool)

        assert df_preprocessed.isna().sum().sum() == 0

        df_preprocessed = pd.get_dummies(df_preprocessed, columns=['electricity_last_contract_term','province'], drop_first=True)

        return df_preprocessed


    def batch_predict(self, data: DF) -> np1d:      
        prediction_probability = self.model.predict_proba(data[self.predictors])
        buy_toon_chance = prediction_probability[:,-1]
        return buy_toon_chance
    
    def store_predictions(self, hashed_ids: np1d, buy_toon_chance: np1d)->None:
        prospects = DF(dict(possible_prospect=buy_toon_chance>0.5)) 
        chances = DF(dict(reject_toon_chance=1-buy_toon_chance,buy_toon_chance=buy_toon_chance))
        customer_id = DF(dict(customer_id=hashed_ids))
        df_output = pd.concat(
            [
                customer_id, 
                prospects.reset_index(drop=True),
                chances.reset_index(drop=True)
            ],
                axis=1) \
                    .sort_values(['buy_toon_chance', 'reject_toon_chance'],
                    ascending = [False, True])
        
        output_path = Path(f'{self.processing_time}.csv')
        df_output.to_csv(output_path, index=False)
        logger_task1.info(f"Predictions stored at: {output_path}")

    def process_dataset(self, data: DF):
        if self.response_col not in data:
            data[self.response_col] = False
        data = data[data[self.response_col]==False]
        data = data.drop(self.response_col, axis=1)
        hashed_ids = data[self.id_col].values

        df_preprocessed = self.preprocess_data(data)

        buy_toon_chance = self.batch_predict(df_preprocessed)

        self.store_predictions(hashed_ids, buy_toon_chance,)

    def run(self, dataset_path: str):
        self.processing_time = datetime.now().strftime("%Y%m%d_%H_%M_%S")  # NB: will overwrite if processing < 1 sec
        logger_task1.info(f'Reading data from {dataset_path}...')
        data = pd.read_csv(dataset_path, sep=',')
        self.process_dataset(data)


if __name__ == "__main__":
    predictor = Predictor(Path(Path(__file__).parent,'models', MODEL_FILENAME))
    predictor.run(DATASET_PATH)
