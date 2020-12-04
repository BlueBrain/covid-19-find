


import covidlib as cl

import pandas as pd

import os

import json

import sys

import cdata as cd

ccode="FR"

test_directory='BBP_testing'

country_df = cd.getcountrydata(ccode)

datesandseverities=pd.read_csv('db1.csv',index_col='Code')

past_severities=json.loads(datesandseverities.loc[ccode]['Severities'])

past_dates=json.loads(datesandseverities.loc[ccode]['Trigger Dates'])

print('past_dates=',past_dates)

print('past_severities=', past_severities)

 #temporary. Front_end will provide real data

# =============================================================================

# fixed_params={

#     'test_directory':'bbp_testing',\

#     'total_pop':8200000, \

#     'hospital_beds':33000, \

#     'prop_15_64': 0.66, \

#     'age_gt_64':0.20 ,\

#     'prop_urban': 0.72, \

#     'prop_below_pl':0.05, \

#     'prop_woh':0.4, \

#     'staff_per_bed':2.5,\

#     'past_dates':past_dates,\

#     'past_severities':past_severities,\

#     'expert_mode':False,\

#     'run_multiple_test_scenarios':True,\

#     'save_results':False,\

#     'fatality_reduction':0.35,\

#     'num_days':450}

# =============================================================================

fixed_params=cl.get_system_params(test_directory)

fixed_params.update(cd.getcountryparams(ccode))

fixed_params.update({'past_dates':past_dates,'past_severities':past_severities,'expert_mode':True})

with open('kenny-test-3.json', 'w') as outfile:
            json.dump(fixed_params, outfile)

scenario_params=[]

scenario_params.append({

    'severity':[0.95, 0.85],\

    'trig_values':['2020-12-04','2020-12-14'],\

    'trig_def_type':['date','date'],\

    'trig_op_type':['=','='],\

    'num_tests_mitigation':[13000,13000],\

    'type_test_mitigation':['PCR','PCR'],\

    'sensitivity':[0.95,0.95],\

    'specificity':[0.95,0.05],\

    'num_tests_care':[10000,10000],\

    'type_tests_care':['PCR','PCR'],\

    'prop_contacts_traced':[0.25,0.25],\

    'imported_infections_per_day':[50,50],\

    'requireddxtests':[2,2],\

    'is_counterfactual':['False','False'],\

    'test_strategy':['no testing','no testing'],\

    'results_period':[1,1],\

    'prop_asymptomatic_tested':[0.1,0.1],

    'fatality_reduction_recent':[0.35,0.35]

    })

    

scenario_params.append({

    'severity':[0.95,0.85],\

    'trig_values':['2020-10-03','2020-12-13'],\

    'trig_def_type':['date','date'],\

    'trig_op_type':['=','='],\

    'num_tests_mitigation':[250000,250000],\

    'type_test_mitigation':['PCR','PCR'],\

    'sensitivity':[0.95,0.95],\

    'specificity':[0.95,0.95],\

    'num_tests_care':[10000,10000],\

    'type_tests_care':['PCR','PCR'],\

    'prop_contacts_traced':[0.25,0.25],\

    'imported_infections_per_day':[50,50],\

    'requireddxtests':[2,2],\

    'is_counterfactual':['False','False'],\

    'test_strategy':['special groups with symptoms','special groups with symptoms'],\

    'results_period':[1,1],\

    'prop_asymptomatic_tested':[0.02,0.02],

    'fatality_reduction_recent':[0.35,0.35]

    })

    

scenario_params.append({

    'severity':[0.95, 0.85],\

    'trig_values':['2020-10-03','2020-12-13'],\

    'trig_def_type':['date','date'],\

    'trig_op_type':['=','='],\

    'num_tests_mitigation':[250000,250000],\

    'type_test_mitigation':['PCR','PCR'],\

    'sensitivity':[0.95,0.95],\

    'specificity':[0.95,0.95],\

    'num_tests_care':[10000,10000],\

    'type_tests_care':['PCR','PCR'],\

    'prop_contacts_traced':[0.25,0.25],\

    'imported_infections_per_day':[50,50],\

    'requireddxtests':[2,2],\

    'is_counterfactual':['False','False'],\

    'test_strategy':['all symptomatic','all symptomatic'],\

    'results_period':[1,1],\

    'prop_asymptomatic_tested':[0.02,0.02],

    'fatality_reduction_recent':[0.35,0.35]

    })

    

scenario_params.append({

    'severity':[0.95, 0.85],\

    'trig_values':['2020-10-03','2020-12-13'],\

    'trig_def_type':['date','date'],\

    'trig_op_type':['=','>'],\

    'num_tests_mitigation':[250000,250000],\

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

    'prop_asymptomatic_tested':[0.02,0.02],

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