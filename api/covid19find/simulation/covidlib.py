
# contains function definitions for covid simulation
# author:  JP Vergara

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys

def get_system_params(sysfile):
         
         p = {}

         sysp = pd.read_csv(sysfile,header=None)
         (rows,cols) = sysp.shape
         nonblanks = 1
         for i in range(0,rows):
            param_name = sysp.iloc[i,0]
            if param_name == 'num_compartments':
               num_compartments = int(sysp.iloc[i,1])
               nonblanks = num_compartments
            if param_name == 'num_testkit_types':
               num_testkit_types = int(sysp.iloc[i,1])
               nonblanks = num_testkit_types
            p[param_name] = []
            countnonblanks = 0
            for j in range(1,cols):
               val = sysp.iloc[i,j]
               p[param_name].append(val)
               if not pd.isnull(val):
                  countnonblanks = countnonblanks+1
            if (param_name != 'num_compartments') and (param_name != 'num_testkit_types') and countnonblanks != nonblanks:
               print("Warning: variable ",param_name," does not have enough values")

         return p

def get_beta(betafile, n, pops, targetbeta):
         beta_table = pd.read_csv(betafile,header=None)
         (rows,cols) = beta_table.shape
         beta = np.zeros((n,n))
         for i in range(1,n+1):
            for j in range(1,n+1):
               beta[i-1,j-1] = beta_table.iloc[i,j]
         result = calibratebeta(n, beta, pops, targetbeta)
         return result

def run_simulation(fixed_params, **kwargs):

         sysfile = 'system_params.csv'
         initial_betafile = 'initial_betas.csv'
         final_betafile = 'final_betas.csv'
         scenariosfile='scenarios.csv'
         if len(kwargs)>0:
             scenarios=kwargs['scenarios']
         else:
             scenarios=[]
         p = get_system_params(sysfile)
         num_compartments = int(p['num_compartments'][0])
         num_testkit_types=int(p['num_testkit_types'][0])
         
#     These are defined in compartment parameters - no need to define here:
#     p['compartment']=['Hospitals','Other high contact ','Rest of population']
#     p['init_infected']=[100,100,100]

         p['testkits']=['PCR','RDT','Chest xrays']
         p['sensitivity'][0]=fixed_params['sensitivity_PCR']
         p['sensitivity'][1]=fixed_params['sensitivity_RDT']
         p['sensitivity'][2]=fixed_params['sensitivity_xray']
         p['specificity'][0]=fixed_params['specificity_PCR']
         p['specificity'][1]=fixed_params['specificity_RDT']
         p['specificity'][2]=fixed_params['specificity_xray']
         p['num_tests'][0]=fixed_params['num_tests_PCR']
         p['num_tests'][1]=fixed_params['num_tests_RDT']
         p['num_tests'][2]=fixed_params['num_tests_xray']
 #        p['test_symptomatic_only']=['true','true','true']
         
         #define size of compartments   
         hosp_staff=fixed_params['hospital_beds']*fixed_params['staff_per_bed']
         high_risk_urban=fixed_params['total_pop']*fixed_params['prop_urban']*fixed_params['prop_below_pl']
         other_high_contact=fixed_params['total_pop']*fixed_params['prop_15_64']*fixed_params['prop_woh']
         p['init_pop'][0]=fixed_params['hospital_beds']*fixed_params['staff_per_bed']
         p['init_pop'][1]=high_risk_urban+other_high_contact
         p['init_pop'][2]=fixed_params['total_pop']-hosp_staff-int(p['init_pop'][1])
         #read in any advanced settings
# =============================================================================
#          p['intervention_type']=intervention_type
#          p['intervention_timing']=intervention_timing
#          p['symptomatic_only']=symptomatic_only
#          p['prop_hospital']=prop_hospital
#          p['prop_other_hc']=prop_other_hc
# =============================================================================
# =============================================================================
#          else: #defaults
#              p['intervention_type']=2
#              p['intervention_timing']=2
#              p['symptomatic_only']=True
#              p['prop_hospitals']=0.5
#              p['prop_other_hc']=0.5
# =============================================================================
#  Since intervention type can be defined differently for different scenarios this stuff will now be defined in process_scenarios
# =============================================================================
# 
#          pre_beta = float(p['beta_pre_inversion'][0])
#          #fix post intervention beta according to type of intervention
#          if intervention_type==0:
#              post_beta = float(p['beta_pre_inversion'][0])
#          else:
#              if intervention_type==1:
#                  post_beta=float(p['beta_post_inversion_1'][0])
#              else:
#                  post_beta=float(p['beta_post_inversion_2'][0])
#          initial_beta = get_beta(initial_betafile, num_compartments, p['init_pop'], pre_beta)
#          final_beta = get_beta(final_betafile, num_compartments, p['init_pop'], post_beta)
# 
# =============================================================================
         results = process_scenarios(num_compartments,p,scenarios,scenariosfile)
         return results

def process_scenarios(num_compartments,p,scenarios,scenariosfile):
         initial_betafile = 'initial_betas.csv'
         final_betafile = 'final_betas.csv'
         scenariosfile='scenarios.csv'
         num_tests_performed=np.zeros(num_compartments)
         expert_mode=True
#read default values for scenarios - these may be richer than the values defined by the expert user
         scenarios_table= pd.read_csv(scenariosfile,header=None)
# read in user defined values
         for i in range(0, len(scenarios)):
             prop_hospital=float(scenarios[i]['prop_hospital'])
             prop_other_hc=float(scenarios[i]['prop_other_hc'])
             intervention_type=scenarios[i]['intervention_type']
             intervention_timing=scenarios[i]['intervention_timing']
             symptomatic_only=scenarios[i]['symptomatic_only']
             prop_rop=1-(prop_hospital+prop_other_hc)
             name_row= pd.Series(['SCENARIO'+str(i+1),'SCENARIO'+str(i+1),None,None,None],index=[0,1,2,3,4])
             props_row= pd.Series(['SCENARIO'+str(i+1),'prop_tests',prop_hospital, prop_other_hc, prop_rop],index=[0,1,2,3,4])
             intervention_type_row= pd.Series(['SCENARIO'+str(i+1),'intervention_type',intervention_type,None,None],index=[0,1,2,3,4])
             intervention_timing_row=pd.Series(['SCENARIO'+str(i+1),'intervention_timing',intervention_timing,None,None],index=[0,1,2,3,4])
             symptomatic_only_row=pd.Series(['SCENARIO'+str(i+1),'symptomatic_only',symptomatic_only,None,None],index=[0,1,2,3,4])
   #          custom_dict_2={0:'CUSTOM',1:'init_infected',2:1,3: 1,4: 1}
   #          scenarios_table=scenarios_table.append(name_row,ignore_index=True)
             scenarios_table=scenarios_table.append(props_row,ignore_index=True)
             scenarios_table=scenarios_table.append(intervention_type_row,ignore_index=True)
             scenarios_table=scenarios_table.append(intervention_timing_row,ignore_index=True)
             scenarios_table=scenarios_table.append(symptomatic_only_row,ignore_index=True)
         (rows,cols)=scenarios_table.shape
  #       print ('scenarios table=', scenarios_table, 'rows=', rows, 'cols=',cols)
         scenarios=[]
         scenario_labels={}
         scenario_params={}
         for i in range(0,rows):
             key = scenarios_table.iloc[i,0]
             if key in scenario_params:
                temp=[scenarios_table.iloc[i,1]]
                for j in range(2,cols):
                    temp.append(scenarios_table.iloc[i,j])
                scenario_params[key].append(temp)
             else: # first instance of scenario key contains name
                scenario_labels[key] = scenarios_table.iloc[i,1]
                scenario_params[key]=[]
                scenarios.append(key)
         num_scenarios = len(scenario_params)
#        print(scenarios)
#        print(scenario_labels)
#         print('scenario params=',scenario_params)

         total_tests_by_scenario=np.zeros(num_scenarios)
         total_deaths_by_scenario=np.zeros(num_scenarios)
         max_infected_by_scenario=np.zeros(num_scenarios)
         max_isolated_by_scenario=np.zeros(num_scenarios)

         scenario_names=[]
         dataframes=[]

         for i in range(1,num_scenarios+1):
             key = scenarios[i-1]
      #       print('i=',i,'key=',key)
             scenario_name=str(key)+': '+scenario_labels[key]
             scenario_names.append(scenario_name)
             if expert_mode:
                 print ('*************')
                 print ('SCENARIO ',str(i),': ',scenario_labels[key])
                 print ('*************')
             filename = scenario_name+'_out.csv'
             p['scenario_name']=scenario_name # JPV: not sure why you need this
             for param_with_vals in scenario_params[key]:
        #        print('param_with_vals=', param_with_vals)
                param = param_with_vals[0]
       #         print('param=',param)
                num_vals = len(param_with_vals)
                for j in range(1, num_vals):
                  target=param_with_vals[j]
                  p[param][j-1]=target
             pre_beta = float(p['beta_pre_inversion'][0])
#          #fix post intervention beta according to type of intervention
             print('intervention_type', p['intervention_type'][0])
             if p['intervention_type'][0]==0:
               post_beta = float(p['beta_pre_inversion'][0])
             else:
              if p['intervention_type'][0]==1:
               post_beta=float(p['beta_post_inversion_1'][0])
              else:
               post_beta=float(p['beta_post_inversion_2'][0])
             initial_beta = get_beta(initial_betafile, num_compartments, p['init_pop'], pre_beta)
             print('post_beta=',post_beta)
             final_beta = get_beta(final_betafile, num_compartments, p['init_pop'], post_beta)
             beta=initial_beta.copy() #this is essential - otherwise the beta gets modified inside the simulation

             df = simulate(num_compartments,p,beta,final_beta)
             dataframes.append(df)
             
             df.to_csv(filename,index=False)
             
             dfsum = df.groupby(['days']).sum().reset_index()  #gives result by day summed across compartments
             dfsumcomp = df.groupby(['compartment']).sum().reset_index() #gives results by day grouped by individual compartment
             dfmaxcomp = df.groupby(['compartment']).max().reset_index() #ori
             for j in range(0,num_compartments):
                comp = dfmaxcomp['compartment'][j]
                dfcomp = df.loc[df['compartment'] == comp]
                
               # print('num_daily tests in ',comp,' =', num_tests_performed[i])
                if expert_mode:
                    print('total population in compartment',comp,p['init_pop'][j])
                    print('total tests in compartment',comp,'=',dfsumcomp['new_tested'][j])
                    print('total_deaths in ',comp,'=', dfsumcomp['new_deaths'][j])
                    print('max_infections in ',comp,'=',dfmaxcomp['total_infected'][j])
                    print('max in isolation in ',comp,'=',dfmaxcomp['total_isolated'][j])
                    print()
                    plot_results(scenario_name,comp,int(num_tests_performed[j]),dfcomp['days'],dfcomp['total_isolated'],dfcomp['total_infected'],dfcomp['tested'],dfcomp['total_infected_notisolated'],dfcomp['total_confirmed'],dfcomp['total_deaths'],dfcomp['susceptibles'])
         
             
             if expert_mode:
                 plot_results(scenario_name,'ALL',dfsumcomp['new_tested'],dfsum['days'],dfsum['total_isolated'],dfsum['total_infected'],dfsum['tested'],dfsum['total_infected_notisolated'],dfsum['total_confirmed'],dfsum['total_deaths'],dfsum['susceptibles'])
                 print('************')
             total_tests_by_scenario[i-1]=dfsumcomp['new_tested'].sum()
             total_deaths_by_scenario[i-1]=dfsumcomp['new_deaths'].sum()
             max_infected_by_scenario[i-1]=dfsum['total_infected'].max()
             max_isolated_by_scenario[i-1]=dfsum['total_isolated'].max()
             if expert_mode:
                 print('Total tested  =',total_tests_by_scenario[i-1])
             
                 print('Max infected=',max_infected_by_scenario[i-1])
                 print('Max isolated=',max_isolated_by_scenario[i-1])
                 print('Total deaths=',total_deaths_by_scenario[i-1])
                 print('************')
                 print('')
         if expert_mode:
             print('******************')
             print('Comparison between scenarios')
             print('******************')
             print('')
             print ('Total tests')
             print('')
             for i in range(0,num_scenarios):
                 print('Scenario ',i,total_tests_by_scenario[i])
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
             print('')
             print('Max isolated')
             print('')
             for i in range(0,num_scenarios):
                print('Scenario ',i,max_isolated_by_scenario[i])
           
             #=============================================================================
             print('')
         return(dataframes, total_tests_by_scenario,total_deaths_by_scenario,max_infected_by_scenario,max_isolated_by_scenario)
 
 

def simulate(num_compartments,params,beta, final_beta):
    num_days = int(params['num_days'][0])
    inversion_date = int(params['inversion_date'][0])
    beta_pre_inversion = float(params['beta_pre_inversion'][0])
    alpha_post_inversion = float(params['alpha_post_inversion'][0])
    latent_period =  int(params['latent_period'][0])
    incubation_period =  int(params['incubation_period'][0])
    infection_fatality_rate=float(params['infection_fatality_rate'][0])
    recovery_period = int(params['recovery_period'] [0])
    tau = infection_fatality_rate/recovery_period
    gamma = (1-infection_fatality_rate)/recovery_period
    test_start = int(params['test_start'][0])
    num_testkit_types=int(params['num_testkit_types'][0])
    print('symptomatic only=',params['symptomatic_only'][0])
    test_symptomatic_only = params['symptomatic_only'][0].upper() == 'TRUE'  #There is a system parameter which defines this differentéy
    p_positive_if_symptomatic = float(params['p_positive_if_symptomatic'][0])
    background_rate_symptomatic=float(params['background_rate_symptomatic'][0])
    intervention_timing=int(params['intervention_timing'][0])
    intervention_threshold_1=int(params['intervention_threshold_1'][0])
    intervention_threshold_2=int(params['intervention_threshold_2'][0])
    intervention_threshold_3=int(params['intervention_threshold_3'][0])
    compartment = []
    init_pop = np.zeros(num_days)
    init_infected = np.zeros(num_days)
    prop_tests = np.zeros(num_compartments)
    num_tests=np.zeros(num_compartments)
    sensitivity=np.zeros(num_testkit_types)
    specificity=np.zeros(num_testkit_types)
    for i in range(0,num_compartments):
         compartment.append(params['compartment'][i])
         init_infected[i] = params['init_infected'][i] 
         prop_tests[i]=float(params['prop_tests'][i])
    for k in range(0,num_testkit_types):
         sensitivity[k]=float(params['sensitivity'][k])
         specificity[k]=float(params['specificity'][k])
         num_tests[k]=int(params['num_tests'][k])
 # ############
 # In this version of the code there are only 3 compartments. 
 # The second compartment aggregates people in high risk professions and
 # People in degraded urban areas. 
 # It would probably be better to separate them into two compartments
 # #################
    if num_compartments!=3:
        print("Error!!! Current version only allows 3 compartments")
        sys.exit()
        
    init_pop[0]=int(params['init_pop'][0])
    init_pop[1]=int(params['init_pop'][1])
    init_pop[2]=int(params['init_pop'][2])
    if params['intervention_type'][0]==0: #if there is no intervention beta will never go down
        alpha=beta*0
    else:
        alpha=beta/alpha_post_inversion #alpha post inversion is now actually a multiplier. Name is wrong. 
 # =============================================================================
  # Initialize arrays storing time series
    days=np.zeros(num_days)
    beta_arr = np.zeros((num_days,num_compartments))
    infected = np.zeros((num_days,num_compartments))
    infectednotisolated=np.zeros((num_days,num_compartments))
    newinfected = np.zeros((num_days,num_compartments))
    tested=np.zeros((num_days,num_compartments))
    newtested=np.zeros((num_days,num_compartments))
    newisolated=np.zeros((num_days,num_compartments))
    newisolatedinfected=np.zeros((num_days,num_compartments))
    isolatedinfected=np.zeros((num_days,num_compartments))
    isolated=np.zeros((num_days,num_compartments))
    susceptibles = np.zeros((num_days,num_compartments))
    recovered = np.zeros((num_days,num_compartments))
    newrecovered = np.zeros((num_days,num_compartments))
    confirmed = np.zeros((num_days,num_compartments))
    newconfirmed = np.zeros((num_days,num_compartments))
    deaths = np.zeros((num_days,num_compartments))
    newdeaths = np.zeros((num_days,num_compartments))
    population = np.zeros((num_days,num_compartments))
    susceptible_prop =np.ones((num_days,num_compartments))
    newinfected=np.zeros((num_days,num_compartments))
         # number of infected generated by compartment i in compartment j
    compart_newinfected=np.zeros((num_days,num_compartments,num_compartments))
    
 
    for i in range(num_compartments):
       newinfected[0,i]=init_infected[i] 
       population[0,i] = init_pop[i]
       susceptibles[0,i] = init_pop[i]-init_infected[i]
       if susceptibles[0,i]<0:
           susceptibles[0,i]=0
       infected[0,i] = newinfected[0,i]
       infectednotisolated[0,i]=init_infected[i]

 
    
 
    totaldeaths=np.zeros(num_compartments)
    maxinfected=np.zeros(num_compartments)
    maxisolated=np.zeros(num_compartments)
    totalisolated=np.zeros(num_compartments)
   
     # calculate new infections day by day for each compartment
    if intervention_timing==0:
        intervention_threshold=float('inf')
    else:
        if intervention_timing==1:
            intervention_threshold=intervention_threshold_1
        else:
            if intervention_timing==2:
                intervention_threshold=intervention_threshold_2
            else:
                intervention_threshold=intervention_threshold_3
    for t in range(1,num_days):
       days[t]=t
       #adjust value of betas - we assume they fall linearly with time after the intervention until they reach a lower bound
 #      if t > inversion_date:
       total_deaths=0
       #adds up total number of confirmed cases. If greater than a threshold starts intervention
       for i in range(0,num_compartments):
           total_deaths=total_deaths+deaths[t-1,i]
       if total_deaths>=intervention_threshold:  #intervention happens when number of deaths passes a threshold
           for i in range (0,num_compartments):
               for j in range(0,num_compartments):
                   if beta[i,j]-alpha[i,j] > final_beta[i,j]:
                       beta[i,j]=beta[i,j]-alpha[i,j]
                   else:
                       beta[i,j] = final_beta[i,j]
       # add up number of new infected for each compartment - total correct at end of loops
       for i in range(0,num_compartments): #this is the compartment doing the infecting
           newinfected[t,i]=0
           sum_infected_not_isolated=0
           for j in range(0, num_compartments):      
       # beta_arr[t] = beta #this is legacy code
             #This computes how many infections compart i will cause in compartment j - this seems t

               compart_newinfected[t-1,i,j] = infectednotisolated[t-1,i]*beta[i,j]*susceptible_prop[t-1,j] #this records how many new infections compart i will cause in compart j 
             # For very high beta this becomes unreliable 
       for i in range(0,num_compartments): #now each compartment adds up the total of new infections
           newinfected[t-1,i]=0
           for j in range(0,num_compartments):
             newinfected[t-1,i]=newinfected[t-1,i]+compart_newinfected[t-1,j,i]
             if newinfected[t-1,i]>susceptibles[t-1,i]:
                 newinfected[t-1,i]=susceptibles[t-1,i]
     
       for i in range(0,num_compartments): 
           true_positives=0
           false_positives=0
           for k in range(0,num_testkit_types): #accumulate true and false positives across different kinds of tests
               tests_available=prop_tests[i]*num_tests[k]
   #            print ('compartment=',i,' test_type=',k,'prop_tests=', prop_tests[i],'num_tests=',num_tests[k],'tests_available=',tests_available)
               if tests_available>0:
                   true_positive_rate=sensitivity[k]
                   false_positive_rate=1-specificity[k]
                   if t < test_start:
                      newtested[t-1,i] = 0
                      newisolated[t-1,i] = 0
                      newisolatedinfected[t-1,i] =  0
                   else:
                      if population[t-1,i] >= tests_available:
                         newtested[t-1,i] = tests_available
                      else:
                         newtested[t-1,i] = population[t-1,i]
                   if test_symptomatic_only:
                       #CAUTION THIS IS NEW CODE
                         if t>incubation_period:
                             total_symptomatic=population[t-1,i]*background_rate_symptomatic+infectednotisolated[t-incubation_period,i]
                         else:
                             total_symptomatic=population[t-1,i]*background_rate_symptomatic
                         if total_symptomatic<tests_available:
                             newtested[t-1,i]=total_symptomatic
                         p_positive_if_symptomatic=infectednotisolated[t-1,i]/total_symptomatic
                         true_positives = true_positives+newtested[t-1,i] * p_positive_if_symptomatic * true_positive_rate
                         false_positives = false_positives+newtested[t-1,i] * (1-p_positive_if_symptomatic) * false_positive_rate
                     
                   else: #also testing non-symptomatic
                     true_positives = true_positives+newtested[t-1,i] * infectednotisolated[t-1,i]/population[t-1,i] * true_positive_rate
                     
                     if true_positives>infectednotisolated[t-1,i]:
                         true_positives=infectednotisolated[t-1,i]
                     false_positives=false_positives+newtested[t-1,i] * (1-infectednotisolated[t-1,i]/population[t-1,i]) * false_positive_rate
        
   #                  print('true_positives=', true_positives,'false positives=', false_positives,'new tested',newtested[t,i],'infected not isolated',infectednotisolated[t-1,i],'true positive rate', true_positive_rate)   
          # Put all positive cases into isolation
           #print('true_positives=', true_positives,'false positives=', false_positives,'new tested',newtested[t-1,i],'infected not isolated',infectednotisolated[t-1,i],'true positive rate', true_positive_rate,'false positive rate',false_positive_rate)   
        #   print('true_positives=', true_positives,'false positives', false_positives)     
           newisolated[t-1,i] = true_positives+false_positives
           newisolatedinfected[t-1,i] = true_positives
      #     newrecovered[t-1,i] = 0
     #      if t >= recovery_period:
     #         newrecovered[t-1,i] = newinfected[t-recovery_period-1,i]*gamma
           newrecovered[t-1,i]=infected[t-1,i]*gamma  
           newdeaths[t,i] = 0
   #        if t >= death_period:
           newdeaths[t-1,i] = infected[t-1,i]*tau
           newconfirmed[t-1,i] = newisolated[t-1,i]
           infected[t,i] = infected[t-1,i]+newinfected[t-1,i]-newrecovered[t-1,i]-newdeaths[t-1,i]
           if infected[t,i]<0:
               infected[t,i]=0
           recovered[t,i] = recovered[t-1,i]+newrecovered[t-1,i]
    #       susceptibles[t,i] = susceptibles[t-1,i]-newinfected[t-1,i]-newdeaths[t-1,i]-newrecovered[t-1,i] #added recovered
           deaths[t,i] = deaths[t-1,i]+newdeaths[t-1,i]
           population[t,i] = population[t-1,i]-newdeaths[t-1,i]
           
           susceptibles[t,i]=population[t,i]-infected[t,i]-recovered[t,i] 
          
     
     #      susceptibles[t,i]=population[t,i]-isolated[t,i]-recovered[t,i]  #this is an accounting identity
           if susceptibles[t,i]<0:  #defensive programming - I don't know why they go negative but they do
               susceptibles[t,i]=0 
    #       print ('t=',t,'susceptibles',susceptibles[t,i],'infected=',infected[t,i],'recovered', recovered[t,i],'population=',population[t,i],'susceptible_prop=',susceptible_prop[t,i])
           susceptible_prop[t,i] = susceptibles[t,i]/population[t,i] #another accounting identity
  #         if i==0:
           tested[t,i] = tested[t-1,i] + newtested[t-1,i]
           confirmed[t,i]=confirmed[t-1,i] + newconfirmed[t-1,i]  # JPV changed
           if t >= recovery_period:
              isolated[t,i] = isolated[t-1,i] + newisolated[t-1,i] - isolated[t-1,i]*gamma-isolated[t-1,i]*tau
              isolatedinfected[t,i] = isolatedinfected[t-1,i] + newisolatedinfected[t-1,i]- isolated[t-1,i]*gamma-isolated[t-1,i]*tau  # JPV changed
           else:
              isolated[t,i] = isolated[t-1,i] + newisolated[t-1,i]
              isolatedinfected[t,i] = isolatedinfected[t-1,i] + newisolatedinfected[t-1,i]
  #         print('t=',t,'infected=',infected[t,i],'isolated=',isolated[t,i])   
           if infected[t,i] - isolated[t,i] > 0:
              infectednotisolated[t,i] = infected[t,i] - (isolated[t,i]) #accounting identity            
            
           else:
              infectednotisolated[t,i] = 0
 
 # =============================================================================
    df = pd.DataFrame({
          'days': range(0,num_days),
          'compartment': np.full(num_days,compartment[0]),
          'population' : np.round(population[:,0],1),
          'susceptibles' : np.round(susceptibles[:,0],1),
          'total_isolated': np.round(isolated[:,0],1),
          'total_infected': np.round(infected[:,0],1),
          'tested': np.round(tested[:,0],1),
          'total_infected_notisolated': np.round(infectednotisolated[:,0],1),
          'total_confirmed': np.round(confirmed[:,0],1),
          'total_deaths': np.round(deaths[:,0],1),
          'total_recovered': np.round(recovered[:,0],1),
          'beta': np.round(beta_arr[:,0],5),
          'susceptible_prop' : np.round(susceptible_prop[:,0],1),
          'new_tested': np.round(newtested[:,0],1),
          'num_infected': np.round(newinfected[:,0],1),
          'num_isolated': np.round(newisolated[:,0],1),
          'num_isolated_infected': np.round(newisolatedinfected[:,0],1),
          'num_confirmed': np.round(newconfirmed[:,0],1),
          'num_recovered': np.round(newrecovered[:,0],1),
          'new_deaths': np.round(newdeaths[:,0],1)
         })
    for i in range(1,num_compartments):
       dfadd = pd.DataFrame({
          'days': range(0,num_days),
          'compartment': np.full(num_days,compartment[i]),
          'population' : np.round(population[:,i],1),
          'susceptibles' : np.round(susceptibles[:,i],1),
          'total_isolated': np.round(isolated[:,i],1),
          'total_infected': np.round(infected[:,i],1),
          'tested': np.round(tested[:,i],1),
          'total_infected_notisolated': np.round(infectednotisolated[:,i],1),
          'total_confirmed': np.round(confirmed[:,i],1),
          'total_deaths': np.round(deaths[:,i],1),
          'total_recovered': np.round(recovered[:,i],1),
          'beta': np.round(beta_arr[:,i],5),
          'susceptible_prop' : np.round(susceptible_prop[:,i],1),
          'new_tested': np.round(newtested[:,i],1),
          'num_infected': np.round(newinfected[:,i],1),
          'num_isolated': np.round(newisolated[:,i],1),
          'num_isolated_infected': np.round(newisolatedinfected[:,i],1),
          'num_confirmed': np.round(newconfirmed[:,i],1),
          'num_recovered': np.round(newrecovered[:,i],1),
          'new_deaths': np.round(newdeaths[:,i],1)
         })
       df = df.append(dfadd)
 # =============================================================================
    return df


 
 
def plot_results(scenario_name,compartment,num_tests, days,num_isolated,num_infected,new_tested,infected_not_isolated,confirmed,deaths,susceptibles):
     
     fig = plt.figure()
    # ax = fig.add_subplot(111)
    # width=0.8
    #  ax.set_title(title)
    # plt.plot(days,num_isolated,color='b', label="Num_isolated")
     plt.plot (days, num_infected,color='r',label="Num_infected")
    # plt.plot (days, confirmed,color='g',label="Confirmed cases")
    # plt.plot (days, infected_not_isolated,color='y',label="Infected_not_isolated")
    # plt.plot (days, deaths,color='k',label="Deaths")
    # plt.gca().set_ylim(0, 0.40)
     plt.title(scenario_name+': '+compartment+' - Infected')
     plt.ylabel('Number')
     plt.xlabel('Day')
     plt.legend(title= "Legend")
     plt.show()
     plt.close()
     plt.plot (days, deaths,color='k',label="Deaths")
     plt.title(scenario_name+': '+compartment+' - Deaths')
     plt.ylabel('Number')
     plt.xlabel('Day')
     plt.legend(title= "Legend")
     plt.show()
     plt.close()
     plt.plot(days,num_isolated,color='b', label="Num_isolated")
     plt.title(scenario_name+': '+compartment+' - Isolated')
     plt.ylabel('Number')
     plt.xlabel('Day')
     plt.legend(title= "Legend")
     plt.show()
     plt.close()
     plt.plot(days,susceptibles,color='c', label="Susceptibles")
     plt.title(scenario_name+': '+compartment+' - Susceptibles')
     plt.ylabel('Number')
     plt.xlabel('Day')
     plt.legend(title= "Legend")
     plt.show()
     plt.close()
     
def calibratebeta(n,beta,pops,targetbeta):
    b = aggregatebeta(n,beta,pops)
    adjust=targetbeta/b
    beta=beta*adjust
    new_b=aggregatebeta(n,beta,pops)
    
    return beta

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

def getscenarios():
    
    scenariosfile='scenarios.csv'
    scenarios_table= pd.read_csv(scenariosfile,header=None)
    scenarios=[]
    scenario_labels={}
    scenario_params={}
   
    p={}
    (rows,cols)=scenarios_table.shape
    for i in range(0,rows):
        key = scenarios_table.iloc[i,0]
        if key in scenario_params:
           temp=[scenarios_table.iloc[i,1]]
           for j in range(2,cols):
               temp.append(scenarios_table.iloc[i,j])
           scenario_params[key].append(temp)
        else: # first instance of scenario key contains name
           scenario_labels[key] = scenarios_table.iloc[i,1]
           scenario_params[key]=[]
           scenarios.append(key)
    num_scenarios = len(scenario_params)
    scenario_names=[]
    scenario_array=[]
    
    print('scenario_array=',scenario_array)
    for i in range(1,num_scenarios+1):
             row_dict={}
             key = scenarios[i-1]
             scenario_name=str(key)+': '+scenario_labels[key]
             scenario_names.append(scenario_name)
             for param_with_vals in scenario_params[key]:
                param = param_with_vals[0]
                print ('scenario',i, 'param', param)
                if param =='prop_tests':
                    row_dict.update({'prop_hospitals':float(param_with_vals[1])})
                    row_dict.update({'prop_other_hc':float(param_with_vals[2])})
                else:
                    if param in ['intervention_type','intervention_timing','symptomatic_only']:
                        value=param_with_vals[1]
                        row_dict.update({param:value})
                
             scenario_array.append(row_dict)
    return(scenario_array)
