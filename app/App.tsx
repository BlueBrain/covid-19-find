import * as React from 'react';
import TestSelector from './components/ScenarioEditorPanel';
import Countries from './containers/countries';
import Simulation from './containers/simulation';
import { SimulationRequest } from './types/simulation';
import { DEFAULT_SIMULATION_REQUEST_PARAMS } from './defaults';

const App: React.FC = () => {
  const [queryParams, setQueryParams] = React.useState<SimulationRequest>(
    DEFAULT_SIMULATION_REQUEST_PARAMS,
  );
  // const [queryParams, setQueryParams] = useQueryString({
  //   // nested values edgecase
  //   // to prevent [object Object] in url
  //   scenarios: {
  //     parse: entry => JSON.parse(entry),
  //     stringify: entry => JSON.stringify(entry),
  //   },
  // });

  const [
    { countrySelectFormReady, testsFormReady },
    setFormsReady,
  ] = React.useState<{
    countrySelectFormReady: boolean;
    testsFormReady: boolean;
  }>({ countrySelectFormReady: false, testsFormReady: false });

  const handleSubmit = changedValues => {
    setQueryParams({
      ...queryParams,
      ...changedValues,
    });

    const forms: HTMLFormElement[] = [
      document.querySelector('#country-select-form'),
      document.querySelector('#tests-form'),
    ];

    forms.forEach(form => form.reportValidity());
  };

  return (
    <>
      {/* Panel 1 */}
      <Countries
        countrySelectFormReady={countrySelectFormReady}
        setCountrySelectFormReady={(countrySelectFormReady: boolean) => {
          setFormsReady({
            testsFormReady,
            countrySelectFormReady,
          });
        }}
        // @ts-ignore
        values={queryParams}
        onSubmit={values => {
          // Reset all values if country code is changed
          if (values.countryCode !== queryParams.countryCode) {
            handleSubmit({
              ...DEFAULT_SIMULATION_REQUEST_PARAMS,
              countryCode: values.countryCode,
            });
            // mark forms as dirty or not ready
            // if the country changes
            setFormsReady({
              countrySelectFormReady: false,
              testsFormReady: false,
            });
            return;
          }

          handleSubmit(values);
        }}
      />
      {/* Panel 2 */}
      <TestSelector
        {...queryParams}
        onSubmit={handleSubmit}
        testsFormReady={testsFormReady}
        setTestsFormReady={(testsFormReady: boolean) => {
          setFormsReady({
            countrySelectFormReady,
            testsFormReady,
          });
        }}
      />
      {/* Panel 3 */}
      {countrySelectFormReady && testsFormReady && (
        // @ts-ignore
        <Simulation simulationParams={queryParams} />
      )}
      {(!countrySelectFormReady || !testsFormReady) && (
        <section>
          <p>Please complete the steps to view simulation results</p>
        </section>
      )}
    </>
  );
};

export default App;
