import pytest
from ..covid19find.countryrepository import CountryRepository

country_repo = CountryRepository()


class TestCountryRepository:

    def test_country_details_CH(self):
        assert country_repo.country_details("CH") == {'activePopulationProportion': 0.66,
                                                      'countryCode': 'CH',
                                                      'highContactPopulation': None,
                                                      'hospitalBeds': 34620,
                                                      'over64Proportion': 0.20232131715771232,
                                                      'population': 8655000,
                                                      'remoteAreasPopulationProportion': None,
                                                      'urbanPopulationInDegradedHousingProportion': None,
                                                      'urbanPopulationProportion': 0.73,
                                                      'incomeCategory': "High income"}

    def test_country_details_AR(self):
        assert country_repo.country_details("AR") == {'activePopulationProportion': 0.64,
                                                      'countryCode': 'AR',
                                                      'highContactPopulation': None,
                                                      'hospitalBeds': 225980,
                                                      'over64Proportion': 0.12159494203026819,
                                                      'population': 45196000,
                                                      'remoteAreasPopulationProportion': None,
                                                      'urbanPopulationInDegradedHousingProportion': None,
                                                      'urbanPopulationProportion': 0.91,
                                                      'incomeCategory': 'Upper Middle income'}

    def test_country_details_EG(self):
        assert country_repo.country_details("EG") == {'activePopulationProportion': 0.6,
                                                      'countryCode': 'EG',
                                                      'highContactPopulation': None,
                                                      'hospitalBeds': 102334,
                                                      'over64Proportion': 0.05846609142611447,
                                                      'population': 102334000,
                                                      'remoteAreasPopulationProportion': None,
                                                      'urbanPopulationInDegradedHousingProportion': None,
                                                      'urbanPopulationProportion': 0.42,
                                                      'incomeCategory': 'Lower middle income'}

    def test_country_details_AD(self):
        assert country_repo.country_details("AD") == None

    def test_country_details_BQ(self):
        assert country_repo.country_details("BQ") == {'activePopulationProportion': None,
                                                      'countryCode': 'BQ',
                                                      'highContactPopulation': None,
                                                      'hospitalBeds': None,
                                                      'over64Proportion': None,
                                                      'population': 26000,
                                                      'remoteAreasPopulationProportion': None,
                                                      'urbanPopulationInDegradedHousingProportion': None,
                                                      'urbanPopulationProportion': None,
                                                      'incomeCategory': None}

    def test_country_details_IN(self):
        assert country_repo.country_details("IN") == {'activePopulationProportion': 0.66,
                                                      'countryCode': 'IN',
                                                      'highContactPopulation': None,
                                                      'hospitalBeds': None,
                                                      'over64Proportion': 0.07224416813284598,
                                                      'population': 1380004000,
                                                      'remoteAreasPopulationProportion': None,
                                                      'urbanPopulationInDegradedHousingProportion': None,
                                                      'urbanPopulationProportion': 0.34,
                                                      'incomeCategory': 'Lower middle income'}
