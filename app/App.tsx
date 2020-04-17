import * as React from 'react';
import useQueryString from './hooks/useQuerySring';
import Header from './components/Header';
import Hero from './components/Hero';
import TopSection from './components/TopSection';
import TestSelector from './components/TestSelector';
import Countries from './containers/countries';
import Simulation from './containers/simulation';
import About from './components/About';
import { SimulationParams } from './API';
import Contact from './containers/contact';

const DEFAULT_PARAMS = {
  countryCode: null,
  population: null,
  hospitalBeds: null,
  highContactPopulation: null,
  urbanPopulationProportion: null,
  hospitalStaffPerBed: 4,
  urbanPopulationInDegradedHousingProportion: null,
  hospitalEmployment: null,
  sensitivityPCR: 0.95,
  sensitivityRDT: 0.85,
  sensitivityXray: 0.9,
  specificityPCR: 0.95,
  specificityRDT: 0.9,
  specificityXray: 0.9,
  numTestsPCR: 1000,
  numTestsRDT: 1000,
  numTestsXray: 1000,
};

const App: React.FC = () => {
  const [queryParams, setQueryParams] = useQueryString();

  React.useEffect(() => {
    // Implement default values
    const [, countryCode] = navigator.language.split('-');
    setQueryParams({
      ...DEFAULT_PARAMS,
      countryCode,
      ...queryParams,
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

    // Validate forms, and scroll to the next if valid
    // If any form is invalid, will scroll to that form
    // and report the invalidity
    for (let i = 0; i <= forms.length; i++) {
      const form = forms[i];
      if (form.checkValidity()) {
        if (i == 1) {
          return document.querySelector('#simulation-results')?.scrollIntoView({
            behavior: 'smooth',
          });
        }
        forms[i + 1]?.scrollIntoView({
          behavior: 'smooth',
        });
      } else {
        form.reportValidity();
        form.scrollIntoView({
          behavior: 'smooth',
        });
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
          onSubmit={handleSubmit}
        />
        <TestSelector {...queryParams} onSubmit={handleSubmit} />
        <Simulation simulationParams={queryParams as SimulationParams} />
        <About />
        <Contact />
      </main>
    </div>
  );
};

export default App;
