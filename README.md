![BBP-FIND - Github banner](https://user-images.githubusercontent.com/3679766/146044128-e74000fd-4a0e-43dd-82cd-ebca89fedc99.jpg)

# covid-19-find

BBP/FIND COVID-19 project

## Architecture

The application consists of four main parts:

- the simulation code
- the optimizer code
- the HTTP API
- the web frontend

The HTTP API is a wrapper around the simulation code which translates HTTP requests made by the frontend into the
parameters required by simulation code. The API also exposes data about the current state of the pandemic.

### Simulator

The simulator simulates the dynamics of the epidemic for a user-specified country from November 2019 until a specified number of days after the current date (by default 180 days).

The simulation compares the impact of four testing strategies. 

No Testing: no diagnostic tests are performed

High Contact Groups first: testing prioritizes people who cannot isolate easily (essential workers, people living in degraded urban areas), regardless of whether or not they are showing symptoms

Symptomatic First: testing prioritizes people with symptoms that could indicate infection with CODID-19

Open Public Testing: testing is performed on a first-come first-served basis, where tests are offered to anyone who asks for one.

The Simulator is based on a multi-compartmental discrete-time SIR model, modified to take account of the effects of testing (i.e. isolation of people testing positive and a proportion of their social contacts) and of key time-lags (lag between infection and first symptoms, lag between infection and death, lag between appearance of symptoms and isolation of patients with positive test results). 

No attempt is made to  model government interventions or changes in social behavior in response to changes in the dynamics of the pandemic (e.g. imposition of new restrictions or spontaneous reductions in social interactions following a rise in cases). As a result, the simulation is likely to over-estimate future cases and deaths when infections are rising and underestimate these values when infections are falling.

The simulation model considers three compartments:

- Health care workers
- Other high contact individuals (essential workers, people living in degraded urban conditions)
- Rest of the population

The size of the compartments is estimated using country demographic data. Baselines rates of transmission within and between compartments are defined such that transmission is faster within than between compartments, and faster among health-care workers and other high-contact individuals than in the rest of the population.  Daily rates of transmission are scaled using data from the optimizer (see below). Changes to baseline IFRs are scaled on the basis of trends in observed CFR. In this way the simulation implicitly takes account of the impact of vaccination on transmission and deaths.  

Input consists of:

- Epidemiological parameters (latent period of virus, time from infection to symptoms, time from infection to death, baselines IFR by age group)
- Country demographic and social parameters (population size, number of hospital beds, income category, urban population , population>=65, population 15-64 as % of total population)
- Country time series for deaths, cases, and tests performed
- Estimated severity of government intervention at different phases of the epidemic (see below)
- User determined parameters for future phases of the epidemic (stringency of government intervention, effectiveness of border controls and trace and contact procedures, number, category, sensitivity, specificity of diagnostic tests used per day, mean time from symptoms to test results)

Output consists of estimates of:

- Total numbers and numbers by compartment of new infections, deaths, cases (positive test results) and isolated patients from the November 2019 until a specified number of days after the current date (by default 180).

The Web front-end visualizes these values as graphs and summary values.

### Optimizer

The Optimizer, which is run at regular intervals, generates two parallel time series representing respectively the stringency of government intervention at different phases of the pandemic and the start date for each phase. Empirical testing has shown that these parameters alone are enough to accurately reproduce the dynamics of the pandemic for most countries. 

The values of the parameters are chosen to minimize the absolute difference between the time series for the observed and simulated number of deaths between the start of the epidemic and the current date. Goodness of fit is represented by a score.

When the score does not meet a pre-defined validity criterion, simulation results are flagged as potentially unreliable. This may occur when the simulator encounters discrepancies in the input data (e.g. very large day to day variations in reported deaths, cases or test numbers) or when total numbers of deaths are extremely small.

A fast-running version of the Optimizer generates the same time series modifying only the parameters for the most recent periods.

### API

The purpose of the API is to translate HTTP requests made by the frontend into the parameters required by simulation
code. The API also exposes data about the current state of the pandemic as well as list of available countries. The code
is situated in `api` directory. The API is written in Python using [flask](https://flask.palletsprojects.com/en/1.1.x/).

#### Available endpoints

- `GET /countries` - lists the available countries
- `GET /countries/<country_code>` - fetch statistical data for a given country, Example response:

```json
{
  "activePopulationProportion": 0.66,
  "countryCode": "CH",
  "highContactPopulation": null,
  "hospitalBeds": 34620,
  "over64Proportion": 0.20232131715771232,
  "population": 8655000,
  "remoteAreasPopulationProportion": null,
  "urbanPopulationInDegradedHousingProportion": null,
  "urbanPopulationProportion": 0.73
}
```

- `GET /api/covid19data/<country_code>` - fetch COVID-19 statistics for a given country. Example response:

```json
{
  "currentActive": 218086,
  "currentEffectiveness": 0.9,
  "timeseries": [
    {
      "currentActive": 0,
      "date": "2020-01-22",
      "newConfirmed": 0,
      "newDeaths": 0,
      "newRecovered": 0,
      "newTests": null,
      "newTestsPositiveProportion": null,
      "totalConfirmed": 0,
      "totalDeaths": 0,
      "totalRecovered": 0,
      "totalTests": 0
    }
  ],
  "totalConfirmed": 545535,
  "totalDeaths": 9849,
  "totalRecovered": 317600,
  "totalTests": 4797666
}
```

- `GET /api/scenarios` - fetch the default scenarios for the simulator

- `POST /api/simulation` - this endpoint runs the actual simulation. The request payload is defined
  in [simulation-request.schema.json](api/covid19find/simulation-request.schema.json). The response payload is defined
  in [simulation-response.schema.json](api/test/simulation-response.schema.json)

#### Configuration

The API can be configured using the following environment variables:

- `DATA_DIR` - the directory where the application will download and process data. Needs to be writable by the user
  running the app.
- `PUBLIC_URL` - the prefix used by all the api endpoints
- `FLASK_ENV` - flask environment setting, should be set to `production` in production deployments.

#### Tests

Some basic tests are implemented in [test](api/test) directory. They verify that the simulation code runs successfully
with the default parameters and that the response is in the correct format. It does not verify correctness of the
output. The tests can be run by running `pytest` in `api` directory.

#### Running the app for the first time

When running the app for the first time, the app will download and process COVID-19 data
from [Johns Hopkins University](https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_time_series)
and [FIND](https://raw.githubusercontent.com/dsbbfinddx/FINDCov19TrackerData/master/processed/data_all.csv). This might
take a few minutes, during which the API will not function.

### User Interface

The UI is a React.js application. It uses a container (data) and component (presentation) model. We use typescript throughout the app and maintain typings for props and interfaces.

The app is split into 3 sections, two of which request user input, and a third results panel.

#### State Management

The application maintains state in a React hook at the root app level `app/App.tsx`. The user manipulates this central state through the two forms. This state is used to create save files as downloadable JSON.

#### Validation

Validation is done through the native HTML5 api, and at certain points through the app validation is manually triggered. Manual validations for date inputs are done on the 2nd form.

#### Phase form inputs

in `app/components/ScenarioEditor/phaseForm.ts` there is an object that configures the phase editor in panel 2. By changing this object you can change add new inputs or change labels without touching any React component.

example:

```json
{
  "title": "Testing for Care",
  "input": [
    {
      "label": "Test Type",
      "type": INPUT_TYPES.select,
      "min": 0,
      "key": "typeTestsCare",
      "options": [
        {
          "label": TEST_TYPES.PCR,
          "value": TEST_TYPES.PCR
        },
        {
          "label": TEST_TYPES.RDT,
          "value": TEST_TYPES.RDT
        }
      ]
    },
    {
      "label": "Total tests per day",
      "type": INPUT_TYPES.number,
      "min": 0,
      "key": "numTestsCare"
    },
    {
      "label": "Recommended number of tests for care of one patient",
      "type": INPUT_TYPES.number,
      "min": 0,
      "key": "requiredDxTests"
    }
  ]
}
```

#### Tooltips

We maintain tooltips outside of the components in `tooltips.ts`. Be are: some of the keys might not match the labels presented in the interface as the properties have evolved.

#### API

There is a single API class that is the interface for all calls to the backend in `app/API.ts`, and is called in React components using `hooks/useAPI.ts`.

## Development

### Webapp

Install dependencies:

```sh
yarn
```

To start the webapp in development mode, run:

```sh
yarn start
```

Lint code:

```sh
yarn lint
```

Check style:

```sh
yarn style
```

If you have errors when running the app, it might be related to cache. You can remove the cache folder and try to run
the app again:

```
rm -fr dist/ .cache/
```

## Build Webapp for production

Compile app in `dist/` folder.

```sh
yarn build
```

## Install API dependencies

```sh
cd api
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

## Run for API for development

```sh
cd api
. venv/bin/activate
flask run
```

List of country codes from https://datahub.io/core/country-list#data-cli with modifications to match COVID19 data.

COVID19 data for countries
from https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_time_series

## Running from packaged release:

Download and unzip latest release from https://github.com/BlueBrain/covid-19-find/releases and run

```bash
cd api
pip install -r requirements.txt
./run-api.sh
```

The server downloads data
from https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_time_series and
periodically updates it. The data is saved by default to `/tmp`, but the directory can be configured using `DATA_DIR`
environment variable.

Per instructions
from [Flask documentation](https://flask.palletsprojects.com/en/1.1.x/tutorial/deploy/#run-with-a-production-server), it
is running `waitress` as the WSGI server, but any other WSGI server can be used instead if preferred.

## Configuring the client for deployment

There are two ENV vars to configure URLS for the client during build time. They both have defaults. They can be relative
or absolute paths.

- `API_URL` (default `/api`) - the base url where the client calls the API (eg `/api/simulation`)
- `PUBLIC_URL` (default `/`) - the path where the compiled static assets are hosted and publicly available.


## Acknowledgements

The development of this software is a joint collaboration between:

- Richard Walker, a consultant of the Blue Brain Project, who coordinated the development of this project.
- EPFL Blue Brain Project, a research center of the École polytechnique fédérale de Lausanne (EPFL).
- Department of Information Systems and Computer Science, Ateneo de Manila University, Philippines.
- FIND.

## Funding 

The development of this software was supported by funding to:
- the Blue Brain Project, from the Swiss government's ETH Board of the Swiss Federal Institutes of Technology.
- FIND from Unitaid.


Copyright © 2020-2021 Blue Brain Project/EPFL & Ateneo de Manila University, Manila, the Philippines

