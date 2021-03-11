import pycountry
import numpy as np
import pandas as pd
import os


path_prefix = os.path.abspath(os.path.dirname(__file__))
total_pop_file = os.path.join(path_prefix, 'data/total_pop.csv')
age_distr_file = os.path.join(path_prefix, 'data/age_distr.csv')
pcnt_urban_file = os.path.join(path_prefix, 'data/pcnt_urban.csv')
hospital_beds_file = os.path.join(path_prefix, 'data/hospital_beds.csv')
pop_15_to_64_file = os.path.join(path_prefix, 'data/15_to_64.csv')
income_category_file=os.path.join(path_prefix,'data/income_category.csv')


#This routine creates a numeric code for each alpha-3 country code in our basic dataset
#The numeric code is the one used to access future data

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
            "data": pd.read_csv(total_pop_file)}

age_distr = {"country": "LocID",
            "name": "Location",
            "year": "Time",
            "age": "AgeGrp",
            "total_pop": "PopTotal",
            "units": 1e3,
            "data": pd.read_csv(age_distr_file)}

active_pop = {"country": "Country Code",
            "name": "Country Name",
            "units": 1e-2,
            "data": convert_to_numeric("Country Code", pd.read_csv(pop_15_to_64_file))}

pcnt_urban = {"country": "Country Code",
             "name": "Country Name",
             "units": 1,
             "data": convert_to_numeric("Country Code", pd.read_csv(pcnt_urban_file))}

hospital_beds = {"country": "Country Code",
                "name": "Country Name",
                "units": 1,
                "data": convert_to_numeric("Country Code", pd.read_csv(hospital_beds_file))}

income_category = {"country":"Country Code",
                   "name":"Country Name",
                   "units": None,
                   "data":convert_to_numeric("Country Code",pd.read_csv(income_category_file))}
