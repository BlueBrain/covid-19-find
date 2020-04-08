import React from 'react';
import ReactDOM from 'react-dom';
import Header from './components/Header';
import Hero from './components/Hero';
import ActionBox from './components/ActionBox';
import API from './API';
import APIProvider from './APIProvider';
import Countries from './containers/countries';

const api = new API();

ReactDOM.render(
  <APIProvider api={api}>
    <div>
      <Header />
      <Hero />
      <main>
        <section>
          <div className="half">
            <h2 className="underline">Predictive Scenarios</h2>
            <div>
              Fill in this <em>three step process</em> to view proposed{' '}
              <em>scenarios</em> for optimal allocations of scarce resources in
              the attempt to help predict the effects of different strategies
              for Coronavirus testing in your country
            </div>
          </div>
          <div className="half">
            <div className="shoutout">
              <h2>Disclaimer</h2>
              <p>
                Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
                eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut
                enim ad minim veniam, quis nostrud exercitation ullamco laboris
                nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor
                in reprehenderit in voluptate velit esse cillum dolore eu fugiat
                nulla pariatur. Excepteur sint occaecat cupidatat non proident,
                sunt in culpa qui officia deserunt mollit anim id est laborum.
              </p>
              <button className="btn">Read All</button>
            </div>
          </div>
        </section>
        <Countries />
        <ActionBox />
      </main>
    </div>
  </APIProvider>,
  document.getElementById('app'),
);
