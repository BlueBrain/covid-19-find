#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 09:25:47 2020

@author: richard
"""


import covidlib as cl
#fictitious everyone in hospitals
total_pop=60462000
hospital_beds=180000
pop_high_contact=10000000
prop_urban=0.7
degraded=0.1
staff_per_bed=4
sensitivity_PCR=0.95
sensitivity_RDT=0.85
sensitivity_xray=0.9
specificity_PCR=0.99
specificity_RDT=0.99
specificity_xray=0.99
num_tests_PCR=2000
num_tests_RDT=0
num_tests_xray=0
#Instead of giving hospital employment it now uses hospital beds
dataframes, total_tests_by_scenario,total_deaths_by_scenario,max_infected_by_scenario,max_isolated_by_scenario=cl.run_simulation(total_pop,hospital_beds,pop_high_contact,prop_urban,degraded, \
                   staff_per_bed,sensitivity_PCR, \
                   sensitivity_RDT,sensitivity_xray,specificity_PCR,specificity_RDT,specificity_xray, \
                   num_tests_PCR,num_tests_RDT,num_tests_xray)
print ('total deaths by scenario')
for i in range (0,len(total_deaths_by_scenario)):
    print ('scenario: ',i,': ', total_deaths_by_scenario[i])
print('total tests by scenario')
for i in range (0,len(total_tests_by_scenario)):
    print ('scenario: ',i,': ', total_tests_by_scenario[i])
print('Max infected by scenario')
for i in range (0,len(max_infected_by_scenario)):
    print ('scenario: ',i,': ', max_infected_by_scenario[i])