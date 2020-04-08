import * as React from 'react';
import useAPI from '../hooks/useAPI';

import CountrySelector from '../components/CountrySelector';

const Countries: React.FC = ({ children }) => {
  const [countries, setCountries] = React.useState([]);
  const api = useAPI();

  React.useEffect(() => {
    api
      .countries()
      .then(response => setCountries(response.countries))
      .catch(console.error);
  }, []);

  const submitCountry = (country: any) => {
    console.log('country', country);
  };

  return (
    <CountrySelector countries={countries} onClickSubmit={submitCountry} />
  );
};

export default Countries;
