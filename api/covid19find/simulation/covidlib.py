# contains function definitions for covid simulation
# author:  JP Vergara

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import math
import csv
import datetime as dt
import copy
import os
import json
import ast


a=1

class CustomError(Exception):
     pass

cl_path_prefix = os.path.abspath(os.path.dirname(__file__))

def write_json(adict,afilename):
    adict2={}
    for akey in adict.keys():
        value=adict[akey]
        try:
            newvalue=ast.literal_eval(value)
        except:
            newvalue=value
        adict2.update({akey:newvalue})     
    with open(afilename,'w') as outfile: 
        json.dump(adict2, outfile)

def get_system_params(params_dir):
   sysfile=os.path.join(cl_path_prefix, params_dir, 'system_params.json')
   with open(sysfile) as infile: 
       try:
           system_params=json.load(infile)
       except FileNotFoundError:
           raise FileNotFoundError ('System parameters file not found')
           return()
   return(system_params)
   

def get_default_scenarios(params_dir):
   parfile=os.path.join(cl_path_prefix, params_dir, 'default_parameters.json')
   with open(parfile) as infile: 
       try:
           default_scenarios=json.load(infile)
       except FileNotFoundError:
           raise FileNotFoundError ('Scenario parameters file not found')
           return()
   return(default_scenarios)

def get_next_phases_scenarios(params_dir):
   defaults=get_default_scenarios(params_dir)
   next_phases=[]
   today=dt.datetime.now()
   next=today+dt.timedelta(days=14)
   todaystr=today.strftime("%Y-%m-%d")
   nextstr=next.strftime("%Y-%m-%d")
   for i in range(0,len(defaults)):
       adict={}
       for akey in defaults[i].keys():
           val=defaults[i][akey]
           newval=[val,val]
           adict.update({akey:newval})
       adict.update({'trig_values':[todaystr,nextstr]})
       next_phases.append(adict)
   return(next_phases)

######################################################################
# get_beta:
#    reads and returns an nxn beta matrix from a csv file;
#    n indicates the number of compartments
######################################################################

def get_beta(betafile, n):
    beta_table = pd.read_csv(betafile,header=None)
    (rows,cols) = beta_table.shape
    beta = np.zeros((n,n))
    for i in range(1,n+1):
       for j in range(1,n+1):
          beta[i-1,j-1] = beta_table.iloc[i,j]
    return beta

######################################################################
# Scenarios class:
#   encapsulates a Scenarios object containing:
#          num_scenarios - number of scenarios
#          scenarios - scenario code (keys for dictionary)
#          scenario_labels - scenario name (for printing)
#          scenarios_params - dictionary containing variables to be overridden
#                            per scenario, with corresponding values
#
#  read_from_csv: populates the Scenario attributes from a csv file
######################################################################

class Scenarios:

   def __init__(self):
      self.scenarios=[]
      self.scenario_labels={}
      self.scenario_params={}
      self.num_scenarios = 3   #this could be a systems parameter

   def read_from_csv(self,filename):
      temp = []
      var_keycheck = {}
      scenarios_table= pd.read_csv(filename,header=None)
      (rows,cols)=scenarios_table.shape
      for i in range(0,rows):
         key = scenarios_table.iloc[i,0]
         if key in self.scenario_params:
            var = scenarios_table.iloc[i,1]
            val = scenarios_table.iloc[i,3]
            if var in var_keycheck:
               temp.append(val)
            else:
               var_keycheck[var] = 1
               temp = [var,val]
               self.scenario_params[key].append(temp)
         else: # first instance of scenario key contains name
            var_keycheck={}
            self.scenario_labels[key] = scenarios_table.iloc[i,1]
            self.scenario_params[key]=[]
            self.scenarios.append(key)
   #   self.num_scenarios = len(self.scenarios)
            self.num_scenarios = 1 #temporary instruction to speed up testing

def get_scenarios(scenariosfile):
   sc = Scenarios()
   sc.read_from_csv(scenariosfile) #we might do without this
   return sc

######################################################################
# update_system_params:
#    update the parameter dictionary incorporating overrides
#    from fixed_params
######################################################################

#checks the population values in the fixed params. Returns 0 if this is no error - else -1
# now we no longer allow users to fix values for prop_Woh and prop_below_pl this is no longer required. I have commented the call in the main code
def validate_fixed_params(fixed_params):
    hosp_staff=fixed_params['hospital_beds']*fixed_params['staff_per_bed']
 #   poor_urban=fixed_params['total_pop']*fixed_params['prop_urban']*fixed_params['prop_below_pl']
    remaining_pop=fixed_params['total_pop']-poor_urban
    if remaining_pop<0:
        return(-1)
    woh=remaining_pop*fixed_params['prop_15_64']*fixed_params['prop_woh'] #working outside home
    other_hc=poor_urban+woh
    rop=fixed_params['total_pop']-hosp_staff-other_hc
    if rop<0:
        return(-1)
    else:
        return(0)

def update_system_params2(p, fixed_params):
    #update defaults values if overridden by fixed_params
    
    p.update(fixed_params)
    if p['income_category']=='H':
        prop_below_pl=0.08
        prop_woh=0.4
    elif p['income_category']=='UM':
        prop_below_pl=0.16
        prop_woh=0.5
    elif p['income_category']=='LM':
        prop_below_pl=0.30
        prop_woh=0.6
    else:
        prop_below_pl=0.5
        prop_woh=0.9
    hosp_staff=int(p['hospital_beds'])*float(p['staff_per_bed'])
    poor_urban=int(p['total_pop'])*float(p['prop_urban'])*prop_below_pl
    remaining_pop=int(p['total_pop'])-poor_urban
    woh=remaining_pop*float(p['prop_15_64'])*prop_woh #working outside home
    other_hc=poor_urban+woh
    rop=int(p['total_pop'])-hosp_staff-other_hc
    p['init_pop'][0]=hosp_staff
    p['init_pop'][1]=other_hc
    p['init_pop'][2]=rop
    p['total_pop']=int(fixed_params['total_pop'])
    if p['expert_mode']==True:
        print('init pop=',p['init_pop'])
    #compute age_corrected IFR for country

    prop_gt_64=p['age_gt_64']
    prop_15_64=p['prop_15_64']
    prop_1_14=1-(prop_gt_64+prop_15_64)
    IFR_1_14=float(p['IFR_1_14'])
    IFR_15_64=float(p['IFR_15_64'])
    IFR_gt_64=float(p['IFR_gt_64'])
    p['IFR_corrected']=IFR_1_14*prop_1_14+IFR_15_64*prop_15_64+IFR_gt_64*prop_gt_64
    p['past_dates']=fixed_params['past_dates']
    p['past_severities']=fixed_params['past_severities']
    p['num_days']=fixed_params['num_days']
    return


######################################################################
# compute reduction IFR:
#    Uses data on actual deaths and cases to compute instantaneous CFR
#    on Jan 1 2021, and today (uses averages over 7 days)
#    Reduction in CFR is a good measure of the impact of vaccination
######################################################################

def compute_reduction_IFR(country_df,day1):
    new_deaths_last_week=country_df.iloc[-1]['accumulated_deaths']-country_df.iloc[-8]['accumulated_deaths']
    new_cases_last_week=country_df.iloc[-1]['accumulated_cases']-country_df.iloc[-8]['accumulated_cases']
    cfr_last_week=new_deaths_last_week/new_cases_last_week
#Our automated test procedure uses a static country_df. The if statement makes sure this does not cause an error in computation
    if len(country_df)<406:
        reduction_cfr=0
    else:
        new_deaths_jan1=country_df.iloc[405]['accumulated_deaths']-country_df.iloc[397]['accumulated_deaths']
        new_cases_jan1=country_df.iloc[405]['accumulated_cases']-country_df.iloc[397]['accumulated_cases']
        if new_cases_jan1>0:
            cfr_jan1=new_deaths_jan1/new_cases_jan1
        else:
            cfr_jan1=0
        if cfr_jan1>0:
            reduction_cfr=(cfr_jan1-cfr_last_week)/cfr_jan1
        else: 
            reduction_cfr=0
    reduction_ifr=reduction_cfr*0.88
    return(reduction_ifr)

######################################################################
# run_simulation:
#    takes in fixed user-specified system and scenario parameters
#    and calls process_scenarios with updated parameters
#    - default parameter data are read in from csv files
#      (system_params.csv, initial_betas.csv, scenarios.csv)
#    - parameter dictionaries are built from these files and
#      then updated from the fixed user-specified system/scenario parameters
#    - process_scenarios is called after the parameters are reconciled
#
#    returns:
#        results produced by process_scenarios
#        - dataframes and various derivative outputs
######################################################################


def run_simulation(country_df_raw,fixed_params, **kwargs):
#optimization is performed using 'symptomatic first' - so simulations of past
#also use 'symptomatic first'. This is also a temp fix for open problem with result_period
   
   
   day1 = dt.datetime.strptime(country_df_raw.iloc[0]['Date'],"%Y-%m-%d")-dt.timedelta(days=60)
   empty_df=create_empty_country_df(day1, 60)
   frames=[empty_df,country_df_raw]
   country_df_raw=pd.concat(frames,ignore_index=True)
# =============================================================================
#    validation_result=validate_fixed_params(fixed_params)
#    if validation_result==-1:
#        raise CustomError('Invalid population numbers')
#        return()
# =============================================================================
   params_dir = ""
   if 'test_directory' in fixed_params:
       params_dir = fixed_params['test_directory']
   try:
       initial_betafile = os.path.join(cl_path_prefix, params_dir, 'initial_betas.csv')
   except FileNotFoundError:
       raise FileNotFoundError('initial_betas file not found')
       return()
   win_length=28
 
#   country_df=country_df_raw.rolling(win_length,center=True).mean()
   country_df=country_df_raw.rolling(win_length).mean()
   country_df['Date']=country_df_raw['Date']
   fixed_params['fatality_reduction']=compute_reduction_IFR(country_df,day1)
 #  country_df['accumulated_deaths']=country_df['accumulated_deaths']
   end_day=None
   keys=kwargs.keys()
   if len(kwargs)>0:
      scenarios_user_specified=kwargs['scenarios']
      if 'end_day' in keys:
       end_day=kwargs['end_day']
      
   else:
      scenarios_user_specified=[]

# set up system parameters

 #  p = get_system_params(sysfile)
 # not sure why I need this twice.
   try:
       p=get_system_params(params_dir) 
   except FileNotFoundError:
       raise FileNotFoundError('System parameters file not found')
       return()
  # write_json(p,sysfilejson) 

   update_system_params2(p, fixed_params) # note: p is updated
   # print('JPV-',p['num_days'])
   # print('JPV-',p['past_severities'])
   # print('JPV-',p['past_dates'])

# read initial beta matrix

   num_compartments = p['num_compartments']
   initial_beta = get_beta(initial_betafile, num_compartments)  #don't think this is needed

 #  results = process_scenarios(p, sc, initial_beta, target_betas)
   filename=os.path.join(fixed_params['test_directory'],'parameter dump.json')
   write_parameters(filename,p,scenarios_user_specified)
   today=(dt.datetime.now()-day1).days
   if end_day==None:
       end_day=today+180
       p['num_days']=end_day
   try:
       results = process_scenarios(country_df,p, scenarios_user_specified, initial_beta, params_dir,end_day)
   except:
       raise
       return()
   return results

######################################################################
# process_scenarios:
#    takes in system parameters, scenarios, initial beta matrix
#    and then calls simulate for each scenario
#    - betas_lockdown and betas_mild matrices are read here
#      (todo:  elevate this step to run_simulation)
#      note that final_beta may differ per scenario
#
#    returns:
#        results for each scenario
######################################################################

    
def process_scenarios(country_df,p,scenarios,initial_beta, params_dir,end_date):

   num_compartments = int(p['num_compartments'])
   num_scenarios = len(scenarios)

   no_intervention_betafile = os.path.join(cl_path_prefix, params_dir, 'initial_betas.csv')
   max_intervention_betafile = os.path.join(cl_path_prefix, params_dir, 'lockdown_betas.csv')
   num_tests_performed=np.zeros(num_compartments)
   expert_mode=p['expert_mode']
   total_tests_mit_by_scenario=np.zeros(num_scenarios)
   total_tests_care_by_scenario=np.zeros(num_scenarios)
   total_serotests_by_scenario_5=np.zeros(num_scenarios)
   total_serotests_by_scenario_10=np.zeros(num_scenarios)
   total_serotests_by_scenario_25=np.zeros(num_scenarios)
   total_cases_by_scenario=np.zeros(num_scenarios)
   total_deaths_by_scenario=np.zeros(num_scenarios)
   total_infected_by_scenario=np.zeros(num_scenarios)
   max_infected_by_scenario=np.zeros(num_scenarios)
   max_isolated_by_scenario=np.zeros(num_scenarios)
   scenario_names=['Counterfactual','Half hospitals','Protect capacity'] #could have these as parameters
   dataframes=[]
   test_column_names=['scenario','tests administered','deaths', 'lives saved']
   test_df= pd.DataFrame(columns=test_column_names)
   default_scenarios=[]
   try:
       default_scenarios=get_default_scenarios(params_dir)
   except FileNotFoundError:
           raise FileNotFoundError ('Default scenario parameters file not found')
           return()
   for i in range(0,num_scenarios):
      scenario_name='scenario' + ' '+ str(i) #it should have a proper name
      results_dir='results'
      filename =os.path.join(cl_path_prefix, results_dir, scenario_name+'_out.csv')
      total_actual_deaths=country_df['accumulated_deaths'].max()
      if total_actual_deaths<=p['imported_infections_limit_very_low']:
          default_scenarios[i]['imported_infections_per_day']=0
      elif total_actual_deaths<=p['imported_infections_limit_low']:
          default_scenarios[i]['imported_infections_per_day']=p['imported_infections_below_limit']
      elif total_actual_deaths<=p['imported_infections_limit_high']:
          default_scenarios[i]['imported_infections_per_day']=p['imported_infections_above_limit']
      else:
          default_scenarios[i]['imported_infections_per_day']=p['imported_infections_very_high']
      #fix the default strategy for the past to 'symptomatic only' - scenarios only differentiate in the future.
      default_scenarios[i]['test_strategy']='symptomatic first'
      past=create_past(p,default_scenarios[i],p['past_dates'],p['past_severities'])
      p.update(past)
      min_betas = get_beta(max_intervention_betafile, num_compartments)
      max_betas = get_beta(no_intervention_betafile, num_compartments)
      day1 = dt.datetime.strptime(country_df.iloc[0]['Date'],"%Y-%m-%d")
      shift=0
 
      
      #reads the trig values in scenarios i and converts to simulation days - does not yet check for type of trigger
      
      
      for j in range(0,len(scenarios[i]['trig_values'])):
          if(scenarios[i]['trig_def_type'][j]=='date'):
              date=dt.datetime.strptime(scenarios[i]['trig_values'][j], '%Y-%m-%d')
              scenarios[i]['trig_values'][j]=(date-day1).days
                     
      scenario=create_scenario(past,scenarios[i])
      # Converts qualitative labels for user parameters into numerical values read from the system parameters file
      for j in range(0,len(scenario['trig_values'])):
           if scenario['imported_infections_per_day'][j]=='highly effective':
              scenario['imported_infections_per_day'][j]=p['imported_infections_below_limit']
           elif scenario['imported_infections_per_day'][j]=='fairly effective':
              scenario['imported_infections_per_day'][j]=p['imported_infections_above_limit']
           elif scenario['imported_infections_per_day'][j]=='not effective':
              scenario['imported_infections_per_day'][j]=p['imported_infections_very_high']
           if scenario['prop_contacts_traced'][j]=='none':
              scenario['prop_contacts_traced'][j]=p['prop_for_no_tracing']
           elif scenario['prop_contacts_traced'][j]=='fairly effective':
              scenario['prop_contacts_traced'][j]=p['prop_for_fair_tracing']
           elif scenario['prop_contacts_traced'][j]=='highly effective':
              scenario['prop_contacts_traced'][j]=p['prop_for_good_tracing']
           #capture severity of last phase in the past
           if j>=1:
               current_sev=scenario['severity'][j-1]
           else:
               current_sev=0
          #transforms effectiveness labels into numerical values
           if scenario['severity'][j]=='major tightening':
               scenario['severity'][j]=current_sev+(1-current_sev)*p['major_tightening']
           elif scenario['severity'][j]=='mild tightening':
               scenario['severity'][j]=current_sev+(1-current_sev)*p['mild_loosening']
           elif scenario['severity'][j]=='no change':
               scenario['severity'][j]=current_sev
           elif scenario['severity'][j]=='mild loosening':
               scenario['severity'][j]=current_sev*(1-p['mild_loosening'])
           elif scenario['severity'][j]=='major loosening':
               scenario['severity'][j]=current_sev*(1-p['major_loosening']) 
           #reverses previous change if user requests this - but only does this if there is a previous phase
           if scenario['severity'][j]=='reverse last change':
           #avoid indexing non-existent severity
              if j>=2:
                  scenario ['severity'][j]=scenario ['severity'][j-2]
              else:
                  scenario ['severity'][j]=scenario ['severity'][j-1]
                                        
      p.update(scenario)
      nmultipliers=len(p['test_multipliers'])
      par = Par(p)
      #overwrites default value of day1
      par.day1=day1
      par.shift=shift
      #call simday today
      simphase,simday=computetoday(day1,par.trig_values)
      par.fatality_reduction_per_day=math.exp(np.log(1-(par.fatality_reduction))/(simday-par.no_improvement_period))
      sim = Sim(par.num_days,par.num_compartments)
      sim.set_initial_conditions(par)
      use_real_testdata=True
      #Startday here is  hard coded to 1
      sim,df = simulate(country_df,sim,par,max_betas,min_betas,1,end_date,0,use_real_testdata)
      if par.save_results==True:
          df.to_csv(filename,index=False,date_format='%Y-%m-%d')
      first_valid_date_4_reff=dt.datetime.strptime('2020-01-22', '%Y-%m-%d').date()
      dataframes.append(df) 
      dfsum = df.groupby(['dates']).sum().reset_index()
      #eliminate spurious computation of Reff where number of infected very low
      dfsum['reff']=(dfsum['newinfected']/dfsum['infected']*(p['recovery_period']+p['incubation_period'])).where(dfsum['dates'].dt.date>=first_valid_date_4_reff,other=0)
      dfsum['positive rate']=dfsum['newconfirmed']/dfsum['newtested_mit']
      dfsum['detection rate']=dfsum['newconfirmed']/dfsum['newinfected']
      dfsum['ppv']=dfsum['truepositives']/(dfsum['truepositives']+dfsum['falsepositives'])
      dfsum['npv']=dfsum['truenegatives']/(dfsum['truenegatives']+dfsum['falsenegatives'])
      dfsum['incidence']=dfsum['newinfected']/(dfsum['population'])
      dfsum['prevalence']=(dfsum['accumulatedinfected']-dfsum['deaths'])/dfsum['population']
      dfsum['actualdeaths']=np.round(sim.actualdeaths,decimals=3)
      dfsum['actualcases']=np.round(sim.actualcases,decimals=3)
      dfsum['actualnewtests_mit']=np.round(sim.actualnewtests_mit,decimals=3)
      dfsum['actualnewdeaths']=np.round(sim.actualnewdeaths,decimals=3)
      dfsum['actualnewcases']=np.round(sim.actualnewcases,decimals=3)
      dfsum['p_case_all']=dfsum['p_case_all']/3
      dfsum['p_case_all_simulated']=dfsum['p_case_all_simulated']/3  #I am not sure this is correct
      
      dataframes.append(dfsum)
      # do extra simulations to test different test strategies
      # loops through the test_kit multipliers
      
      if par.run_multiple_test_scenarios:
#          print('beginning simulations with different number of tests')
          for j in range(0,len(par.test_multipliers)):
            test_par=Par(p)
            test_par.day1=day1
            test_par.shift=shift
            test_par.fatality_reduction_per_day=math.exp(np.log(1-(test_par.fatality_reduction))/(simday-test_par.no_improvement_period))
            simphase,simday=computetoday(day1,par.trig_values)
            sim = Sim(par.num_days,par.num_compartments)
            current_phase,today=computetoday(par.day1,par.trig_values)
            start_current_phase=par.trig_values[current_phase]
            for k in range(current_phase,len(par.trig_values)):
                test_par.num_tests_mitigation[k]=par.num_tests_mitigation[k]*test_par.test_multipliers[j]
            sim = Sim(par.num_days,par.num_compartments)
            sim.set_initial_conditions(test_par)
            use_real_testdata=True
            sim,df_tests=simulate(country_df,sim,test_par,max_betas,min_betas,1,end_date,0,use_real_testdata)
            dfsum_tests = df_tests.groupby(['dates']).sum().reset_index()
            deaths=dfsum_tests['newdeaths'].sum()
            if j==0:
                baseline_deaths=dfsum_tests['newdeaths'].sum()
            lives_saved=baseline_deaths-deaths
            tests_administered=dfsum_tests['newtested_mit'][int(start_current_phase):par.num_days].sum()
#           print('tests administered from start of phase',tests_administered,'baseline=',baseline_deaths,'deaths=',deaths,'lives_saved=', lives_saved)
            a_dict={
            'scenario':i,\
            'tests administered':tests_administered,\
            'deaths':deaths,\
            'lives saved':lives_saved}
            #test_df.to_csv('testdf.csv',index=False,date_format='%Y-%m-%d')
            test_df=test_df.append(a_dict,ignore_index=True)
     
        # gives results by day grouped by individual compartment
      
      dfsumcomp = df.groupby(['compartment']).sum().reset_index()
      dfmaxcomp = df.groupby(['compartment']).max().reset_index() #ori
      for j in range(0,num_compartments):
         comp = dfmaxcomp['compartment'][j]
         dfcomp = df.loc[df['compartment'] == comp]
         if expert_mode:
            print('total population in compartment',comp,p['init_pop'][j])
            print('total tested for mitigation in compartment',comp,'=',dfsumcomp['newtested_mit'][j])
            print('total tested for diagnosis and care in compartment',comp,'=',dfsumcomp['actualdxtests'][j])
            print('total_deaths in ',comp,'=', dfsumcomp['newdeaths'][j])
            print('max_infections in ',comp,'=',dfmaxcomp['infected'][j])
            print('total_infections in ',comp,'=',dfsumcomp['newinfected'][j])
            print('max in isolation in ',comp,'=',dfmaxcomp['isolated'][j])
            plot_results(scenario_name,comp,int(num_tests_performed[j]),dfcomp['dates'],dfcomp['isolated'],dfcomp['infected'],dfcomp['tested_mit'],dfcomp['infectednotisolated'],dfcomp['confirmed'],dfcomp['deaths'],dfcomp['susceptibles'],dfcomp['prevalence'])
             
      if expert_mode:
         plot_results(scenario_name,'ALL',dfsumcomp['newtested_mit'],dfsum['dates'],dfsum['isolated'],dfsum['infected'],dfsum['tested_mit'],dfsum['infectednotisolated'],dfsum['confirmed'],dfsum['deaths'],dfsum['susceptibles'],dfsum['prevalence'],country_df['accumulated_deaths'],)
         dfsum.to_csv('richard_dump' + scenario_name+'.csv')
         print('************')

   #   prevalence=dfsum.iloc[par.num_days-1]['prevalence'] 
   #   simday is today - in normal usage we measure today's prevalence
   #   during optimization we use the length of the simulation
# =============================================================================
#       if simday>par.num_days:
#           prevalence=dfsum.iloc[par.num_days-1]['prevalence'] 
#       else:
#           prevalence=dfsum.iloc[simday]['prevalence'] 
# =============================================================================
      prevalence=dfsum.iloc[-1]['prevalence']
      total_tests_mit_by_scenario[i]=dfsumcomp['newtested_mit'].sum()
      total_tests_care_by_scenario[i]=dfsumcomp['actualdxtests'].sum()
      total_serotests_by_scenario_5[i]=sim.compute_sample_size(par,5,prevalence,1.96,0.01)
      total_serotests_by_scenario_10[i]=sim.compute_sample_size(par,10,prevalence,1.96,0.01)
      total_serotests_by_scenario_25[i]=sim.compute_sample_size(par,25,prevalence,1.96,0.01)
      #total_serotests_by_scenario_1000[i]=sim.compute_sample_size(par,1000,prevalence,1.96,0.01)
      total_cases_by_scenario[i]=dfsum['actualnewcases'][0:simday].sum()+dfsum['newconfirmed'][simday:end_date].sum()
 #     total_deaths_by_scenario[i]=dfsum['newdeaths'].sum()
      total_deaths_by_scenario[i]=dfsum['actualnewdeaths'][0:simday].sum()+dfsum['newdeaths'][simday:end_date].sum()
      total_infected_by_scenario[i]=dfsum['newinfected'].sum()
      current_phase,today=computetoday(par.day1,par.trig_values)
      df_from_today=dfsum.iloc[today:par.num_days-1]
      max_infected_by_scenario[i]=df_from_today['newinfected'].max()
      max_isolated_by_scenario[i]=df_from_today['isolated'].max()

      if expert_mode:
         print('Total tested for mitigation =',total_tests_mit_by_scenario[i])
         print('Total tested for care =',total_tests_care_by_scenario[i])
         print('Max infected=',max_infected_by_scenario[i])
         print('Total infected by scenario=',total_infected_by_scenario[i]),
         print('Max isolated=',max_isolated_by_scenario[i])
         print('Total deaths=',total_deaths_by_scenario[i])
         
         print('************')
         print('Tests required for seroprevalence study 95% confidence, max 1% error')
         print('For national study sum requirements for all subpopulations of interest')
         print('************')
         print('Max subgroups 5:', sim.compute_sample_size(par,5,prevalence,1.96,0.01))
         print('Max subgroups 10:', sim.compute_sample_size(par,10,prevalence,1.96,0.01))
         print('Max subgroups 25:',sim.compute_sample_size(par,25,prevalence,1.96,0.01))
         print('************')
   if expert_mode:
      print('******************')
      print('Comparison between scenarios')
      print('******************')
      print('')
      print ('Total tests')
      print('')
      for i in range(0,num_scenarios):
         print('Scenario ',i,' Mitigation:',total_tests_mit_by_scenario[i])
         
      print('')
      print('Total Deaths')
      print('')
            
      for i in range(0,num_scenarios):
         print('Scenario ',i,total_deaths_by_scenario[i])
      print('')
      print('Max infections')
      print('')
      for i in range(0,num_scenarios):
         print('Scenario ',i,max_infected_by_scenario[i])
      print('Total infections')
      print('')
      for i in range(0,num_scenarios):
         print('Scenario ',i,total_infected_by_scenario[i])
        
      print('')
      print('Max isolated')
      print('')
      for i in range(0,num_scenarios):
         print('Scenario ',i,max_isolated_by_scenario[i])
           
      #=============================================================================
      print('')
   results_dict={}
   results_dict.update({
   'total_tests_mit_by_scenario':total_tests_mit_by_scenario,\
   'total_tests_care_by_scenario':total_tests_care_by_scenario,\
   'total_serotests_by_scenario_5':total_serotests_by_scenario_5,\
   'total_serotests_by_scenario_10':total_serotests_by_scenario_10,\
   'total_serotests_by_scenario_25':total_serotests_by_scenario_25,\
   'total_deaths_by_scenario':total_deaths_by_scenario,\
   'max_infected_by_scenario':max_infected_by_scenario,\
   'total_infected_by_scenario':total_infected_by_scenario,\
   'max_isolated_by_scenario':max_isolated_by_scenario,\
   'total_cases_by_scenario':total_cases_by_scenario})
      
#      p=original_p
   
# =============================================================================
#    with open(parfile,'w') as outfile:      
#         json.dump(default_scenarios,outfile)
# =============================================================================
   return(dataframes, test_df,results_dict)

######################################################################
# Par class:
#   encapsulates model parameters for covid simulation
######################################################################

class Par:

   def __init__(self,params):
      self.num_compartments = int(params['num_compartments'])
      self.num_days = int(params['num_days'])
      self.total_pop=int(params['total_pop'])
      self.min_beta_target=float(params['beta_lockdown'])
      self.max_beta_target=float(params['beta_initial'])
      self.beta_adaptation_days = float(params['beta_adaptation_days']) #this is number of days beta takes to shift from initial to final beta
      self.latency_period =  int(params['latency_period'])
      self.incubation_period =  int(params['incubation_period'])
      self.infection_fatality_rate=float(params['IFR_corrected'])
      self.recovery_period = int(params['recovery_period'] )
      self.death_period = int(params['death_period'])
      self.prop_asymptomatic=float(params['prop_asymptomatic'])
      self.tau = self.infection_fatality_rate
      self.gamma = (1-self.infection_fatality_rate)
      self.num_testkit_types=int(params['num_testkit_types'])
      self.num_tests_mitigation=list(map(int,params['num_tests_mitigation']))
      self.num_tests_care=list(map(int,params['num_tests_care']))
      self.sensitivity=list(map(float,params['sensitivity']))
      self.specificity=list(map(float,params['specificity']))
      self.design_effect=float(params['design_effect'])
      self.confirmation_tests=[]
      self.p_positive_if_symptomatic = 0.0
      self.background_rate_symptomatic=float(params['background_rate_symptomatic'])
      self.severity=list(map(float,params['severity']))
      self.trig_values=list(map(float,params['trig_values']))
      self.trig_def_type=params['trig_def_type']
      self.trig_op_type=params['trig_op_type']
      self.max_contacts_per_case=float(params['max_contacts_per_case'])
      self.min_contacts_per_case=float(params['min_contacts_per_case'])
      self.prop_contacts_traced=list(map(float, params['prop_contacts_traced']))
      self.test_multipliers=list(map(int,params['test_multipliers']))
      self.requireddxtests=list(map(int,params['requireddxtests']))
      self.imported_infections_per_day=list(map(float, params['imported_infections_per_day']))
      self.is_counterfactual=[]
      self.fatality_reduction=float(params['fatality_reduction'])
      self.fatality_reduction_per_day=0
      self.fatality_reduction_recent=list(map(float, params['fatality_reduction_recent']))
      self.no_improvement_period=params['no_improvement_period']
      self.retest_period_asymptomatics=params['retest_period_asymptomatics']
      self.run_multiple_test_scenarios=(params['run_multiple_test_scenarios']) 
      self.save_results=params['save_results'] 
      num_compartments = self.num_compartments
      self.compartment = []
      self.init_pop = np.zeros(num_compartments)
      self.init_infected = np.zeros(num_compartments)
      self.num_tests=[self.num_tests_mitigation,self.num_tests_care]
      self.test_strategy=params['test_strategy']
      self.results_period=list(map(int,params['results_period']))
      self.relative_prob_infected=float(params['relative_prob_infected'])
      self.prop_tested_asymptomatic=float(params['prop_tested_asymptomatic'])
      #not sure these instructions are necessary
      self.imported_infections_limit_very_low=float(params['imported_infections_limit_very_low'])
      self.imported_infections_limit_low=float(params['imported_infections_limit_low'])
      self.imported_infections_limit_high=float(params['imported_infections_limit_high'])
      self.imported_infections_below_limit=float(params['imported_infections_below_limit'])
      self.imported_infections_above_limit=float(params['imported_infections_above_limit'])
      self.min_infected_not_isolated=int(params['min_infected_not_isolated'])
      self.alpha=np.zeros(num_compartments)
  #    print ('num_tests=',self.num_tests)
 
      #if we wrote these variables as lists we could copy them without the loops
      
  #    self.prop_tests=[list(map(float,params['prop_hospital'])),list(map(float,params['prop_other_hc']))]
# =============================================================================
#       prop_rop=[]
#       for i in range(0,len(params['prop_hospital'])):
#          value=1-(float(self.prop_tests[0][i])+float(self.prop_tests[1][i]))
#          prop_rop.append(value)
# =============================================================================
 #     self.prop_tests.append(prop_rop)
      for i in range(0,self.num_compartments):
         self.compartment.append(params['compartment'][i])
         self.init_pop[i]=int(params['init_pop'][i])
         self.init_infected[i] = params['init_infected'][i] 
         if self.init_infected[i] > self.init_pop[i]:
            self.init_infected[i] = self.init_pop[i]
# =============================================================================
#       for k in range(0,self.num_testkit_types):
#          self.sensitivity[k]=float(params['sensitivity'][k])
#          self.specificity[k]=float(params['specificity'][k])
# =============================================================================
     #    self.num_tests[k]=params['num_tests'][k]  #this is now a list
   #      self.num_tests.append(params['num_tests'][k] )


  #    self.total_testkits = np.zeros(len(self.num_tests))
   #   self.total_testkits=np.asarray(self.num_tests).sum(axis=0)
      self.day1=dt.datetime.now()  #this is a default value - day1 refers to first day of simulation
      self.shift=0
 #     print('total_testkits',self.total_testkits)
 #     print('AAA total testkits=',self.total_testkits)
      
######################################################################
# Sim class:
#   encapsulates time series and compartment arrays for covid simulation
#
#   get_data_frame:  returns all simulation  arrays as a dataframe
######################################################################

class Sim:
   def __init__(self,num_days,num_compartments):
      self.days=np.zeros(num_days)
      self.dates=[]
      self.beta_arr = np.zeros((num_days,num_compartments))
      self.infected = np.zeros((num_days,num_compartments))
      self.infectednotisolated=np.zeros((num_days,num_compartments))
      self.newimportedinfections=np.zeros((num_days,num_compartments))
      self.newinfected = np.zeros((num_days,num_compartments))
      self.accumulatedinfected=np.zeros((num_days,num_compartments))
      self.tested_mit=np.zeros((num_days,num_compartments))
      self.newtested_mit=np.zeros((num_days,num_compartments))
      self.newisolated=np.zeros((num_days,num_compartments))
      self.newisolatedinfected=np.zeros((num_days,num_compartments))
      self.isolatedinfected=np.zeros((num_days,num_compartments))
      self.isolated=np.zeros((num_days,num_compartments))
      self.susceptibles = np.zeros((num_days,num_compartments))
      self.recovered = np.zeros((num_days,num_compartments))
      self.newrecovered = np.zeros((num_days,num_compartments))
      self.requireddxtests=np.zeros((num_days,num_compartments))
      self.actualdxtests=np.zeros((num_days,num_compartments))
      self.confirmed = np.zeros((num_days,num_compartments))
      self.newconfirmed = np.zeros((num_days,num_compartments))
      self.deaths = np.zeros((num_days,num_compartments))
      self.newdeaths = np.zeros((num_days,num_compartments))
      self.population = np.zeros((num_days,num_compartments))
      self.susceptibleprop =np.ones((num_days,num_compartments))
      self.reff=np.zeros((num_days,num_compartments))
      self.truepositives=np.zeros((num_days,num_compartments))
      self.falsepositives=np.zeros((num_days,num_compartments))
      self.truenegatives=np.zeros((num_days,num_compartments))
      self.falsenegatives=np.zeros((num_days,num_compartments))
      self.ppv=np.zeros((num_days,num_compartments))
      self.npv=np.zeros((num_days,num_compartments))
      self.incidence=np.zeros((num_days,num_compartments))
      self.prevalence=np.zeros((num_days,num_compartments))
      self.actualdeaths=np.zeros(num_days)
      self.importedinfections=np.zeros((num_days,num_compartments))
      self.compart_newinfected=np.zeros((num_days,num_compartments,num_compartments))
      self.total_deaths=np.zeros(num_compartments)
      self.maxinfected=np.zeros(num_compartments)
      self.maxisolated=np.zeros(num_compartments)
      self.totalisolated=np.zeros(num_compartments)
      self.actualcases=np.zeros(num_days)
      self.actualnewdeaths=np.zeros(num_days)
      self.actualnewcases=np.zeros(num_days)
      self.actualnewtests_mit=np.zeros(num_days)
      self.p_case_all_simulated=np.zeros((num_days,num_compartments))
      self.p_case_all=np.zeros((num_days,num_compartments))
      self.uninfected_symptomatic=np.zeros((num_days,num_compartments))
     
      
      

   # set the correct values at t = 0
   def set_initial_conditions(sim,par:Par):
      for i in range(par.num_compartments):
         sim.newinfected[0,i] = par.init_infected[i] 
         sim.population[0,i] = par.init_pop[i]
         sim.susceptibles[0,i] = par.init_pop[i]-par.init_infected[i]
         if sim.susceptibles[0,i]<0:
            sim.susceptibles[0,i]=0
         if sim.population[0,i]>0:
            sim.susceptibleprop[0,i] = sim.susceptibles[0,i]/sim.population[0,i]
         else:
            sim.susceptibleprop[0,i]=0 #avoids a divide by zero error with zero pop in one compartment
         sim.infected[0,i] = sim.newinfected[0,i] # par.init_infected[i]
         sim.infectednotisolated[0,i] = sim.newinfected[0,i] # par.init_infected[i]
 
   # infect compartments at time t using the given beta matrix
         
   def cross_infect(sim,par:Par,beta,t):
      # add up number of new infected for each compartment - total correct at end of loops
      for i in range(0, par.num_compartments): #this is the compartment doing the infecting
         for j in range(0, par.num_compartments):   
            if t>(par.incubation_period-par.latency_period):
                sim.compart_newinfected[t,i,j] = sim.infectednotisolated[t-1-(par.incubation_period-par.latency_period),i]*beta[i,j]*sim.susceptibleprop[t-1-(par.incubation_period-par.latency_period),j]*sim.population[t-1-(par.incubation_period-par.latency_period),j]/sim.population[t-1-(par.incubation_period-par.latency_period),:].sum()
             #this shouldn't be necesary

   # add up infections per compartment at time t (can combine code here with with cross_infect at some point)
            
   def addup_infections(sim,par:Par,t):
      for i in range(0,par.num_compartments):
         sim.newinfected[t,i]=0
         for j in range(0,par.num_compartments):
            sim.newinfected[t,i]=sim.newinfected[t,i]+sim.compart_newinfected[t,j,i]
         if sim.newinfected[t,i]>sim.susceptibles[t-1,i]:#This should be part of i loop - may not be necessary
            sim.newinfected[t,i]=sim.susceptibles[t-1,i]
       
  # computes the number of imported infections for all compartments
            
   def get_imported(sim,par:Par, t,i,phase):
 #it would be better to make this proportional to population
       prop_population_in_compart=np.zeros(par.num_compartments)
       prop_population_in_compart=par.init_pop[i]/np.sum(par.init_pop)
       imported_infections=prop_population_in_compart*par.imported_infections_per_day[phase]
   #    sim.newinfected[t]=sim.newinfected[t]+imported_infections
       return imported_infections
   
   def get_imported2(sim,par:Par, t,phase):
 #it would be better to make this proportional to population
       prop_population_in_compart=np.zeros(par.num_compartments)
       prop_population_in_compart=par.init_pop/np.sum(par.init_pop)
       imported_infections=prop_population_in_compart*par.imported_infections_per_day[phase]
   #    sim.newinfected[t]=sim.newinfected[t]+imported_infections
       return imported_infections
       
   #Computes the sample size required for a national wide seroprevalence survey in which max
   # n. of groups for stratified analysis is given by n_groups
   # assumes a design effect (multiplier to compensate for clustering) specified in system parameters
   
   def compute_sample_size(sim,par,n_groups,prev,z,error):
       group_size=par.total_pop/n_groups
       upper=(z**2*prev*(1-prev))/(error**2)
       lower=1+(z**2*prev*(1-prev)/(error**2*group_size))
       sample_size=(upper/lower)*par.design_effect*n_groups
       return(sample_size)
        
    
   def perform_tests(sim,par:Par,t,phase,use_real_testdata):
        testsperformed=[0,0,0]
        if par.test_strategy[phase]=='symptomatic first':
            testsperformed=sim.perform_tests_symptomatic_first(par,t,phase,use_real_testdata)
        elif par.test_strategy[phase]=='high contact groups first':
            testsperformed=sim.perform_tests_with_priorities(par,t,phase,use_real_testdata,[0,1,2])      
        elif par.test_strategy[phase]=='open public testing':
            testsperformed=sim.perform_tests_open_public(par,t,phase,use_real_testdata)
        elif par.test_strategy[phase]=='no testing':
            return([0,0,0])
        else:
            raise CustomError('Non-existent test strategy')
            return([0,0,0])
        return (testsperformed)
    

   def perform_tests_symptomatic_first(sim,par:Par,t,phase,use_real_testdata):
   # tests are performed for symptomatic patients first - if there are any  left over they are used to test asymptomatics
  
        p_infected=np.zeros(par.num_compartments)
        p_infected_symptomatic=np.zeros(par.num_compartments)
        infected_symptomatic_population=np.zeros(par.num_compartments)
        uninfected_symptomatic_population=np.zeros(par.num_compartments)
        infected_symptomatic_tests=np.zeros(par.num_compartments)
        symptomatic_population=np.zeros(par.num_compartments)
        simphase,today=computetoday(par.day1,par.trig_values)
        infected_symptomatic_population=sim.newinfected[t]*(1-par.prop_asymptomatic)
        uninfected_symptomatic_population=sim.population[t-1]*par.background_rate_symptomatic
        symptomatic_population=infected_symptomatic_population+ uninfected_symptomatic_population
        for i in range(0,par.num_compartments):
            if symptomatic_population[i]>0:
                p_infected_symptomatic[i]=infected_symptomatic_population[i]/symptomatic_population[i]
            else:
                p_infected_symptomatic[i]=0
        prop_tests=sim.population[t-1]/sim.population[t-1].sum()
        if (use_real_testdata) and ispast(par.day1,t+1):
          tests_available=prop_tests*sim.actualnewtests_mit[t]
        else:
          tests_available=prop_tests*par.num_tests_mitigation[phase]
        if tests_available.sum()>0:
        #test all symptomatics first 
            for i in range(0,par.num_compartments):
                if tests_available[i]>symptomatic_population[i]: #shouldn't normally happen
                    infected_symptomatic_tests[i]=infected_symptomatic_population[i]
                else:
 #                   infected_symptomatic_tests[i]=tests_available[i]*(1-par.background_rate_symptomatic)
                    infected_symptomatic_tests[i]=tests_available[i]*p_infected_symptomatic[i]
                p_infected[i]=infected_symptomatic_tests[i]/tests_available[i] 
        adjust_positives_and_negatives(sim,par,t,phase,tests_available,p_infected)   
        return(tests_available)
    
   
   def perform_tests_with_priorities(sim,par:Par,t,phase,use_real_testdata,priorities):
       #tests are used first for health workers (symptomatic and asymptomatic), then for other high risk groups, then for the rest of the population
       # if the number of tests is low only health workers will get tested
        p_infected=np.zeros(par.num_compartments)
        tests_performed=np.zeros(par.num_compartments)
        p_infected_symptomatic=np.zeros(par.num_compartments)
        p_infected_asymptomatic=np.zeros(par.num_compartments)
        infected_symptomatic_population=np.zeros(par.num_compartments)
        uninfected_symptomatic_population=np.zeros(par.num_compartments)
        infected_symptomatic_tests=np.zeros(par.num_compartments)
        symptomatic_population=np.zeros(par.num_compartments)
        simphase,today=computetoday(par.day1,par.trig_values)
        infected_symptomatic_population=sim.newinfected[t]*(1-par.prop_asymptomatic)
        
            
        uninfected_symptomatic_population=sim.population[t-1]*par.background_rate_symptomatic
        symptomatic_population=infected_symptomatic_population+ uninfected_symptomatic_population
        asymptomatic_population=sim.population[t-1]-symptomatic_population
        asymptomatic_eligible=asymptomatic_population/par.retest_period_asymptomatics
        eligible=symptomatic_population+asymptomatic_eligible
        for i in range(0,par.num_compartments):
            if eligible[i]>0:
                p_infected_symptomatic[i]=infected_symptomatic_population[i]/symptomatic_population[i]
            else:
                p_infected_symptomatic[i]=0
        
        if (use_real_testdata) and ispast(par.day1,t+1):
          total_tests_available=sim.actualnewtests_mit[t]
        else:
          total_tests_available=par.num_tests_mitigation[phase]
        if total_tests_available>0:
                
            for k in range(0,par.num_compartments):
                i=priorities[k]
                if total_tests_available>symptomatic_population[i]+asymptomatic_eligible[i]:
                    tests_available_symptomatic=symptomatic_population[i]
                    tests_available_asymptomatic=asymptomatic_eligible[i]
                else:
                    tests_available_symptomatic=total_tests_available*symptomatic_population[i]/sim.population[t-1,i]
                    tests_available_asymptomatic=total_tests_available*asymptomatic_eligible[i]/sim.population[t-1,i]
                if tests_available_symptomatic>symptomatic_population[i]: #shouldn't normally happen
                    infected_symptomatic_tests=infected_symptomatic_population[i]
                else:
 #                   infected_symptomatic_tests[i]=tests_available[i]*(1-par.background_rate_symptomatic)
                    infected_symptomatic_tests=tests_available_symptomatic*p_infected_symptomatic[i]
                tests_performed[i]=tests_available_symptomatic+tests_available_asymptomatic
                p_infected[i]=infected_symptomatic_tests/tests_performed[i]
                total_tests_available=total_tests_available-tests_performed[i]                
# =============================================================================
#         if 673<=t<675:
#             print("t=",t)
#             print("newinfected" ,sim.newinfected[t])
#             print("infected symptomatic population", infected_symptomatic_population)
#             print("asymptomatic population ",asymptomatic_population)
#             print("asymptomatic eligible ",asymptomatic_population)
#             print("asymptomatic eligible", asymptomatic_eligible)
#             print("eligible",eligible)
#             print('p_infected symptomatic',p_infected_symptomatic)
#             print('tests_available symptomatic',tests_available_symptomatic)
#             print('tests_available asymptomatic ',tests_available_asymptomatic)
#             print('tests_performed ', tests_performed)
#             print('p_infected', p_infected)
#             print('total_tests_available')
# =============================================================================
            
            
        adjust_positives_and_negatives(sim,par,t,phase,tests_performed,p_infected)   
        return(tests_performed)
   
   def perform_tests_open_public(sim,par:Par,t,phase,use_real_testdata):
        p_infected=np.zeros(par.num_compartments)
        p_infected_symptomatic=np.zeros(par.num_compartments)
        p_infected_asymptomatic=np.zeros(par.num_compartments)
        infected_symptomatic_population=np.zeros(par.num_compartments)
        uninfected_symptomatic_population=np.zeros(par.num_compartments)
        infected_symptomatic_tests=np.zeros(par.num_compartments)
        symptomatic_population=np.zeros(par.num_compartments)
        simphase,today=computetoday(par.day1,par.trig_values)
        infected_symptomatic_population=sim.newinfected[t]*(1-par.prop_asymptomatic)
        uninfected_symptomatic_population=sim.population[t-1]*par.background_rate_symptomatic
        symptomatic_population=infected_symptomatic_population+ uninfected_symptomatic_population
        for i in range(0,par.num_compartments):
            if symptomatic_population[i]>0:
                p_infected_symptomatic[i]=infected_symptomatic_population[i]/symptomatic_population[i]
            else:
                p_infected_symptomatic[i]=0
        prop_tests=sim.population[t-1]/sim.population[t-1].sum()
        if (use_real_testdata) and ispast(par.day1,t+1):
          tests_available=prop_tests*sim.actualnewtests_mit[t]
        else:
          tests_available=prop_tests*par.num_tests_mitigation[phase]
        if tests_available.sum()>0:
            tests_available_symptomatic=tests_available*(1-par.prop_tested_asymptomatic)
            tests_available_asymptomatic=tests_available*par.prop_tested_asymptomatic       
        #test all symptomatics first 
            for i in range(0,par.num_compartments):
                if tests_available[i]>symptomatic_population[i]: #shouldn't normally happen
                    infected_symptomatic_tests[i]=infected_symptomatic_population[i]
                else:
 #                   infected_symptomatic_tests[i]=tests_available[i]*(1-par.background_rate_symptomatic)
                    infected_symptomatic_tests[i]=tests_available_symptomatic[i]*p_infected_symptomatic[i]
                p_infected[i]=infected_symptomatic_tests[i]/tests_available[i] 
        adjust_positives_and_negatives(sim,par,t,phase,tests_available,p_infected)   
        return(tests_available)
   
   
   def trigger_next_phase(sim,params,t,phase):
       #This function returns true if t meets the criteria previous defined to trigger next phase
       
     
       if params.trig_def_type[phase]=='date': 
           value=t
       elif params.trig_def_type[phase]=='cases':
           value=(np.sum(sim.newconfirmed[t-7:t,:])/7)
       elif params.trig_def_type[phase]=='cases per million':
           value=(np.sum(sim.newconfirmed[t-7:t,:])/7)/(params.total_pop/1000000)
       elif params.trig_def_type[phase]=='deaths':
           value=np.sum(sim.newdeaths[t-7:t])/7
       elif params.trig_def_type[phase]=='increase cases':
           if t>7:               
              value=(np.sum(sim.newisolated[t-7:t,:])/np.sum(sim.newisolated[t-14:t-7,:])-1)
           else:
              value=float('NaN')
              raise CustomError('Unable to compute increase in cases')
       elif params.trig_def_type[phase]=='increase deaths':
           if t>7:
              value=(np.sum(sim.newdeaths[t-7:t,:])/np.sum(sim.newdeaths[t-14:t-7,:])-1)        
           else:
              value=float('NaN')
              raise CustomError('Unable to compute increase in deaths')
       elif params.trig_def_type[phase]=='positives':
           value=(np.sum(sim.newisolated[t-7:t,:])/np.sum(sim.newtested_mit[t-7:t,:]))
 #          print ('positives calculated at',value)
       else:
           raise CustomError('trig_def_type for phase ',str(phase),' does not exist')
           
       if math.isnan(value):
           return(False)
       if params.trig_op_type[phase]=='=':
           if value==int(params.trig_values[phase]):
                return(True)
       else:
           if params.trig_op_type[phase]=='<':
               if value<params.trig_values[phase]:
                   return(True)
           else:
               if params.trig_op_type[phase]=='>':
                   if value>params.trig_values[phase]:
                       if params.trig_def_type[phase]=='positives':
                           print ('t=',t,'positives=',value, 'new > ','phase:',phase)
                       return(True)
       return(False)
   
   def get_data_frame(self,num_days,num_compartments,compartment):
      df = pd.DataFrame({
          'days': range(0,num_days),
          'dates':self.dates[:],
          'day1':range(0,num_days),
          'compartment': np.full(num_days,compartment[0]),
          'population' : np.round(self.population[:,0],3),
          'susceptibles' : np.round(self.susceptibles[:,0],3),
          'isolated': np.round(self.isolated[:,0],3),
          'isolatedinfected': np.round(self.isolatedinfected[:,0],3),
          'infectednotisolated': np.round(self.infectednotisolated[:,0],3),
          'infected': np.round(self.infected[:,0],3),
          'importedinfections':np.round(self.importedinfections[:,0],3),
          'accumulatedinfected': np.round(self.accumulatedinfected[:,0],3),
          'tested_mit': np.round(self.tested_mit[:,0],3),
          'confirmed': np.round(self.confirmed[:,0],3),
          'deaths': np.round(self.deaths[:,0],3),
          'recovered': np.round(self.recovered[:,0],3),
          'beta': np.round(self.beta_arr[:,0],3),
          'susceptibleprop' : np.round(self.susceptibleprop[:,0],3),
          'newtested_mit': np.round(self.newtested_mit[:,0],3),
          'newimportedinfections':np.round(self.newimportedinfections[:,0],3),
          'newinfected': np.round(self.newinfected[:,0],3),
          'newisolated': np.round(self.newisolated[:,0],3),
          'newisolatedinfected': np.round(self.newisolatedinfected[:,0],3),
          'newconfirmed': np.round(self.newconfirmed[:,0],3),
          'newrecovered': np.round(self.newrecovered[:,0],3),
          'requireddxtests': np.round(self.requireddxtests[:,0],3),
          'actualdxtests': np.round(self.actualdxtests[:,0],3),
          'newdeaths': np.round(self.newdeaths[:,0],3),
          'truepositives':np.round(self.truepositives[:,0],3),
          'falsepositives':np.round(self.falsepositives[:,0],3),
          'truenegatives':np.round(self.truenegatives[:,0],3),
          'falsenegatives':np.round(self.falsenegatives[:,0],3),
          'ppv':np.round(self.ppv[:,0],3),
          'npv':np.round(self.npv[:,0],3),
          'incidence':np.round(self.incidence[:,0],3),
          'prevalence':np.round(self.prevalence[:,0],3),
 #         'actualdeaths':self.actualdeaths,
    #      'actualcases':self.actualcases,
 #         'actualtests_mit':self.actualtestedmit
          'p_case_all_simulated': np.round(self.p_case_all_simulated[:,0],3),
          'p_case_all':np.round(self.p_case_all[:,0],3)
          
         })
      for i in range(1,num_compartments):
         dfadd = pd.DataFrame({
            'days': range(0,num_days),
            'dates': self.dates[:],
            'day1':range(0,num_days),
            'compartment': np.full(num_days,compartment[i]),
            'population' : np.round(self.population[:,i],3),
            'susceptibles' : np.round(self.susceptibles[:,i],3),
            'isolated': np.round(self.isolated[:,i],3),
            'isolatedinfected': np.round(self.isolatedinfected[:,i],3),
            'infectednotisolated': np.round(self.infectednotisolated[:,i],3),
            'infected': np.round(self.infected[:,i],3),
            'importedinfections':np.round(self.importedinfections[:,i],3),
            'accumulatedinfected': np.round(self.accumulatedinfected[:,i],3),
            'tested_mit': np.round(self.tested_mit[:,i],3),  
            'confirmed': np.round(self.confirmed[:,i],3),
            'deaths': np.round(self.deaths[:,i],3),
            'recovered': np.round(self.recovered[:,i],3),
            'beta': np.round(self.beta_arr[:,i],3),
            'susceptibleprop' : np.round(self.susceptibleprop[:,i],3),
            'newtested_mit': np.round(self.newtested_mit[:,i],3),
            'newimportedinfections':np.round(self.newimportedinfections[:,i],3),
            'newinfected': np.round(self.newinfected[:,i],3),
            'newisolated': np.round(self.newisolated[:,i],3),
            'newisolatedinfected': np.round(self.newisolatedinfected[:,i],3),
            'newconfirmed': np.round(self.newconfirmed[:,i],3),
            'newrecovered': np.round(self.newrecovered[:,i],3),
            'requireddxtests': np.round(self.requireddxtests[:,i],3),
            'actualdxtests': np.round(self.actualdxtests[:,i],3),
            'newdeaths': np.round(self.newdeaths[:,i],3),
            'truepositives':np.round(self.truepositives[:,i],3),
            'falsepositives':np.round(self.falsepositives[:,i],3),
            'truenegatives':np.round(self.truenegatives[:,i],3),
            'falsenegatives':np.round(self.falsenegatives[:,i],3),
            'ppv':np.round(self.ppv[:,i],3),
            'npv':np.round(self.npv[:,i],3),
            'incidence':np.round(self.incidence[:,i],3),
            'prevalence':np.round(self.prevalence[:,i],3),
            'p_case_all_simulated': np.round(self.p_case_all_simulated[:,i],3),
            'p_case_all':np.round(self.p_case_all[:,i],3)
   #         'actualdeaths':self.actualdeaths
            })
         df = df.append(dfadd)
      return df
  
   def compute_r(self,params,t):
       totalinfected_t=0
       newinfected_t=0
       for i in range(0, params.num_compartments):
           totalinfected_t=totalinfected_t+self.infected[t,i]
           newinfected_t=newinfected_t+self.newinfected[t,i]
       if totalinfected_t>0:
           r=newinfected_t/totalinfected_t*params.recovery_period
       else:
           r=0
   #    print('t=',t,'new_infected',newinfected_t,'infected',totalinfected_t,'re=',r)
       return(r)
           

######################################################################
# adjust_beta:
#    apply deceleration step to beta using alpha
#    final_beta serves as a lower_bound
#    computation depends on sign of alpha - maybe there could be a more elegant solution for this
######################################################################

def adjust_beta(par,beta,final_beta,alpha):
    num_compartments = len(beta)
    for i in range (0,num_compartments):
       for j in range(0,num_compartments):
          if alpha[i,j]>=0:
              if beta[i,j]+alpha[i,j] < final_beta[i,j]:
                 beta[i,j]=beta[i,j]+alpha[i,j]
              else:
                 beta[i,j] = final_beta[i,j]
          else:
              if beta[i,j]+alpha[i,j] >= final_beta[i,j]:
                 beta[i,j]=beta[i,j]+alpha[i,j]
              else:
                 beta[i,j] = final_beta[i,j]
    meanbeta=np.sum(beta*par.init_pop/par.init_pop.sum(),axis=1)
    return(meanbeta,beta)
   
######################################################################
# simulate:
#    takes in system parameters, initial beta matrix, final beta matrix
#    and performs SIR simulation with compartments
#
#    returns:
#        results a dataframe containing simulation results
######################################################################


    
def simulate(country_df,sim, par, max_betas, min_betas,start_day=1, end_day=300,phase=0,use_real_testdata=False):
   
    #why is this -1
    num_phases=len(par.severity)-1
    pops_for_beta=par.init_infected  #temp instruction]
    #fix starting conditions
    meanbeta=[par.max_beta_target,par.max_beta_target,par.max_beta_target]
    initial_betas=generate_betas(min_betas,max_betas,par.severity[phase])  #beta_min,beta_max, min_betas,max_betas, target,pops
    betas = initial_betas.copy() #this is current value of beta matrix
    final_betas=initial_betas
    alpha=(final_betas-initial_betas)/par.beta_adaptation_days
    sim.dates=[par.day1 + dt.timedelta(days=x) for x in range(0,par.num_days)]
    tau=par.tau
    gamma=par.gamma
    
    # acquire data on actual tests, deaths and cases - no problem here 
    for i in range(0,len(country_df)):
    #this allows simulations that are shorter than country_df
        if i<end_day:
            sim.actualnewtests_mit[i]=country_df.iloc[i]['tests']
            sim.actualdeaths[i]=country_df.iloc[i]['accumulated_deaths']
            sim.actualcases[i]=country_df.iloc[i]['accumulated_cases']
            
 #          Fill in missing values - infers values for periods between end of country_df and current date
 #   for i in range(0,len(country_df)+3):
    if (len(country_df)+3)<=par.num_days:
        end_loop=len(country_df)+3
    else:
        end_loop=par.num_days
    for i in range(0,end_loop):
   #this was to fill in missing values when we were using centered averages. Should no longer be necessary - even if required can be moved to a procedure
        if i>350:
            if np.isnan(sim.actualnewtests_mit[i]) or sim.actualnewtests_mit[i]==0:
                sim.actualnewtests_mit[i]=sim.actualnewtests_mit[i-29:i-1].mean()
            if np.isnan(sim.actualcases[i])or sim.actualcases[i]==0:
                sim.actualcases[i]=sim.actualcases[i-1]+sim.actualnewcases[i-29:i-1].mean()
            if np.isnan(sim.actualdeaths[i])or sim.actualcases[i]==0:
                sim.actualdeaths[i]=sim.actualdeaths[i-1]+sim.actualnewdeaths[i-29:i-1].mean()
                
        else:
            if np.isnan(sim.actualcases[i]):
                sim.actualcases[i]=0
            if np.isnan(sim.actualnewtests_mit[i]):
                sim.actualnewtests_mit[i]=0
            if np.isnan(sim.actualdeaths[i]):
                sim.actualdeaths[i]=0
        sim.actualnewdeaths[i]=sim.actualdeaths[i]-sim.actualdeaths[i-1]
        if sim.actualnewdeaths[i]<0:
            sim.actualnewdeaths[i]=0
        sim.actualnewcases[i]=sim.actualcases[i]-sim.actualcases[i-1]
        if sim.actualnewcases[i]<0:
            sim.actualnewcases[i]=0
    last_phase=0
    #The simulation proper starts here
    for t in range(start_day,end_day):
    # Here we determine if there is a need to change phase before continuing
       if phase+1<=num_phases:
           if sim.trigger_next_phase(par,t,phase+1): 
               phase=phase+1
               last_phase=t #records date of last phase
               initial_betas=betas
               if phase<num_phases+1:
                   final_betas=generate_betas(min_betas,max_betas,par.severity[phase])
                   alpha=(final_betas-initial_betas)/par.beta_adaptation_days
               else:  #this feels a little contorted
                   final_betas=initial_betas
                   alpha=(final_betas-initial_betas)/par.beta_adaptation_days
       results_delay=par.results_period[phase]
       time_in_isolation=par.recovery_period-results_delay
       if time_in_isolation<0:
           time_in_isolation=0
       if t==1:
           last_target_recovery=0
           last_target_isolation=0
       sim.days[t]=t
       sim.cross_infect(par,betas,t)
       sim.addup_infections(par,t)
       
       # works out number of contacts per person. Maximum when target beta=max beta
 #      print('max contacts per case=', par.max_contacts_per_case,'prop contacts traced',par.prop_contacts_traced[phase])
 #      print('beta overall',beta_overall,)
   #    contacts_per_person=par.max_contacts_per_case*(1-par.severity[phase])+par.min_contacts_per_case*par.severity[phase]
  
       contacts_per_person=10
       contacts_per_person_isolated=contacts_per_person*par.prop_contacts_traced[phase]
#       print('t=',t,'contacts per person',contacts_per_person,'contacts per person isolated=',contacts_per_person_isolated)
       #perform mitigation testing  
       tests_performed = sim.perform_tests(par,t,phase,use_real_testdata)  
       sim.newtested_mit[t]=tests_performed
               
       # The simulation now proceeds one compartment at a time
       for i in range(0,par.num_compartments):
           infected_secondaries=0
           non_infected_secondaries=0
           sim.newimportedinfections[t,i]=sim.get_imported(par,t,i,phase)
           sim.newinfected[t,i]=sim.newinfected[t,i]+sim.newimportedinfections[t,i]
    # This makes sure the accumulated number of infected is never bigger than the population
           if sim.accumulatedinfected[t-1,i]+sim.newinfected[t,i]>sim.population[t-1,i]:
               sim.newinfected[t,i]=sim.population[t-1,i]-sim.accumulatedinfected[t-1,i]
    # Previously this was inside target loop - that must be wrong
               sim.newisolated[t,i]=0
               sim.newisolatedinfected[t,i]=0
               sim.newconfirmed[t,i]=0
               infected_secondaries=0
               non_infected_secondaries=0
    # The code below ensures there is no double counting if result_period changes - can be a procedure
           for target in range(last_target_isolation+1, t-par.results_period[phase]+1):
                if target-results_delay>0:
                    infected_secondaries_now,non_infected_secondaries_now=compute_secondaries(sim,par,t,i,sim.truepositives[target-results_delay,i],sim.falsepositives[target-results_delay,i],contacts_per_person_isolated,meanbeta,phase)
                  #  infected_secondaries,non_infected_secondaries=compute_secondaries2(par, sim, i,t, sim.truepositives[target-results_delay,i],sim.falsepositives[target-results_delay,i],phase) 
                    infected_secondaries=infected_secondaries+infected_secondaries_now
                    non_infected_secondaries=non_infected_secondaries+non_infected_secondaries_now
                if (t-results_delay)>0:  
                   sim.newisolated[t,i] =  sim.newisolated[t,i]+sim.truepositives[target-results_delay,i]+sim.falsepositives[target-results_delay,i]+infected_secondaries+non_infected_secondaries
# =============================================================================
#                    if sim.newisolated[t,i]>sim.newinfected[target-results_delay,i]+sim.falsepositives[target-results_delay,i]+non_infected_secondaries:
#                         sim.newisolated[t,i]=sim.newinfected[target-results_delay,i]+sim.falsepositives[target-results_delay,i]+non_infected_secondaries
# =============================================================================
                   sim.newisolatedinfected[t,i] =sim.newisolatedinfected[t,i]+ sim.truepositives[target-results_delay,i]+infected_secondaries
# =============================================================================
#                    if sim.newisolatedinfected[t,i]>sim.newisolated[t,i]:
#                         sim.newisolatedinfected[t,i]=sim.newisolated[t,i]
# =============================================================================
                   sim.newconfirmed[t,i] = (sim.newconfirmed[t,i]+sim.truepositives[target-results_delay,i]+sim.falsepositives[target-results_delay,i])
#============================================================================================
# The statement below causes cases to collapse irrealistically as we approach current date - this raises questions about the other comnditionals.
# I think the conditionals come too late in the code. We need to stop things at root
# e.g. when we compute secondaries
# =============================================================================
#                    if sim.newconfirmed[t,i]>sim.newinfected[target-results_delay,i]+sim.falsepositives[target-results_delay,i]:
#                        sim.newconfirmed[t,i]=sim.newinfected[target-results_delay,i]+sim.falsepositives[target-results_delay,i]
# =============================================================================
# =============================================================================
#            if i==0 and t==550: 
#                print('infected sec=',infected_secondaries,'non_infected_sec=', non_infected_secondaries, 'new isolated=',sim.newisolated[t,i])
# =============================================================================
           if t-(par.recovery_period+par.incubation_period)>=0:
               sim.newrecovered[t,i] = sim.newinfected[t-(par.recovery_period+par.incubation_period),i]*gamma
           else:
               sim.newrecovered[t,i]=0
 #          if t- par.death_period>=0 and not ispast(par.day1, t):
           if t- par.death_period>=0:
               sim.newdeaths[t,i] = sim.newinfected[t-(par.death_period+par.incubation_period),i]*tau
           if sim.newdeaths[t,i]<0:
               sim.newdeaths[t,i]=0
           sim.requireddxtests[t,i]=sim.newrecovered[t,i]*par.requireddxtests[phase] 
           if sim.requireddxtests[t,i]>par.num_tests_care[phase]:
               sim.actualdxtests[t,i]=par.num_tests_care[phase]
           else:
               sim.actualdxtests[t,i]=sim.requireddxtests[t,i]
           sim.tested_mit[t,i] = sim.tested_mit[t-1,i] + sim.newtested_mit[t,i]
           newisolatedrecovered=0
           newisolateddead=0
           newisolatedinfectedrecovered=0
           newisolatedinfecteddead=0
           target=0
         # The code below makes sure that if the results period changes no secondaries are counted double or missed
           for target in range (last_target_recovery+1,t-time_in_isolation+1):
               if target>=0:
                   newisolatedrecovered=newisolatedrecovered+sim.newisolated[target,i]*gamma
                   newisolatedinfectedrecovered=newisolatedinfectedrecovered+sim.newisolatedinfected[target,i]*gamma  
                   newisolateddead=newisolateddead+sim.newisolatedinfected[target,i]*tau
                   newisolatedinfecteddead=newisolatedinfecteddead+sim.newisolatedinfected[target,i]*tau
               #subtract deaths - this instructions seems wrong - we are only considering newisolated who recover - that's why we multiply by gamma
# =============================================================================
#                if t-par.death_period>=0:
#                    newisolatedrecovered=newisolatedrecovered-sim.newisolated[target-par.death_period,i]*tau
#                    newisolatedinfectedrecovered=newisolatedinfectedrecovered-sim.newisolatedinfected[target-par.death_period,i]*tau
#                    if newisolatedrecovered<0:
#                        newisolatedrecovered=0
#                    if newisolatedinfectedrecovered<0:
#                        newisolatedinfectedrecovered=0
# =============================================================================
           sim.isolated[t,i]=sim.isolated[t-1,i]+sim.newisolated[t,i]-newisolatedrecovered-newisolateddead
           if sim.isolated[t,i]<0:
               sim.isolated[t,i]=0
           sim.isolatedinfected[t,i] = sim.isolatedinfected[t-1,i] + sim.newisolatedinfected[t,i] - newisolatedinfectedrecovered-newisolatedinfecteddead
# =============================================================================
#            if (i==0) and (507<=t<=511):
#                print('t=',t,'isolated infect',sim.isolatedinfected[t,i],'newisolatedinfected',sim.newisolatedinfected[t,i],'IIrecovered',newisolatedinfectedrecovered,'IIdead', newisolatedinfecteddead)
# =============================================================================
           sim.deaths[t,i] = sim.deaths[t-1,i]+sim.newdeaths[t,i]
           sim.recovered[t,i] = sim.recovered[t-1,i]+sim.newrecovered[t,i]
           sim.population[t,i] = sim.population[t-1,i]-sim.newdeaths[t,i]
           sim.infected[t,i] = sim.infected[t-1,i]+sim.newinfected[t,i]-sim.newrecovered[t,i]-sim.newdeaths[t,i]
           sim.susceptibles[t,i]=sim.population[t,i]-sim.infected[t,i]-sim.recovered[t,i] #deaths have already been subtracted from pop
           if sim.susceptibles[t,i]<0:  #defensive programming - I don't know why they go negative but they do
               sim.susceptibles[t,i]=0 
   
           if sim.infected[t,i]>sim.population[t,i]:
               sim.infected[t,i]=sim.population[t,i]
           if sim.infected[t,i]<0:
               sim.infected[t,i]=0
           if sim.isolatedinfected[t,i]<0:
               sim.isolatedinfected[t,i]=0
           if sim.isolatedinfected[t,i]>sim.infected[t,i]:
               sim.isolatedinfected[t,i]=sim.infected[t,i]
           if sim.infected[t,i]>0:
               sim.reff[t,i]=sim.newinfected[t,i]/sim.infected[t,i]*(par.recovery_period+par.incubation_period) #add lag
           else:
               sim.reff[t,i]=np.nan
           
           if sim.population[t,i]>0:
              sim.susceptibleprop[t,i] = sim.susceptibles[t,i]/sim.population[t,i] #another accounting identity
           else:
              sim.susceptibleprop[t,i]=0 #avoids a divide by zero error with zero pop in one compartment
           sim.confirmed[t,i]=sim.confirmed[t-1,i] + sim.newconfirmed[t,i]
           sim.infectednotisolated[t,i]=sim.infected[t,i]-sim.isolatedinfected[t,i]
           
      #     if sim.infectednotisolated[t,i]<0:
      #         sim.infectednotisolated[t,i]=0
      #     sim.newimportedinfections[t,i]=sim.get_imported(par,t,i,phase)
           sim.accumulatedinfected[t,i]=sim.accumulatedinfected[t-1,i]+sim.newinfected[t,i]#+sim.newimportedinfections[t,i]
# =============================================================================
#            if sim.accumulatedinfected[t,i]<sim.population[t-1,i]:
#                 sim.infected[t,i]=sim.infected[t,i]+sim.newimportedinfections[t,i]
#  #               sim.newinfected[t,i]=sim.newinfected[t,i]+sim.newimportedinfections[t,i]
#                 sim.infectednotisolated[t,i]=sim.infectednotisolated[t,i]+sim.newimportedinfections[t,i]
#            else:
#                 sim.infected[t,i]=sim.population[t-1,i]
#                 sim.newinfected[t,i]=0
#                 sim.accumulatedinfected[t,i]=sim.accumulatedinfected[t-1,i]
#                 sim.infectednotisolated[t,i]=sim.infectednotisolated[t-1,i]
# =============================================================================
           #if there infectednotisolated falls below a minimum threshold we bring it back up to threshold - we are not ajusting isolated
# Got rid of mandatory minimum
# =============================================================================
#            if not(sim.infectednotisolated[t,i] >= par.min_infected_not_isolated or t<75 or par.imported_infections_per_day[phase]==0):
#               sim.infectednotisolated[t,i]=par.min_infected_not_isolated
#               if sim.infectednotisolated[t,i]>sim.infected[t,i]:
#                   sim.infected[t,i]=sim.infectednotisolated[t,i]
#               sim.isolatedinfected[t,i]=sim.infected[t,i]-sim.infectednotisolated[t,i]
#               newisolatedinfected=sim.isolatedinfected[t,i]-sim.isolatedinfected[t-1,i]
#               if newisolatedinfected>0:
#                   sim.newisolatedinfected[t,i]=sim.isolatedinfected[t,i]-sim.isolatedinfected[t-1,i]
#               else:
#                   sim.newisolatedinfected[t,i]=0
# =============================================================================
           if sim.population[t,i]>0:
               sim.incidence[t,i]=sim.newinfected[t,i]/sim.population[t,i]
               sim.prevalence[t,i]=sim.accumulatedinfected[t,i]/sim.population[t,i]
           else:
               sim.incidence[t,i]=0
               sim.prevalence[t,i]=0
       
       if(ispast(par.day1,t)): 
           if t>=par.no_improvement_period:
               tau=tau=tau*par.fatality_reduction_per_day
          
       else: #future phases
          tau=par.tau*(1-par.fatality_reduction_recent[phase])
       gamma=1-tau
       meanbeta,betas=adjust_beta(par,betas,final_betas,alpha)
       # this defines where the loops for isolation and recoveries begins on next t
       if last_target_isolation<t-par.results_period[phase]:
           last_target_isolation=t-par.results_period[phase]
       if last_target_recovery<t-time_in_isolation:
           last_target_recovery=t-time_in_isolation
       
 # =============================================================================
    df = sim.get_data_frame(par.num_days,par.num_compartments,par.compartment)
    return sim,df
 
######################################################################
# plot_results:
#     present plots based on scenario parameters passed
######################################################################

def plot_results(scenario_name,compartment,num_tests, dates,newisolated,newinfected,newtested,infected_not_isolated,confirmed,deaths,susceptibles,prevalence,actual_deaths=[]):
     
     fig = plt.figure()
     plt.plot (dates, newinfected,color='r',label="newinfected")
     plt.title(scenario_name+': '+compartment+' - Infected')
     plt.ylabel('Number')
     plt.xlabel('Date')
     plt.xticks(rotation=30) 
     plt.legend(title= "Legend")
     plt.show()
     plt.close()
     plt.plot (dates, deaths,color='k',label="Simulated Deaths")
    
     if len(actual_deaths)>0:
        if len(deaths)-len(actual_deaths)>0:
            padding=np.zeros(len(deaths)-len(actual_deaths))
            actual_deaths=np.concatenate((np.array(actual_deaths),padding))
        else: 
            actual_deaths=actual_deaths[0:len(deaths)]  
        plt.plot(dates,actual_deaths,color='y', label='Actual deaths')
      
     plt.title(scenario_name+': '+compartment+' - Deaths')
     plt.ylabel('Number')
     plt.xlabel('Date')
     plt.xticks(rotation=30) 
     plt.legend(title= "Legend")
     plt.show()
     plt.close()
     plt.plot(dates,newisolated,color='b', label="newisolated")
     plt.title(scenario_name+': '+compartment+' - Isolated')
     plt.ylabel('Number')
     plt.xlabel('Date')
     plt.xticks(rotation=30) 
     plt.legend(title= "Legend")
     plt.show()
     plt.close()
     plt.plot(dates,susceptibles,color='c', label="Susceptibles")
     plt.title(scenario_name+': '+compartment+' - Susceptibles')
     plt.ylabel('Number')
     plt.xlabel('Date')
     plt.xticks(rotation=30) 
     plt.legend(title= "Legend")
     plt.show()
     plt.plot(dates,prevalence,color='r', label="Prevalence")
     plt.title(scenario_name+': '+compartment+' - Prevalence')
     plt.ylabel('Prevalence')
     plt.xlabel('Date')
     plt.xticks(rotation=30) 
     plt.legend(title= "Legend")
     plt.show()
     plt.close()
     

######################################################################
# generate_betas:
#    generates a beta matrix whwere the  average
#    of the betas, weighted by infected_not_isolated
#    is equal to target. 
######################################################################


def generate_betas(min_betas,max_betas, severity):

    new_betas=severity*min_betas+(1-severity)*max_betas #generates a new beta matrix with values lying between min_betas and max_betas
    return(new_betas)

def getcountrydata(csvfilename):
#   df = pd.read_csv(csvfilename,index_col='Date',parse_dates=True)
   df = pd.read_csv(csvfilename)
   return df.fillna(0)

# def aligndeaths(actual,simulated):
   
#    n = min(len(actual),len(simulated))
#    aligneddeaths = [0]*n
#    amark = 0
#    for i in range(0,n-1):
#       if actual[i] >= 20:
#          amark = i
#          break
#    smark = 0
#    for i in range(0,n-1):
#       if simulated[i] >= 20:
#          smark = i
#          break
#    shift=amark-smark
#    for i in range(0,n-1):
#        #handle case of negative shifts
#       if i<shift:
#          aligneddeaths[i] = 0
#       elif i-shift<len(aligneddeaths):
#          aligneddeaths[i] = simulated[i-shift]
   
#    return aligneddeaths, shift
def aligndeaths(actual,simulated):
   n = len(actual)
   m = len(simulated)
   aligneddeaths = [0]*n
   amark = 0
   for i in range(0,n):
      if actual[i] >= 20:
         amark = i
         break
   smark = 0
   for i in range(0,m):
      if simulated[i] >= 20:
         smark = i
         break
   for i in range(0,n):
      if (i < (amark-smark)):
         aligneddeaths[i] = 0
      else:
         shiftedj = i-(amark-smark)
         if shiftedj < 0:
            shiftedj = 0
         elif shiftedj > m-1:
            shiftedj = m-1
         aligneddeaths[i] = simulated[shiftedj]
   return aligneddeaths, amark-smark

def alignactualwithsimulated(dfactual,dfsimdeaths):
   simdeaths = dfsimdeaths.tolist()
   actdeaths = dfactual['accumulated_deaths'].tolist()
   aligneddeaths, shift = aligndeaths(actdeaths,simdeaths)
   dayshift=dt.timedelta(shift)
   day1 = dt.datetime.strptime(dfactual.iloc[0]['Date'],"%Y-%m-%d")+dayshift
  # day1 = dt.datetime.strptime(dfactual.iloc[0]['Date'],"%Y-%m-%d")
  # shift=0
   return day1,shift



def ispast(start_date,t):
    today=dt.datetime.now()
    simday=(today-start_date).days
#changed this - it used to be <=
    if t<simday:
        return(True)
    else:
        return(False)

#returns today's date as a simulation day    
def computetoday(start_date,triggers):
    today=dt.datetime.now()
    simday=(today-start_date).days
    simphase=0
    for i in range(0,len(triggers)):
        if triggers[i]<simday:
            simphase=i
    return simphase,simday

def create_past(param,defaults,trigger_values, severity):
    n_phases=len(trigger_values)
    past={}
# =============================================================================
#     if param['total_pop']>=4000000:
#         defaults['imported_infections_per_day']=4
#     else:
#         defaults['imported_infections_per_day']=0.1
# =============================================================================
    for a_key in defaults.keys():
        a_value=defaults[a_key]
        a_list=[a_value]*n_phases
        past.update({a_key:a_list})
    past.update({'trig_values':trigger_values})
    past.update({'severity':severity})
    return(past)
        

def create_scenario(past,future):
     scenario={}
     for a_key in past.keys():
         past_value=past[a_key]
         if a_key in future:
             future_value=future[a_key]
             sequence=past_value+future_value
             scenario.update({a_key:sequence})
         else:
             print('WARNING - KEY " ', a_key,' " IN SCENARIO PARAMETERS NOT PRESENT IN FIXED PARAMETERS')
     return(scenario)

#normalize betas so the sum of expected infections reaches a target value
# function can be optimized to use matrix multiplication
     
def normalize_betas(p,beta,target):
    expected_infections=np.zeros((len(beta),len(beta)))
    init_pops=list(map(float,p['init_pop']))
    total_pop=sum(init_pops)
    for i in range(0, len(beta)):
        for j in range(0, len(beta)):
            expected_infections[i,j]=beta[i,j]*init_pops[j]/total_pop*init_pops[i]/total_pop
    adjust=target/np.sum(expected_infections)
    return beta*adjust

def compute_secondaries(sim,par,t,i,true_positives, false_positives,contacts_per_person,meanbeta,phase):
    
#I have modified this computation to make sure we do not have more infected_isolated from track and trace than total number of infected

    n_contacts_traced=(true_positives+false_positives)*contacts_per_person
    infected_isolated=meanbeta[i]*par.recovery_period*true_positives*par.prop_contacts_traced[phase]*sim.susceptibleprop[t,i]
  
    if infected_isolated>n_contacts_traced:
        infected_isolated=n_contacts_traced
    # infected_isolated cannot be higher than infected - could be if track and trace highly effective
    if infected_isolated>sim.newinfected[t,i]-true_positives:
        infected_isolated=sim.newinfected[t,i]-true_positives
    not_infected_isolated=n_contacts_traced-infected_isolated

    return infected_isolated, not_infected_isolated


def write_parameters(afilename,fixed_params,scenario_params):
    param_dict={'fixed_params':fixed_params,\
           'scenario_params':scenario_params}
    with open(afilename,'w') as outfile:      
        json.dump(param_dict,outfile,indent=6)
        
def read_parameters(afilename):
    with open(afilename) as infile:      
        data=json.load(infile)
    fixed_params=data['fixed_params']
    scenario_params=data['scenario_params']
    return fixed_params,scenario_params
    
        
def adjust_positives_and_negatives(sim,par,t,phase,tests_performed,p_infected):
    simphase,today=computetoday(par.day1,par.trig_values)
    if sim.actualnewtests_mit[t]>0:
            p_case=sim.actualnewcases[t]/sim.actualnewtests_mit[t]
    else:
            p_case=0   
     #this is only true if all symptomatic_infected are tested
    cases=tests_performed*p_case
    for i in range(0,par.num_compartments):  
# =============================================================================
#        if p_infected[i]>1:
#            p_infected[i]=1
# =============================================================================
        if t<today:
           sim.truenegatives[t,i]=tests_performed[i]-cases[i]
           if sim.truenegatives[t,i]<0:
              sim.truenegatives[t,i]=0
           sim.falsepositives[t,i]= sim.truenegatives[t,i]*(1-par.specificity[phase])
           sim.truepositives[t,i]=cases[i]-sim.falsepositives[t,i]
           sim.falsenegatives[t,i]=sim.truepositives[t,i]*(1-par.sensitivity[phase])
        else:
           sim.truepositives[t,i]=tests_performed[i]*p_infected[i]*par.sensitivity[phase]
           sim.truenegatives[t,i]=tests_performed[i]*(1-p_infected[i])*par.specificity[phase]
           sim.falsepositives[t,i]=sim.truenegatives[t,i]*(1-par.specificity[phase])   
           sim.falsenegatives[t,i]=tests_performed[i]*p_infected[i]*(1-par.sensitivity[phase])
    
           
# =============================================================================
#    #    sim.truepositives[t,i] = testsperformed[i] * p_infected[i]
#         if t==670 and i==2:
#            print('in adjust')
#            print('testsperformed=',tests_performed[i])
#            print('p_infected=',p_infected[i])
#            print('true_positives=',sim.truepositives[t,i])
#            print('false positives=',sim.falsepositives[t,i])
#            print('total positives=',sim.truepositives[t,i]+sim.falsepositives[t,i])
# =============================================================================
      
        if (sim.truepositives[t,i]+sim.falsepositives[t,i])>0:
           sim.ppv[t,i]=sim.truepositives[t,i]/(sim.truepositives[t,i]+sim.falsepositives[t,i])
        else:
           sim.ppv[t,i]=np.nan
        if (sim.truenegatives[t,i]+sim.falsenegatives[t,i])>0:
           sim.npv[t,i]=sim.truenegatives[t,i]/(sim.truenegatives[t,i]+sim.falsenegatives[t,i])
        else:
           sim.npv[t,i]=np.nan
           
           
def create_empty_country_df (start_date, n_records):
    dates=[]
    accumulated_deaths=np.zeros(n_records)
    tests=np.zeros(n_records)
    accumulated_cases=np.zeros(n_records)
    
    for i in range(0,n_records):
        date=start_date+dt.timedelta(days=i)
        date_string=date.strftime("%Y-%m-%d")
        dates.append(date_string)
    data={'Date':dates,'accumulated_deaths':accumulated_deaths, 'tests':tests,'accumulated_cases':accumulated_cases}
    df=pd.DataFrame(data)
    return(df)
        
    
    
    
    
        
    
    



