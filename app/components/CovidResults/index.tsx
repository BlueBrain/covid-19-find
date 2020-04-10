import * as React from 'react';
import { Line } from 'react-chartjs-2';
import Color from 'color';
import colors from '../../colors';

import './covid-results';

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
  countryLabel: string;
}> = ({ data, countryLabel }) => {
  let firstActiveDay = 0;
  const chartData = data.timeseries.filter((entry, index) => {
    if (!firstActiveDay) {
      if (!!entry.currentActive) {
        firstActiveDay = index;
        return true;
      }
      return !!entry.currentActive;
    }
    return true;
  });

  return (
    <div className="result covid-results">
      <div className="stats">
        <h3>
          {data.totalConfirmed.toLocaleString()}
          <br />
          <span className="subtitle"> Coronavirus Cases</span>
        </h3>
        <h3>
          {data.totalDeaths.toLocaleString()}
          <br />
          <span className="subtitle">Deaths</span>
        </h3>
        <h3>
          {data.totalRecovered.toLocaleString()}
          <br />
          <span className="subtitle"> Recovered</span>
        </h3>
      </div>
      <div className="chart">
        <h3 className="title">
          {countryLabel} | Current State of epidemic{' '}
          <a
            title="data from Johns Hopkins University"
            href="https://coronavirus.jhu.edu/map.html"
            target="_blank"
          >
            *
          </a>
        </h3>
        <Line
          options={{
            scales: {
              yAxes: [
                {
                  scaleLabel: {
                    display: true,
                    labelString: 'People',
                  },
                },
              ],
              xAxes: [
                {
                  scaleLabel: {
                    display: true,
                    labelString: 'Days',
                  },
                },
              ],
            },
          }}
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
    </div>
  );
};

export default CovidResults;
