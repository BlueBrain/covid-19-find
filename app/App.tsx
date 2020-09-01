import * as React from 'react';

import ScenarioEditorPanel from './components/ScenarioEditorPanel';
import Countries from './containers/countries';
import Simulation from './containers/simulation';
import { ClientSimulationRequest } from './types/simulation';
import { DEFAULT_SIMULATION_REQUEST_PARAMS } from './defaults';
import useQueryString from './hooks/useQuerySring';

const App: React.FC = () => {
  const [{ state }, setScenarioRequestData] = useQueryString<{
    state: ClientSimulationRequest;
  }>(
    {
      state: {
        ...DEFAULT_SIMULATION_REQUEST_PARAMS,
      },
    },
    {
      // nested values edgecase
      // to prevent [object Object] in url
      state: {
        parse: entry => JSON.parse(atob(entry)),
        stringify: entry => btoa(JSON.stringify(entry)),
      },
    },
  );

  React.useEffect(() => {
    setScenarioRequestData({
      state: {
        ...DEFAULT_SIMULATION_REQUEST_PARAMS,
        ...state,
      },
    });
  }, []);

  const [
    { countrySelectFormReady, testsFormReady },
    setFormsReady,
  ] = React.useState<{
    countrySelectFormReady: boolean;
    testsFormReady: boolean;
  }>({ countrySelectFormReady: false, testsFormReady: false });

  const handleSubmit = changedValues => {
    setScenarioRequestData({
      state: {
        ...state,
        ...changedValues,
      },
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
        values={state}
        onSubmit={values => {
          // Reset all values if country code is changed
          if (values.countryCode !== state.countryCode) {
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
      <ScenarioEditorPanel
        scenarios={state.scenarios}
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
        <Simulation clientSimulationRequest={state} />
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
