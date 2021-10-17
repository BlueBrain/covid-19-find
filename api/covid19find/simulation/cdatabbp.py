from countryrepository import CountryRepository
from coviddatarepository import CovidDataRepository
from simulator import Simulator

data_repo = CovidDataRepository( "/tmp")
parameters_dir = ""
simulator = Simulator(data_repo, parameters_dir)
country_repo = CountryRepository()

def update_bbp_data():
   print("setting up...")
   data_repo = CovidDataRepository( "/tmp")
   data_repo.update_data()
   print("setup done ...")

def get_country_df(countrycode):
   return simulator.get_country_df(countrycode)

def get_fixed_parameters(paramdata):
   # couldn't get below to work because it's missing fields like belowPovertyLineProportion
   # return simulator.get_fixed_parameters(paramdata)
   # so I'm using this for now:
   income_category=paramdata['incomecategory']
   hospbeds = paramdata['hospitalBeds']
   if hospbeds is None:
      hospbeds = paramdata['population']/1000
   propurb = paramdata['urbanPopulationProportion']
   if propurb is None:
      propurb = 0
   else:
      propurb=round(propurb,4)
   propactive =  paramdata['activePopulationProportion']
   if propactive is None:
      propactive = 0
   else:
      propactive=round(propactive,4)
   propoverage = paramdata['over64Proportion']
   if propoverage is None:
      propoverage = 0
   else:
      propoverage=round(propoverage,4)
   params={'total_pop':paramdata['population'],
    'hospital_beds':hospbeds,
    'prop_15_64':propactive,
    'age_gt_64':propoverage,
    'prop_urban':propurb,
    # 'prop_below_pl':0.2,
    # 'prop_woh':0.6,
    'staff_per_bed':2.5,
    'income_category':income_category   
   }
   return params


def get_country_params(countrycode):
   return country_repo.country_details(countrycode)

