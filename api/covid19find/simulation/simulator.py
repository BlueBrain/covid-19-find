import json
import math
import os
import sys
from datetime import date

import pandas as pd


class Simulator:
    IS_SCENARIO_COUNTERFACTUAL = [False, False, False]

    def __init__(self, covid_repository, parameters_directory="production"):
        self.covid_repository = covid_repository
        self.parameters_directory = parameters_directory

    @staticmethod
    def __map_datapoint(dp):
        return {
            "Date": dp["date"],
            "accumulated_deaths": dp["totalDeaths"],
            "accumulated_cases": dp["totalConfirmed"],
            "tests": 0 if dp["newTests"] is None else dp["newTests"]
        }

    def get_country_df(self, country_code):
        if self.covid_repository.data_for(country_code)==None:
            print('Country data is not up to date')
            print('Please run setupbbp.py')
            sys.exit()
        else:   
            covid_data = self.covid_repository.data_for(country_code)["timeseries"]
        return pd.DataFrame.from_records(list(map(self.__map_datapoint, covid_data)))
