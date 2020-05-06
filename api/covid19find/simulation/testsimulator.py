#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 09:25:47 2020

@author: richard
"""


import covidlib as cl
#fictitious everyone in hospitals
num_scenarios=3
fixed_params={'total_pop':8655000, \
    'hospital_beds':34620, \
    'prop_15_64': 0.66, \
    'prop_urban': 0.73, \
    'prop_below_pl':0.05, \
    'prop_woh':0.40, \
    'staff_per_bed':2.5,\
    'sensitivity_PCR':0.95,\
    'sensitivity_RDT':0.85,\
    'sensitivity_xray':0.9,\
    'specificity_PCR':0.95,\
    'specificity_RDT':0.90,\
    'specificity_xray':0.90,\
    'num_tests_PCR':3000,\
    'num_tests_RDT':0,\
    'num_tests_xray':0}
#advanced settings
scenario_params=[None]*num_scenarios
scenario_params[0]={'intervention_type':1, \
    'intervention_timing':2, \
    'symptomatic_only':'True', \
    'prop_hospital': 0.0, \
    'prop_other_hc':1.0}
scenario_params[1]={'intervention_type':2, \
    'intervention_timing':0, \
    'symptomatic_only':'TRUE', \
    'prop_hospital': 0.5, \
    'prop_other_hc':0.5}  
scenario_params[2]={'intervention_type':2, \
    'intervention_timing':5, \
    'symptomatic_only':'TRUE', \
    'prop_hospital': 0.5, \
    'prop_other_hc':0.5}  
    #proportion of tests given to other high contact populations
#Instead of giving hospital employment it now uses hospital beds
scenario_array=cl.getscenarios()
#print('final scenario array=',scenario_array)
dataframes, total_tests_by_scenario,total_deaths_by_scenario,max_infected_by_scenario,max_isolated_by_scenario=\
                   cl.run_simulation(fixed_params,scenarios=scenario_params )
#dataframes, total_tests_by_scenario,total_deaths_by_scenario,max_infected_by_scenario,max_isolated_by_scenario=\
 #                  cl.run_simulation(fixed_params )
print ('total deaths by scenario')
for i in range (0,len(total_deaths_by_scenario)):
    print ('scenario: ',i,': ', total_deaths_by_scenario[i])
print('total tests by scenario')
for i in range (0,len(total_tests_by_scenario)):
    print ('scenario: ',i,': ', total_tests_by_scenario[i])
print('Max infected by scenario')
for i in range (0,len(max_infected_by_scenario)):
    print ('scenario: ',i,': ', max_infected_by_scenario[i])