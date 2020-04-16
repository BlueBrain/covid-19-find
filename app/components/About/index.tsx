import * as React from 'react';

import './about.less';

const bbpLogo = require('../../assets/images/EPFL-BBP-logo.jpg');
const findLogo = require('../../assets/images/find-logo.png');
const connectionImage = require('../../assets/images/connection.png');

const About: React.FC = () => {
  const [expanded, setExpanded] = React.useState(false);

  return (
    <section className="about">
      <div className="half image-container">
        <img className="connection-image" src={connectionImage} />
        <div>
          <img className="find-logo" src={findLogo} />
          <img className="bbp-logo" src={bbpLogo} />
        </div>
      </div>
      <div className="half content">
        <h2 className="title underline">About</h2>
        <p>
          The aim of the{' '}
          <a
            target="_blank"
            href="https://www.epfl.ch/research/domains/bluebrain/"
          >
            EPFL Blue Brain Project
          </a>
          , a Swiss brain research initiative founded and directed by Professor
          Henry Markram, is to build biologically detailed digital
          reconstructions and simulations of the rodent brain, and ultimately,
          the human brain.
        </p>
        {expanded && (
          <>
            <p>
              The supercomputer-based reconstructions and simulations built by
              Blue Brain offer a radically new approach for understanding the
              multilevel structure and function of the brain.
            </p>
            <p>
              Blue Brain has deployed its computing expertise and resources to
              support FIND in the development of this web platform, as part of{' '}
              <a
                target="_blank"
                href="https://www.epfl.ch/research/domains/bluebrain/blue-brain-and-covid-19/"
              >
                Blue Brain’s COVID-19 effort
              </a>
              .
            </p>
          </>
        )}
        <button className="clear" onClick={() => setExpanded(!expanded)}>
          {expanded ? 'Collapse' : 'Read More'}
        </button>
      </div>
    </section>
  );
};

export default About;
