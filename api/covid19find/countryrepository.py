import json
import os

from .simulation.getcountrydata import get_country_data


class CountryRepository:
    def __init__(self):
        country_codes_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), "country_codes.json")
        with open(country_codes_file) as country_codes_file:
            countries = json.load(country_codes_file)
            self.country_data = {
                "countries": countries
            }

    def country_list(self):
        return self.country_data

    def country_details(self, country_code):
        (population, urban_population_percentage, urban_population_in_degraded_housing_percentage, over_65_percentage,
         hospital_employment, high_contact_population, remote_areas_population_percentage) = get_country_data(
            country_code)
        return {
            "countryCode": country_code,
            "population": population,
            "urbanPopulationPercentage": urban_population_percentage,
            "urbanPopulationInDegradedHousingPercentage": urban_population_in_degraded_housing_percentage,
            "over65Percentage": over_65_percentage,
            "hospitalEmployment": hospital_employment,
            "highContactPopulation": high_contact_population,
            "remoteAreasPopulationPercentage": remote_areas_population_percentage
        }
