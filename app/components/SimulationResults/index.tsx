import * as React from 'react';
import { Line } from 'react-chartjs-2';
import { Scenarios } from '../../API';
import { union } from 'lodash';
import './simulation-results.less';
import colors from '../../colors';
import Color from 'color';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSpinner } from '@fortawesome/free-solid-svg-icons';

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
  const open = !!data;

  const selectedScenario = (data || [])[selectedScenarioIndex];

  const descriptions = [
    {
      name: 'Baseline',
      description:
        'This imaginary scenario shows the predicted course of the epidemic, with no of any kind. By comparing it with the other scenarios you can see the significance of testing in terms of saved lives and infections.',
    },
    {
      name: 'Identify/isolate infected people',
      description:
        'In this scenario, 50% of available tests are used to test hospital staff and 50% are used for other groups at high risk of contracting or transmitting the infection (e.g. shopkeepers, police, factory and transport workers whose work requires a high level of contact with the public; people living in degraded housing in large cities). Tests are limited to individuals already showing symptoms. The goal is to identify and isolate the highest possible number of infected people, helping to slow down or reverse the course of the epidemic',
    },
    {
      name: 'Protect hospital capabilities',
      description:
        'In this scenario, all available tests are used to test hospital staff, if possible repeatedly.  Tests are limited to individuals already showing symptoms. The goal is to reduce the burden of the epidemic on hospital staff, preserving the capabilities necessary to help others.',
    },
  ];

  console.log({ data });
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
      title: 'Infected in Hospitals',
      key: 'num_infected',
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
          if (
            graph.key === 'num_infected' &&
            entry.compartment !== 'Hospitals'
          ) {
            return;
          }
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
                {descriptions[selectedScenarioIndex].name}
              </h2>
              <p>{descriptions[selectedScenarioIndex].description}</p>
            </div>
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
                                labelString: 'Number of People',
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
