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
          <h2>Disclaimer</h2>
          <p>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
            eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim
            ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut
            aliquip ex ea commodo consequat. Duis aute irure dolor in
            reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla
            pariatur. Excepteur sint occaecat cupidatat non proident, sunt in
            culpa qui officia deserunt mollit anim id est laborum.
          </p>
          <button className="btn">Read All</button>
        </div>
      </div>
    </section>
  );
};

export default TopSection;
