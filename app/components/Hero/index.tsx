import * as React from 'react';
import { IoIosPlay } from 'react-icons/io';

import './Hero.less';

const className = 'hero';

const Hero: React.FC = () => {
  return (
    <section className={className}>
      <span className="gradient"></span>
      <div className="content">
        {/* <h1 className="title">Covid-19</h1> */}
        <h2 className="subtitle underline">
          Diagnostic Implementation Simulator
        </h2>
        <a
          href="#country-selection"
          onClick={e => {
            e.preventDefault();
            document.querySelector('#country-select-form').scrollIntoView({
              behavior: 'smooth',
            });
          }}
        >
          <button className="btn icon">
            Start Simulation{'  '}
            <i className="icon-play">
              <IoIosPlay />
            </i>
          </button>
        </a>
      </div>
    </section>
  );
};

export default Hero;
