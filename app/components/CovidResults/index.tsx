import * as React from 'react';
import { Line } from 'react-chartjs-2';
import colors from '../../colors';
import Color from 'color';

export type CovidData = {
  currentActive: number;
  timeseries: {
    currentActive: number;
    date: string;
    totalConfirmed: number;
    totalDeaths: number;
    totalRecovered: number;
  }[];
  totalConfirmed: number;
  totalDeaths: number;
  totalRecovered: number;
};

const CovidResults: React.FC<{
  data: CovidData;
}> = ({ data }) => {
  const chartData = data.timeseries.filter(entry => !!entry.currentActive);

  return (
    <>
      <section>
        <div className="half">
          <h2 className="underline">
            {data.totalConfirmed.toLocaleString()} Coronavirus Cases
          </h2>
          <h2 className="underline">
            {data.totalDeaths.toLocaleString()} Deaths
          </h2>
          <h2 className="underline">
            {data.totalRecovered.toLocaleString()} Recovered
          </h2>
        </div>
        <div className="half">
          <Line
            data={{
              backgroundColor: '#fff',
              datasets: [
                {
                  label: 'Current Active',
                  data: chartData.map(entry => entry.currentActive),
                  borderColor: [colors.aubergine],
                  backgroundColor: [
                    Color(colors.aubergine)
                      .alpha(0.2)
                      .toString(),
                  ],
                },
                {
                  label: 'Total Confirmed',
                  data: chartData.map(entry => entry.totalConfirmed),

                  borderColor: [colors.blueGray],
                  backgroundColor: [
                    Color(colors.blueGray)
                      .alpha(0.2)
                      .toString(),
                  ],
                },
                {
                  label: 'Total Deaths',
                  data: chartData.map(entry => entry.totalDeaths),
                  borderColor: [colors.pomegranate],

                  backgroundColor: [
                    Color(colors.pomegranate)
                      .alpha(0.2)
                      .toString(),
                  ],
                },
                {
                  label: 'Total Recovered',
                  data: chartData.map(entry => entry.totalRecovered),
                  borderColor: [colors.turqouise],
                  backgroundColor: [
                    Color(colors.turqouise)
                      .alpha(0.2)
                      .toString(),
                  ],
                },
              ],
              labels: chartData.map(entry => entry.date),
            }}
          />
        </div>
      </section>
    </>
  );
};

export default CovidResults;
