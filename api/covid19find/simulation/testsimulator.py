# This version of the test program is designed for tests where it is necessary
# to manually change the test parameters
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
ccode="FR"
test_directory="bbp_testing"
n_records=60
countrycode = ccode
countryname = cd.getcountryname(countrycode)
country_df = cd.getcountrydata(countrycode)
day1 = dt.datetime.strptime(country_df.iloc[0]['Date'],"%Y-%m-%d")
# This is code I plan to use to resolve china problem
#empty_df=cl.create_empty_country_df(day1, n_records)
#frames=[empty_df,country_df]
#country_df=pd.concat(frames)
#country_df = cd.getcountrydata(ccode)
datesandseverities=pd.read_csv('db1.csv',index_col='Code')
past_severities=json.loads(datesandseverities.loc[ccode]['Severities'])
past_dates=json.loads(datesandseverities.loc[ccode]['Trigger Dates'])
# =============================================================================
#past_dates= [1, 15, 70, 117, 144, 168, 195, 222, 249, 276, 296, 322, 341, 363, 383] 
#past_severities= [0.0, 1.0, 0.0, 0.95, 0.9, 0.85, 0.7, 0.75, 0.65, 0.85, 0.9, 0.8, 0.85]
# =============================================================================
print('past_dates=',past_dates)
print('past_severities=', past_severities)

 #temporary. Front_end will provide real data
fixed_params={
    'test_directory':'bbp_testing',\
    'total_pop':8200000, \
    'hospital_beds':33000, \
    'prop_15_64': 0.66, \
    'age_gt_64':0.20 ,\
    'prop_urban': 0.72, \
    'prop_below_pl':0.05, \
    'prop_woh':0.4, \
    'staff_per_bed':2.5,\
    'past_dates':past_dates,\
    'past_severities':past_severities,\
    'expert_mode':False,\
    'run_multiple_test_scenarios':True,\
    'save_results':False,\
    'fatality_reduction':0.35,\
    'num_days':450}
fixed_params=cl.get_system_params(test_directory)
fixed_params.update(cd.getcountryparams(ccode))
fixed_params.update({'past_dates':past_dates,'past_severities':past_severities,'expert_mode':True})

scenario_params=[]
#scenario parameters are parameters that change from scenario to scenario


scenario_params.append({
    'severity':['major tightening','reverse last change'],\
    'trig_values':['2021-01-25','2021-03-01'],\
    'trig_def_type':['date','date'],\
    'trig_op_type':['=','=','='],\
    'num_tests_mitigation':[0,0,0],\
    'type_test_mitigation':['PCR','PCR','PCR'],\
    'sensitivity':[0.95,0.95],\
    'specificity':[0.99,0.998],\
    'num_tests_care':[10000,10000,10000],\
    'type_tests_care':['PCR','PCR','PCR'],\
    'prop_contacts_traced':['fairly effective','fairly effective'],\
    'imported_infections_per_day':['not effective','not effective'],\
    'requireddxtests':[0,0,0],\
    'is_counterfactual':['False','False','False'],\
    'test_strategy':['no testing','no testing','no testing'],\
    'results_period':[3,3,3],\
    'prop_asymptomatic_tested':[0.4,0.4,0.4],
    'fatality_reduction_recent':[0.35,0.35,0.35]
    })
    
scenario_params.append({
    'severity':['major tightening','reverse last change'],\
    'trig_values':['2021-01-25','2021-03-01'],\
    'trig_def_type':['date','date'],\
    'trig_op_type':['=','=','='],\
    'num_tests_mitigation':[32000,32000,32000],\
    'type_test_mitigation':['PCR','PCR','PCR'],\
    'sensitivity':[0.95,0.95],\
    'specificity':[0.99,0.998],\
    'num_tests_care':[10000,10000,10000],\
    'type_tests_care':['PCR','PCR','PCR'],\
    'prop_contacts_traced':['fairly effective','fairly effective'],\
    'imported_infections_per_day':['not effective','not effective'],\
    'requireddxtests':[0,0,0],\
    'is_counterfactual':['False','False','False'],\
    'test_strategy':['high contact groups first','high contact groups first'],\
    'results_period':[3,3],\
    'prop_asymptomatic_tested':[0.4,0.4],
    'fatality_reduction_recent':[0.35,0.35]
    })
    
scenario_params.append({
    'severity':['major tightening','reverse last change'],\
    'trig_values':['2021-01-25','2021-03-01'],\
    'trig_def_type':['date','date'],\
    'trig_op_type':['=','=','='],\
    'num_tests_mitigation':[250000,250000],\
    'type_test_mitigation':['PCR','PCR'],\
    'sensitivity':[0.95,0.95],\
    'specificity':[0.998,0.998],\
    'num_tests_care':[10000,1000],\
    'type_tests_care':['PCR','PCR'],\
    'prop_contacts_traced':['fairly effective','fairly effective'],\
    'imported_infections_per_day':['not effective','not effective'],\
    'requireddxtests':[0,0],\
    'is_counterfactual':['False','False'],\
    'test_strategy':['symptomatic first','symptomatic first'],\
    'results_period':[3,3],\
    'prop_asymptomatic_tested':[0.4,0.4],
    'fatality_reduction_recent':[0.35,0.35]
    })
    
scenario_params.append({
    'severity':['major tightening','reverse last change'],\
    'trig_values':['2021-01-25','2021-03-01'],\
    'trig_def_type':['date','date'],\
    'trig_op_type':['=','='],\
    'num_tests_mitigation':[250000,250000],\
    'type_test_mitigation':['PCR','PCR'],\
    'sensitivity':[0.95,0.95],\
    'specificity':[0.99,0.998],\
    'num_tests_care':[10000,10000],\
    'type_tests_care':['PCR','PCR'],\
    'prop_contacts_traced':['fairly effective','fairly effective'],\
    'imported_infections_per_day':['not effective','not effective'],\
    'requireddxtests':[0,0,0],\
    'is_counterfactual':['False','False','False'],\
    'test_strategy':['open public testing','open public testing'],\
    'results_period':[3,3],\
    'prop_asymptomatic_tested':[0.4,0.4],
    'fatality_reduction_recent':[0.35,0.35]
    })
try:
    filename=os.path.join(fixed_params['test_directory'],'parameters.json')
except FileNotFoundError:
    print('')
    print('parameters file in ', fixed_params['test_directory'], ' not found')
    sys.exit()
cl.write_parameters(filename,fixed_params,scenario_params)
try:
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
print('Total cases by scenario')
for i in range (0,len(results_dict['total_cases_by_scenario'])):
    print ('scenario: ',i,': ', results_dict['total_cases_by_scenario'][i])
    
print('test_df=',test_df)
        
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

