import pytest
from ..covid19find.countryrepository import CountryRepository

country_repo = CountryRepository()


class TestCountryRepository:

    def test_country_details_CH(self):
        assert country_repo.country_details("CH") == {'activePopulationProportion': 0.66,
                                                      'countryCode': 'CH',
                                                      'highContactPopulation': None,
                                                      'hospitalBeds': 34620,
                                                      'over65Proportion': None,
                                                      'population': 8655000,
                                                      'remoteAreasPopulationProportion': None,
                                                      'urbanPopulationInDegradedHousingProportion': None,
                                                      'urbanPopulationProportion': 0.73}

    def test_country_details_AR(self):
        assert country_repo.country_details("AR") == {'activePopulationProportion': 0.64,
                                                      'countryCode': 'AR',
                                                      'highContactPopulation': None,
                                                      'hospitalBeds': 225980,
                                                      'over65Proportion': 0.11366459421187718,
                                                      'population': 45196000,
                                                      'remoteAreasPopulationProportion': None,
                                                      'urbanPopulationInDegradedHousingProportion': None,
                                                      'urbanPopulationProportion': 0.91}

    def test_country_details_EG(self):
        assert country_repo.country_details("EG") == {'activePopulationProportion': 0.6,
                                                      'countryCode': 'EG',
                                                      'highContactPopulation': None,
                                                      'hospitalBeds': 102334,
                                                      'over65Proportion': None,
                                                      'population': 102334000,
                                                      'remoteAreasPopulationProportion': None,
                                                      'urbanPopulationInDegradedHousingProportion': None,
                                                      'urbanPopulationProportion': 0.42}
