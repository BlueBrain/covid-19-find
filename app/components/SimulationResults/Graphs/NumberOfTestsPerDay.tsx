import * as React from 'react';
import { Line } from 'react-chartjs-2';
import Color from 'color';
import { draw } from 'patternomaly';

import { ScenarioResult, ClientScenarioData } from '../../../types/simulation';
import useWindowWidth from '../../../hooks/useWindowWidth';
import colors from '../../../colors';
import {
  COLORS_BY_SCENARIO_INDEX,
  GRAPH_PATTERNS_LIST,
  SELECTED_COLOR_ALPHA,
  UNSELECTED_COLOR_ALPHA,
} from '../../../config';

const NumberOfTestsPerDay: React.FC<{
  scenariosResults: ScenarioResult[];
  selectedScenarioIndex: number;
  clientScenariosInput: ClientScenarioData[];
}> = ({ scenariosResults, selectedScenarioIndex, clientScenariosInput }) => {
  const title = 'Number of tests per day';
  const color = colors.turqouise;

  const screenWidth = useWindowWidth();
  const isMobile = screenWidth.width < 400;

  const patterns = GRAPH_PATTERNS_LIST;

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
                  labelString: 'Number of Tests (per day)',
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
          datasets: scenariosResults.map((scenario, index) => {
            const selected = selectedScenarioIndex === index;
            const graphPatterns = patterns.map(patternKey => ({
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
            }));
            return {
              label: clientScenariosInput[index].name,
              data: scenario.data.total.map(entry => entry.newTests),
              borderColor: COLORS_BY_SCENARIO_INDEX[index],
              backgroundColor: selected
                ? graphPatterns[index].selected
                : graphPatterns[index].unselected,
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

export default NumberOfTestsPerDay;
