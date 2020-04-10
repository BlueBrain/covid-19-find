import os
import urllib.request
from werkzeug.datastructures import MultiDict
from collections import OrderedDict
import datetime
import csv
import json


class CovidDataRepository:
    confirmed_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"

    deaths_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"

    recovered_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"

    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.raw_data_dir = os.path.join(data_dir, "raw")
        self.country_data_dir = os.path.join(data_dir, "country_data")

    def __read_and_sum(self, filename):

        grouped_country_data = MultiDict()
        with open(os.path.join(self.raw_data_dir, filename)) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                country_name = row["Country/Region"]
                grouped_country_data.add(country_name, row)
        summed_country_data = dict()

        for country, data in grouped_country_data.items(multi=True):
            # remove all the entries which are not count data
            data.popitem(last=False)
            data.popitem(last=False)
            data.popitem(last=False)
            data.popitem(last=False)
            country_data = summed_country_data.get(country, OrderedDict())
            # Do
            for date, value in data.items():
                current_count = country_data.get(date, 0)
                country_data[date] = current_count + int(value)
            summed_country_data[country] = country_data
        return summed_country_data

    def update_data(self):
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.raw_data_dir, exist_ok=True)
        os.makedirs(self.country_data_dir, exist_ok=True)

        urllib.request.urlretrieve(self.confirmed_url,
                                   os.path.join(self.raw_data_dir, "time_series_covid19_confirmed_global.csv"))
        urllib.request.urlretrieve(self.deaths_url,
                                   os.path.join(self.raw_data_dir, "time_series_covid19_deaths_global.csv"))
        urllib.request.urlretrieve(self.recovered_url,
                                   os.path.join(self.raw_data_dir, "time_series_covid19_recovered_global.csv"))

        confirmed_data = self.__read_and_sum("time_series_covid19_confirmed_global.csv")
        deaths_data = self.__read_and_sum("time_series_covid19_deaths_global.csv")
        recovered_data = self.__read_and_sum("time_series_covid19_recovered_global.csv")

        merged_data = dict()
        for country in confirmed_data:
            country_timeseries_data = []
            for date in confirmed_data[country]:
                confirmed = confirmed_data[country][date]
                deaths = deaths_data[country][date]
                recovered = recovered_data[country][date]
                country_timeseries_data.append({
                    "date": datetime.datetime.strptime(date, "%m/%d/%y").date().isoformat(),
                    "totalConfirmed": confirmed,
                    "totalDeaths": deaths,
                    "totalRecovered": recovered,
                    "currentActive": confirmed - deaths - recovered
                })
            last_data = country_timeseries_data[-1]
            merged_data[country.replace('*', '')] = {
                "totalConfirmed": last_data["totalConfirmed"],
                "totalDeaths": last_data["totalDeaths"],
                "totalRecovered": last_data["totalRecovered"],
                "currentActive": last_data["currentActive"],
                "timeseries": country_timeseries_data
            }

        countries = self.__load_country_codes()
        for country, data in merged_data.items():
            country_code = None
            if country in countries:
                country_code = countries[country]
            # because sometimes United States is just US
            elif len(country) == 2:
                country_code = country

            if country_code:
                with open(os.path.join(self.country_data_dir, country_code + ".json"), "w") as country_file:
                    json.dump(data, country_file)
            else:
                print("Couldn't find country code for: " + country)

    def data_for(self, country_code):
        try:
            with open(os.path.join(self.country_data_dir, country_code + ".json")) as country_file:
                return json.load(country_file)
        except FileNotFoundError:
            return None

    def __load_country_codes(self):
        country_codes_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), "country_codes.json")
        countries = {}
        with open(country_codes_file) as country_codes_file:
            data = json.load(country_codes_file)
            for c in data:
                countries[c["name"]] = c["countryCode"]
        return countries
