#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 09:25:47 2020

@author: richard
"""


import covidlib as cl
import pandas as pd
#fictitious everyone in hospitals

#fixed parameters are parameters that are the same for all scenarios
country_df = cl.getcountrydata('Switzerland.csv') #temporary. Front_end will provide real data
fixed_params={'total_pop':8200000, \
    'hospital_beds':33000, \
    'prop_15_64': 0.66, \
    'age_gt_64':0.18 ,\
    'prop_urban': 0.72, \
    'prop_below_pl':0.05, \
    'prop_woh':0.4, \
    'staff_per_bed':2.5,\
    
    }
#advanced settings
#target_betas=[0.35,0.35,0.35,0.08,0.08,0.15,0.2] #these are betas at start of each period 
#phase_start_days=[13,26,100,150,600,1200] #This and the preceding statement is temporary - will be used for target betas for each phase
scenario_params=[]
#scenario parameters are parameters that change from scenario to scenario
# The parameter values in this test code are fictitious
# scenario 0
scenario_params.append({
    'symptomatic_only':['True','True','True','True','True','True'], \
    'prop_hospital': [0.3, 0.3,0.3,0.3,0.3],\
    'prop_other_hc':[0.3,0.3,0.3,0.3,0.3],\
    'prop_rop':[0.4,0.4,0.4,0.4,0.4],\
    'severity':[0.,0.7,0.9,0.87,0.65],\
    'trig_values':[1,40,55,75,85],\
    'trig_def_type':['date','date','date','date','date','date'],\
    'trig_op_type':['=','=','=','=','='],\
    'num_tests_mitigation':[10,10,10,7000,15000],\
    'type_test_mitigation':['PCR','PCR','PCR','PCR','PCR'],\
    'sensitivity':[0.95,0.95,0.95,0.95,0.95],\
    'specificity':[0.95,0.95,0.95,0.95,0.95],\
    'num_tests_care':[0,0,0,0,0],\
    'type_tests_care':['PCR','PCR','PCR','PCR','PCR'],\
    'prop_contacts_traced':[0,0,1.0,1.0,1.0,1.0],\
    'test_multipliers':[0,1,2,3],
    'imported_infections_per_day':[0,0,20,20,20],
    'requireddxtests':[0,1,2,2,2]})
# scenario 1
scenario_params.append({
    'symptomatic_only':['True','True','True','True','True','True'], \
    'prop_hospital': [0.3, 0.3,0.3,0.3,0.3],\
    'prop_other_hc':[0.3,0.3,0.3,0.3,0.3],\
    'prop_rop':[0.4,0.4,0.4,0.4,0.4],\
    'severity':[0.1,0.8,0.6,0.4,0.8],\
    'trig_values':[1,22,90,150,200],\
    'trig_def_type':['date','date','date','date','date','date'],\
    'trig_op_type':['=','=','=','=','='],\
    'num_tests_mitigation':[0,0,0,0,0],\
    'type_test_mitigation':['PCR','PCR','PCR','PCR','PCR'],\
    'sensitivity':[0.95,0.95,0.95,0.95,0.95],\
    'specificity':[0.95,0.95,0.95,0.95,0.95],\
    'num_tests_care':[0,0,0,0,0],\
    'type_tests_care':['PCR','PCR','PCR','PCR','PCR'],\
    'prop_contacts_traced':[0,0,1.0,1.0,1.0,1.0],\
    'test_multipliers':[0,1,2,3],
    'imported_infections_per_day':[0,0,20,20,20],
    'requireddxtests':[0,1,2,2,2]})
#scenario 2
scenario_params.append({
     'symptomatic_only':['True','True','True','True','True','True'], \
    'prop_hospital': [0.3, 0.3,0.3,0.3,0.3],\
    'prop_other_hc':[0.3,0.3,0.3,0.3,0.3],\
    'prop_rop':[0.4,0.4,0.4,0.4,0.4],\
    'severity':[0.1,0.8,0.6,0.4,0.8],\
    'trig_values':[1,22,90,150,200],\
    'trig_def_type':['date','date','date','date','date','date'],\
    'trig_op_type':['=','=','=','=','='],\
    'num_tests_mitigation':[0,0,0,0,0],\
    'type_test_mitigation':['PCR','PCR','PCR','PCR','PCR'],\
    'sensitivity':[0.95,0.95,0.95,0.95,0.95],\
    'specificity':[0.95,0.95,0.95,0.95,0.95],\
    'num_tests_care':[0,0,0,0,0],\
    'type_tests_care':['PCR','PCR','PCR','PCR','PCR'],\
    'prop_contacts_traced':[0,0,1.0,1.0,1.0,1.0],\
    'test_multipliers':[0,1,2,3],
    'imported_infections_per_day':[0,0,20,20,20],
    'requireddxtests':[0,1,2,2,2]})
#print('scenario params=',scenario_params)

# =============================================================================
#     'symptomatic_only':['True','True','True','True','True','False','True'], \
#     'prop_hospital': [0.0, 0.0,0.0,0.0,0.0,0.5,0.0],\
#     'prop_other_hc':[0.0,0.0,0.0,0.0,0.0,0.5,0.0],\
#     'severity':[0.02,0.42,0.42,1.0,1.0,0.95,0.95],\
#     'trig_values':[1,20,33,52,94,120,200],
#     'num_tests_PCR':[0,0,0,0,0,3500,0],\
#     'num_tests_RDT':[0,0,0,0,0,0,0,],\
#     'num_tests_xray':[0,0,0,0,0,0,0],\
#     'trig_op_type':['=','=','=','=','=','=','='], \
#     'trig_def_type':['date','date','date','date','date','date','date'],\
#     'prop_contacts_traced':[0,0,0,0,0,0.25,0]}
# scenario_params[2]={
#     'symptomatic_only':['True','True','True','True','True','False','True'], \
#     'prop_hospital': [0.0, 0.0,0.0,0.0,0.0,0.5,0.0],\
#     'prop_other_hc':[0.0,0.0,0.0,0.0,0.0,0.5,0.0],\
#     'severity':[0.02,0.42,0.42,1.0,1.0,0.95,0.95],\
#     'trig_values':[1,20,33,52,94,120,200],
#     'num_tests_PCR':[0,0,0,0,0,3500,0],\
#     'num_tests_RDT':[0,0,0,0,0,0,0,],\
#     'num_tests_xray':[0,0,0,0,0,0,0],\
#     'trig_op_type':['=','=','=','=','=','=','='], \
#     'trig_def_type':['date','date','date','date','date','date','date'],\
#     'prop_contacts_traced':[0,0,0,0,0,0.25,0]}
# =============================================================================
 #   'init_infected':[1,1,1]}
 #   'target_betas':[0.35,0.28, 0.035,0.2,0.06] } I would like to write this but currently not possible
# =============================================================================
#  scenarios 1 and 2 temporarily commented for easier testing
# scenario_params[1]={'intervention_type':0, \
#     'intervention_timing':2, \
#     'symptomatic_only':'TRUE', \
#     'prop_hospital': 0.5, \
#     'prop_other_hc':0.5}
#   #  'target_betas':[0.35,0.28, 0.035,0.2,0.06] }  
# scenario_params[2]={'intervention_type':0, \
#     'intervention_timing':2, \
#     'symptomatic_only':'TRUE', \
#     'prop_hospital': 1.0, \
#     'prop_other_hc':0.0}
# =============================================================================
  #  'target_betas':[0.35,0.28, 0.035,0.2,0.06] }  
# =============================================================================
# fixed_params={'total_pop':38928000, \
#     'hospital_beds':1000, \
#     'prop_15_64': 0.54, \
#     'age_gt_64':0.023 ,\
#     'prop_urban': 0.25, \
#     'prop_below_pl':0.7, \
#     'prop_woh':0.80, \
#     'staff_per_bed':2.5,\
#     'sensitivity_PCR':0.95,\
#     'sensitivity_RDT':0.85,\
#     'sensitivity_xray':0.9,\
#     'specificity_PCR':0.95,\
#     'specificity_RDT':0.90,\
#     'specificity_xray':0.90,\
#     'num_tests_PCR':0,\
#     'num_tests_RDT':0,\
#     'num_tests_xray':0}
# #advanced settings
# scenario_params=[None]*num_scenarios
# scenario_params[0]={'intervention_type':2, \
#     'intervention_timing':1, \
#     'symptomatic_only':'True', \
#     'prop_hospital': 0.0, \
#     'prop_other_hc':1.0}
# scenario_params[1]={'intervention_type':2, \
#     'intervention_timing':2, \
#     'symptomatic_only':'TRUE', \
#     'prop_hospital': 0.5, \
#     'prop_other_hc':0.5}  
# scenario_params[2]={'intervention_type':2, \
#     'intervention_timing': 1, \
#     'symptomatic_only':'TRUE', \
#     'prop_hospital': 0.5, \
#     'prop_other_hc':0.5}  
# =============================================================================
    #proportion of tests given to other high contact populations
#Instead of giving hospital employment it now uses hospital beds
#scenario_array=cl.getscenarios()  #this appears to do nothing
#print('final scenario array=',scenario_array)
dataframes, test_df,results_dict=cl.run_simulation(country_df,fixed_params,scenarios=scenario_params)
#dataframes, total_tests_by_scenario,total_deaths_by_scenario,max_infected_by_scenario,max_isolated_by_scenario=\
 #                  cl.run_simulation(fixed_params )
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
        print ('scenario: ',i,': ', results_dict['total_infected_by_scenario'])

print("\nhash checksum of dataframes:")
for df in dataframes:
   print(pd.util.hash_pandas_object(df).sum())

