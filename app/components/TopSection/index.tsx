import * as React from 'react';

import './top-section.less';

import bbpLogo from '../../assets/images/EPFL-BBP-logo.jpg';
import ataneoLogo from '../../assets/images/ateneo-logo.jpg';
import unitaidLogo from '../../assets/images/unitaid-logo.png';
import gettingStartedGuide from '../../assets/pdf/Getting started with the FIND Diagnostic Simulator.pdf';

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
            Department of Information Systems and Computer Science, Ateneo de Manila University
          </a>
          , Manila, the Philippines, and was supported by funding from{' '}
          <a href="https://unitaid.org" target="_blank">
            Unitaid 
          </a>
          <br />
          <p>
            Learn how to use this simulator with our{' '}
            <a
              href={gettingStartedGuide}
              download="Getting started with the FIND Diagnostic Simulator"
              target="_blank"
            >
              Getting Started Guide
            </a>
          </p>
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
          <a href="https://unitaid.org/" target="_blank">
            <img className="unitaid-logo" src={unitaidLogo} />
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
