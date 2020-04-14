import * as React from 'react';
import useAPI from '../hooks/useAPI';

import CountrySelector, {
  CountryParams,
} from '../components/CountrySelector';
import CovidResults, { CovidData } from '../components/CovidResults';

const Countries: React.FC<CountryParams & {
  onSubmit?: (value: CountryParams) => void;
}> = ({
  onSubmit,
  total_pop,
  pop_hospitals,
  pop_high_contact,
  prop_urban,
  prop_isolated,
  degraded,
  ge_65,
  prop_tests_hospitals,
  prop_tests_high_contact,
  prop_tests_rest_of_population,
}) => {
  const [, defaultCountryCode] = navigator.language.split('-');
  const [countries, setCountries] = React.useState([]);
  const [countryInfo, setCountryInfo] = React.useState<{
    loading: boolean;
    error: Error | null;
    data: {
      countryInfo: CountryParams;
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

  const open = !countryInfo.loading;

  const countryLabel = countries.find(
    // @ts-ignore reverse this so that the API returns better formatted data
    entry => entry.countryCode === countryInfo?.data?.countryInfo?.countryCode,
  )?.name;

  return (
    <section className="input" id="country-selection">
      <div className="action-box">
        <CountrySelector
          countries={countries}
          onSubmit={onSubmit}
          countryInfo={
            { 
              total_pop,
              pop_hospitals,
              pop_high_contact,
              prop_urban,
              prop_isolated,
              degraded,
              ge_65,
              prop_tests_hospitals,
              prop_tests_high_contact,
              prop_tests_rest_of_population
              ...countryInfo?.data?.countryInfo
            }}
          onClickSelectCountry={loadCountryData}
          defaultCountryCode={defaultCountryCode}
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
                // @ts-ignore remove this with better formatted data
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
