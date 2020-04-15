import * as React from 'react';
import { Line } from 'react-chartjs-2';
import { Scenarios } from '../../API';
import { union, keyBy } from 'lodash';
import './simulation-results.less';
import colors from '../../colors';
import Color from 'color';

export type SimulationResultsData = any;

function toLetters(num: number): string {
  var mod = num % 26,
    pow = (num / 26) | 0,
    out = mod ? String.fromCharCode(64 + mod) : (--pow, 'Z');
  return pow ? toLetters(pow) + out : out;
}

const SimulationResults: React.FC<{
  loading: boolean;
  error: Error | null;
  data: Scenarios | null;
}> = ({ loading, error, data }) => {
  const [selectedScenarioIndex, setSelectedScenarioIndex] = React.useState(0);
  const open = !loading;

  const selectedScenario = (data || [])[selectedScenarioIndex];

  const labels = union(
    ...(data || []).map(entry => entry.data.map(entry => entry.days)),
  );
  const graphs = [
    {
      title: 'Deaths',
      key: 'new_deaths',
      color: colors.pomegranate,
    },
    {
      title: 'Confirmed',
      key: 'num_confirmed',
      color: colors.blueGray,
    },
    {
      title: 'Recovered',
      key: 'num_recovered',
      color: colors.turqouise,
    },
    {
      title: 'Isolated',
      key: 'num_isolated',
      color: colors.aubergine,
    },
  ];
  const datasets = (data || []).map((entry, index) => {
    return {
      label: `Scenario ${toLetters(index + 1).toLocaleUpperCase()}`,
      data: entry.data.reduce((memo, entry) => {
        const key = entry.days;
        const day = {
          ...(memo[key] || {}),
        };
        graphs.forEach(graph => {
          day[graph.key] = (day[graph.key] || 0) + Number(entry[graph.key]);
        });
        memo[key] = day;
        return memo;
      }, {}),
    };
  });

  return (
    <section className="input" id="simulation-results">
      <div className="action-box primary">
        <div className="title">
          <div className="number">
            <span>3</span>
          </div>
          <h2 className="underline">
            Select and view <em>Proposed Scenarios</em>
          </h2>
        </div>
        <div className="container">
          {!!data && (
            <ul className="scenarios">
              {data.map((scenario, index) => {
                return (
                  <li
                    className={`scenario ${
                      selectedScenarioIndex === index ? 'selected' : ''
                    }`}
                    key={`scenario ${index}`}
                  >
                    <button
                      onClick={() => {
                        setSelectedScenarioIndex(index);
                      }}
                    >
                      {datasets[index].label}
                    </button>
                  </li>
                );
              })}
            </ul>
          )}
        </div>
        <div className="triangle primary"></div>
      </div>
      <div
        className={`results-drop primary ${open ? 'open' : ''}`}
        // To prevent flashing
        style={{ minHeight: 443 }}
      >
        {selectedScenario && (
          <>
            <div className="stats horizontal">
              <h3>
                {Math.ceil(selectedScenario.maxInfected).toLocaleString()}
                <br />
                <span className="subtitle">Max Infected</span>
              </h3>
              <h3>
                {Math.ceil(selectedScenario.totalDeaths).toLocaleString()}
                <br />
                <span className="subtitle">Total Deaths</span>
              </h3>
              <h3>
                {Math.ceil(selectedScenario.maxIsolated).toLocaleString()}
                <br />
                <span className="subtitle">Max Isolated</span>
              </h3>
              <h3>
                {Math.ceil(selectedScenario.totalTests).toLocaleString()}
                <br />
                <span className="subtitle"> Total Tests</span>
              </h3>
            </div>
            <div className="charts">
              {graphs.map(graph => {
                return (
                  <div className="chart" key={`chart-${graph.title}`}>
                    <h3 className="title">{graph.title}</h3>
                    <Line
                      options={{
                        scales: {
                          yAxes: [
                            {
                              scaleLabel: {
                                display: true,
                                labelString: 'People',
                              },
                              gridLines: {
                                color: '#00000005',
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
                        datasets: datasets.map((dataset, index) => {
                          const selected = selectedScenarioIndex === index;
                          return {
                            label: dataset.label,
                            data: Object.values(dataset.data).map(
                              values => values[graph.key],
                            ),
                            borderColor: [
                              selected
                                ? graph.color
                                : Color(graph.color)
                                    .alpha(0.4)
                                    .toString(),
                            ],
                            backgroundColor: [
                              Color(graph.color)
                                .alpha(0.2)
                                .toString(),
                            ],
                          };
                        }),
                        labels,
                      }}
                    />
                  </div>
                );
              })}
            </div>
            <div className="disclaimer">
              <p>
                This web tool estimates the relative impact of different
                deployment strategies for diagnostic tests in the current acute
                phase of the COVID-19 pandemic. The tool is not intended to
                replace detailed epidemiological models or the estimates of
                deaths and of epidemic duration coming from such models.
              </p>
            </div>
          </>
        )}
      </div>
    </section>
  );
};

export default SimulationResults;
