import * as React from 'react';
import useQueryString from './hooks/useQuerySring';
import Header from './components/Header';
import Hero from './components/Hero';
import TopSection from './components/TopSection';
import TestSelector from './components/TestSelector';
import Countries from './containers/countries';
import Simulation from './containers/simulation';
import About from './components/About';
import API, { SimulationParams, DEFAULT_SCENARIO_LIST } from './API';
import Contact from './containers/contact';
import Footer from './components/Footer';
import ScrollToTop from './components/ScrollToTop';
import ScenarioEditor from './components/ScenarioEditor';

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

  // Key presses
  // Don't allow enter to submit form
  React.useEffect(() => {
    const handleEnterPress = event => {
      if (event.key === 'Enter') {
        event.preventDefault();
      }
    };
    window.addEventListener('keydown', handleEnterPress);
    return () => {
      window.removeEventListener('keydown', handleEnterPress);
    };
  }, []);

  const handleSubmit = (changedValues, skipScroll = false) => {
    setQueryParams({
      ...queryParams,
      ...changedValues,
    });

    if (skipScroll) {
      return;
    }

    const forms: HTMLFormElement[] = [
      document.querySelector('#country-select-form'),
      document.querySelector('#tests-form'),
    ];

    // Validate forms, and scroll to the next if valid
    // If any form is invalid, will scroll to that form
    // and report the invalidity
    for (let i = 0; i <= forms.length; i++) {
      const form = forms[i];
      if (form.checkValidity() && form.dataset.dirty) {
        if (i == forms.length - 1) {
          // Show results if all are valid
          forms.forEach(form => {
            delete form.dataset.dirty;
          });
          return;
        }
      } else {
        form.reportValidity();
        break;
      }
    }
  };

  return (
    <div>
      <Header />
      <Hero />
      <main>
        <TopSection />
        <Countries
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
        <TestSelector {...queryParams} onSubmit={handleSubmit}>
          <ScenarioEditor
            scenarios={queryParams.scenarios}
            onSubmit={handleSubmit}
          />
        </TestSelector>
        <Simulation simulationParams={queryParams as SimulationParams} />
        <About />
        {/* <Contact /> */}
        <Footer />
      </main>
      <ScrollToTop />
    </div>
  );
};

export default App;
