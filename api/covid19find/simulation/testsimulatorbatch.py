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
import copy


#fixed parameters are parameters that are the same for all scenario
 #temporary. Front_end will provide real data

codes=['FR','CN','IN','PH','SE','CH','DE','NG','GB','NE','US','PE','AU','CU','TH','BE','CL','VN','CA']
cl_path_prefix = os.path.abspath(os.path.dirname(__file__))
test_directory="bbp_testing"
results_dir='results'
results_df=pd.DataFrame(columns=['Country', 'Scenario','Simulated Deaths','Simulated cases','Tests','Severity'])
scenario_params_orig=[]
scenario_params_orig.append({
    'severity':[1.0, 1.0],\
    'trig_values':['2020-12-15','2021-01-25'],\
    'trig_def_type':['date','date','date'],\
    'trig_op_type':['=','=','='],\
    'num_tests_mitigation':[0,0,0],\
    'type_test_mitigation':['PCR','PCR','PCR'],\
    'sensitivity':[0.95,0.95],\
    'specificity':[1.0,1.0],\
    'num_tests_care':[10000,10000,10000],\
    'type_tests_care':['PCR','PCR','PCR'],\
    'prop_contacts_traced':[0.20,0.20,0.20],\
    'imported_infections_per_day':[1,1,1],\
    'requireddxtests':[0,0,0],\
    'is_counterfactual':['False','False','False'],\
    'test_strategy':['no testing','no testing','no testing'],\
    'results_period':[3,3,3],\
    'prop_asymptomatic_tested':[0.4,0.4,0.4],
    'fatality_reduction_recent':[0.35,0.35,0.35]
    })
    
scenario_params_orig.append({
    'severity':[1.0, 1.0],\
    'trig_values':['2020-12-15','2021-01-25'],\
    'trig_def_type':['date','date','date'],\
    'trig_op_type':['=','=','='],\
    'num_tests_mitigation':[32000,32000,32000],\
    'type_test_mitigation':['PCR','PCR','PCR'],\
    'sensitivity':[0.95,0.95],\
    'specificity':[1.0,1.0],\
    'num_tests_care':[10000,10000,10000],\
    'type_tests_care':['PCR','PCR','PCR'],\
    'prop_contacts_traced':[0.20,0.20,0.20],\
    'imported_infections_per_day':[1,1,1],\
    'requireddxtests':[0,0,0],\
    'is_counterfactual':['False','False','False'],\
    'test_strategy':['high contact groups first','high contact groups first','high contact groups first'],\
    'results_period':[3,3,3],\
    'prop_asymptomatic_tested':[0.4,0.4,0.4],
    'fatality_reduction_recent':[0.35,0.35,0.35]
    })
    
scenario_params_orig.append({
    'severity':[1.0, 1.0 ],\
    'trig_values':['2020-12-15','2021-01-25'],\
    'trig_def_type':['date','date','date'],\
    'trig_op_type':['=','=','='],\
    'num_tests_mitigation':[32000,32000,32000],\
    'type_test_mitigation':['PCR','PCR','PCR'],\
    'sensitivity':[0.95,0.95],\
    'specificity':[1.0,1.0],\
    'num_tests_care':[10000,10000,10000],\
    'type_tests_care':['PCR','PCR','PCR'],\
    'prop_contacts_traced':[0.2,0.2,0.2],\
    'imported_infections_per_day':[1,1,1],\
    'requireddxtests':[0,0,0],\
    'is_counterfactual':['False','False','False'],\
    'test_strategy':['symptomatic first','symptomatic first','symptomatic first'],\
    'results_period':[3,3,3],\
    'prop_asymptomatic_tested':[0.4,0.4,0.4],
    'fatality_reduction_recent':[0.35,0.35,0.35]
    })
    
scenario_params_orig.append({
    'severity':[1.0, 1.0],\
    'trig_values':['2020-12-15','2021-01-25'],\
    'trig_def_type':['date','date','date'],\
    'trig_op_type':['=','=','='],\
    'num_tests_mitigation':[32000,32000,32000],\
    'type_test_mitigation':['PCR','PCR','PCR'],\
    'sensitivity':[0.95,0.95],\
    'specificity':[1.0,1.0],\
    'num_tests_care':[10000,10000,10000],\
    'type_tests_care':['PCR','PCR','PCR'],\
    'prop_contacts_traced':[0.20,0.20,0.20],\
    'imported_infections_per_day':[1,1,1],\
    'requireddxtests':[0,0,0],\
    'is_counterfactual':['False','False','False'],\
    'test_strategy':['open public testing','open public testing','open public testing'],\
    'results_period':[3,3,3],\
    'prop_asymptomatic_tested':[0.4,0.4,0.4],
    'fatality_reduction_recent':[0.35,0.35,0.35]
    })

datesandseverities=pd.read_csv('db1.csv',index_col='Code')

for ccode in codes:
    
    scenario_params=copy.deepcopy(scenario_params_orig)
    fixed_params=cl.get_system_params(test_directory)
    n_records=60
    countrycode = ccode
    countryname = cd.getcountryname(countrycode)
    country_df = cd.getcountrydata(countrycode)
    day1 = dt.datetime.strptime(country_df.iloc[0]['Date'],"%Y-%m-%d")  
    past_severities=json.loads(datesandseverities.loc[ccode]['Severities'])
    past_dates=json.loads(datesandseverities.loc[ccode]['Trigger Dates'])
    
    fixed_params.update(cd.getcountryparams(ccode))
    fixed_params.update({'past_dates':past_dates,'past_severities':past_severities,'expert_mode':False})
    
    try:
        dataframes, test_df,results_dict=cl.run_simulation(country_df,fixed_params,scenarios=scenario_params)
    except FileNotFoundError as inst:
        print('')
        print('Exception raised by simulation:',inst)
        sys.exit()
  # =========================================================================
    
    a_row={}
    for i in range (0,len(results_dict['total_deaths_by_scenario'])):
        a_row.update({'Country':ccode})
        a_row.update({'Scenario':i})
        a_row.update({'Simulated deaths': results_dict['total_deaths_by_scenario'][i]})
        a_row.update({'Simulated cases': results_dict['total_cases_by_scenario'][i]})
        a_row.update({'Tests': results_dict['total_tests_mit_by_scenario'][i]})
 #       a_row.update({'Severity': results_dict['severity_by_scenario'][i]})
        results_df=results_df.append(a_row,ignore_index=True)
        results_df=results_df.sort_values(by=['Country'])
    afilename =os.path.join(cl_path_prefix, results_dir, 'batch_results.csv')
with open(afilename,'w') as outfile:      
   results_df.to_csv(outfile)
                      
    

