import * as React from 'react';
import { Line } from 'react-chartjs-2';
import ReactTooltip from 'react-tooltip';
import Color from 'color';
import moment from 'moment';

import colors from '../../colors';
import useWindowWidth from '../../hooks/useWindowWidth';
import TrendIndicator from '../TrendIndicator';

import './covid-results.less';

export const makeSlidingAverage = (
  array: { [key: string]: number | string }[],
  key: string,
) => (entry, index) => {
  const valuesToAverage = [];
  for (let i = index - 7; i < index; i++) {
    if (i >= 0) {
      valuesToAverage.push(array[i][key] || 0);
    }
  }

  const average =
    valuesToAverage.length > 1
      ? valuesToAverage.reduce((memo, entry) => memo + entry, 0) /
        valuesToAverage.length
      : valuesToAverage[0];

  // results should always be greater than 0
  // sometimes rolling average can create negative values
  return average < 0 ? 0 : average;
};

export type CovidData = {
  currentActive: number;
  currentEffectiveness: number;
  timeseries: {
    currentActive: number;
    date: string;
    totalConfirmed: number;
    totalDeaths: number;
    totalRecovered: number;
    newConfirmed: number;
    newDeaths: number;
    newRecovered: number;
    [key: string]: number | string;
  }[];
  meanTestsLast7Days: number;
  totalConfirmed: number;
  totalRecovered: number;
  totalDeaths: number;
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
      if (entry.currentActive) {
        firstActiveDay = index;
        return true;
      }
      return !!entry.currentActive;
    }
    return true;
  });

  const screenWidth = useWindowWidth();
  const isMobile = screenWidth.width < 500;

  const totalConfirmed = getLastWeekNumbers('totalConfirmed', data.timeseries);
  const totalDeaths = getLastWeekNumbers('totalDeaths', data.timeseries);
  const totalRecovered = getLastWeekNumbers('totalRecovered', data.timeseries);

  const showRecovered =
    Number(totalRecovered.present) > Number(totalConfirmed.present) * 0.2;

  return (
    <div className="result covid-results">
      <div className="stats">
        <h3>
          <span>{data.totalConfirmed.toLocaleString()}</span>{' '}
          <TrendIndicator
            {...({
              ...totalConfirmed,
              upIsGood: false,
            } as { previous: number; present: number })}
          />
          <span className="subtitle"> COVID-19 Positive Tests</span>
        </h3>
        <h3>
          <span>{data.totalDeaths.toLocaleString()}</span>{' '}
          <TrendIndicator
            {...({
              ...totalDeaths,
              upIsGood: false,
            } as { previous: number; present: number })}
          />
          <span className="subtitle">Deaths attributed to COVID-19</span>
        </h3>
        <h3>
          {showRecovered ? (
            <>
              {' '}
              <span>{data.totalRecovered.toLocaleString()}</span>{' '}
              <TrendIndicator
                {...(totalRecovered as {
                  previous: number;
                  present: number;
                })}
              />
              <span className="subtitle"> People Recovered from COVID-19</span>
            </>
          ) : (
            <>
              <span>N/A</span>{' '}
              <span className="subtitle"> People Recovered from COVID-19</span>
            </>
          )}
        </h3>
        <h3>
          <span>{data.meanTestsLast7Days}</span>{' '}
          <span className="subtitle">Mean tests per day</span>
        </h3>
      </div>
      <div className="charts">
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
                    id: 'A',
                    position: 'left',
                    scaleLabel: {
                      display: true,
                      labelString: 'Number of positive tests',
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
                  {
                    id: 'B',
                    position: 'right',
                    scaleLabel: {
                      display: true,
                      labelString: 'Number of Deaths',
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
                      labelString: 'Date',
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
                  label: 'New Positive Tests',
                  yAxisID: 'A',
                  data: chartData
                    .map(makeSlidingAverage(chartData, 'newConfirmed'))
                    .map(entry => Math.floor(Number(entry))),
                  borderColor: [colors.blueGray],
                  backgroundColor: [
                    Color(colors.blueGray)
                      .alpha(0.2)
                      .toString(),
                  ],
                },
                {
                  label: 'New Deaths',
                  yAxisID: 'B',

                  data: chartData
                    .map(makeSlidingAverage(chartData, 'newDeaths'))
                    .map(entry => Math.floor(Number(entry))),
                  borderColor: [colors.pomegranate],

                  backgroundColor: [
                    Color(colors.pomegranate)
                      .alpha(0.2)
                      .toString(),
                  ],
                },

                showRecovered
                  ? {
                      label: 'New Recovered',
                      yAxisID: 'A',
                      data: chartData
                        .map(makeSlidingAverage(chartData, 'newRecovered'))
                        .map(entry => Math.floor(Number(entry))),
                      borderColor: [colors.turqouise],
                      backgroundColor: [
                        Color(colors.turqouise)
                          .alpha(0.2)
                          .toString(),
                      ],
                    }
                  : null,
              ].filter(Boolean),
              labels: chartData.map(entry => entry.date),
            }}
          />
        </div>
        <div className="chart">
          <h3 className="title">
            {countryLabel} | Current State of Testing{' '}
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
                    id: 'A',
                    position: 'left',
                    scaleLabel: {
                      display: true,
                      labelString: 'Number of Tests (per day)',
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
                  {
                    id: 'B',
                    type: 'linear',
                    position: 'right',
                    scaleLabel: {
                      display: true,
                      labelString: 'Positive (per day)',
                    },
                    ticks: {
                      beginAtZero: true,
                      callback: value => {
                        if (!value) {
                          return;
                        }
                        return `${(value * 100).toLocaleString()}%`;
                      },
                    },
                  },
                ],
                xAxes: [
                  {
                    scaleLabel: {
                      display: true,
                      labelString: 'Date',
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
                  label: 'Tests Performed',
                  yAxisID: 'A',
                  data: chartData
                    .map(makeSlidingAverage(chartData, 'newTests'))
                    .map(entry => Math.floor(Number(entry))),
                  borderColor: [colors.turqouise],
                  backgroundColor: [
                    Color(colors.turqouise)
                      .alpha(0.2)
                      .toString(),
                  ],
                },
                {
                  label: 'Tests Positive',
                  yAxisID: 'B',
                  data: chartData
                    .map(
                      makeSlidingAverage(
                        chartData,
                        'newTestsPositiveProportion',
                      ),
                    )
                    .map(entry => Number(entry).toFixed(4)),
                  borderColor: [colors.pomegranate],
                  backgroundColor: [
                    Color(colors.pomegranate)
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
    </div>
  );
};

export default CovidResults;
