import React from 'react';
import ReactDOM from 'react-dom';
import Header from './components/Header';
import Hero from './components/Hero';
import TopSection from './components/TopSection';
import ActionBox from './components/ActionBox';
import API from './API';
import APIProvider from './APIProvider';
import TestSelector from './components/TestSelector';
import Countries from './containers/countries';
import Simulation from './containers/simulation';
import About from './components/About';

const api = new API();

ReactDOM.render(
  <APIProvider api={api}>
    <div>
      <Header />
      <Hero />
      <main>
        <TopSection />
        <Countries />
        <TestSelector />
        <Simulation />
        <About />
      </main>
    </div>
  </APIProvider>,
  document.getElementById('app'),
);
