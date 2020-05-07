import * as React from 'react';
import { Line, Bar } from 'react-chartjs-2';
import { Scenarios, Scenario } from '../../API';
import { union } from 'lodash';
import './simulation-results.less';
import colors from '../../colors';
import Color from 'color';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSpinner } from '@fortawesome/free-solid-svg-icons';
import useWindowWidth from '../../hooks/useWindowWidth';

export type SimulationResultsData = any;

export function toLetters(num: number): string {
  var mod = num % 26,
    pow = (num / 26) | 0,
    out = mod ? String.fromCharCode(64 + mod) : (--pow, 'Z');
  return pow ? toLetters(pow) + out : out;
}

const SimulationResults: React.FC<{
  loading: boolean;
  error: Error | null;
  data: Scenarios | null;
  scenarios: Scenario[];
}> = ({ loading, error, data, scenarios }) => {
  const [selectedScenarioIndex, setSelectedScenarioIndex] = React.useState(0);
  const open = !!data;

  const screenWidth = useWindowWidth();
  const isMobile = screenWidth.width < 400;

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
      title: 'Confirmed Cases',
      key: 'num_confirmed',
      color: colors.blueGray,
    },
    {
      title: 'Recovered',
      key: 'num_recovered',
      color: colors.turqouise,
    },
    {
      title: 'Infected hospital staff ',
      key: 'total_infected',
      color: colors.aubergine,
    },
    {
      title: 'Total Infections',
      key: 'total_infected',
      color: colors.aubergine,
    },
  ];

  const comparisons = [
    {
      key: 'totalDeaths',
      title: 'Total Deaths',
      color: colors.pomegranate,
    },
    {
      key: 'maxInfected',
      title: 'Peak Infected',
      color: colors.aubergine,
    },
    {
      key: 'maxIsolated',
      title: 'Peak Isolated',
      color: colors.turqouise,
    },
  ];

  const datasets = (data || []).map((entry, index) => {
    return {
      label:
        index === 0
          ? 'Baseline'
          : `Scenario ${toLetters(index).toLocaleUpperCase()}`,
      data: entry.data.reduce((memo, entry) => {
        const key = entry.days;
        const day = {
          ...(memo[key] || {}),
        };
        graphs.forEach(graph => {
          if (
            graph.key === 'total_infected' &&
            graph.title.includes('hospital') &&
            entry.compartment !== 'Hospitals'
          ) {
            // dont't add up things just for the hospital compartment
            return;
          }
          day[graph.title] =
            (Number(day[graph.title]) || 0) + Number(entry[graph.key]);
        });
        memo[key] = day;
        return memo;
      }, {}),
    };
  });

  return (
    <section className="input" id="simulation-results">
      {open && (
        <>
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
            <div className="triangle primary">
              <div className={`loader ${loading ? 'loading' : ''}`}>
                <FontAwesomeIcon icon={faSpinner} pulse />
              </div>
            </div>
          </div>
          <div className={`results-drop primary ${open ? 'open' : ''}`}>
            {selectedScenario && (
              <>
                <div className="scenario-description">
                  <h2 className="underline">
                    {scenarios[selectedScenarioIndex].name}
                  </h2>
                  <p>{scenarios[selectedScenarioIndex].description}</p>{' '}
                </div>
                <div className="comparison">
                  <div
                    className="chart"
                    key={`chart-cross-scenario-comparison`}
                  >
                    <h3 className="title">Cross-Scenario Comparison</h3>
                    <div className="flex">
                      {comparisons.map(({ key, title, color }, index) => {
                        return (
                          <div className="graph">
                            <Bar
                              width={null}
                              height={null}
                              options={{
                                tooltips: {
                                  callbacks: {
                                    label: (tooltipItem, data) => {
                                      return `${title}: ${tooltipItem.yLabel?.toLocaleString(
                                        undefined,
                                        { maximumFractionDigits: 0 },
                                      )}`;
                                    },
                                  },
                                },
                                aspectRatio: isMobile ? 1 : 2,
                                scales: {
                                  yAxes: [
                                    {
                                      scaleLabel: {
                                        display: true,
                                        labelString: title,
                                      },
                                      gridLines: {
                                        color: '#00000005',
                                      },
                                      ticks: {
                                        // beginAtZero: true,
                                        // Include a dollar sign in the ticks
                                        callback: function(value) {
                                          return value?.toLocaleString(
                                            undefined,
                                            {
                                              maximumFractionDigits: 0,
                                            },
                                          );
                                        },
                                      },
                                    },
                                  ],
                                  xAxes: [
                                    {
                                      gridLines: {
                                        color: '#00000005',
                                      },
                                      ticks: {
                                        maxRotation: isMobile ? 90 : 0, // angle in degrees
                                      },
                                    },
                                  ],
                                },
                                elements: {
                                  point: {
                                    radius: 0,
                                  },
                                  bar: {
                                    borderWidth: 2,
                                  },
                                },
                                legend: {
                                  display: false,
                                },
                              }}
                              data={{
                                datasets: [
                                  {
                                    label: key,
                                    data: data.map(scenario => scenario[key]),
                                    backgroundColor: Color(color)
                                      .alpha(0.5)
                                      .toString(),
                                    borderColor: Color(color).toString(),
                                  },
                                ],
                                labels: datasets.map(dataset => dataset.label),
                              }}
                            />
                          </div>
                        );
                      })}
                    </div>
                  </div>
                </div>
                <div className="stats horizontal">
                  <h3>
                    {Math.ceil(
                      selectedScenario.maxInfected,
                    ).toLocaleString(undefined, { maximumFractionDigits: 0 })}
                    <br />
                    <span className="subtitle">
                      Maximum number of <br /> expected infections
                    </span>
                  </h3>
                  <h3>
                    {Math.ceil(
                      selectedScenario.totalDeaths,
                    ).toLocaleString(undefined, { maximumFractionDigits: 0 })}
                    <br />
                    <span className="subtitle">Total expected deaths</span>
                  </h3>
                  <h3>
                    {Math.ceil(
                      selectedScenario.maxIsolated,
                    ).toLocaleString(undefined, { maximumFractionDigits: 0 })}
                    <br />
                    <span className="subtitle">
                      Maximum number of <br /> people in isolation
                    </span>
                  </h3>
                  <h3>
                    {Math.ceil(
                      selectedScenario.totalTests,
                    ).toLocaleString(undefined, { maximumFractionDigits: 0 })}
                    <br />
                    <span className="subtitle">
                      Total number of <br />
                      tests conducted
                    </span>
                  </h3>
                </div>{' '}
                <div className="charts">
                  {graphs.map(graph => {
                    return (
                      <div className="chart" key={`chart-${graph.title}`}>
                        <h3 className="title">{graph.title}</h3>
                        <Line
                          width={null}
                          height={null}
                          options={{
                            tooltips: {
                              callbacks: {
                                label: (tooltipItem, data) => {
                                  const label =
                                    data.datasets[tooltipItem.datasetIndex]
                                      .label || '';
                                  return `${label}: ${tooltipItem.yLabel?.toLocaleString(
                                    undefined,
                                    { maximumFractionDigits: 0 },
                                  )}`;
                                },
                              },
                            },
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
                                    callback: function(value, index, values) {
                                      return value?.toLocaleString(undefined, {
                                        maximumFractionDigits: 0,
                                      });
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
                            datasets: datasets.map((dataset, index) => {
                              const selected = selectedScenarioIndex === index;
                              return {
                                label: dataset.label,
                                data: Object.values(dataset.data).map(
                                  values => values[graph.title],
                                ),
                                borderColor: [
                                  selected
                                    ? graph.color
                                    : Color(graph.color)
                                        .alpha(0.2)
                                        .toString(),
                                ],
                                backgroundColor: [
                                  selected
                                    ? Color(graph.color)
                                        .alpha(0.2)
                                        .toString()
                                    : Color(graph.color)
                                        .alpha(0)
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
                  <p className="disclaimer-text">
                    This web tool estimates the relative impact of different
                    deployment strategies for diagnostic tests in the current
                    acute phase of the COVID-19 pandemic. The tool is not
                    intended to replace detailed epidemiological models or the
                    estimates of deaths and of epidemic duration coming from
                    such models.
                  </p>
                </div>
              </>
            )}
          </div>
        </>
      )}
    </section>
  );
};

export default SimulationResults;
