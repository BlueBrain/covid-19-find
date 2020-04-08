#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 10:14:56 2020

@author: richard
"""
#Usage. Call with the ISO 3166 code for a specific country. The function
# returns:
#Size of population
# % of population in large urban areas
# % of population in large urban areas in degraded housing
# % of population 65 or older
# Number of hospital employees
# Size of population with unavoidably high level of social contacts (essential occupations, slum dwellers etc.)
# % of population in remote areas with low level of contact to each other and to rest of country
def get_country_data(country_code):
    #partly fictitious sample data for phillipines
    population=105000000
    pc_urban=46.9
    pc_degraded=40
    pc_gte_65=4.75
    hosp_employ=50000
    high_contact_pop=20000000
    pc_remote_areas=-1 #-1 is code for data not available
    return (population, pc_urban, pc_degraded, pc_gte_65,hosp_employ,high_contact_pop,pc_remote_areas)