import * as React from 'react';
import { omitBy, isNil } from 'lodash';
import useAPI from '../hooks/useAPI';

import CountrySelector, {
  CountrySelectorResponse,
} from '../components/CountrySelector';
import CovidResults, { CovidData } from '../components/CovidResults';
import { CountryResponse, SimulationParams } from '../API';

const Countries: React.FC<{
  onSubmit?: (
    value: CountrySelectorResponse | { countryCode?: string | null },
  ) => void;
  values: SimulationParams & { countryCode?: string | null };
}> = ({ onSubmit, values }) => {
  const [countries, setCountries] = React.useState([]);
  const [countryInfo, setCountryInfo] = React.useState<{
    loading: boolean;
    error: Error | null;
    data: {
      countryInfo: CountryResponse;
      covidData: CovidData;
    } | null;
  }>({
    loading: true,
    error: null,
    data: null,
  });
  const api = useAPI();

  React.useEffect(() => {
    api
      .countries()
      .then(response => setCountries(response.countries))
      .catch(console.error);
  }, []);

  React.useEffect(() => {
    if (values.countryCode) {
      loadCountryData(values.countryCode);
    }
  }, [values.countryCode]);

  const loadCountryData = async (countryCode: string) => {
    try {
      setCountryInfo({
        loading: true,
        error: null,
        data: null,
      });
      const countryInfo = await api.country(countryCode);
      const covidData = await api.countryCovidData(countryCode);
      setCountryInfo({
        loading: false,
        error: null,
        data: {
          countryInfo,
          covidData,
        },
      });
    } catch (error) {
      console.log({ error });
      setCountryInfo({
        error,
        loading: false,
        data: null,
      });
    }
  };

  const selectCountry = (countryCode: string) => {
    onSubmit({ countryCode });
  };

  const open = !countryInfo.loading;

  const countryLabel = countries.find(
    entry => entry.countryCode === countryInfo?.data?.countryInfo?.countryCode,
  )?.name;

  return (
    <section className="input" id="country-selection">
      <div className="action-box">
        <CountrySelector
          countries={countries}
          onSubmit={onSubmit}
          countryInfo={{
            ...values,
            ...omitBy(countryInfo?.data?.countryInfo || {}, isNil),
          }}
          onClickSelectCountry={selectCountry}
        />
      </div>
      <div
        className={`results-drop ${open ? 'open' : ''}`}
        // To prevent flashing
        style={{ minHeight: 443 }}
      >
        {!!countryInfo &&
          !!countryInfo?.data &&
          !!countryInfo.data.covidData.timeseries && (
            <CovidResults
              data={countryInfo.data.covidData}
              countryLabel={
                countryLabel || countryInfo?.data?.countryInfo.countryCode
              }
            />
          )}
        {/* TODO do something on error */}
        {!!countryInfo && !!countryInfo.error && countryInfo.error.message}
      </div>
    </section>
  );
};

export default Countries;
