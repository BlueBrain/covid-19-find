#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 09:25:47 2020

@author: richard
"""


import covidlib as cl
total_pop=12050000
hospital_beds=50000
pop_high_contact=2000000
pop_rest=8072000
prop_urban=0.4
prop_isolated=0.2
degraded=0.4
ge_65=0.045
high_contact=0.3 #this seem to be a duplication of prop_tests_high contact
isolated_area=0.2
prop_tests_hospitals=None, #legacy variable - to be removed in next release
prop_tests_high_contact=None #legacy variable - to be removed in next release
prop_tests_rest_of_population=None #legacy variable - to be removed in next release
sensitivity_PCR=0.95
sensitivity_RDT=0.85
sensitivity_xray=0.9
specificity_PCR=0.99
specificity_RDT=0.99
specificity_xray=0.99
num_tests_PCR=1000
num_tests_RDT=1000
num_tests_xray=1000
#Instead of giving hospital employment it now uses hospital beds
dataframes, total_tests_by_scenario,total_deaths_by_scenario,max_infected_by_scenario,max_isolated_by_scenario=cl.run_simulation(total_pop,hospital_beds,pop_high_contact,prop_urban,prop_isolated,degraded,ge_65, \
                   prop_tests_hospitals, prop_tests_high_contact,prop_tests_rest_of_population,sensitivity_PCR, \
                   sensitivity_RDT,sensitivity_xray,specificity_PCR,specificity_RDT,specificity_xray, \
                   num_tests_PCR,num_tests_RDT,num_tests_xray)
print('total deaths by scenario')
for i in range (1,len(total_deaths_by_scenario)):
    print ('scenario: ',i,': ', total_deaths_by_scenario[i])