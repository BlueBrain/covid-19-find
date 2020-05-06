import pycountry
from Countries import Country
import os
import json

path_prefix = os.path.abspath(os.path.dirname(__file__))
data_dir = os.path.join(path_prefix, 'data/countries')


def __int_or_none(val):
    if val is None:
        return None
    else:
        return int(val)


def __percentage_to_proportion_or_none(val):
    if val is None:
        return None
    else:
        return val / 100


def country_details(country_code):
    # (population, urban_population_percentage, urban_population_in_degraded_housing_percentage, over_65_percentage,
    #  hospital_employment, high_contact_population, remote_areas_population_percentage) =
    pcountry = pycountry.countries.get(alpha_2=country_code)

    if pcountry is None:
        return None
    country = Country(int(pcountry.numeric), 2020, age=64)
    try:
        nearest = country.search_avail_stats()
    except ValueError:
        return None
    over64proportion = None
    over64count = nearest["overX"][0]
    population = nearest["pop"][0]
    if over64count is not None:
        over64proportion = over64count / population

    active_population_proportion = None
    active_population_count = nearest["active_pop"][0]
    if active_population_count is not None:
        active_population_proportion = active_population_count / population
    hospital_beds_per_1000 = nearest["hosp_beds"][0]
    hospital_beds = None
    if population is not None and hospital_beds_per_1000 is not None:
        hospital_beds = (population / 1000.0) * hospital_beds_per_1000
    return {
        "countryCode": country_code,
        "population": __int_or_none(population),
        "activePopulationProportion": active_population_proportion,
        "urbanPopulationProportion": __percentage_to_proportion_or_none(nearest["urban"][0]),
        "urbanPopulationInDegradedHousingProportion": __percentage_to_proportion_or_none(
            nearest["degraded"][0]),
        "over64Proportion": over64proportion,
        "hospitalBeds": hospital_beds,
        "highContactPopulation": __int_or_none(nearest["high_contact"][0]),
        "remoteAreasPopulationProportion": __percentage_to_proportion_or_none(nearest["remote"][0])
    }


os.makedirs(data_dir, exist_ok=True)

for c in pycountry.countries:
    try:
        country_data = country_details(c.alpha_2)
        if country_data is not None:
            with open(os.path.join(data_dir, c.alpha_2 + ".json"), "w") as country_file:
                json.dump(country_data, country_file)

    except IndexError:
        print(c.alpha_2)
        print(c.name)