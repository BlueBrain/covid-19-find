import * as React from 'react';
import { Line, Bar, Bubble } from 'react-chartjs-2';
import * as ChartAnnotation from 'chartjs-plugin-annotation';
import Color from 'color';
import moment from 'moment';
import { maxBy } from 'lodash';
import { draw } from 'patternomaly';

import useWindowWidth from '../../hooks/useWindowWidth';
import {
  ClientScenarioData,
  SimulationResults,
  ScenarioResult,
} from '../../types/simulation';
import NumberOfTestsPerDay from './Graphs/NumberOfTestsPerDay';
import RNaught from './Graphs/RNaught';
import Prevalence from './Graphs/Prevalence';
import LivesSaved from './Graphs/LivesSaved';
import { PDFFromElement } from '../../libs/download';
import colors from '../../colors';
import AwaitingInput from './AwaitingInput';
import { truncate } from '../../libs/strings';
import {
  COLORS_BY_SCENARIO_INDEX,
  GRAPH_PATTERNS_LIST,
  SELECTED_COLOR_ALPHA,
  UNSELECTED_COLOR_ALPHA,
} from '../../config';
import { isScoreInvalid } from '../../API';

import './simulation-results.less';
import TooltipLabel from '../TooltipLabel';

function scaleValueFromLargestValueAgainstViewportWidth(
  value: number,
  minValue: number,
  maxValue: number,
) {
  const vw = Math.max(
    document.documentElement.clientWidth || 0,
    window.innerWidth || 0,
  );

  function scaleBetween(
    unscaledNum: number,
    minAllowed: number,
    maxAllowed: number,
    min: number,
    max: number,
  ) {
    return (
      ((maxAllowed - minAllowed) * (unscaledNum - min)) / (max - min) +
      minAllowed
    );
  }
  const smallesetNonZeroMinValueInPixels = 20;
  return scaleBetween(
    value,
    minValue === 0 ? 0 : smallesetNonZeroMinValueInPixels,
    vw / 20,
    minValue,
    maxValue,
  );
}

const SimulationResults: React.FC<{
  ready: boolean;
  loading: boolean;
  error: Error | null;
  simulationResults: SimulationResults;
  clientScenariosInput: ClientScenarioData[];
}> = ({ loading, ready, error, simulationResults, clientScenariosInput }) => {
  const PDFRef = React.useRef();

  const { scenarios: scenariosResults } = simulationResults || {
    scenarios: [],
  };

  const [selectedScenarioIndex, setSelectedScenarioIndex] = React.useState(0);
  const open = !!simulationResults && ready && !error;

  const screenWidth = useWindowWidth();
  const isMobile = screenWidth.width < 400;

  const selectedScenario = (scenariosResults || [])[selectedScenarioIndex];

  const patterns = GRAPH_PATTERNS_LIST;

  const graphs = [
    {
      title: 'Deaths/day',
      key: 'newDeaths',
      actualKey: 'actualDeaths',
      cohort: 'total',
    },
    {
      title: 'Total Infections/day',
      key: 'newInfected',
      cohort: 'total',
    },
    {
      title: 'Positive tests/day',
      key: 'newConfirmed',
      actualKey: 'actualCases',
      cohort: 'total',
    },
    
    {
      title: 'Infected hospital staff/day',
      key: 'newInfected',
      cohort: 'hospitals',
    },
    
  ];

  const comparisons = [
    {
      key: 'totalDeaths',
      title: 'Total Deaths',
    },
    {
      key: 'totalInfected',
      title: 'Total Infected',
    },
    {
      key: 'maxInfected',
      title: 'Peak Infected/day (from today)',
    },
    {
      key: 'maxIsolated',
      title: 'Peak in Isolation (from today)',
    },
  ];

  const datasets = Array.from(scenariosResults as ScenarioResult[]).map(
    (scenarioResult, scenarioIndex) => {
      return {
        label: clientScenariosInput[scenarioIndex]?.name,
        data: scenarioResult.data.total.reduce(
          (memo, entry, timeseriesIndex) => {
            const key = entry.date;
            const day = {
              ...(memo[key] || {}),
            };
            graphs.forEach(graph => {
              day[`${graph.key}-${graph.cohort}`] =
                scenarioResult.data[graph.cohort][timeseriesIndex][graph.key];
              if (graph.actualKey) {
                const actualDataToday =
                  scenarioResult.data[graph.cohort][timeseriesIndex][
                    graph.actualKey
                  ] || 0;

                const dailyChangeClamped =
                  actualDataToday > 0 ? actualDataToday : 0;

                day[
                  `actual-${graph.cohort}-${graph.actualKey}`
                ] = dailyChangeClamped;
              }
            });
            memo[key] = day;
            return memo;
          },
          {},
        ),
      };
    },
  );

  const handlePDFDownloadClick = () => {
    if (PDFRef.current) {
      PDFFromElement(PDFRef.current);
    }
  };

  return (
    <section className="input" id="simulation-results">
      {open ? (
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
            <div className="triangle primary"></div>
          </div>
          <div
            className={`results-drop primary ${open ? 'open' : ''}`}
            ref={PDFRef}
          >
            {selectedScenario && (
              <>
                <div className="scenario-description">
                  <h2 className="underline">
                    {clientScenariosInput[selectedScenarioIndex].name}
                  </h2>

                  {isScoreInvalid(simulationResults.score) && (
                    <h3 className="warning">
                      Current estimates of epidemic parameters for this country
                      are not reliable
                    </h3>
                  )}

                  {/* <p>{clientScenariosInput[selectedScenarioIndex].description}</p>{' '} */}
                  <button onClick={handlePDFDownloadClick}>
                    Download As PDF
                  </button>
                </div>
                <div className="chart">
                  <h3 className="title">Scenarios for next six months</h3>
                  <p style={{ textAlign: 'center', opacity: '0.5' }}>
                    The size of the circles represents the number of simulated
                    deaths
                  </p>
                  
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

                            const deaths = dataset.data[
                              tooltipItem.index
                            ].deaths.toLocaleString(undefined, {
                              maximumFractionDigits: 0,
                            });
                            return `${dataset.label}: ${deaths} deaths`;
                          },
                        },
                      },
                      scales: {
                        yAxes: [
                          {
                            // suggestedMin: 0,
                            // type: 'logarithmic',
                            beginAtZero: true,
                            scaleLabel: {
                              display: true,
                              labelString: 'Total people in Isolation',
                            },
                            gridLines: {
                              color: '#00000005',
                            },
                            ticks: {
                              // beginAtZero: true,
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
                            // type: 'logarithmic',
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
                      layout: {
                        padding: {
                          left: 60,
                          right: 60,
                          top: 60,
                          bottom: 60,
                        },
                      },
                    }}
                    data={{
                      datasets: simulationResults.scenarios.map(
                        (scenario, index) => {
                          const accumulatedIsolated = scenario.data.total.reduce(
                            (memo, entry) => {
                              return memo + entry.newIsolated;
                            },
                            0,
                          );

                          const totalDeaths = simulationResults.scenarios.map(
                            scenario => scenario.totalDeaths,
                          );
                          const minDeaths = Math.min(...totalDeaths);
                          const maxDeaths = Math.max(...totalDeaths);

                          const data = {
                            x: scenario.totalInfected,
                            y: accumulatedIsolated,
                            r: scaleValueFromLargestValueAgainstViewportWidth(
                              scenario.totalDeaths,
                              0,
                              maxDeaths,
                            ),
                            // r: scenario.totalDeaths,
                            deaths: scenario.totalDeaths,
                          };

                          // The x axis will show the total number of infected, y axis the total number of people in isolation, and the diameter of the circle will be proportional to the total number of deaths
                          return {
                            data: [data],
                            label: clientScenariosInput[index].name,
                            backgroundColor: patterns.map(patternKey =>
                              draw(
                                // @ts-ignore
                                patternKey,
                                Color(COLORS_BY_SCENARIO_INDEX[index])
                                  .alpha(SELECTED_COLOR_ALPHA)
                                  .toString(),
                              ),
                            )[index],
                          };
                        },
                      ),

                      borderColor: COLORS_BY_SCENARIO_INDEX.map(color =>
                        Color(color).toString(),
                      ),
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
                      {comparisons.map(({ key, title }, index) => {
                        console.log(key);
                        const graphPatterns = simulationResults.scenarios.map(
                          (scenario, scenarioIndex) => {
                            console.log(scenario);
                            const patternKey = patterns[scenarioIndex];
                            return draw(
                              // @ts-ignore
                              patternKey,
                              Color(COLORS_BY_SCENARIO_INDEX[scenarioIndex])
                                .alpha(UNSELECTED_COLOR_ALPHA)
                                .toString(),
                            );
                          },
                        );
                        return (
                          <div className="graph">
                            <h4 className="title">{title}</h4>
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
                                        beginAtZero: true, // comment out this line if you want chart to zoom in on the meaningful range
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
                                        callback: value => {
                                          const MAX_CHAR_LENGTH = 10;
                                          return truncate(
                                            value,
                                            MAX_CHAR_LENGTH,
                                          );
                                        },
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
                                    backgroundColor: graphPatterns,
                                    borderColor: COLORS_BY_SCENARIO_INDEX.map(
                                      color => Color(color).toString(),
                                    ),
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
                      selectedScenario.totalInfected,
                    ).toLocaleString(undefined, { maximumFractionDigits: 0 })}
                    <br />
                    <span className="subtitle">
                      Total number of <br /> expected infections
                    </span>
                  </h3>
                  <h3>
                    {Math.ceil(
                      selectedScenario.totalDeaths,
                    ).toLocaleString(undefined, { maximumFractionDigits: 0 })}
                    <br />
                    <span className="subtitle">
                      Total number of <br /> expected deaths
                    </span>
                  </h3>
                  <h3>
                    {Math.ceil(
                      selectedScenario.totalPositiveTests,
                    ).toLocaleString(undefined, { maximumFractionDigits: 0 })}
                    <br />
                    <span className="subtitle">
                      Total number of <br /> positive tests
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
                          plugins={[ChartAnnotation]}
                          width={null}
                          height={null}
                          options={{
                            annotation: {
                              annotations: [
                                // Add a vertical line
                                // that represents today's date
                                // so that the data that represents the future
                                // and thus conjecture
                                // is more obvious
                                {
                                  type: 'line',
                                  mode: 'vertical',
                                  scaleID: 'x-axis-0',
                                  value: selectedScenario.data.total.findIndex(
                                    entry =>
                                      entry.date ===
                                      moment(Date.now()).format('YYYY-MM-DD'),
                                  ),
                                  borderColor: colors.aubergine,
                                  borderWidth: 2,
                                },
                              ],
                            },
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
                                    labelString: 'Number of People',
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
                            datasets: [
                              ...datasets.map((dataset, index) => {
                                const selected =
                                  selectedScenarioIndex === index;
                                const graphPatterns = patterns.map(
                                  patternKey => ({
                                    selected: draw(
                                      // @ts-ignore
                                      patternKey,
                                      Color(COLORS_BY_SCENARIO_INDEX[index])
                                        .alpha(SELECTED_COLOR_ALPHA)
                                        .toString(),
                                    ),
                                    unselected: draw(
                                      // @ts-ignore
                                      patternKey,
                                      Color(COLORS_BY_SCENARIO_INDEX[index])
                                        .alpha(UNSELECTED_COLOR_ALPHA)
                                        .toString(),
                                    ),
                                  }),
                                );

                                return {
                                  label: dataset.label,
                                  data: Object.values(dataset.data).map(
                                    values =>
                                      values[`${graph.key}-${graph.cohort}`],
                                  ),
                                  borderDash:
                                    index === 0 ? [] : [index * 4, index * 4],
                                  borderColor: COLORS_BY_SCENARIO_INDEX[index],
                                  backgroundColor: selected
                                    ? graphPatterns[index].selected
                                    : graphPatterns[index].unselected,
                                  hidden: !selected,
                                };
                              }),
                              ...(graph.actualKey
                                ? [
                                    {
                                      label: 'Actual',
                                      data: Object.values(
                                        datasets[selectedScenarioIndex].data,
                                      ).map(
                                        values =>
                                          values[
                                            `actual-${graph.cohort}-${graph.actualKey}`
                                          ],
                                      ),
                                      borderColor: 'black',
                                    },
                                  ]
                                : []),
                            ],
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
                    {selectedScenario.testsNeededForCare.toLocaleString(
                      undefined,
                      { maximumFractionDigits: 0 },
                    )}
                    <br />
                    <span className="subtitle">
                      Number of tests <br /> used for patient care
                    </span>
                  </h3>
                  <h3>
                    {selectedScenario.testsNeededForMitigation.toLocaleString(
                      undefined,
                      { maximumFractionDigits: 0 },
                    )}
                    <br />
                    <span className="subtitle">
                      Number of tests used and required <br /> for epidemic
                      mitigation
                    </span>
                  </h3>
                </div>
                <div style={{ margin: '0 auto', width: '50%' }}>
                  <TooltipLabel
                    label="Samples Required for Serological Studies"
                    tooltipKey={'Samples Required for Serological Studies'}
                    wrapper={({ children }) => (
                      <h3 style={{ color: '#697881', textAlign: 'center' }}>
                        {children}
                      </h3>
                    )}
                  />
                  <table>
                    <tr>
                      <th>Number of Subgroups</th>
                      <th>Tests Required</th>
                    </tr>
                    {scenariosResults[
                      selectedScenarioIndex
                    ].samplesRequiredForSerologicalStudies.map(
                      (entry, index) => (
                        <tr>
                          <td>{entry.numSubgroups}</td>
                          <td>{entry.testsRequired}</td>
                        </tr>
                      ),
                    )}
                  </table>
                </div>
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
                <hr />
                <div className="charts">
                  <LivesSaved
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
      ) : (
        <AwaitingInput
          {...{
            loading,
            error,
            ready,
          }}
        />
      )}
    </section>
  );
};

export default SimulationResults;
