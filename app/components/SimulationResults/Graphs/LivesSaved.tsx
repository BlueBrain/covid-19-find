import * as React from 'react';
import { Line } from 'react-chartjs-2';

import { TestingImpact } from '../../../types/simulation';
import useWindowWidth from '../../../hooks/useWindowWidth';

const LivesSaved: React.FC<{
  testingImpact: TestingImpact[];
}> = ({ testingImpact }) => {
  const title = 'Lives Saved';

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
          legend: {
            display: false,
          },
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
                  labelString: 'Lives saved',
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
                  labelString: 'Increase in Testing',
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
          labels: testingImpact.map((impact, index) => `${index + 1}x`),
          datasets: [
            {
              label: 'Lives Saved',
              data: testingImpact.map(impact => impact.livesSaved),
            },
          ],
        }}
      />
    </div>
  );
};

export default LivesSaved;
