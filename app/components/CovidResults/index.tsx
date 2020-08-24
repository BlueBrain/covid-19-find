import * as React from 'react';
import { Line } from 'react-chartjs-2';
import ReactTooltip from 'react-tooltip';
import Color from 'color';
import moment from 'moment';

import colors from '../../colors';
import useWindowWidth from '../../hooks/useWindowWidth';

import './covid-results';
import TrendIndicator from '../TrendIndicator';

const makeSlidingAverage = (array: any[], key: string) => (entry, index) => {
  const valuesToAverage = [];
  for (let i = index - 7; i < index; i++) {
    if (i >= 0) {
      valuesToAverage.push(array[i][key]);
    }
  }

  const average =
    valuesToAverage.length > 1
      ? valuesToAverage.reduce((memo, entry) => memo + entry, 0) /
        valuesToAverage.length
      : valuesToAverage[0];

  return average;
};

export type CovidData = {
  currentActive: number;
  timeseries: {
    currentActive: number;
    date: string;
    totalConfirmed: number;
    totalDeaths: number;
    totalRecovered: number;
    newConfirmed: number;
    newDeaths: number;
    newRecovered: number;
  }[];
  totalConfirmed: number;
  totalDeaths: number;
  totalRecovered: number;
};

const getLastWeekNumbers = (
  key: string,
  timeseries: CovidData['timeseries'],
) => {
  return {
    previous: timeseries[timeseries.length - 8][key],
    present: timeseries[timeseries.length - 1][key],
  };
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

  const screenWidth = useWindowWidth();
  const isMobile = screenWidth.width < 500;

  return (
    <div className="result covid-results">
      <div className="stats">
        <h3>
          <span>{data.totalConfirmed.toLocaleString()}</span>{' '}
          <TrendIndicator
            {...{
              ...getLastWeekNumbers('totalConfirmed', data.timeseries),
              upIsGood: false,
            }}
          />
          <span className="subtitle"> COVID-19 Positive Tests</span>
        </h3>
        <h3>
          <span>{data.totalDeaths.toLocaleString()}</span>{' '}
          <TrendIndicator
            {...{
              ...getLastWeekNumbers('totalDeaths', data.timeseries),
              upIsGood: false,
            }}
          />
          <span className="subtitle">Deaths attributed to COVID-19</span>
        </h3>
        <h3>
          <span>{data.totalRecovered.toLocaleString()}</span>{' '}
          <TrendIndicator
            {...getLastWeekNumbers('totalRecovered', data.timeseries)}
          />
          <span className="subtitle"> People Recovered from COVID-19</span>
        </h3>
      </div>
      <div className="chart">
        <h3 className="title">
          {countryLabel} | Current State of epidemic{' '}
          <a
            title="data from Johns Hopkins University"
            href="https://coronavirus.jhu.edu/map.html"
            target="_blank"
            data-tip
            data-for="jh-tooltip"
          >
            *
          </a>
          <ReactTooltip id="jh-tooltip">
            <p>case data from Johns Hopkins University</p>
          </ReactTooltip>
        </h3>
        <Line
          width={null}
          height={null}
          options={{
            aspectRatio: isMobile ? 1 : 2,
            scales: {
              yAxes: [
                {
                  scaleLabel: {
                    display: true,
                    labelString: 'Number of People (per day)',
                  },
                  gridLines: {
                    color: '#00000005',
                  },
                  ticks: {
                    beginAtZero: true,
                    // Include a dollar sign in the ticks
                    callback: value => {
                      return value?.toLocaleString();
                    },
                  },
                },
              ],
              xAxes: [
                {
                  scaleLabel: {
                    display: true,
                    labelString: 'Days',
                  },
                  gridLines: {
                    color: '#00000005',
                  },
                  ticks: {
                    beginAtZero: true,
                    // Include a dollar sign in the ticks
                    callback: value => {
                      return moment(value).format('DD MMM');
                    },
                  },
                },
              ],
            },
            elements: {
              point: {
                radius: 0,
              },
              line: {
                borderWidth: 1,
              },
            },
          }}
          data={{
            backgroundColor: '#fff',
            datasets: [
              {
                label: 'New Cases',
                data: chartData.map(
                  makeSlidingAverage(chartData, 'newConfirmed'),
                ),

                borderColor: [colors.blueGray],
                backgroundColor: [
                  Color(colors.blueGray)
                    .alpha(0.2)
                    .toString(),
                ],
              },
              {
                label: 'New Deaths',
                data: chartData.map(makeSlidingAverage(chartData, 'newDeaths')),
                borderColor: [colors.pomegranate],

                backgroundColor: [
                  Color(colors.pomegranate)
                    .alpha(0.2)
                    .toString(),
                ],
              },
              {
                label: 'New Recovered',
                data: chartData.map(
                  makeSlidingAverage(chartData, 'newRecovered'),
                ),
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
