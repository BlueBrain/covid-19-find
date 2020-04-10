import pycountry
import numpy as np
import pandas as pd


def convert_to_numeric(country_key, data):
    codes = data[country_key].values
    numeric = []
    for code in codes:
        country = pycountry.countries.get(alpha_3=code)
        if country is None:
            numeric.append(None)
        else:
            numeric.append(np.int64(country.numeric))
    data[country_key] = numeric
    return data


defaults = {"this_year": "2020"}

total_pop = {"country": "Country code",
            "name": "Region, subregion, country or area *",
            "units": 1e3,
            "data": pd.read_csv("./data/total_pop.csv")}

age_distr = {"country": "LocID",
            "name": "Location",
            "year": "Time",
            "age": "AgeGrp",
            "total_pop": "PopTotal",
            "units": 1e3,
            "data": pd.read_csv("./data/age_distr.csv")}

pcnt_urban = {"country": "Country Code",
             "name": "Country Name",
             "units": 1,
             "data": convert_to_numeric("Country Code", pd.read_csv("./data/pcnt_urban.csv"))}

hospital_beds = {"country": "Country Code",
                "name": "Country Name",
                "units": 1,
                "data": convert_to_numeric("Country Code", pd.read_csv("./data/hospital_beds.csv"))}
