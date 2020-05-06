import json
import os


class CountryRepository:
    def __init__(self):
        self.country_data_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "countrydata", "data",
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
                return json.load(country_file)
        except FileNotFoundError:
            return None
