import * as React from 'react';
import { Line } from 'react-chartjs-2';
import Color from 'color';
import colors from '../../colors';
import useWindowWidth from '../../hooks/useWindowWidth';

import './covid-results';
import ReactTooltip from 'react-tooltip';

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

const CovidResults: React.FC<{
  data: CovidData;
  countryLabel: string;
}> = ({ data, countryLabel }) => {
  // TODO filter by first active Day
  // let firstActiveDay = 0;
  // const chartData = data.timeseries.filter((entry, index) => {
  //   if (!firstActiveDay) {
  //     if (!!entry.currentActive) {
  //       firstActiveDay = index;
  //       return true;
  //     }
  //     return !!entry.currentActive;
  //   }
  //   return true;
  // });
  const chartData = data.timeseries.slice(
    Math.max(data.timeseries.length - 7, 1),
  );

  const screenWidth = useWindowWidth();
  const isMobile = screenWidth.width < 500;

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
            data-tip
            data-for="jh-tooltip"
          >
            *
          </a>
          <ReactTooltip id="jh-tooltip">
            <p>data from Johns Hopkins University</p>
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
                    labelString: 'Number of People',
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
              // {
              //   label: 'Current Active',
              //   data: chartData.map(entry => entry.currentActive),
              //   borderColor: [colors.aubergine],
              //   backgroundColor: [
              //     Color(colors.aubergine)
              //       .alpha(0.2)
              //       .toString(),
              //   ],
              // },
              {
                label: 'New Cases',
                data: chartData.map(entry => entry.newConfirmed),

                borderColor: [colors.blueGray],
                backgroundColor: [
                  Color(colors.blueGray)
                    .alpha(0.2)
                    .toString(),
                ],
              },
              {
                label: 'New Deaths',
                data: chartData.map(entry => entry.newDeaths),
                borderColor: [colors.pomegranate],

                backgroundColor: [
                  Color(colors.pomegranate)
                    .alpha(0.2)
                    .toString(),
                ],
              },
              {
                label: 'New Recovered',
                data: chartData.map(entry => entry.newRecovered),
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
      <div className="stats">
        <h3>
          {(
            chartData[0].newConfirmed -
            chartData[chartData.length - 1].newConfirmed / 7
          )?.toLocaleString(undefined, {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2,
          })}
          <br />
          <span className="subtitle"> Daily New Cases</span>
        </h3>
        <h3>
          {(
            chartData[0].newDeaths -
            chartData[chartData.length - 1].newDeaths / 7
          )?.toLocaleString(undefined, {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2,
          })}
          <br />
          <span className="subtitle">Daily New Deaths</span>
        </h3>
        <h3>
          {(
            chartData[0].newRecovered -
            chartData[chartData.length - 1].newRecovered / 7
          )?.toLocaleString(undefined, {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2,
          })}
          <br />
          <span className="subtitle"> Daily New Recovered</span>
        </h3>
      </div>
    </div>
  );
};

export default CovidResults;
