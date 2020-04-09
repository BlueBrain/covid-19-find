# covid-19-find

BBP/FIND COVID-19 project

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

If you have errors when running the app, it might be related to cache.
You can remove the cache folder and try to run the app again:

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

## Run API

```sh
cd api
. venv/bin/activate
flask run
```


List of country codes from https://datahub.io/core/country-list#data-cli with modifications to match COVID19 data.

COVID19 data for countries from https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_time_series