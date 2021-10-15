import * as React from 'react';
import { omitBy, isNil } from 'lodash';

import useAPI from '../hooks/useAPI';
import CountrySelector, {
  CountrySelectorResponse,
} from '../components/CountrySelector';
import CovidResults, { CovidData } from '../components/CovidResults';
import { CountryData } from '../types/simulation';
import { CountryResponse } from '../types/country';

const Countries: React.FC<{
  onCountryData?: (numberOftest: number) => void;
  countrySelectFormReady: boolean;
  setCountrySelectFormReady: (value: boolean) => void;
  onSubmit?: (
    value: CountrySelectorResponse | { countryCode?: string | null },
  ) => void;
  values: CountryData;
}> = ({
  onCountryData,
  onSubmit,
  values,
  setCountrySelectFormReady,
  countrySelectFormReady,
}) => {
  const [countries, setCountries] = React.useState([]);
  const [countryInfo, setCountryInfo] = React.useState<{
    loading: boolean;
    error: Error | null;
    data: {
      countryInfo: CountryResponse;
      covidData: CovidData;
    } | null;
  }>({
    loading: false,
    error: null,
    data: null,
  });

  const api = useAPI();
  React.useEffect(() => {
    api.countries().then(response => setCountries(response.countries));
  }, []);

  const loadCountryData = async (countryCode: string) => {
    try {
      setCountryInfo({
        loading: true,
        error: null,
        data: null,
      });
      const countryInfo = await api.country(countryCode);
      const covidData = await api.countryCovidData(countryCode);
      onCountryData(covidData.meanTestsLast7Days);
      setCountryInfo({
        loading: false,
        error: null,
        data: {
          countryInfo,
          covidData,
        },
      });
    } catch (error) {
      setCountryInfo({
        error,
        loading: false,
        data: null,
      });
    }
  };

  React.useEffect(() => {
    if (values.countryCode) {
      loadCountryData(values.countryCode);
    }
  }, [values.countryCode]);

  // Reset county details when country code changes
  const selectCountry = (countryCode: string) => {
    setCountrySelectFormReady(false);
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

  // TODO refactor by removing presentation logic
  // perhaps consider creating a seperate presentation component
  // for the section types
  return (
    <section className="input" id="country-selection">
      <div className="action-box">
        <CountrySelector
          countries={countries}
          onSubmit={(values, valid) => {
            onSubmit(values);
            // dont show as ready until the form is valid
            setCountrySelectFormReady(valid);
          }}
          onChange={() => {
            setCountrySelectFormReady(false);
          }}
          countryInfo={{
            ...values,
            ...omitBy(countryInfo?.data?.countryInfo || {}, isNil),
          }}
          onClickSelectCountry={selectCountry}
          loading={countryInfo.loading}
        />
      </div>
      {countrySelectFormReady &&
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
