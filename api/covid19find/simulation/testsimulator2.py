# This version of the test program is designed to test 
# the simulator when all parameters are loaded with default values
# and the scenarios contain two phases each characterized by the same default values
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 09:25:47 2020
@author: richard
"""

import covidlib as cl
import pandas as pd
import os
import json
import sys
import cdata as cd
import datetime as dt


#fixed parameters are parameters that are the same for all scenario
 #temporary. Front_end will provide real data
ccode = 'FR'
n_records=0
country_df = cd.getcountrydata(ccode)
datesandseverities=pd.read_csv('db1.csv',index_col='Code')
day1 = dt.datetime.strptime(country_df.iloc[0]['Date'],"%Y-%m-%d")-dt.timedelta(days=n_records)
empty_df=cl.create_empty_country_df(day1, n_records)
frames=[empty_df,country_df]
country_df=pd.concat(frames)
past_severities=json.loads(datesandseverities.loc[ccode]['Severities'])
past_dates=json.loads(datesandseverities.loc[ccode]['Trigger Dates'])
#past_severities=[0.0, 0.05, 0.55, 1.0, 0.05, 1.0, 0.8, 0.65, 0.95, 1.0]
#past_dates=[1, 21, 48, 62, 104, 119, 203, 217, 232, 260]
print('past_dates=',past_dates)
print('past_severities=', past_severities)
 #temporary. Front_end will provide real data

test_directory='BBP_testing'
#This loads the default system parameters
fixed_params=cl.get_system_params(test_directory)
fixed_params.update(cd.getcountryparams(ccode))
fixed_params.update({'past_dates':past_dates,'past_severities':past_severities,'expert_mode':True})
#This loads country data
# =============================================================================
# fixed_params.update({
#     'total_pop':8200000, \
#     'hospital_beds':33000, \
#     'prop_15_64': 0.66, \
#     'age_gt_64':0.20 ,\
#     'prop_urban': 0.72, \
#     'prop_below_pl':0.05, \
#     'prop_woh':0.4, \
#     'staff_per_bed':2.5,\
#     'past_dates':past_dates,\
#     'past_severities':past_severities})
# =============================================================================
# =============================================================================

scenario_params=[]
#scenario parameters are parameters that change from scenario to scenario

scenario_params=cl.get_next_phases_scenarios(fixed_params['test_directory'])
try:
    filename=os.path.join(fixed_params['test_directory'],'parameters.json')
except FileNotFoundError:
    print('')
    print('parameters file in ', fixed_params['test_directory'], ' not found')
    sys.exit()
cl.write_parameters(filename,fixed_params,scenario_params)
try:

    with open('testsimulator2-params.json', 'w') as outfile:
            json.dump([country_df.to_json(), fixed_params, scenario_params], outfile)
    dataframes, test_df,results_dict=cl.run_simulation(country_df,fixed_params,scenarios=scenario_params)
except FileNotFoundError as inst:
    print('')
    print('Exception raised by simulation:',inst)
    sys.exit()
# =============================================================================
# except KeyError as inst:
#     print('')
#     print('Exception raised by simulation:',inst)
#     sys.exit()
# =============================================================================
# The following lines protect the program against unexpected errors. Commented for testing purposes to get full error messages
# =============================================================================
# except Exception as inst :
#     print(' ')
#     print('Exception raised by simulation:',inst)
#     sys.exit()
# =============================================================================
print ('total deaths by scenario')
for i in range (0,len(results_dict['total_deaths_by_scenario'])):
    print ('scenario: ',i,': ', results_dict['total_deaths_by_scenario'][i])
print('total tests by scenario')
for i in range (0,len(results_dict['total_tests_mit_by_scenario'])):
    print ('scenario: ',i,': ', results_dict['total_tests_mit_by_scenario'][i])
print('Max infected by scenario')
for i in range (0,len(results_dict['max_infected_by_scenario'])):
    print ('scenario: ',i,': ', results_dict['max_infected_by_scenario'][i])
print('Total infected by scenario')
for i in range (0,len(results_dict['total_infected_by_scenario'])):
    print ('scenario: ',i,': ', results_dict['total_infected_by_scenario'][i])
        
#print ('results dict=',results_dict)

print("\nhash checksum of dataframes:")
for df in dataframes:
   print(pd.util.hash_pandas_object(df).sum())
afilename=os.path.join(fixed_params['test_directory'],'result_summary.csv')
adict={'deaths':results_dict['total_deaths_by_scenario']}
afile= open(afilename,'w')
for i in range (0,len(results_dict['total_deaths_by_scenario'])):
     outstring='scenario: ' + str(i,) + ', ' + str( results_dict['total_deaths_by_scenario'][i])
     afile.write (outstring)
afile.close()