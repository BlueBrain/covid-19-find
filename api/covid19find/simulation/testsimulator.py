#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 09:25:47 2020

@author: richard
"""


import covidlib as cl
import pandas as pd
import os
import json

#fixed parameters are parameters that are the same for all scenarios
country_df = cl.getcountrydata('France.csv') #temporary. Front_end will provide real data
fixed_params={'total_pop':65274000, \
    'hospital_beds':391644, \
    'prop_15_64': 0.62, \
    'age_gt_64':0.2195 ,\
    'prop_urban': 0.8, \
    'prop_below_pl':0.1, \
    'prop_woh':0.4, \
    'staff_per_bed':2.5,\
    'test_directory':'scratch1',\
    'past_dates':[1, 63, 165],\
    'past_severities':[0.0,0.945,0.6],\
    'expert_mode':True
    }
scenario_params=[]
#scenario parameters are parameters that change from scenario to scenario
# For test purposes scenarios 0 and 1 are commented out. In final version they will return
# Pls do not delecte
# The parameter values in this test code are fictitious

# scenario 0
# =============================================================================
# scenario_params.append({
#     'symptomatic_only':['True','True','True','True','True','True'], \
#     'prop_hospital': [0.3, 0.3,0.3,0.3,0.3],\
#     'prop_other_hc':[0.3,0.3,0.3,0.3,0.3],\
#     'prop_rop':[0.4,0.4,0.4,0.4,0.4],\
#     'severity':[0.3, 0.9, 0.8, 0.4, 0.0],\
#     'trig_values':[1,44,74,88,199],\
#     'trig_def_type':['date','date','date','date','date','date'],\
#     'trig_op_type':['=','=','=','=','='],\
#     'num_tests_mitigation':[0,0,0,0,0],\
#     'type_test_mitigation':['PCR','PCR','PCR','PCR','PCR'],\
#     'sensitivity':[0.95,0.95,0.95,0.95,0.95],\
#     'specificity':[0.95,0.95,0.95,0.95,0.95],\
#     'num_tests_care':[0,0,0,0,0],\
#     'type_tests_care':['PCR','PCR','PCR','PCR','PCR'],\
#     'prop_contacts_traced':[0,0,0.25,0.25,0.25,0.25],\
#     'test_multipliers':[0,1,2,3],
#     'imported_infections_per_day':[0,0,20,20,20],
#     'requireddxtests':[0,1,2,2,2]})
# =============================================================================
# This now represents current phase + next phase - params for other phases are inferred by optimization program
# =============================================================================
# scenario_params.append({   
# 'symptomatic_only':['True','True'], \
#     'prop_hospital': [0.3, 0.3],\
#     'prop_other_hc':[0.3,0.3],\
#     'prop_rop':[0.4,0.4],\
#     'severity':[0.8, 0.8],\
#     'trig_values':['2020-09-11','2020-12-30'],\
#     'trig_def_type':['date','date'],\
#     'trig_op_type':['=','='],\
#     'num_tests_mitigation':[0,0],\
#     'type_test_mitigation':['PCR','PCR'],\
#     'sensitivity':[0.95,0.95],\
#     'specificity':[0.95,0.95],\
#     'num_tests_care':[0,0],\
#     'type_tests_care':['PCR','PCR'],\
#     'prop_contacts_traced':[0.25,0.25],\
#     'imported_infections_per_day':[20,20],
#     'requireddxtests':[1,2],
#     'is_counterfactual':['True','True']})
# =============================================================================

# =============================================================================
# scenario_params.append({
#    'symptomatic_only':['True','True'], \
#     'prop_hospital': [0.5, 0.5],\
#     'prop_other_hc':[0.5,0.5],\
#     'prop_rop':[0.0,0.0],\
#     'severity':[0.8, 0.8],\
#     'trig_values':['2020-09-11','2020-12-30'],\
#     'trig_def_type':['date','date'],\
#     'trig_op_type':['=','='],\
#     'num_tests_mitigation':[3000,3000],\
#     'type_test_mitigation':['PCR','PCR'],\
#     'sensitivity':[0.95,0.95],\
#     'specificity':[0.95,0.95],\
#     'num_tests_care':[0,0],\
#     'type_tests_care':['PCR','PCR'],\
#     'prop_contacts_traced':[0.25,0.25],\
#     'imported_infections_per_day':[20,20],\
#     'requireddxtests':[1,2],\
#     'is_counterfactual':['False','False']})
# =============================================================================
#scenario 2
scenario_params.append({
    'symptomatic_only':['True','True'], \
    'prop_hospital': [0.4, 0.4],\
    'prop_other_hc':[0.3,0.3],\
    'prop_rop':[0.3,0.3],\
    'severity':[0.9, 0.9 ],\
    'trig_values':['2020-10-04','2020-12-30'],\
    'trig_def_type':['date','date'],\
    'trig_op_type':['=','='],\
    'num_tests_mitigation':[130000,130000],\
    'type_test_mitigation':['PCR','PCR'],\
    'sensitivity':[0.95,0.95],\
    'specificity':[0.95,0.95],\
    'num_tests_care':[10000,10000],\
    'type_tests_care':['PCR','PCR'],\
    'prop_contacts_traced':[0.25,0.25],\
    'imported_infections_per_day':[50,50],\
    'requireddxtests':[2,2],\
    'is_counterfactual':['False','False'],\
    'test_strategy':['open public testing','open public testing'],\
    'results_period':[1,1],\
    'prop_asymptomatic_tested':[0.01,0.01]
    })
filename=os.path.join(fixed_params['test_directory'],'parameters.json')
cl.write_parameters(filename,fixed_params,scenario_params)
dataframes, test_df,results_dict=cl.run_simulation(country_df,fixed_params,scenarios=scenario_params)

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

