import * as React from 'react';
import { Line } from 'react-chartjs-2';

export type SimulationResultsData = any;

const SimulationResults: React.FC<{
  data: SimulationResultsData;
  title: string;
}> = ({ data, title }) => {
  return (
    <>
      <Line data={data} />
    </>
  );
};

export default SimulationResults;
