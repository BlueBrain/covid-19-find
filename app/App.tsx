import * as React from 'react';

import ScenarioEditorPanel from './components/ScenarioEditorPanel';
import Countries from './containers/countries';
import Simulation from './containers/simulation';
import { ClientSimulationRequest, Scenario } from './types/simulation';
import { DEFAULT_SIMULATION_REQUEST_PARAMS } from './defaults';
import SaveScenariosButton from './components/SaveScenariosButton';
import LoadScenariosButton from './components/LoadScenariosButton';
import useAPIContext from './hooks/useAPI';
import useQueryString from './hooks/useQuerySring';
import { decodeClientState, encodeClientState } from './libs/stateLoader';
import { CovidData } from './components/CovidResults';

const App: React.FC = () => {
  const api = useAPIContext();
  const [defaultScenarios, setDefaultScenarios] = React.useState(
    DEFAULT_SIMULATION_REQUEST_PARAMS.scenarios,
  );
  const [{ state }, setScenarioRequestData] = useQueryString<{
    state: ClientSimulationRequest;
  }>(
    {
      state: {
        ...DEFAULT_SIMULATION_REQUEST_PARAMS,
      },
    },
    {
      state: {
        parse: decodeClientState,
        stringify: encodeClientState,
      },
    },
  );

  React.useEffect(() => {
    if (state.scenarios.length) {
      api.scenarios().then(({ scenarios }: { scenarios: Scenario[] }) => {
        // @ts-ignore
        setDefaultScenarios(scenarios);

        setScenarioRequestData({
          state: {
            scenarios,
            ...state,
          },
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

    for (let i = 0; i <= forms.length - 1; i++) {
      const form = forms[i];
      const valid = form.reportValidity();
      if (!valid) {
        break;
      }
    }
  };

  const handleLoadState = state => {
    setScenarioRequestData({
      state,
    });
  };

  return (
    <>
      <section>
        <a
          href="https://www.finddx.org/covid-19/dx-imp-sim/about/"
          target="_parent"
          style={{ marginRight: '1em' }}
        >
          <button className="btn simple">
            About the Dx Implementation Sim
          </button>
        </a>
        <LoadScenariosButton onLoad={handleLoadState} state={state} />
      </section>
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
        defaultScenarios={defaultScenarios}
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
      <Simulation
        clientSimulationRequest={state}
        ready={countrySelectFormReady && testsFormReady}
      />
      {/* CONTROL PANEL */}
      <section>
        <SaveScenariosButton
          disabled={!countrySelectFormReady || !testsFormReady}
          state={state}
        />
      </section>
    </>
  );
};

export default App;
