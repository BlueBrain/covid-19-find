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
#testset=['test1_1','test1_2','test1_3','test1_4','test1_5','test1_6','test1_7','test1_8','test2_3b']
testset=['test1_1']
country_df = cl.getcountrydata('Switzerland.csv') #temporary. Front_end will provide real data
results=[]
for test_directory in testset:
#define parameters not included in previous tests - this overwrites values in files - needs to be eliminated
   
    filename=os.path.join(test_directory,'parameters.json')
    fixed_params,scenario_params=cl.read_parameters(filename)
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
    results.append(results_dict['total_deaths_by_scenario'][0])
    afile.close()
    for i in range(0,len(results)):
        print (testset[i],':',results,' deaths')

