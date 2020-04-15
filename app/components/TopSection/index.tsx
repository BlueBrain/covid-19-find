import * as React from 'react';

import './top-section.less';

const TopSection: React.FC = () => {
  return (
    <section className="top-section">
      <div className="half content">
        <h2 className="underline">Predictive Scenario Simulator</h2>
        <div className="description">
          Fill in this <em>three step process</em> to view proposed{' '}
          <em>simulation scenarios</em> for optimal allocations of scarce
          resources in the attempt to help predict the effects of different
          strategies for Coronavirus testing in your country
        </div>
      </div>
      <div className="half">
        <div className="shoutout">
          <span className="gradient"></span>
          <div className="disclamer">
            <h2>Disclaimer</h2>
            <p>
              This web tool estimates the relative impact of different
              deployment strategies for diagnostic tests in the current acute
              phase of the COVID-19 pandemic. The tool is not intended to
              replace detailed epidemiological models or the estimates of deaths
              and of epidemic duration coming from such models.
            </p>
            <button className="btn">Read All</button>
          </div>
        </div>
      </div>
    </section>
  );
};

export default TopSection;
