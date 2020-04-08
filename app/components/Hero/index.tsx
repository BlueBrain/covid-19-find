import * as React from 'react';

import './Hero.less';

const className = 'hero';

const Hero: React.FC = () => {
  return (
    <section className={className}>
      <span className="gradient"></span>
      <div className="content">
        <h1 className="title">Covid-19</h1>
        <h2 className="subtitle underline">
          Strategy Proposals for <br />
          country-specific allocation of <br />
          resoures
        </h2>
        <button className="btn icon">
          <i className="icon-play"></i>Start Simulation{' '}
        </button>
      </div>
    </section>
  );
};

export default Hero;
``;
