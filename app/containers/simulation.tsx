import * as React from 'react';
import useAPI from '../hooks/useAPI';
import SimulationResults from '../components/SimulationResults';

const Simulation: React.FC<{ compartment: string }> = ({
  compartment = 'Hospitals',
}) => {
  const api = useAPI();
  const [datasets, setDatasets] = React.useState(null);

  React.useEffect(() => {
    api
      .simulation()
      .then(data => {
        console.log(data);
        const filteredData = data.filter(
          entry => entry.compartment === compartment,
        );
        const datasets = filteredData.reduce(
          (memo, entry, index) => {
            memo.numDeaths.push(Number(entry.num_deaths));
            memo.infected.push(Number(entry.num_infected));
            memo.susceptibles.push(Number(entry.susceptibles));
            memo.labels.push(`day ${entry.days}`);
            return memo;
          },
          {
            numDeaths: [],
            infected: [],
            susceptibles: [],
            labels: [],
          },
        );
        setDatasets(datasets);
      })
      .catch(console.error);
  }, []);

  return (
    datasets && (
      <SimulationResults
        data={{
          gridlines: {
            color: '#fff',
          },
          backgroundColor: '#fff',
          datasets: [
            {
              label: 'Deaths',
              data: datasets.numDeaths,
              borderColor: ['#fff'],
            },
            {
              label: 'Infected',
              data: datasets.infected,
              borderColor: ['#fff'],
            },
            {
              label: 'Susceptibles',
              data: datasets.susceptibles,
              borderColor: ['#fff'],
            },
          ],
          labels: datasets.labels,
        }}
        title={compartment}
      />
    )
  );
};

export default Simulation;
