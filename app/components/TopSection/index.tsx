import * as React from 'react';

import './top-section.less';

const TopSection: React.FC = () => {
  return (
    <section className="top-section">
      <div className="half content">
        <h2 className="underline">
          {' '}
          COVID-19 Diagnostic Implementation Simulator{' '}
        </h2>
        <div className="description">
          This Diagnostic Implementation Simulator for SARS-CoV-2 diagnostics
          simulates scenarios for optimal allocation of resources. It uses
          modeling data to estimate the potential impact of deploying different
          testing strategies for COVID-19.
          <br />
          <br />
          The simulator has been developed with our partners at the{' '}
          <a href="https://www.epfl.ch/research/domains/bluebrain/">
            EPFL Blue Brain Project
          </a>{' '}
          and <a href="http://ateneo.edu/">Ateneo de Manila University</a>,
          Manila, the Philippines.
        </div>
      </div>
      <div className="half">
        <div className="shoutout">
          <span className="gradient"></span>
          <div className="disclamer">
            <h2>Please Note</h2>
            <p>
              This tool is not intended to replace detailed epidemiological
              models for country decision making or the estimates of deaths and
              of epidemic duration coming from such models.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
};

export default TopSection;
