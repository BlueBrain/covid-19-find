import * as React from 'react';
import { Line, Bar, Bubble } from 'react-chartjs-2';
import './simulation-results.less';
import colors from '../../colors';
import Color from 'color';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSpinner } from '@fortawesome/free-solid-svg-icons';
import useWindowWidth from '../../hooks/useWindowWidth';
import { ClientScenarioData, SimulationResults } from '../../types/simulation';
import NumberOfTestsPerDay from './Graphs/NumberOfTestsPerDay';
import RNaught from './Graphs/RNaught';
import Prevalence from './Graphs/Prevalence';

export function toLetters(num: number): string {
  const mod = num % 26;
  let pow = (num / 26) | 0;
  const out = mod ? String.fromCharCode(64 + mod) : (--pow, 'Z');
  return pow ? toLetters(pow) + out : out;
}

const DEATH_CLIENT_WIDTH_SCALE_FACTOR = 100;

const SimulationResults: React.FC<{
  loading: boolean;
  error: Error | null;
  simulationResults: SimulationResults;
  clientScenariosInput: ClientScenarioData[];
}> = ({ loading, error, simulationResults, clientScenariosInput }) => {
  const { scenarios: scenariosResults } = simulationResults || {
    scenarios: [],
  };

  const [selectedScenarioIndex, setSelectedScenarioIndex] = React.useState(0);
  const open = !!simulationResults;

  const screenWidth = useWindowWidth();
  const isMobile = screenWidth.width < 400;

  const selectedScenario = (scenariosResults || [])[selectedScenarioIndex];

  const graphs = [
    {
      title: 'Deaths',
      key: 'totalDeaths',
      cohort: 'total',
      color: colors.pomegranate,
    },
    {
      title: 'Confirmed Cases',
      key: 'newConfirmed',
      cohort: 'total',
      color: colors.blueGray,
    },
    {
      title: 'Recovered',
      key: 'newRecovered',
      cohort: 'total',
      color: colors.turqouise,
    },
    {
      title: 'Infected hospital staff ',
      key: 'totalInfected',
      cohort: 'hospitals',
      color: colors.aubergine,
    },
    {
      title: 'Total Infections',
      key: 'totalInfected',
      cohort: 'total',
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
      key: 'totalInfected',
      title: 'Total Infected',
      color: colors.aubergine,
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

  const datasets = scenariosResults.map((entry, scenarioIndex) => {
    return {
      label: clientScenariosInput[scenarioIndex].name,
      data: entry.data.total.reduce((memo, entry, timeseriesIndex) => {
        const key = entry.date;
        const day = {
          ...(memo[key] || {}),
        };
        graphs.forEach(graph => {
          // if (
          //   graph.key === 'totalInfected' &&
          //   graph.title.includes('hospital')
          // ) {
          //   // dont't add up things just for the hospital compartment
          //   return;
          // }
          day[graph.key] =
            scenariosResults[scenarioIndex].data[graph.cohort][timeseriesIndex][
              graph.key
            ];
          // (Number(day[graph.key]) || 0) + Number(entry[graph.key]);
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
              {!!clientScenariosInput && (
                <ul className="scenarios">
                  {clientScenariosInput.map((clientScenarioInput, index) => {
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
                          {clientScenarioInput.name}
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
                    {clientScenariosInput[selectedScenarioIndex].name}
                  </h2>
                  {/* <p>{clientScenariosInput[selectedScenarioIndex].description}</p>{' '} */}
                </div>
                <div className="chart">
                  <h3 className="title">Scenarios Summary Graph</h3>
                  <Bubble
                    width={null}
                    height={null}
                    options={{
                      aspectRatio: isMobile ? 1 : 2,
                      tooltips: {
                        callbacks: {
                          label: (tooltipItem, data) => {
                            const dataset =
                              data.datasets[tooltipItem.datasetIndex];

                            const deaths = (
                              dataset.data[tooltipItem.index].r *
                              DEATH_CLIENT_WIDTH_SCALE_FACTOR
                            ).toLocaleString(undefined, {
                              maximumFractionDigits: 0,
                            });
                            return `${dataset.label}: ${deaths} deaths`;
                          },
                        },
                      },
                      scales: {
                        yAxes: [
                          {
                            scaleLabel: {
                              display: true,
                              labelString: 'Total people in Isolation',
                            },
                            gridLines: {
                              color: '#00000005',
                            },
                            ticks: {
                              // beginAtZero: true,
                              // Include a dollar sign in the ticks
                              callback: function(value) {
                                return value?.toLocaleString(undefined, {
                                  maximumFractionDigits: 0,
                                });
                              },
                            },
                          },
                        ],
                        xAxes: [
                          {
                            gridLines: {
                              color: '#00000005',
                            },
                            scaleLabel: {
                              display: true,
                              labelString: 'Total people infected',
                            },
                            ticks: {
                              callback: function(value) {
                                return value?.toLocaleString(undefined, {
                                  maximumFractionDigits: 0,
                                });
                              },
                              maxRotation: isMobile ? 90 : 0, // angle in degrees
                            },
                          },
                        ],
                      },
                    }}
                    data={{
                      datasets: simulationResults.scenarios.map(
                        (scenario, index) => {
                          const data = scenario.data.total.reduce(
                            (memo, entry) => {
                              const x = memo.x + entry.totalInfected;
                              const y = memo.y + entry.newIsolated;
                              const r = memo.r + entry.totalDeaths;
                              return {
                                x,
                                y,
                                r,
                              };
                            },
                            { x: 0, y: 0, r: 0 },
                          );
                          // this is a grim line of code.
                          // we need to scale deaths down to a viewable scale
                          data.r = data.r / DEATH_CLIENT_WIDTH_SCALE_FACTOR;
                          // The x axis will show the total number of infected, y axis the total number of people in isolation, and the diameter of the circle will be proportional to the total number of deaths
                          return {
                            data: [data],
                            label: clientScenariosInput[index].name,
                          };
                        },
                      ),
                      backgroundColor: Color(colors.aubergine)
                        .alpha(0.5)
                        .toString(),
                      borderColor: Color(colors.aubergine).toString(),
                      labels: clientScenariosInput.map(
                        scenario => scenario.name,
                      ),
                    }}
                  />
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
                                    data: simulationResults.scenarios.map(
                                      scenario => scenario[key],
                                    ),
                                    backgroundColor: Color(color)
                                      .alpha(0.5)
                                      .toString(),
                                    borderColor: Color(color).toString(),
                                  },
                                ],
                                labels: clientScenariosInput.map(
                                  scenario => scenario.name,
                                ),
                              }}
                            />
                          </div>
                        );
                      })}
                    </div>
                  </div>
                </div>
                <hr />
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
                </div>
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
                                    labelString: 'Date',
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
                            labels: selectedScenario.data.total.map(
                              entry => entry.date,
                            ),
                          }}
                        />
                      </div>
                    );
                  })}
                </div>
                <hr />
                <div className="stats horizontal">
                  <h3>
                    {Math.ceil(
                      selectedScenario.data.hospitals.reduce(
                        (memo, entry) => memo + entry.newTests,
                        0,
                      ),
                    ).toLocaleString(undefined, { maximumFractionDigits: 0 })}
                    <br />
                    <span className="subtitle">
                      Number of tests <br /> used for patient care
                    </span>
                  </h3>
                  <h3>
                    {Math.ceil(
                      selectedScenario.data.total.reduce(
                        (memo, entry) => memo + entry.requiredDxTests,
                        0,
                      ),
                    ).toLocaleString(undefined, { maximumFractionDigits: 0 })}
                    <br />
                    <span className="subtitle">
                      Number of tests used and required <br /> for epidemic
                      mitigation
                    </span>
                  </h3>
                  <h3>
                    {Math.ceil(
                      selectedScenario.data.total.reduce(
                        (memo, entry) => memo + entry.requiredDxTests,
                        0,
                      ),
                    ).toLocaleString(undefined, { maximumFractionDigits: 0 })}
                    <br />
                    <span className="subtitle">
                      Number of tests required to <br /> estimate seroprevalence
                    </span>
                  </h3>
                </div>
                <div></div>
                <div className="charts">
                  <NumberOfTestsPerDay
                    clientScenariosInput={clientScenariosInput}
                    scenariosResults={scenariosResults}
                    selectedScenarioIndex={selectedScenarioIndex}
                  />
                  <RNaught
                    clientScenariosInput={clientScenariosInput}
                    scenariosResults={scenariosResults}
                    selectedScenarioIndex={selectedScenarioIndex}
                  />
                  <Prevalence
                    clientScenariosInput={clientScenariosInput}
                    scenariosResults={scenariosResults}
                    selectedScenarioIndex={selectedScenarioIndex}
                  />
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
