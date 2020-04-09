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


## Running from packaged release:

Download and unzip latest release from https://github.com/BlueBrain/covid-19-find/releases and run

```bash
cd api
pip install -r requirements.txt
./run-api.sh 
```

The server downloads data from https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_time_series and periodically updates it.
The data is saved by default to `/tmp`, but the directory can be configured using `DATA_DIR` environment variable.

Per instructions from [Flask documentation](https://flask.palletsprojects.com/en/1.1.x/tutorial/deploy/#run-with-a-production-server), it is running `waitress` as the WSGI server, but any other WSGI server can be used instead if preferred.