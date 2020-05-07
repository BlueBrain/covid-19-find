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
  const [ready, setReady] = React.useState(false);
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

  // Reset county details when country code changes
  const selectCountry = (countryCode: string) => {
    setReady(false);
    onSubmit({
      countryCode,
      workingOutsideHomeProportion: null,
      hospitalBeds: null,
      hospitalEmployment: null,
      population: null,
      over64Proportion: null,
      belowPovertyLineProportion: null,
      urbanPopulationProportion: null,
    });
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
          onSubmit={(values, valid) => {
            onSubmit(values);
            // dont show as ready until the form is valid
            setReady(valid);
          }}
          onChange={() => {
            setReady(false);
          }}
          countryInfo={{
            ...values,
            ...omitBy(countryInfo?.data?.countryInfo || {}, isNil),
          }}
          onClickSelectCountry={selectCountry}
          loading={countryInfo.loading}
        />
      </div>
      {ready &&
        !!countryInfo &&
        !!countryInfo?.data &&
        !!countryInfo.data.covidData.timeseries && (
          <div className={`results-drop ${open ? 'open' : ''}`}>
            {' '}
            <CovidResults
              data={countryInfo.data.covidData}
              countryLabel={
                countryLabel || countryInfo?.data?.countryInfo.countryCode
              }
            />
          </div>
        )}
      {/* TODO do something on error */}
      {!!countryInfo && !!countryInfo.error && (
        <h3>No Covid-19 Case Data found for this country.</h3>
      )}
    </section>
  );
};

export default Countries;
