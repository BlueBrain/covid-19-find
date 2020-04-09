import * as React from 'react';
import useAPI from '../hooks/useAPI';

import CountrySelector from '../components/CountrySelector';
import CovidResults, { CovidData } from '../components/CovidResults';

const Countries: React.FC = ({ children }) => {
  const [, defaultCountryCode] = navigator.language.split('-');

  const [countries, setCountries] = React.useState([]);
  const [countryInfo, setCountryInfo] = React.useState<{
    covidData?: CovidData;
  }>({});
  const api = useAPI();

  React.useEffect(() => {
    api
      .countries()
      .then(response => setCountries(response.countries))
      .catch(console.error);
  }, []);

  const loadCountryData = async (countryCode: string) => {
    const info = await api.country(countryCode);
    const covidData = await api.countryCovidData(countryCode);
    setCountryInfo({
      ...info,
      covidData,
    });
  };

  const submitCountry = () => {
    console.log('clicked Submit', { countryInfo });
  };

  return (
    <>
      <CountrySelector
        countries={countries}
        onClickSubmit={submitCountry}
        countryInfo={countryInfo}
        onClickSelectCountry={loadCountryData}
        defaultCountryCode={defaultCountryCode}
      />
      {!!countryInfo && !!countryInfo.covidData && (
        <CovidResults data={countryInfo.covidData} />
      )}
    </>
  );
};

export default Countries;
