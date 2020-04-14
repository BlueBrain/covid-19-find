import * as React from 'react';
import useAPI from '../hooks/useAPI';

import CountrySelector from '../components/CountrySelector';
import CovidResults, { CovidData } from '../components/CovidResults';
import { CountryResponse, SimulationParams } from '../API';

const Countries: React.FC<SimulationParams & {
  onSubmit?: (value: CountryResponse) => void;
}> = ({
  onSubmit,
  population,
  hospitalBeds,
  highContactPopulation,
  urbanPopulationProportion,
  remoteAreasPopulationProportion,
  urbanPopulationInDegradedHousingProportion,
  over65Proportion,
  hospitalEmployment,
}) => {
  const [, defaultCountryCode] = navigator.language.split('-');
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
    entry => entry.countryCode === countryInfo?.data?.countryInfo?.countryCode,
  )?.name;

  return (
    <section className="input" id="country-selection">
      <div className="action-box">
        <CountrySelector
          countries={countries}
          onSubmit={onSubmit}
          countryInfo={{
            population,
            hospitalBeds,
            highContactPopulation,
            urbanPopulationProportion,
            remoteAreasPopulationProportion,
            urbanPopulationInDegradedHousingProportion,
            over65Proportion,
            hospitalEmployment,
            ...countryInfo?.data?.countryInfo,
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
