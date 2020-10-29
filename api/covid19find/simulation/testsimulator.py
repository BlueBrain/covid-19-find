
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


#fixed parameters are parameters that are the same for all scenario
 #temporary. Front_end will provide real data
country_df = cl.getcountrydata('Switzerland.csv')
datesandseverities=pd.read_csv('db1.csv',index_col='Code')
past_severities=json.loads(datesandseverities.loc['CH']['Severities'])
past_dates=json.loads(datesandseverities.loc['CH']['Trigger Dates'])
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
    'expert_mode':True,
    'run_multiple_test_scenarios':True,
    'save_results':True}

scenario_params=[]
#scenario parameters are parameters that change from scenario to scenario
# Here we only append 1 scenario. In the final version there will be 3 
# Pls do not delecte

scenario_params.append({
    'severity':[0.9, 0.95],\
    'trig_values':['2020-09-15','2020-12-30'],\
    'trig_def_type':['date','date'],\
    'trig_op_type':['=','='],\
    'num_tests_mitigation':[13000,13000],\
    'type_test_mitigation':['PCR','PCR'],\
    'sensitivity':[0.95,0.95],\
    'specificity':[0.95,0.95],\
    'num_tests_care':[10000,10000],\
    'type_tests_care':['PCR','PCR'],\
    'prop_contacts_traced':[0.25,0.25],\
    'imported_infections_per_day':[1,1],\
    'requireddxtests':[2,2],\
    'is_counterfactual':['False','False'],\
    'test_strategy':['no testing','no testing'],\
    'results_period':[1,1],\
    'prop_asymptomatic_tested':[0.02,0.02]
    })
    
scenario_params.append({
    'severity':[0.7, 0.95],\
    'trig_values':['2020-09-15','2020-10-15'],\
    'trig_def_type':['date','date'],\
    'trig_op_type':['=','='],\
    'num_tests_mitigation':[13000,13000],\
    'type_test_mitigation':['PCR','PCR'],\
    'sensitivity':[0.95,0.95],\
    'specificity':[0.95,0.95],\
    'num_tests_care':[10000,10000],\
    'type_tests_care':['PCR','PCR'],\
    'prop_contacts_traced':[0.25,0.25],\
    'imported_infections_per_day':[100,100],\
    'requireddxtests':[2,2],\
    'is_counterfactual':['False','False'],\
    'test_strategy':['special groups with symptoms','special groups with symptoms'],\
    'results_period':[1,1],\
    'prop_asymptomatic_tested':[0.02,0.02]
    })
    
scenario_params.append({
    'severity':[0.7, 0.95],\
    'trig_values':['2020-09-15','2020-10-15'],\
    'trig_def_type':['date','date'],\
    'trig_op_type':['=','='],\
    'num_tests_mitigation':[13000,13000],\
    'type_test_mitigation':['PCR','PCR'],\
    'sensitivity':[0.95,0.95],\
    'specificity':[0.95,0.95],\
    'num_tests_care':[10000,10000],\
    'type_tests_care':['PCR','PCR'],\
    'prop_contacts_traced':[0.25,0.25],\
    'imported_infections_per_day':[100,100],\
    'requireddxtests':[2,2],\
    'is_counterfactual':['False','False'],\
    'test_strategy':['all symptomatic','all symptomatic'],\
    'results_period':[1,1],\
    'prop_asymptomatic_tested':[0.02,0.02]
    })
    
scenario_params.append({
    'severity':[0.7, 0.95],\
    'trig_values':['2020-09-15','2020-10-15'],\
    'trig_def_type':['date','date'],\
    'trig_op_type':['=','='],\
    'num_tests_mitigation':[13000,13000],\
    'type_test_mitigation':['PCR','PCR'],\
    'sensitivity':[0.95,0.95],\
    'specificity':[0.95,0.95],\
    'num_tests_care':[10000,10000],\
    'type_tests_care':['PCR','PCR'],\
    'prop_contacts_traced':[0.25,0.25],\
    'imported_infections_per_day':[100,100],\
    'requireddxtests':[2,2],\
    'is_counterfactual':['False','False'],\
    'test_strategy':['open public testing','open public testing'],\
    'results_period':[1,1],\
    'prop_asymptomatic_tested':[0.02,0.02]
    })
try:
    filename=os.path.join(fixed_params['test_directory'],'parameters.json')
except FileNotFoundError:
    print('parameters file in ', fixed_params['test_directory'], ' not found')
    sys.exit()
cl.write_parameters(filename,fixed_params,scenario_params)
try:
    dataframes, test_df,results_dict=cl.run_simulation(country_df,fixed_params,scenarios=scenario_params)
except FileNotFoundError:
    sys.exit()
except KeyError:
    sys.exit()
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

