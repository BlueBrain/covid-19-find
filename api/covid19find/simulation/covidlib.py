
# contains function definitions for covid simulation
# author:  JP Vergara

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import csv
import datetime as dt
import copy



def get_system_params(sysfile):
#this is a simplified replacement for get_system_params
   p = {}
   csv_reader = csv.reader(open(sysfile), delimiter=',')
   for a_row in csv_reader:
        param_name=a_row[0]
        if len(a_row)==2:
            val=a_row[1]
        else:
            val=[]
            for i in range(1,len(a_row)):
                val.append(a_row[i])
        p[param_name]=val
   print('p=',p)
   return p

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

######################################################################
# get_scenarios:
#    reads parameters for a number of scenarios from a csv file
#    returns:
#       Scenarios object containing:
#          scenarios - scenario code (keys for dictionary)
#          scenario_labels - scenario name (for printing)
#          scenarios_params - dictionary containing variables to be overridden
#                            per scenario, with corresponding values
######################################################################

def get_scenarios(scenariosfile):
   sc = Scenarios()
   sc.read_from_csv(scenariosfile) #we might do without this
   return sc

######################################################################
# update_system_params:
#    update the parameter dictionary incorporating overrides
#    from fixed_params
######################################################################

def update_system_params(p, fixed_params):
   num_compartments = int(p['num_compartments'])
   num_testkit_types=int(p['num_testkit_types'])
         
#     These are defined in compartment parameters - no need to define here:
#     p['compartment']=['Hospitals','Other high contact ','Rest of population']
#     p['init_infected']=[100,100,100]

# =============================================================================
#    p['testkits']=['PCR','RDT','Chest xrays']
#    p['sensitivity'][0]=fixed_params['sensitivity_PCR']
#    p['sensitivity'][1]=fixed_params['sensitivity_RDT']
#    p['specificity'][0]=fixed_params['specificity_PCR']
#    p['specificity'][1]=fixed_params['specificity_RDT']
# =============================================================================
#   p['trig_def_type'][0]=fixed_params['trig_def_type']
#   p['trig_op_type'][0]=fixed_params['trig_op_type']
#   p['trig_values']=fixed_params['trig_values']
#   p['test_symptomatic_only']=['true','true','true']
         
   #define size of compartments   
   hosp_staff=fixed_params['hospital_beds']*fixed_params['staff_per_bed']
   high_risk_urban=fixed_params['total_pop']*fixed_params['prop_urban']*fixed_params['prop_below_pl']
   other_high_contact=(fixed_params['total_pop']-high_risk_urban-hosp_staff)*fixed_params['prop_15_64']*fixed_params['prop_woh']
   p['init_pop'][0]=fixed_params['hospital_beds']*fixed_params['staff_per_bed']
   p['init_pop'][1]=high_risk_urban+other_high_contact
   p['init_pop'][2]=fixed_params['total_pop']-hosp_staff-int(p['init_pop'][1])
   p['total_pop']=int(fixed_params['total_pop'])
   #compute age_corrected IFR

   prop_gt_64=fixed_params['age_gt_64']
   prop_15_64=fixed_params['prop_15_64']
   prop_1_14=1-(prop_gt_64+prop_15_64)
#   print ('prop_gt_64=', prop_gt_64)
 #  print ('prop_15_64=', prop_15_64)
 #  print ('prop_1_14=', prop_1_14)
   IFR_1_14=float(p['IFR_1_14'])
   IFR_15_64=float(p['IFR_15_64'])
   IFR_gt_64=float(p['IFR_gt_64'])
 #  print('term 1',IFR_1_14*prop_1_14)
 #  print('term 2',IFR_15_64*prop_15_64)
 #  print('term 3',IFR_gt_64*prop_gt_64)
   p['IFR_corrected']=IFR_1_14*prop_1_14+IFR_15_64*prop_15_64+IFR_gt_64*prop_gt_64
 #  print('IFR corrected=',p['IFR_corrected'])

   return


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

def run_simulation(country_df,fixed_params, **kwargs):

   sysfile = 'system_params.csv'
   initial_betafile = 'initial_betas.csv'

   if len(kwargs)>0:
      scenarios_user_specified=kwargs['scenarios']
  #    phase_start_days=kwargs['phase_start_days']
   else:
      scenarios_user_specified=[]
   #   phase_start_days=[]

# set up system parameters

   p = get_system_params(sysfile)
   update_system_params(p, fixed_params) # note: p is updated

# read initial beta matrix

   num_compartments = int(p['num_compartments'][0])
   initial_beta = get_beta(initial_betafile, num_compartments)  #don't think this is needed

 #  results = process_scenarios(p, sc, initial_beta, target_betas)
   results = process_scenarios(country_df,p, scenarios_user_specified, initial_beta)
   
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

def process_scenarios(country_df,p,scenarios,initial_beta):

#   original_p=p.copy() #make sure p starts clean each time
   num_compartments = int(p['num_compartments'])
   num_scenarios = len(scenarios)

   no_intervention_betafile = 'initial_betas.csv'
   max_intervention_betafile = 'lockdown_betas.csv'
#   mild_betafile='betas_mild.csv'
   num_tests_performed=np.zeros(num_compartments)
   expert_mode=True

#   print(sc.scenarios)
#   print(sc.scenario_labels)
#   print('scenario params=',sc.scenario_params)

   total_tests_mit_by_scenario=np.zeros(num_scenarios)
   total_tests_care_by_scenario=np.zeros(num_scenarios)
   total_deaths_by_scenario=np.zeros(num_scenarios)
   total_infected_by_scenario=np.zeros(num_scenarios)
   max_infected_by_scenario=np.zeros(num_scenarios)
   max_isolated_by_scenario=np.zeros(num_scenarios)
   scenario_names=[]
   dataframes=[]
   for i in range(0,num_scenarios):
 #     key = sc.scenarios[i-1] #If this is an array no need for a key
#      print('i=',i,'key=',key)
      scenario_name='SCENARIO' + ' '+ str(i)  #it should have a proper name
   #   scenario_names.append(scenario_name)  #name can be one item in dictionary
      if expert_mode:
         print ('*************')
         print ('scenario_name')
         print ('*************')
      parameters_filename=scenario_name+'_params.csv'
      filename = scenario_name+'_out.csv'
      summary_filename=scenario_name+'_summary.csv'
      scenario_default=get_system_params(parameters_filename)
      print('scenario default=',scenario_default)
      print('scenarios i=',scenarios[i])
  #    p['scenario_name']=scenario_name # JPV: not sure why you need this
 #     apply_scenario_to_p_2(p,scenario_default)
      p.update(scenario_default)
 #     print('p with default,p')
      # update p according to scenario_params[key]
 #     apply_scenario_to_p(p, sc.scenario_params[key])  #this can be index
      p.update(scenarios[i]) 
 #     print('p after user input',p)
 #     beta_max = float(p['beta_max'][0]) #this is the maximum value of overall beta for any intervention
#      beta_min=float(p['beta_min'][0]) #this is the lowest value of overall beta for any intervention
      nmultipliers=len(p['test_multipliers'])
      test_df=pd.DataFrame({
          'tests': p['test_multipliers'],
          'livessaved':np.zeros(nmultipliers),
          'reff':np.zeros(nmultipliers)})
      min_betas = get_beta(max_intervention_betafile, num_compartments)
      max_betas = get_beta(no_intervention_betafile, num_compartments)
      
      date_par=Par(p)
      date_sim = Sim(date_par.num_days,date_par.num_compartments)
      date_sim.set_initial_conditions(date_par)
     
        # run an initial simulation to determine the starting date of the epidemic
      throw,date_df=simulate(country_df,date_sim,date_par,max_betas,min_betas,1,75)
      dfsum_dates = date_df.groupby(['days']).sum().reset_index()
      # This will be updated when we have new optimization code - 
      df_date_result, day1 = alignactualwithsimulated(country_df,dfsum_dates['deaths'])
      
      #compute main simulation and store results
   #   sim=copy.deepcopy(old_sim)
      par = Par(p)
      par.day1=day1
      sim = Sim(par.num_days,par.num_compartments)
      sim.set_initial_conditions(par)
      sim,df = simulate(country_df,sim,par,max_betas,min_betas,1,par.num_days)
      df.to_csv(filename,index=False,date_format='%Y-%m-%d')
  #    old_sim=copy.deepcopy(sim)
      dataframes.append(df) 
      # do extra simulations to test different test strategies
      print('line before j')
      for j in range(0,len(par.test_multipliers)):
        print ('j=',j)
        test_par=Par(p)
  #      sim=copy.deepcopy(old_sim)
        for k in range(0,par.num_testkit_types): #maybe this should be for one phase only
             test_par.num_tests[k]=np.array(test_par.num_tests[k])*test_par.test_multipliers[j]
  # This line of code is incorrect - the phase should be the current phase
        current_phase=computecurrentphase(par.day1,par.trig_values)
        print('start date=', par.day1,'current phase=',current_phase)    
        throw,df_tests=simulate(country_df,sim,par,max_betas,min_betas,30,test_par.num_days,current_phase)
        dfsum_tests = df_tests.groupby(['days']).sum().reset_index()
        test_df['tests']=sum(map(int,p['num_tests']))
        test_df['deaths']=dfsum_tests['newdeaths'].sum()
        test_df['reff']=dfsum_tests['newinfected'][int(p['num_days'])-1]/dfsum_tests['infected'][int(p['num_days'])-1]
      print ('test_df=',test_df)
      dfsum = df.groupby(['dates']).sum().reset_index()
      
#      dfactual = getcountrydata('Switzerland.csv')
      
# =============================================================================
#       numpydate=np.datetime64(day1,format="%Y-%m.%d %I:%M:%S %p")
#       print('numpy date',numpydate)
# =============================================================================
 #     df['day1']=pd.to_datetime(day1,format="%Y-%m-%d")
 #     print('day1 df',df['day1'])
   #   df['date']=df['day1']+pd.to_timedelta(df['days'],unit='d')
     
 #     print('df date=',df['date'])
#      dfsum['total_deaths'].to_csv('simdeaths.csv',index=False)
        # gives result by day summed across compartments
  #    dfsum['day1']=pd.to_datetime(day1,format="%Y-%m-%d")
  #    dfsum['date']=dfsum['day1']+pd.to_timedelta(dfsum['days'],unit='d')
      dfsum['reff']=dfsum['newinfected']/dfsum['infected']*int(p['recovery_period'][0])
 #     print(dfsum['Reff'].to_string(index=False))
      dfsum['positive rate']=dfsum['newisolated']/dfsum['newtested_mit']
 #     print(dfsum['Positive rate'].to_string(index=False))
      dfsum['detection rate']=dfsum['newisolated']/dfsum['newinfected']
      dfsum['ppv']=dfsum['truepositives']/(dfsum['truepositives']+dfsum['falsepositives'])
      dfsum['npv']=dfsum['truenegatives']/(dfsum['truenegatives']+dfsum['falsenegatives'])
      dfsum['incidence']=dfsum['newinfected']/(dfsum['population'])
      dfsum['prevalence']=dfsum['accumulatedinfected']/(dfsum['population'])
     
  #    print(dfsum['Detection rate'].to_string(index=False))
      dataframes.append(dfsum)
      dfsum.to_csv(summary_filename,index=False,date_format='%Y-%m-%d')
      dfsumcomp = df.groupby(['compartment']).sum().reset_index()
        # gives results by day grouped by individual compartment
      dfmaxcomp = df.groupby(['compartment']).max().reset_index() #ori
      for j in range(0,num_compartments):
         comp = dfmaxcomp['compartment'][j]
         dfcomp = df.loc[df['compartment'] == comp]
                
#       print('num_daily tests in ',comp,' =', num_tests_performed[i])

         if expert_mode:
            print('total population in compartment',comp,p['init_pop'][j])
            print('total tested for triage in compartment',comp,'=',dfsumcomp['newtested_mit'][j])
            print('total tested for diagnosis and care in compartment',comp,'=',dfsumcomp['actualdxtests'][j])
            print('total_deaths in ',comp,'=', dfsumcomp['newdeaths'][j])
            print('max_infections in ',comp,'=',dfmaxcomp['infected'][j])
            print('total_infections in ',comp,'=',dfsumcomp['newinfected'][j])
            print('max in isolation in ',comp,'=',dfmaxcomp['isolated'][j])
    
      #      plot_results(scenario_name,comp,int(num_tests_performed[j]),dfcomp['days'],dfcomp['isolated'],dfcomp['infected'],dfcomp['tested'],dfcomp['infectednotisolated'],dfcomp['total_confirmed'],dfcomp['total_deaths'],dfcomp['susceptibles'])
            plot_results(scenario_name,comp,int(num_tests_performed[j]),dfcomp['dates'],dfcomp['isolated'],dfcomp['infected'],dfcomp['tested_mit'],dfcomp['infectednotisolated'],dfcomp['confirmed'],dfcomp['deaths'],dfcomp['susceptibles'],dfcomp['prevalence'])
             
      if expert_mode:
#         print('prev before ALL plot=',dfsum['prevalence'])
         plot_results(scenario_name,'ALL',dfsumcomp['newtested_mit'],dfsum['dates'],dfsum['isolated'],dfsum['infected'],dfsum['tested_mit'],dfsum['infectednotisolated'],dfsum['confirmed'],dfsum['deaths'],dfsum['susceptibles'],dfsum['prevalence'],country_df['accumulated_deaths'],)
         print('************')

      total_tests_mit_by_scenario[i]=dfsumcomp['newtested_mit'].sum()
      total_tests_care_by_scenario[i]=dfsumcomp['actualdxtests'].sum()
      total_deaths_by_scenario[i]=dfsumcomp['newdeaths'].sum()
      max_infected_by_scenario[i]=dfsum['infected'].max()
      total_infected_by_scenario[i]=dfsum['newinfected'].sum()
      max_isolated_by_scenario[i]=dfsum['isolated'].max()

      if expert_mode:
         print('Total tested for mitigation =',total_tests_mit_by_scenario[i])
         print('Total tested for care =',total_tests_care_by_scenario[i])
         print('Max infected=',max_infected_by_scenario[i])
         print('Total infected by scenario=',total_infected_by_scenario[i]),
         print('Max isolated=',max_isolated_by_scenario[i])
         print('Total deaths=',total_deaths_by_scenario[i])
         prevalence=dfsum.iloc[par.num_days-1]['prevalence']
         print('************')
         print('Tests required for seroprevalence study 95% confidence, max 1% error')
         print('For national study sum requirements for all subpopulations of interest')
         print('************')
         print('Max subgroups 5:', sim.compute_sample_size(par,5,prevalence,1.96,0.01))
         print('Max subgroups 10:', sim.compute_sample_size(par,10,prevalence,1.96,0.01))
         print('Max subgroups 100:',sim.compute_sample_size(par,100,prevalence,1.96,0.01))
         print('Max subgroups 1000:',sim.compute_sample_size(par,1000,prevalence,1.96,0.01))
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
         print('Scenario ',i,' Care: ',total_tests_care_by_scenario[i])
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
   'total_deaths_by_scenario':total_deaths_by_scenario,\
   'max_infected_by_scenario':max_infected_by_scenario,\
   'total_infected_by_scenario':total_infected_by_scenario,\
   'max_isolated_by_scenario':max_isolated_by_scenario})
      
#      p=original_p
   return(dataframes, test_df,results_dict)

######################################################################
# Par class:
#   encapsulates model parameters for covid simulation
######################################################################

class Par:

   def __init__(self,params):
      self.num_compartments = int(params['num_compartments'])
      self.num_days = int(params['num_days'])
# =============================================================================
#       self.inversion_date = int(params['inversion_date'][0])
#       self.beta_pre_inversion = float(params['beta_pre_inversion'][0])
#       self.beta_min=float(params['beta_min'][0])
#       self.beta_max=float(params['beta_max'][0])
# =============================================================================
      self.total_pop=int(params['total_pop'])
      self.beta_adaptation_days = float(params['beta_adaptation_days']) #this is number of days beta takes to shift from initial to final beta
      self.latency_period =  int(params['latency_period'])
      self.incubation_period =  int(params['incubation_period'])
      # self.infection_fatality_rate=float(params['infection_fatality_rate'][0])
      self.infection_fatality_rate=float(params['IFR_corrected'])
      self.recovery_period = int(params['recovery_period'] )
      self.death_period = int(params['death_period'])
      self.prop_asymptomatic=float(params['prop_asymptomatic'])
      self.tau = self.infection_fatality_rate/self.recovery_period
      self.gamma = (1-self.infection_fatality_rate)/self.recovery_period
      self.num_testkit_types=int(params['num_testkit_types'])
      self.num_tests_mitigation=params['num_tests_mitigation']
      self.num_tests_care=params['num_tests_care']
      self.sensitivity=params['sensitivity']
      self.specificity=params['specificity']
      self.test_symptomatic_only=[]
      self.design_effect=float(params['design_effect'])
      self.confirmation_tests=[]
      for i in range(0,len(params['symptomatic_only'])):
          self.test_symptomatic_only.append(params['symptomatic_only'][i].upper() == 'TRUE') 
      for i in range(0,len(params['confirmation_tests'])):
          self.confirmation_tests.append(params['confirmation_tests'][i].upper() == 'TRUE') 
   #   self.no_testing=params['no_testing'][0].upper()=='TRUE'  #used to switch off testing in scenario 0
      self.p_positive_if_symptomatic = float(params['p_positive_if_symptomatic'])
      self.background_rate_symptomatic=float(params['background_rate_symptomatic'])
      self.severity=params['severity']
      self.trig_values=params['trig_values']
      self.trig_def_type=params['trig_def_type']
      self.trig_op_type=params['trig_op_type']
      self.max_contacts_per_case=float(params['max_contacts_per_case'])
      self.min_contacts_per_case=float(params['min_contacts_per_case'])
      self.prop_contacts_traced=params['prop_contacts_traced']
      self.test_multipliers=params['test_multipliers']
      self.requireddxtests=params['requireddxtests']
      self.imported_infections_per_day=params['imported_infections_per_day']
      num_compartments = self.num_compartments
      num_testkit_types = self.num_testkit_types
      self.compartment = []
      #If the variables were lists we would not need to initialize them all
      self.init_pop = np.zeros(num_compartments)
      self.init_infected = np.zeros(num_compartments)
      self.prop_tests = np.zeros(num_compartments)
   #   self.num_tests=np.zeros(num_compartments)
      self.num_tests_mit=list(map(int,params['num_tests_mitigation']))
      self.num_tests_care=list(map(int,params['num_tests_care']))
      self.num_tests=[self.num_tests_mit,self.num_tests_care]
  #    print ('num_tests=',self.num_tests)
 
      #if we wrote these variables as lists we could copy them without the loops
      
      self.prop_tests=[params['prop_hospital'],params['prop_other_hc']]
      prop_rop=[]
      for i in range(0,len(params['prop_hospital'])):
         value=1-(float(self.prop_tests[0][i])+float(self.prop_tests[1][i]))
         prop_rop.append(value)
      self.prop_tests.append(prop_rop)
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


      self.total_testkits = np.zeros(len(self.num_tests))
      self.total_testkits=np.asarray(self.num_tests).sum(axis=0)
      self.day1=dt.datetime.now()
      print('total_testkits',self.total_testkits)
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
      self.require_dx_tests = np.zeros((num_days,num_compartments))
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

      # number of infected generated by compartment i in compartment j
      self.compart_newinfected=np.zeros((num_days,num_compartments,num_compartments))

      self.total_deaths=np.zeros(num_compartments)
      self.maxinfected=np.zeros(num_compartments)
      self.maxisolated=np.zeros(num_compartments)
      self.totalisolated=np.zeros(num_compartments)
      
      

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
      # tested, deaths, recovered: total and new are zero (default)
   #      print('BEFORE SIMULATION')
      #   print('compartment=',i,'population',sim.population[0,i], 'init_infected',par.init_infected[i],
       #   'susceptibles',sim.susceptibles[0,i],'infected',sim.infected[0,i],
   #       'infected non isolated',sim.infectednotisolated[0,i])

   # infect compartments at time t using the given beta matrix
   def cross_infect(sim,par:Par,beta,t):
      # add up number of new infected for each compartment - total correct at end of loops
      for i in range(0, par.num_compartments): #this is the compartment doing the infecting
         for j in range(0, par.num_compartments):      
            #This computes how many infections compart i will cause in compartment j
#            sim.compart_newinfected[t,i,j] = sim.infectednotisolated[t-1,i]*beta[i,j]*sim.susceptibleprop[t-1,j]
            sim.compart_newinfected[t,i,j] = sim.infectednotisolated[t-1-(par.incubation_period-par.latency_period),i]*beta[i,j]*sim.susceptibleprop[t-1-(par.incubation_period-par.latency_period),j]
                #this records how many new infections compart i will cause in compart j 
# =============================================================================
#             if i==1 and j==1:
#                print ('i=',i,'j=',j,'compart_new_infected', sim.compart_newinfected[t,i,j],
#                           'infected not isolated=',sim.infectednotisolated[t-1,i],
#                           'beta=',beta[i,j],'suscept_prop',sim.susceptibleprop[t-1,j],
#                           'suscept=',sim.susceptibles[t-1,j])
# =============================================================================

   # add up infections per compartment at time t (can combine code here with with cross_infect at some point)
   def addup_infections(sim,par:Par,t):
      for i in range(0,par.num_compartments):
         sim.newinfected[t,i]=0
         for j in range(0,par.num_compartments):
            sim.newinfected[t,i]=sim.newinfected[t,i]+sim.compart_newinfected[t,j,i]
         if sim.newinfected[t,i]>sim.susceptibles[t-1,i]:#This should be part of i loop - may not be necessary
            sim.newinfected[t,i]=sim.susceptibles[t-1,i]
   #      calc_beta=sim.newinfected[t,i]/sim.infectednotisolated[t-1,i]
  #       print('compartment=',i,'calc_beta=',calc_beta)
              # print ('cutting new infections')

   # perform tests for compartment i at time t; return true positives, false positives, and number of tests performed
   
   # add in a user-determined, phase-specific number of exogeneous infections per day
   def add_imported(sim,par:Par, t,phase):
       prop_infections_in_compart=np.zeros(par.num_compartments)
       if np.sum(sim.newinfected[t])>0:
            prop_infections_in_compart=sim.newinfected[t]/np.sum(sim.newinfected[t])
       else:
  #          prop_infections_in_compart=np.array([0.333,0.333,0.333]) #should be num compartments
            prop_infections_in_compart.fill(1.0/par.num_compartments)
       imported_infections=prop_infections_in_compart*par.imported_infections_per_day[phase]
       sim.newinfected[t]=sim.newinfected[t]+imported_infections
       
   #Computes the sample size required for a national wide seroprevalence survey in which max
   # n. of groups for stratified analysis is given by n_groups
   # assumes a design effect (multiplier to compensate for clustering) specified in system parameters
   def compute_sample_size(sim,par,n_groups,prev,z,error):
       group_size=par.total_pop/n_groups
       upper=(z**2*prev*(1-prev))/(error**2)
       lower=1+(z**2*prev*(1-prev)/(error**2*group_size))
       sample_size=(upper/lower)*par.design_effect*n_groups
       return(sample_size)
        
    
   def perform_tests(sim,par:Par,i,t,phase):
      truepositives=0
      falsepositives=0
      truenegatives=0
      falsenegatives=0
    #  print('In perform tests')
      accum_tests_performed=0
      tests_available=par.prop_tests[i][phase]*par.num_tests_mit[phase]  
# =============================================================================
#       if par.confirmation_tests[phase]:
#           tests_available=tests_available-sim.newisolated[t-1,i] #we do a confirmation tests for everyone isolated in previous period
# =============================================================================
  #        print ('compartment=',i,' test_type=',k,'prop_tests=', par.prop_tests[i][phase],'num_tests=',par.num_tests[k][phase],'tests_available=',tests_available)
      if tests_available>0:
# =============================================================================
#              true_positive_rate=par.sensitivity[k] #misleading
#              false_positive_rate=1-par.specificity[k] #misleading
# =============================================================================
         if sim.population[t-1,i] >= tests_available:
            tests_performed = tests_available
         else:
            tests_performed = sim.population[t-1,i] 
         if par.test_symptomatic_only[phase]: 
#            print('In sysmptomatic only')
            if (t)>par.incubation_period:  ## JPV: change to (t+1) to t when richard gives go ahead
               total_symptomatic=sim.population[t-1-par.incubation_period,i]*par.background_rate_symptomatic+(1-par.prop_asymptomatic)*sim.infectednotisolated[(t-1)-par.incubation_period,i]
            else:
               total_symptomatic=sim.population[t-1,i]*par.background_rate_symptomatic
            
            if par.total_testkits[phase]>0:
                total_symptomatic_for_test=total_symptomatic*par.num_tests_mit[phase]/par.total_testkits[phase]
            else:
                total_symptomatic_for_test=0
            if total_symptomatic_for_test<tests_available:
               tests_performed=total_symptomatic_for_test
#                   print ('compartment',i,'prop testsi',par.prop_tests[i],'testkit type=',k,'available=', tests_available,'symptomatic',total_symptomatic,'tested=',tests_performed)
            if total_symptomatic>0:
               p_positive_if_symptomatic=sim.infectednotisolated[t-1-par.incubation_period,i]*par.background_rate_symptomatic/total_symptomatic
           #    print('p_positive if symptomatic=',p_positive_if_symptomatic)
            else:
               p_positive_if_symptomatic=0
            truepositives = truepositives+tests_performed * p_positive_if_symptomatic * par.sensitivity[phase]
  #          print('p positive if symptomatic=',p_positive_if_symptomatic )
            falsepositives = falsepositives+tests_performed * (1-p_positive_if_symptomatic) * (1-par.specificity[phase])
        
         else: #also testing non-symptomatic
#            print ('testing all')
            if sim.population[t-1,i]>0:
                truepositives = truepositives+tests_performed * sim.infectednotisolated[t-1-par.incubation_period,i]/sim.population[t-1,i] * par.sensitivity[phase]
                if truepositives>sim.infectednotisolated[t-1-par.incubation_period,i]:
                   truepositives=sim.infectednotisolated[t-1-par.incubation_period,i]
                falsepositives=falsepositives+tests_performed * sim.infectednotisolated[t-1-par.incubation_period,i]/sim.population[t-1,i] * (1-par.selectivity[phase])
            else:
                truepositives=0
                falsepositives=0
         truenegatives=truenegatives+(falsepositives*par.specificity[phase])/(1-par.specificity[phase])
         falsenegatives=tests_performed-(truepositives+falsepositives+truenegatives)
         sim.truepositives[t,i]=truepositives
         sim.falsepositives[t,i]=falsepositives
         sim.truenegatives[t,i]=truenegatives
         sim.falsenegatives[t,i]=falsenegatives
         sim.ppv[t,i]=truepositives/(truepositives+falsepositives)
         sim.npv[t,i]=truenegatives/(truenegatives+falsenegatives)
         accum_tests_performed=accum_tests_performed+tests_performed
 #            print('tests=',tests_performed, 'tp=',truepositives,'fp=',falsepositives,'tn=', truenegatives, 'fn=',falsenegatives )
# print('truepositives=', truepositives,'false positives=', falsepositives,'new tested',sim.newtested[t,i],'infected not isolated',sim.infectednotisolated[t,i],'true positive rate', true_positive_rate,'false positive rate',false_positive_rate)
      return (truepositives,falsepositives,accum_tests_performed)
   
   def trigger_next_phase(sim,params,t,phase):
       #This function returns true if t meets the criteria previous defined to trigger next phase
       
       if params.trig_def_type[phase]=='date': 
           value=t
       else:
           if params.trig_def_type[phase]=='cases':
               value=np.sum(sim.newconfirmed[t-1,:])
     #          print('t=',t,'phase=',phase,'cases as trigger value=',value)
           else:
               if params.trig_def_type[phase]=='deaths':
                   value=np.sum(sim.newdeaths[t-1,:])
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
                       return(True)
       return(False)

               
                   
            

   def get_data_frame(self,num_days,num_compartments,compartment):
      df = pd.DataFrame({
          'days': range(0,num_days),
          'dates':self.dates[:],
          'day1':range(0,num_days),
          'compartment': np.full(num_days,compartment[0]),
          'population' : np.round(self.population[:,0],1),
          'susceptibles' : np.round(self.susceptibles[:,0],1),
          'isolated': np.round(self.isolated[:,0],1),
          'infected': np.round(self.infected[:,0],1),
          'accumulatedinfected': np.round(self.accumulatedinfected[:,0],1),
          'tested_mit': np.round(self.tested_mit[:,0],1),
          'infectednotisolated': np.round(self.infectednotisolated[:,0],1),
          'confirmed': np.round(self.confirmed[:,0],1),
          'deaths': np.round(self.deaths[:,0],1),
          'recovered': np.round(self.recovered[:,0],1),
          'beta': np.round(self.beta_arr[:,0],5),
          'susceptibleprop' : np.round(self.susceptibleprop[:,0],1),
          'newtested_mit': np.round(self.newtested_mit[:,0],1),
          'newinfected': np.round(self.newinfected[:,0],1),
          'newisolated': np.round(self.newisolated[:,0],1),
          'newisolatedinfected': np.round(self.newisolatedinfected[:,0],1),
          'newconfirmed': np.round(self.newconfirmed[:,0],1),
          'newrecovered': np.round(self.newrecovered[:,0],1),
          'requireddxtests': np.round(self.requireddxtests[:,0],1),
          'actualdxtests': np.round(self.actualdxtests[:,0],1),
          'newdeaths': np.round(self.newdeaths[:,0],1),
          'truepositives':np.round(self.truepositives[:,0],1),
          'falsepositives':np.round(self.falsepositives[:,0],1),
          'truenegatives':np.round(self.truenegatives[:,0],1),
          'falsenegatives':np.round(self.falsenegatives[:,0],1),
          'ppv':np.round(self.ppv[:,0],3),
          'npv':np.round(self.npv[:,0],3),
          'incidence':np.round(self.incidence[:,0],3),
          'prevalence':np.round(self.prevalence[:,0],3)
         })
      for i in range(1,num_compartments):
         dfadd = pd.DataFrame({
            'days': range(0,num_days),
            'dates': self.dates[:],
            'day1':range(0,num_days),
            'compartment': np.full(num_days,compartment[i]),
            'population' : np.round(self.population[:,i],1),
            'susceptibles' : np.round(self.susceptibles[:,i],1),
            'isolated': np.round(self.isolated[:,i],1),
            'infected': np.round(self.infected[:,i],5),
            'accumulatedinfected': np.round(self.accumulatedinfected[:,i],1),
            'tested_mit': np.round(self.tested_mit[:,i],1),
            'infectednotisolated': np.round(self.infectednotisolated[:,i],1),
            'confirmed': np.round(self.confirmed[:,i],1),
            'deaths': np.round(self.deaths[:,i],1),
            'recovered': np.round(self.recovered[:,i],1),
            'beta': np.round(self.beta_arr[:,i],5),
            'susceptibleprop' : np.round(self.susceptibleprop[:,i],1),
            'newtested_mit': np.round(self.newtested_mit[:,i],1),
            'newinfected': np.round(self.newinfected[:,i],5),
            'newisolated': np.round(self.newisolated[:,i],1),
            'newisolatedinfected': np.round(self.newisolatedinfected[:,i],1),
            'newconfirmed': np.round(self.newconfirmed[:,i],1),
            'newrecovered': np.round(self.newrecovered[:,i],1),
            'requireddxtests': np.round(self.requireddxtests[:,i],1),
            'actualdxtests': np.round(self.actualdxtests[:,0],1),
            'newdeaths': np.round(self.newdeaths[:,i],1),
            'truepositives':np.round(self.truepositives[:,i],1),
            'falsepositives':np.round(self.falsepositives[:,i],1),
            'truenegatives':np.round(self.truenegatives[:,i],1),
            'falsenegatives':np.round(self.falsenegatives[:,i],1),
            'ppv':np.round(self.ppv[:,i],3),
            'npv':np.round(self.npv[:,i],3),
            'incidence':np.round(self.incidence[:,i],3),
            'prevalence':np.round(self.prevalence[:,i],3)
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

def adjust_beta(beta,final_beta,alpha):
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
    return(beta)
   
######################################################################
# simulate:
#    takes in system parameters, initial beta matrix, final beta matrix
#    and performs SIR simulation with compartments
#
#    returns:
#        results a dataframe containing simulation results
######################################################################


    
def simulate(country_df,sim, par, max_betas, min_betas,start_day=1, end_day=200,phase=0):
# =============================================================================
#     par = Par(params)
#     num_compartments = par.num_compartments
#     num_testkit_types = par.num_testkit_types
#     num_days = par.num_days
#     num_phases=len(par.severity)-1
#  #   betas = max_betas.copy()
#  #   print('trig values)',params['trig_values'])
# # =============================================================================
# #     if par.intervention_type==0:
# #         # if there is no intervention beta will never go down
# #         alpha=beta*0
# #     else:
# #         # alpha=beta/alpha_post_inversion
# #         #alpha post inversion is now actually a multiplier. Name is wrong. 
# #         alpha=(beta-final_beta)/par.alpha_post_inversion
# #         #all betas should go down at same speed.
# # =============================================================================
# 
#     sim = Sim(num_days,num_compartments)
#     sim.set_initial_conditions(par)
# =============================================================================
    
    
    num_phases=len(par.severity)-1
 #   num_compartments = par.num_compartments
#    num_testkit_types = par.num_testkit_types
    pops_for_beta=par.init_infected  #temp instruction]
    #fix starting condition
    initial_betas=generate_betas(min_betas,max_betas,par.severity[phase])  #beta_min,beta_max, min_betas,max_betas, target,pops
#    phase_duration=par.trig_values[phase+1]-par.trig_values[phase]
#    beta_overall=par.severity[phase]
    betas = initial_betas.copy() #this is current value of beta matrix
  #  final_betas=generate_betas(min_betas,max_betas,par.severity[phase+1])
    final_betas=initial_betas
    alpha=(final_betas-initial_betas)/par.beta_adaptation_days
    sim.dates=[par.day1 + dt.timedelta(days=x) for x in range(0,par.num_days)]
#    alpha_overall=(par.severity[phase+1]-par.severity[phase])/phase_duration
    for t in range(start_day,end_day):
       if phase+1<=num_phases:
           if sim.trigger_next_phase(par,t,phase+1): 
               phase=phase+1
               for i in range(0,par.num_compartments):
                   pops_for_beta[i]=sim.infectednotisolated[t-1,i] #maybe could make this a slice
       #        initial_betas=generate_betas(min_betas,max_betas,par.severity[phase])  #beta_min,beta_max, min_betas,max_betas, target,pops
       #        betas = initial_betas.copy() #this is current value of beta matrix
       #        beta_overall=par.severity[phase]
        #       phase_duration=par.trig_values[phase+1]-par.trig_values[phase]
               initial_betas=betas
               if phase<num_phases+1:
                   final_betas=generate_betas(min_betas,max_betas,par.severity[phase])
                   alpha=(final_betas-initial_betas)/par.beta_adaptation_days
        #           alpha_overall=(par.severity[phase+1]-par.severity[phase])/phase_duration
               else:  #this feels a little contorted
                   final_betas=initial_betas
                   alpha=(final_betas-initial_betas)/par.beta_adaptation_days
   #            alpha_overall=(par.severity[phase+1]-par.severity[phase])/phase_duration
       sim.days[t]=t
  #     print('t=',t,'phase=',phase,'beta_overall=',beta_overall)
       sim.cross_infect(par,betas,t)
       sim.addup_infections(par,t)
       sim.add_imported(par,t,phase)
       # works out number of contacts per person. Maximum when target beta=max beta
 #      print('max contacts per case=', par.max_contacts_per_case,'prop contacts traced',par.prop_contacts_traced[phase])
 #      print('beta overall',beta_overall,)
       contacts_per_person=par.max_contacts_per_case*(1-par.severity[phase])+par.min_contacts_per_case*par.severity[phase]
       contacts_per_person_isolated=contacts_per_person*par.prop_contacts_traced[phase]
 #      print('t=',t,'contacts per person isolated=',contacts_per_person_isolated)
       for i in range(0,par.num_compartments):
           #perform mitigation testing
           (truepositives,falsepositives,accum_tests_performed) = sim.perform_tests(par,i,t,phase)  
           
           # compute "dailies"
           # note: sim.newinfected[t,i] updated in addup_infections call
           sim.newtested_mit[t,i]=accum_tests_performed
   #        print('true pos',truepositives,'false pos',falsepositives, 'contacts_per_person',contacts_per_person_isolated)
           sim.newisolated[t,i] = (truepositives+falsepositives) *(1+contacts_per_person_isolated)  #We isolate all people who are infected plus a certain proportion of their contacts
           sim.newisolatedinfected[t,i] = truepositives #this does not yet take account of contacts
           sim.newconfirmed[t,i] = sim.newisolated[t,i]
           if t-1-par.incubation_period>=0:
               sim.newrecovered[t,i] = sim.infected[t-1-par.recovery_period,i]*par.gamma  
       #        sim.newrecovered[t,i] = sim.infected[t-1,i]*par.gamma  
               sim.newdeaths[t,i] = sim.infected[t-1-par.death_period,i]*par.tau #needs testng
           else:
               sim.newrecovered[t,i]=0
               sim.newdeaths[t,i]=0
           sim.requireddxtests[t,i]=sim.newrecovered[t,i]*par.requireddxtests[phase] 
           if sim.requireddxtests[t,i]>par.num_tests_care[phase]:
               sim.actualdxtests[t,i]=par.num_tests_care[phase]
           else:
               sim.actualdxtests[t,i]=sim.requireddxtests[t,i]
   #            print('new infected=', sim.newinfected[t,i],',new recovered=',sim.newrecovered[t,i],',new deaths=',sim.newdeaths[t,i])
           # update totals
   
           sim.tested_mit[t,i] = sim.tested_mit[t-1,i] + sim.newtested_mit[t,i]
           sim.isolated[t,i] = sim.isolated[t-1,i] + sim.newisolated[t,i] - sim.isolated[t-1,i]*par.gamma-sim.isolated[t-1,i]*par.tau
           sim.isolatedinfected[t,i] = sim.isolatedinfected[t-1,i] + sim.newisolatedinfected[t,i] - sim.isolatedinfected[t-1,i]*par.gamma-sim.isolatedinfected[t-1,i]*par.tau
   
           sim.deaths[t,i] = sim.deaths[t-1,i]+sim.newdeaths[t,i]
           sim.recovered[t,i] = sim.recovered[t-1,i]+sim.newrecovered[t,i]
           sim.infected[t,i] = sim.infected[t-1,i]+sim.newinfected[t,i]-sim.newrecovered[t,i]-sim.newdeaths[t,i]
           if sim.infected[t,i]<0.0:
              sim.infected[t,i]=0.0
           if sim.infected[t,i]>0:
               sim.reff[t,i]=sim.newinfected[t,i]/sim.infected[t,i]*par.recovery_period
           else:
               sim.reff[t,i]=np.nan
           sim.accumulatedinfected[t,i]=sim.accumulatedinfected[t-1,i]+sim.newinfected[t,i]
           sim.population[t,i] = sim.population[t-1,i]-sim.newdeaths[t,i]
   
           sim.susceptibles[t,i]=sim.population[t,i]-sim.infected[t,i]-sim.recovered[t,i] #deaths have already been subtracted from pop
   
           if sim.susceptibles[t,i]<0:  #defensive programming - I don't know why they go negative but they do
               sim.susceptibles[t,i]=0 
   
           if sim.population[t,i]>0:
              sim.susceptibleprop[t,i] = sim.susceptibles[t,i]/sim.population[t,i] #another accounting identity
           else:
              sim.susceptibleprop[t,i]=0 #avoids a divide by zero error with zero pop in one compartment
   
           sim.confirmed[t,i]=sim.confirmed[t-1,i] + sim.newconfirmed[t,i]
   
           if sim.infected[t,i] - sim.isolated[t,i] > 0.0:
              sim.infectednotisolated[t,i] = sim.infected[t,i] - (sim.isolated[t,i]) #accounting identity 
           else:
              sim.infectednotisolated[t,i] = 0.0
           sim.incidence[t,i]=sim.newinfected[t,i]/sim.population[t,i]
           sim.prevalence[t,i]=sim.accumulatedinfected[t,i]/sim.population[t,i]
  #         print('t=',t, 'acc_i=',sim.accumulatedinfected[t,i],'pop=',sim.population[t,i], 'prev=',sim.prevalence[t,i])
  #     r=sim.compute_r(par,t)
 #      print('t=',t,'r=',r)
       betas=adjust_beta(betas,final_betas,alpha)
  #     print('t=',t,'betas=',betas)# apply deceleration on beta - for next period
  #     beta_overall=beta_overall+alpha_overall
       
           
  #         print('t=',t,'phase=',phase)       
            
      #  sim,params,t,phase
  
     
 # =============================================================================
    df = sim.get_data_frame(par.num_days,par.num_compartments,par.compartment)
    return sim,df
 
######################################################################
# plot_results:
#     present plots based on scenario parameters passed
######################################################################

def plot_results(scenario_name,compartment,num_tests, dates,newisolated,newinfected,newtested,infected_not_isolated,confirmed,deaths,susceptibles,prevalence,actual_deaths=[]):
     
 #    print('prevalence going into plot=',prevalence)
     fig = plt.figure()
    # ax = fig.add_subplot(111)
    # width=0.8
    #  ax.set_title(title)
    # plt.plot(days,newisolated,color='b', label="newisolated")
     plt.plot (dates, newinfected,color='r',label="newinfected")
    # plt.plot (days, confirmed,color='g',label="Confirmed cases")
    # plt.plot (days, infected_not_isolated,color='y',label="Infected_not_isolated")
    # plt.plot (days, deaths,color='k',label="Deaths")
    # plt.gca().set_ylim(0, 0.40)
     plt.title(scenario_name+': '+compartment+' - Infected')
     plt.ylabel('Number')
     plt.xlabel('Date')
     plt.legend(title= "Legend")
     plt.show()
     plt.close()
     plt.plot (dates, deaths,color='k',label="Simulated Deaths")
    
     if len(actual_deaths)>0:
        print('len simulated=',len(deaths),'len actual=',len(actual_deaths))
        padding=np.zeros(len(deaths)-len(actual_deaths))
        actual_deaths=np.concatenate((np.array(actual_deaths),padding))
        plt.plot(dates,actual_deaths,color='g', label='Actual deaths')
     plt.title(scenario_name+': '+compartment+' - Deaths')
     plt.ylabel('Number')
     plt.xlabel('Date')
     plt.legend(title= "Legend")
     plt.show()
     plt.close()
     plt.plot(dates,newisolated,color='b', label="newisolated")
     plt.title(scenario_name+': '+compartment+' - Isolated')
     plt.ylabel('Number')
     plt.xlabel('Date')
     plt.legend(title= "Legend")
     plt.show()
     plt.close()
     plt.plot(dates,susceptibles,color='c', label="Susceptibles")
     plt.title(scenario_name+': '+compartment+' - Susceptibles')
     plt.ylabel('Number')
     plt.xlabel('Date')
     plt.legend(title= "Legend")
     plt.show()
     plt.plot(dates,prevalence,color='r', label="Prevalence")
     plt.title(scenario_name+': '+compartment+' - Prevalence')
     plt.ylabel('Prevalence')
     plt.xlabel('Date')
     plt.legend(title= "Legend")
     plt.show()
     plt.close()
     
######################################################################
# calibrate_beta:
#    normalizes beta matrix based on an aggregate beta target
#    returns:
#       calibrated beta matrix
######################################################################

def calibratebeta(n,beta,pops,targetbeta):
    b = aggregatebeta(n,beta,pops)
    adjust=targetbeta/b
    beta=beta*adjust
    new_b=aggregatebeta(n,beta,pops)
    return beta

######################################################################
# aggregate_beta:
#    computes aggregate beta given initial beta matrix & compartment populations
#    returns:
#       aggregate beta (scalar)
######################################################################

def aggregatebeta(n,betas,pops):
  # print('pops=',pops)
   total = 0
   P = np.sum(pops)
#   print('betas=',betas)
   for j in range(n):
     col_sum = 0
     for i in range(0,n):
 #       print('i=',i,'j=',j)
        col_sum = col_sum + betas[i][j]
     total = total + col_sum*pops[j]
   aggb = total/P
   return aggb

######################################################################
# generate_betas:
#    generates a beta matrix whwere the  average
#    of the betas, weighted by infected_not_isolated
#    is equal to target. 
######################################################################


def generate_betas(min_betas,max_betas, severity):
    #target is now expressed on a scale of 0 to 1
# =============================================================================
#     severity=(beta_max-target)/(beta_max-beta_min)
#     if severity<0:  #this can happen if target severity outside allowed range
#         severity=0
#     if severity>1: #this can happen if target severity outside allowed range
#         severity=1#generates a severity score from 0 to 1 (no intervention to lockdown)
# =============================================================================
 #   print ('severity=',severity)
    new_betas=severity*min_betas+(1-severity)*max_betas #generates a new beta matrix with values lying between min_betas and max_betas
# =============================================================================
#     agg=aggregatebeta(len(max_betas), severity_betas, pops)
#     adjust=target/agg
#     new_betas=severity_betas*adjust
#     agg=aggregatebeta(len(max_betas), new_betas, pops)
# =============================================================================
    return(new_betas)

# =============================================================================
# def simulatedeaths(fixed_params):
#    sysfile = 'system_params.csv'
#    initial_betafile = 'initial_betas.csv'
#    final_betafile = initial_betafile
#    p = get_system_params(sysfile)
#    update_system_params(p, fixed_params)
#    num_compartments = int(p['num_compartments'][0])
#    initial_beta = get_beta(initial_betafile, num_compartments)
#    final_beta = get_beta(final_betafile, num_compartments)
#    df = simulate(p,initial_beta,final_beta)
#    dfsum = df.groupby(['days']).sum().reset_index()
#    return dfsum
# =============================================================================

def getcountrydata(csvfilename):
   df = pd.read_csv(csvfilename)
   return df.fillna(0)

def aligndeaths(actual,simulated):
   n = len(actual)
   #defensive: deals with case of simulated less than actual - this should not happen
   if len(simulated)<len(actual):
       padding=np.zeros(len(actual)-len(simulated))
       simulated=np.concatenate((np.array(simulated),padding))
   aligneddeaths = [0]*n
   amark = 0
   for i in range(0,n-1):
      if actual[i] >= 20:
         amark = i
         break
   smark = 0
   for i in range(0,n-1):
      if simulated[i] >= 20:
         smark = i
         break
   for i in range(0,n-1):
      if (i < (amark-smark)):
         aligneddeaths[i] = 0
      else:
         aligneddeaths[i] = simulated[i-(amark-smark)]
   return aligneddeaths, amark-smark

def alignactualwithsimulated(dfactual,dfsimdeaths):
   simdeaths = dfsimdeaths.tolist()
   print('sim_deaths=', simdeaths)
   actdeaths = dfactual['accumulated_deaths'].tolist()
   print('act_deaths=',actdeaths)
   aligneddeaths, shift = aligndeaths(actdeaths,simdeaths)
   print('shift=',shift)
   dfactual['Sim'] = aligneddeaths
   day1_literal=dfactual.iloc[shift]['Date']
   print('day1_literal=',day1_literal)
   day1 = dt.datetime.strptime(dfactual.iloc[shift]['Date'],"%Y-%m-%d")
   return dfactual, day1


def computecurrentphase(start_date,triggers):
    today=dt.datetime.now()
    simday=(today-start_date).days
    simphase=0
    for i in range(0,len(triggers)):
        if triggers[i]<simday:
            simphase=i
    return simphase
        
    
    



