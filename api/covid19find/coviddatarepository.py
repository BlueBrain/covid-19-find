import os
import urllib.request
from werkzeug.datastructures import MultiDict
from collections import OrderedDict
import datetime
import csv
import json

from .simulation.covidlib import cl_path_prefix


class CovidDataRepository:
    confirmed_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"

    deaths_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"

    recovered_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"

    tests_url = "https://raw.githubusercontent.com/dsbbfinddx/FINDCov19TrackerData/master/processed/data_all.csv"

    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.raw_data_dir = os.path.join(data_dir, "raw")
        self.country_data_dir = os.path.join(data_dir, "country_data")
        self.country_codes = self.__load_country_codes()
        self.past_phases = self.__load_past_phases()

    def __load_past_phases(self):
        past_phases = {}
        with open(os.path.join(cl_path_prefix, "db1.csv")) as past_phases_file:
            csv_reader = csv.reader(past_phases_file, delimiter=',')
            # skip header
            next(csv_reader)
            for row in csv_reader:
                country_code = row[1]
                past_phases[country_code] = {
                    "severities": json.loads(row[3]),
                    "dates": json.loads(row[4]),
                    "score": float(row[5])
                }
        return past_phases

    def __int_or_none(self, string_int):
        try:
            return int(string_int)
        except ValueError:
            return None

    def __int_or_zero(self, string_int):
        try:
            return int(float(string_int))
        except ValueError:
            return 0

    def __read_find(self, filename):
        grouped_country_data = dict()
        with open(os.path.join(self.raw_data_dir, filename)) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row["set"] != "country":
                    continue
                country_code = row["unit"]
                country_data = grouped_country_data.get(country_code, OrderedDict())
                new_tests_positive = self.__divide_if_not_none(
                    self.__int_or_none(row["new_cases_orig"]),
                    self.__int_or_none(row["new_tests_orig"])
                )
                country_data[row["time"]] = {
                    "newTests": self.__int_or_none(row["new_tests_orig"]),
                    "totalTests": self.__int_or_none(row["all_cum_tests"]),
                    "newTestsPositiveProportion": new_tests_positive if new_tests_positive is not None and new_tests_positive < 1.0 else None
                }
                grouped_country_data[country_code] = country_data
        return grouped_country_data

    def __get_country_code(self, country_name):
        country_name = country_name.replace('*', '')
        if country_name in self.country_codes:
            return self.country_codes[country_name]
            # because sometimes United States is just US
        elif len(country_name) == 2:
            return country_name
        else:
            print("Couldn't find country code for: " + country_name)
            return None

    def __read_and_sum_johns_hopkins(self, filename):

        grouped_country_data = MultiDict()
        with open(os.path.join(self.raw_data_dir, filename)) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                country_name = row["Country/Region"]
                country_code = self.__get_country_code(country_name)
                if country_code:
                    grouped_country_data.add(country_code, row)
        summed_country_data = dict()

        for country, data in grouped_country_data.items(multi=True):
            # remove all the entries which are not count data
            del data["Province/State"]
            del data["Country/Region"]
            del data["Lat"]
            del data["Long"]
            country_data = summed_country_data.get(country, OrderedDict())
            # Do
            for date, value in data.items():
                iso_date = datetime.datetime.strptime(date, "%m/%d/%y").date().isoformat()
                current_count = country_data.get(iso_date, 0)
                country_data[iso_date] = current_count + self.__int_or_zero(value)
            summed_country_data[country] = country_data
        return summed_country_data

    def __add_new_values(self, timeseries_data):
        timeseries_data[0]["newConfirmed"] = timeseries_data[0]["totalConfirmed"]
        timeseries_data[0]["newDeaths"] = timeseries_data[0]["totalDeaths"]
        timeseries_data[0]["newRecovered"] = timeseries_data[0]["totalRecovered"]
        for i in range(1, len(timeseries_data)):
            timeseries_data[i]["newConfirmed"] = timeseries_data[i]["totalConfirmed"] - timeseries_data[i - 1][
                "totalConfirmed"]
            timeseries_data[i]["newDeaths"] = timeseries_data[i]["totalDeaths"] - timeseries_data[i - 1]["totalDeaths"]
            timeseries_data[i]["newRecovered"] = timeseries_data[i]["totalRecovered"] - timeseries_data[i - 1][
                "totalRecovered"]

    def __get_or_none(self, data, country_code, date, key):
        return data.get(country_code, {}).get(date, {}).get(key)

    def __divide_if_not_none(self, dividend, divisor):
        if dividend is not None and divisor:
            return float(dividend) / float(divisor)
        else:
            return None

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
        urllib.request.urlretrieve(self.tests_url,
                                   os.path.join(self.raw_data_dir, "data_all.csv"))

        confirmed_data = self.__read_and_sum_johns_hopkins("time_series_covid19_confirmed_global.csv")
        deaths_data = self.__read_and_sum_johns_hopkins("time_series_covid19_deaths_global.csv")
        recovered_data = self.__read_and_sum_johns_hopkins("time_series_covid19_recovered_global.csv")
        tests_data = self.__read_find("data_all.csv")

        merged_data = dict()
        for country in confirmed_data:
            country_timeseries_data = []
            for date in confirmed_data[country]:
                confirmed = confirmed_data[country][date]
                deaths = deaths_data[country][date]
                recovered = recovered_data[country][date]
                total_tests = self.__get_or_none(tests_data, country, date, "totalTests")
                new_tests = self.__get_or_none(tests_data, country, date, "newTests")
                new_tests_positive = self.__get_or_none(tests_data, country, date, "newTestsPositiveProportion")
                country_timeseries_data.append({
                    "date": date,
                    "newTests": new_tests,
                    "newTestsPositiveProportion": new_tests_positive,
                    "totalConfirmed": confirmed,
                    "totalDeaths": deaths,
                    "totalRecovered": recovered,
                    "totalTests": total_tests,
                    "currentActive": confirmed - deaths - recovered
                })
                self.__add_new_values(country_timeseries_data)
                last_data = country_timeseries_data[-1]
                merged_data[country.replace('*', '')] = {
                    "totalConfirmed": last_data["totalConfirmed"],
                    "totalDeaths": last_data["totalDeaths"],
                    "totalRecovered": last_data["totalRecovered"],
                    "totalTests": last_data["totalTests"],
                    "currentActive": last_data["currentActive"],
                    "meanTestsLast7Days": sum(map(self.__new_tests_or_zero, country_timeseries_data[-7:])),
                    "timeseries": country_timeseries_data
                }

        for country, data in merged_data.items():
            with open(os.path.join(self.country_data_dir, country + ".json"), "w") as country_file:
                json.dump(data, country_file)

    def data_for(self, country_code):
        try:
            with open(os.path.join(self.country_data_dir, country_code + ".json")) as country_file:
                covid_data = json.load(country_file)
                covid_data["currentEffectiveness"] = self.past_phases[country_code]["severities"][-1]
                return covid_data
        except FileNotFoundError:
            return None

    def __new_tests_or_zero(self, entry):
        if entry["newTests"] is not None:
            return entry["newTests"]
        else:
            return 0

    def __load_country_codes(self):
        country_codes_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), "country_codes.json")
        countries = {}
        with open(country_codes_file) as country_codes_file:
            data = json.load(country_codes_file)
            for c in data:
                countries[c["name"]] = c["countryCode"]
        return countries
