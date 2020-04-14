import * as React from 'react';
import Header from './components/Header';
import Hero from './components/Hero';
import TopSection from './components/TopSection';
import TestSelector from './components/TestSelector';
import Countries from './containers/countries';
import Simulation from './containers/simulation';
import About from './components/About';
import { SimulationParams } from './API';

const DEFAULT_PARAMS: SimulationParams = {
  population: 80000000,
  hospitalBeds: 10000,
  highContactPopulation: 1000000,
  urbanPopulationProportion: 0.46,
  remoteAreasPopulationProportion: 0.1,
  urbanPopulationInDegradedHousingProportion: 0.1,
  over65Proportion: 0.25,
  hospitalTestsProportion: 0.5,
  highContactTestsProportion: 0.5,
  restOfPopulationTestsProportion: 0,
  hospitalEmployment: 4,
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
