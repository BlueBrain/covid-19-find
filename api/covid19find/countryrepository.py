import json
import os
from .countrydata.Countries import Country

from .simulation.getcountrydata import get_country_data
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
        over65percentage = None
        over65count = country.get_overX()
        if over65count is not None:
            over65percentage = over65count / country.get_population()

        return {
            "countryCode": country_code,
            "population": country.get_population(),
            "urbanPopulationPercentage": country.get_pcnt_urban(),
            "urbanPopulationInDegradedHousingPercentage": country.get_pcnt_degraded(),
            "over65Percentage": over65percentage,
            "hospitalEmployment": None,
            "hospitalBeds": country.get_hosp_beds(),
            "highContactPopulation": country.get_high_contact(),
            "remoteAreasPopulationPercentage": country.get_remote()
        }
