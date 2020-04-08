import * as React from 'react';
import World from '@svg-maps/world';
import { SVGMap } from 'react-svg-map';

import './action-box.less';

const ActionBox: React.FC = () => {
  return (
    <>
      <section>
        <div className="action-box">
          <div className="title">
            <div className="number">
              <span>1</span>
            </div>
            <h2 className="underline">
              Enter your <em>Country Information</em>
            </h2>
          </div>
          <div className="container">
            <div className="input"></div>
            <div className="world">
              <SVGMap map={World} />
              <button className="action">Submit</button>
            </div>
          </div>
        </div>
      </section>

      <section>
        <div className="action-box primary">
          <div className="title">
            <div className="number">
              <span>2</span>
            </div>
            <h2 className="underline">
              Check out these <em>Cool Graphs</em>
            </h2>
          </div>
          <div className="container"></div>
        </div>
      </section>
    </>
  );
};

export default ActionBox;
