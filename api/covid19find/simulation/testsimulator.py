#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 09:25:47 2020

@author: richard
"""


import covidlib as cl
total_pop=12050000
pop_hospitals=50000
pop_high_contact=2000000
pop_rest=10000000
prop_urban=0.4
prop_isolated=0.2
degraded=0.4
ge_65=0.045
high_contact=0.3
isolated_area=0.2
prop_tests_hospitals=0.5,
prop_tests_high_contact=0.5
prop_tests_rest_of_population=0
sensitivity_PCR=0.95
sensitivity_RDT=0.85
sensitivity_xray=0.9
selectivity_PCR=0.95
selectivity_RDT=0.9
selectivity_xray=0.9
num_tests_PCR=1000
num_tests_RDT=1000
num_tests_xray=1000
cl.run_simulation(total_pop,pop_hospitals,pop_high_contact,prop_urban,prop_isolated,degraded,ge_65, \
                   prop_tests_hospitals, prop_tests_high_contact,prop_tests_rest_of_population,sensitivity_PCR, \
                   sensitivity_RDT,sensitivity_xray,selectivity_PCR,selectivity_RDT,selectivity_xray, \
                   num_tests_PCR,num_tests_RDT,num_tests_xray)