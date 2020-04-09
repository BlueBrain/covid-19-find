import * as React from 'react';
import { Line } from 'react-chartjs-2';

export type SimulationResultsData = any;

const SimulationResults: React.FC<{
  data: SimulationResultsData;
  title: string;
}> = ({ data, title }) => {
  return (
    <>
      <section>
        <div className="action-box primary">
          <div className="title">
            <div className="number">
              <span>2</span>
            </div>
            <h2 className="underline">{title}</h2>
          </div>
          <div className="container">
            <Line data={data} />
          </div>
        </div>
      </section>
    </>
  );
};

export default SimulationResults;
