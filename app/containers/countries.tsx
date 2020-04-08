import * as React from 'react';
import useAPI from '../hooks/useAPI';

const Countries: React.FC = ({ children }) => {
  const api = useAPI();
  const [countries, setCountries] = React.useState([]);

  React.useEffect(() => {
    api
      .countries()
      .then(setCountries)
      .catch(console.error);
  }, []);

  console.log({ countries });

  return <>{children}</>;
};

export default Countries;
