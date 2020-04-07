import * as React from 'react';

import './Hero.less';

const className = 'hero';

const Hero: React.FC = () => {
  return (
    <section className={className}>
      <div className="content">
        <h1 className="title">Covid-19</h1>
        <div className="subtitle">
          Strategy Proposals for country-specific allocation of resoures
        </div>
        <hr />
        <button>Start Simulation</button>
      </div>
    </section>
  );
};

export default Hero;
