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
 #temporary. Front_end will provide real data
testset=['test1_1','test1_2','test1_3','test1_4','test1_5','test1_6','test1_7','test1_8','test2_3b']
country_df = cl.getcountrydata('Switzerland.csv') #temporary. Front_end will provide real data
for test_directory in testset:
    print('test directory=', test_directory)
#define parameters not included in previous tests
    new_fixed_params={ 'past_dates':[1, 29, 50, 73, 135, 140],\
        'past_severities':[0.0, 0.2, 0.91, 0.98, 0.6, 0.75],\
        'expert_mode':'False',\
        'test_directory':test_directory}
    new_scenario_params={'test_strategy':['open public testing','open public testing'],\
        'results_period':[1,1],\
        'prop_asymptomatic_tested':[0.01,0.01]}
    
    filename=os.path.join(test_directory,'parameters.json')
    fixed_params,scenario_params=cl.read_parameters(filename)
    fixed_params.update(new_fixed_params)
    scenario_params[0].update(new_scenario_params)
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

