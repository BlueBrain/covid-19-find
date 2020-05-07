import * as React from 'react';
import useQueryString from './hooks/useQuerySring';
import Header from './components/Header';
import Hero from './components/Hero';
import TopSection from './components/TopSection';
import TestSelector from './components/TestSelector';
import Countries from './containers/countries';
import Simulation from './containers/simulation';
import API, { SimulationParams, DEFAULT_SCENARIO_LIST } from './API';
import Footer from './components/Footer';
import ScrollToTop from './components/ScrollToTop';

const DEFAULT_PARAMS = {
  countryCode: null,
  population: null,
  hospitalBeds: null,
  workingOutsideHomeProportion: null,
  urbanPopulationProportion: null,
  hospitalStaffPerBed: 2.5,
  activePopulationProportion: null,
  belowPovertyLineProportion: null,
  hospitalEmployment: null,
  over64Proportion: null,
  sensitivityPCR: 0.95,
  sensitivityRDT: 0.85,
  sensitivityXray: 0,
  specificityPCR: 0.95,
  specificityRDT: 0.9,
  specificityXray: 0,
  numTestsPCR: 1000,
  numTestsRDT: 1000,
  numTestsXray: 0,
  scenarios: DEFAULT_SCENARIO_LIST,
};

const App: React.FC = () => {
  const [queryParams, setQueryParams] = useQueryString({
    // nested values edgecase
    // to prevent [object Object] in url
    scenarios: {
      parse: entry => JSON.parse(entry),
      stringify: entry => JSON.stringify(entry),
    },
  });

  const [
    { countrySelectFormReady, testsFormReady },
    setFormsReady,
  ] = React.useState<{
    countrySelectFormReady: boolean;
    testsFormReady: boolean;
  }>({ countrySelectFormReady: false, testsFormReady: false });

  React.useEffect(() => {
    const api = new API();
    const [, countryCode] = navigator.language.split('-');

    // Fetch default scenarios from API
    api
      .scenarios()
      .then(({ scenarios }) => {
        // Implement default values
        setQueryParams({
          ...DEFAULT_PARAMS,
          scenarios: scenarios.map((scenario, index) => ({
            ...DEFAULT_SCENARIO_LIST[index],
            ...scenario,
            hospitalTestProportion: scenario.hospitalTestProportion * 100,
            otherHighContactPopulationTestProportion:
              scenario.otherHighContactPopulationTestProportion * 100,
          })),
          countryCode,
          ...queryParams,
        });
      })
      .catch(error => {
        console.warn('Could not load default scenarios');
        setQueryParams({
          ...DEFAULT_PARAMS,
          countryCode,
          ...queryParams,
        });
      });
  }, []);

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
    <div>
      <Header />
      <Hero />
      <main>
        <TopSection />
        <Countries
          countrySelectFormReady={countrySelectFormReady}
          setCountrySelectFormReady={(countrySelectFormReady: boolean) => {
            setFormsReady({
              testsFormReady,
              countrySelectFormReady,
            });
          }}
          values={queryParams as SimulationParams}
          onSubmit={values => {
            // Reset all values if country code is changed
            // Except for scenarios
            // which will be preserved
            if (values.countryCode !== queryParams.countryCode) {
              handleSubmit({
                ...DEFAULT_PARAMS,
                countryCode: values.countryCode,
                scenarios: queryParams.scenarios,
              });
              return;
            }

            handleSubmit(values);
          }}
        />
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
        {countrySelectFormReady && testsFormReady && (
          <Simulation simulationParams={queryParams as SimulationParams} />
        )}
        {(!countrySelectFormReady || !testsFormReady) && (
          <section>
            <p>Please complete the steps to view simulation results</p>
          </section>
        )}
        <Footer />
      </main>
      <ScrollToTop />
    </div>
  );
};

export default App;
