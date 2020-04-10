import * as React from 'react';
import Header from './components/Header';
import Hero from './components/Hero';
import TopSection from './components/TopSection';
import TestSelector from './components/TestSelector';
import Countries from './containers/countries';
import Simulation from './containers/simulation';
import About from './components/About';
import { SimulationParams } from './API';

const DEFAULT_PARAMS = {
  total_pop: 80000000,
  pop_hospitals: 10000,
  pop_high_contact: 1000000,
  prop_urban: 0.46,
  prop_isolated: 0.1,
  degraded: 0.1,
  ge_65: 0.25,
  prop_tests_hospitals: 0.5,
  prop_tests_high_contact: 0.5,
  prop_tests_rest_of_population: 0,
  sensitivity_PCR: 0.95,
  sensitivity_RDT: 0.85,
  sensitivity_xray: 0.9,
  selectivity_PCR: 0.95,
  selectivity_RDT: 0.9,
  selectivity_xray: 0.9,
  num_tests_PCR: 1000,
  num_tests_RDT: 1000,
  num_tests_xray: 1000,
};

const App: React.FC = () => {
  const [values, setValues] = React.useState<SimulationParams>(DEFAULT_PARAMS);

  const handleSubmit = changedValues => {
    setValues({
      ...values,
      ...changedValues,
    });
  };

  return (
    <div>
      <Header />
      <Hero />
      <main>
        <TopSection />
        <Countries {...values} onSubmit={handleSubmit} />
        <TestSelector {...values} onSubmit={handleSubmit} />
        <Simulation simulationParams={values} />
        <About />
      </main>
    </div>
  );
};

export default App;
