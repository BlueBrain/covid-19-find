import * as React from 'react';
import { Line } from 'react-chartjs-2';
import Color from 'color';

import { ScenarioResult, ClientScenarioData } from '../../../types/simulation';
import useWindowWidth from '../../../hooks/useWindowWidth';
import colors from '../../../colors';

const Prevalence: React.FC<{
  scenariosResults: ScenarioResult[];
  selectedScenarioIndex: number;
  clientScenariosInput: ClientScenarioData[];
}> = ({ scenariosResults, selectedScenarioIndex, clientScenariosInput }) => {
  const title = 'Prevalence';
  const color = colors.aubergine;

  const screenWidth = useWindowWidth();
  const isMobile = screenWidth.width < 400;

  return (
    <div
      className="chart"
      key={`chart-${title
        .toLocaleLowerCase()
        .split(' ')
        .join('-')}`}
    >
      <h3 className="title">{title}</h3>
      <Line
        width={null}
        height={null}
        options={{
          tooltips: {
            callbacks: {
              label: (tooltipItem, data) => {
                const label =
                  data.datasets[tooltipItem.datasetIndex].label || '';
                return `${label}: ${tooltipItem.yLabel?.toLocaleString(
                  undefined,
                  { maximumFractionDigits: 8 },
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
                  labelString: 'Prevalence (per day)',
                },
                gridLines: {
                  color: '#00000005',
                },
                ticks: {
                  beginAtZero: true,
                  callback: function(value, index, values) {
                    return value?.toLocaleString(undefined, {
                      maximumFractionDigits: 8,
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
          datasets: scenariosResults.map((scenario, index) => {
            const selected = selectedScenarioIndex === index;
            return {
              label: clientScenariosInput[index].name,
              data: scenario.data.total.map(entry => entry.prevalence),
              borderColor: [
                selected
                  ? color
                  : Color(color)
                      .alpha(0.2)
                      .toString(),
              ],
              backgroundColor: [
                selected
                  ? Color(color)
                      .alpha(0.2)
                      .toString()
                  : Color(color)
                      .alpha(0)
                      .toString(),
              ],
            };
          }),
          labels: scenariosResults[selectedScenarioIndex].data.total.map(
            entry => entry.date,
          ),
        }}
      />
    </div>
  );
};

export default Prevalence;
