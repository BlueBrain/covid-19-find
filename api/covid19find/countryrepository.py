import json
import os

from .simulation.covidlib import cl_path_prefix
from .simulator import INCOME_CATEGORY_CODE_TO_LABEL


class CountryRepository:
    def __init__(self):
        self.country_data_dir = os.path.join(cl_path_prefix, "countrydata", "data",
                                             "countries")
        country_codes_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), "country_codes.json")
        with open(country_codes_file) as country_codes_file:
            countries = json.load(country_codes_file)
            self.country_data = {
                "countries": countries
            }

    def country_list(self):
        return self.country_data

    def country_details(self, country_code):
        try:
            with open(os.path.join(self.country_data_dir, country_code + ".json")) as country_file:
                country_data = json.load(country_file)
                country_data["incomeCategory"] = INCOME_CATEGORY_CODE_TO_LABEL[country_data.pop("incomecategory")]
                return country_data
        except FileNotFoundError:
            return None

    def country_details_with_defaults(self, country_code, default):
        country_details = self.country_details(country_code)
        if country_details is None:
            country_details = default
        return country_details
