import pandas as pd
import requests
import sys
from pathlib import Path

pd.options.mode.chained_assignment = None  # default='warn'

def melt_raw_data(filename, val_name):
	raw_df = pd.read_csv(filename);
	df = raw_df.melt(id_vars=["Province/State", "Country/Region", "Lat", "Long"], 
        var_name="Date", 
        value_name=val_name)
	df["Date"] = pd.to_datetime(df["Date"])
	df = df.groupby(["Country/Region", "Date"])[val_name].sum().reset_index();
	return df;

def download_csv_from_url(csv_url, filename):
	req = requests.get(csv_url);
	url_content = req.content;
	csv_file = open(filename, 'wb');

	csv_file.write(url_content);
	csv_file.close();

deaths_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
deaths_fn = "death_data.csv"
if Path(deaths_fn).is_file():
   print('using existing '+deaths_fn+' file')
else:
   download_csv_from_url(deaths_url, deaths_fn)
deaths_df = melt_raw_data(deaths_fn, "Deaths")
# print(deaths_df);

def get_death_data_by_country(country):
	global deaths_df
	country_name = country
	country_df = deaths_df[deaths_df["Country/Region"] == country_name];
	country_df.rename(columns={"Deaths": "total_deaths"}, inplace=True);
#	print(country_df.info());
#	print("Converting..")
#	print(country_df.info())
	country_df["New deaths"] = country_df['total_deaths'].diff().fillna(country_df['total_deaths'].iloc[0])
	country_df["New deaths"] = country_df["New deaths"].astype(int)
	country_df["Date"] = country_df["Date"].astype(str)

	return country_df[["Date", "New deaths", "total_deaths"]]

def testmodule():
   country = "Spain"
   if len(sys.argv) > 1:
      country = sys.argv[1]
   df = get_death_data_by_country(country)
   df.to_csv("country.csv",index=False)

# testmodule()
