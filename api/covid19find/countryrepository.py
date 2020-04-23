import json
import os
from .countrydata.Countries import Country

import pycountry


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
        # (population, urban_population_percentage, urban_population_in_degraded_housing_percentage, over_65_percentage,
        #  hospital_employment, high_contact_population, remote_areas_population_percentage) =
        pcountry = pycountry.countries.get(alpha_2=country_code)

        if pcountry is None:
            return None
        country = Country(int(pcountry.numeric), 2020, age=65)
        nearest = country.search_avail_stats()
        over65percentage = None
        over65count = nearest["overX"][0]
        population = nearest["pop"][0]
        if over65count is not None:
            over65percentage = over65count / population

        return {
            "countryCode": country_code,
            "population": population,
            "activePopulation": nearest["active_pop"][0],
            "urbanPopulationProportion": nearest["urban"][0],
            "urbanPopulationInDegradedHousingProportion": nearest["degraded"][0],
            "over65Proportion": over65percentage,
            "hospitalEmployment": None,
            "hospitalBeds": (population / 1000.0) * nearest["hosp_beds"][0],
            "highContactPopulation": nearest["high_contact"][0],
            "remoteAreasPopulationProportion": nearest["remote"][0]
        }
