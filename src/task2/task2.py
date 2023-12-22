import logging
import os
from typing import List
import pandas as pd
import pathlib as pl
from pandas import DataFrame as DF
from dotenv import load_dotenv
import requests

load_dotenv()
URL_COUNTRIES = os.getenv('URL_COUNTRIES')
URL_AIRPORTS = os.getenv('URL_AIRPORTS')
HOST_ADDRESS = os.getenv('HOST_ADDRESS')

OUTPUT_FILENAME = 'countries_info.csv'

logger_task2 = logging.getLogger()
logger_task2.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s - [%(filename)s:%(funcName)s]')
handler.setFormatter(formatter)
logger_task2.addHandler(handler)

handler = logging.FileHandler(filename=f'{__file__}.log')
handler.setLevel(logging.INFO)
handler.setFormatter(formatter)
logger_task2.addHandler(handler)


def load_dataframes(URL_COUNTRIES:str, URL_AIRPORTS:str)->(DF,DF):
    df_countries = pd.read_csv(URL_COUNTRIES)
    df_airports = pd.read_csv(URL_AIRPORTS)
    return df_countries, df_airports

def get_countries(df_countries:DF, df_airports:DF)->DF:
    df_merged = df_countries.\
        merge(df_airports, left_on='code', right_on='iso_country').\
        rename(dict(name_x='country', name_y='airport'), axis=1)
    countries_with_airports = df_merged[['country','code']].\
                                                            drop_duplicates('country').\
                                                            reset_index(inplace=False,drop=True)
    logger_task2.info(f"Countries, which info to be fetched:\n {countries_with_airports}")
    return countries_with_airports


def fetch_countries_info(countries_with_airports:DF)->DF:
    countries_info = []
    for _, row in countries_with_airports.iterrows():
        iso_code = row['code']
        url = f"http://{HOST_ADDRESS}/countries/{iso_code}"

        response = requests.get(url)
    
        if response.status_code == 200:
            country_data = response.json()
            countries_info.append(country_data)
        else:
            logger_task2.warning(f"Failed to get data for {row['country']} with iso code {iso_code}")

    countries_info = DF(countries_info)
    return countries_info


def store_countries_info(countries_info:DF)->None:
    output_path = pl.Path(pl.Path(__file__).parent,OUTPUT_FILENAME)
    countries_info.to_csv(output_path, index=False) 
    logger_task2.info(f'Saved all countries info to {output_path.as_posix()}')



def main():
    df_countries, df_airports = load_dataframes(URL_COUNTRIES, URL_AIRPORTS)
    countries_with_airports = get_countries(df_countries, df_airports)
    countries_info = fetch_countries_info(countries_with_airports)
    store_countries_info(countries_info)


if __name__ == '__main__':
    main()