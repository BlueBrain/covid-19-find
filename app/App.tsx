import * as React from 'react';

import ScenarioEditorPanel from './components/ScenarioEditorPanel';
import Countries from './containers/countries';
import Simulation from './containers/simulation';
import { ClientSimulationRequest, Scenario } from './types/simulation';
import { DEFAULT_SIMULATION_REQUEST_PARAMS } from './defaults';
import SaveLoadButtons from './components/SaveLoad';
import useAPIContext from './hooks/useAPI';

const App: React.FC = () => {
  const api = useAPIContext();
  const [defaultScenarios, setDefaultScenarios] = React.useState(
    DEFAULT_SIMULATION_REQUEST_PARAMS.scenarios,
  );
  const [{ state }, setScenarioRequestData] = React.useState<{
    state: ClientSimulationRequest;
  }>({
    state: {
      ...DEFAULT_SIMULATION_REQUEST_PARAMS,
    },
  });

  React.useEffect(() => {
    if (state.scenarios.length) {
      api.scenarios().then(({ scenarios }: { scenarios: Scenario[] }) => {
        // @ts-ignore
        setDefaultScenarios(scenarios);

        setScenarioRequestData({
          // @ts-ignore
          state: { scenarios },
        });
      });
    }
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

  const handleLoadState = state => {
    setScenarioRequestData({
      state,
    });
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
          if (values.countryCode !== state.countryCode) {
            handleSubmit({
              ...DEFAULT_SIMULATION_REQUEST_PARAMS,
              scenarios: defaultScenarios,
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
      <section>
        <SaveLoadButtons state={state} onLoad={handleLoadState} />
      </section>
    </>
  );
};

export default App;
