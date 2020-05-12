import * as React from 'react';

import './top-section.less';

const bbpLogo = require('../../assets/images/EPFL-BBP-logo.jpg');
const ataneoLogo = require('../../assets/images/ateneo-logo.jpg');

const TopSection: React.FC = () => {
  return (
    <section className="top-section">
      <div className="half content">
        {/* <h2 className="underline">
          {' '}
          COVID-19 Diagnostic Implementation Simulator{' '}
        </h2> */}
        <div className="description">
          This Diagnostic Implementation Simulator for SARS-CoV-2 diagnostics
          simulates scenarios for optimal allocation of resources. It uses
          modeling data to estimate the potential impact of deploying different
          testing strategies for COVID-19.
          <br />
          <br />
          The simulator has been developed with our partners at the{' '}
          <a
            href="https://www.epfl.ch/research/domains/bluebrain/"
            target="_blank"
          >
            EPFL Blue Brain Project
          </a>{' '}
          and{' '}
          <a href="http://ateneo.edu/" target="_blank">
            Ateneo de Manila University
          </a>
          , Manila, the Philippines.
        </div>
        <div style={{ marginTop: '1rem' }}>
          <a
            href="https://www.epfl.ch/research/domains/bluebrain/"
            target="_blank"
          >
            <img
              className="bbp-logo"
              src={bbpLogo}
              style={{ width: '100px', marginRight: '1rem' }}
            />
          </a>
          <a href="http://ateneo.edu/" target="_blank">
            <img
              className="ateneo-logo"
              src={ataneoLogo}
              style={{ height: '100px' }}
            />
          </a>
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
