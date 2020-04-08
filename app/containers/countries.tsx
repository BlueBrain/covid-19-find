import * as React from 'react';
import useAPI from '../hooks/useAPI';

import CountrySelector from '../components/CountrySelector';

const Countries: React.FC = ({ children }) => {
  const [countries, setCountries] = React.useState([]);
  const [countryInfo, setCountryInfo] = React.useState({});
  const api = useAPI();

  React.useEffect(() => {
    api
      .countries()
      .then(response => setCountries(response.countries))
      .catch(console.error);
  }, []);

  const loadCountryData = async (countryCode: string) => {
    const info = await api.country(countryCode);

    setCountryInfo(info);
  };

  const submitCountry = () => {
    console.log('clicked Submit');
  };

  return (
    <CountrySelector
      countries={countries}
      onClickSubmit={submitCountry}
      countryInfo={countryInfo}
      onClickSelectCountry={loadCountryData}
    />
  );
};

export default Countries;
