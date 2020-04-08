import * as React from 'react';

import './action-box.less';

const ActionBox: React.FC = () => {
  return (
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
  );
};

export default ActionBox;
