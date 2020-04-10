
# contains function definitions for covid simulation
# author:  JP Vergara

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys

def run_simulation(total_pop,pop_hospitals,pop_high_contact,prop_urban,prop_isolated,degraded,ge_65, \
                   prop_tests_hospitals, prop_tests_high_contact,prop_tests_rest_of_population,sensitivity_PCR, \
                   sensitivity_RDT,sensitivity_xray,selectivity_PCR,selectivity_RDT,selectivity_xray, \
                   num_tests_PCR,num_tests_RDT,num_tests_xray):
         expert_mode=False
         simsfile = 'compart_params.csv'
         
         betafile = 'betas.csv'
#         testkitfile='test_kits.csv'
         userparsfile='user_params.csv'
         scenariosfile='scenarios.csv'
         
 # =============================================================================
 #         if len(sys.argv) > 1:
 #            simsfile = sys.argv[1]
 #         if len(sys.argv) > 2:
 #            userparsfile = sys.argv[2]
 #         if len(sys.argv) > 3:
 #            betafile = sys.argv[3]
 #         if len(sys.argv) > 4:
 #            testkitfile = sys.argv[4]
 #         if len(sys.argv) > 5:
 #            scenariosfile = sys.argv[5]
 # =============================================================================
         
         sims = pd.read_csv(simsfile,header=None)
         (rows,cols) = sims.shape
         #print('System parameter file: {:d} rows, {:d} cols'.format(rows,cols))
         num_compartments = cols-1
         num_tests_performed=np.zeros(num_compartments)
         
         p = {}
         for i in range(0,rows):
            p[sims.iloc[i,0]] = []
            for j in range(1,cols):
               p[sims.iloc[i,0]].append(sims.iloc[i,j])
               
         userpars = pd.read_csv(userparsfile,header=None)
         (rows,cols) = userpars.shape
         #print('User parameter file: {:d} rows, {:d} cols'.format(rows,cols))
         for i in range(0,rows):
            p[userpars.iloc[i,0]] = []
            for j in range(1,cols):
               p[userpars.iloc[i,0]].append(userpars.iloc[i,j])
         if not(expert_mode):
         
             p['compartment']=['Hospitals','Other high contact ','Rest of population']
             p['testkits']=['PCR','RDT','Chest xrays']
             p['init_infected']=[100,5000,4000]
             p['total_pop'][0]=total_pop
             p['init_pop'][0]=pop_hospitals
             p['high_contact'][0]=pop_high_contact
             p['prop_urban'][0]=prop_urban
             p['isolated_area'][0]=prop_isolated
             p['degraded'][0]=degraded
             p['ge_65'][0]=ge_65
             p['prop_tests'][0]=prop_tests_hospitals
             p['prop_tests'][1]=prop_tests_high_contact
             p['prop_tests'][2]=prop_tests_rest_of_population
             p['sensitivity'][0]=sensitivity_PCR
             p['sensitivity'][1]=sensitivity_RDT
             p['sensitivity'][2]=sensitivity_xray
             p['selectivity'][0]=selectivity_PCR
             p['selectivity'][1]=selectivity_RDT
             p['selectivity'][2]=selectivity_xray
             p['num_tests'][0]=num_tests_PCR
             p['num_tests'][1]=num_tests_RDT
             p['num_tests'][2]=num_tests_xray
             p['test_symptomatic_only']=['true','true','true']
         
            
         num_testkit_types=int(p['num_testkit_types'][0])
         
         
         
         beta_table = pd.read_csv(betafile,header=None)
         (rows,cols) = beta_table.shape
         print('beta file: {:d} rows, {:d} cols'.format(rows,cols))
         initial_beta = np.zeros((num_compartments,num_compartments))
         for i in range(1,num_compartments+1):
            for j in range(1,num_compartments+1):
               initial_beta[i-1,j-1] = beta_table.iloc[i,j]
               
         
         # =============================================================================
         # #Initialize testkit_table
         # testkit_table= pd.read_csv(testkitfile,header=None)
         # (rows,cols)=testkit_table.shape
         # #print('test kit table: {:d} rows, {:d} cols'.format(rows,cols))
         # num_testkit_types=rows
         # testkits=[]
         # for i in range(0,num_testkit_types):
         #     aline=[]
         #     for j in range(0,cols):
         #         aline.append(testkit_table.iloc[i,j])
         #     testkits.append(aline) 
         # =============================================================================
         
         # Initialize scenarios_table
         scenarios_table= pd.read_csv(scenariosfile,header=None)
         (rows,cols)=scenarios_table.shape
         #print('scenarios: {:d} rows, {:d} cols'.format(rows,cols))
         num_scenarios=rows-1
         total_tests_by_scenario=np.zeros(num_scenarios+1)
         total_deaths_by_scenario=np.zeros(num_scenarios+1)
         max_infected_by_scenario=np.zeros(num_scenarios+1)
         max_isolated_by_scenario=np.zeros(num_scenarios+1)
         
         scenarios=[]
         for i in range(0,num_scenarios+1):
             aline=[]
             for j in range(0,cols):
                 aline.append(scenarios_table.iloc[i,j])
             scenarios.append(aline)
         print('scenarios=', scenarios)    
         
         
         #      print('parameter set to',p['prop_tests'][j-1])    
         scenario_names=[]
         dataframes=[]
         for i in range(1,num_scenarios+1):
             scenario_name='SCENARIO'+str(i)+': '+str(scenarios[i][0])
             scenario_names.append(scenario_name)
             print ('*************')
             print ('SCENARIO ',i,': ', scenarios[i][0])
             print ('*************')
             filename = scenario_name+'_out.csv'
             p['scenario_name']=scenario_name
             for j in range(1, num_compartments+1):
               target=scenarios[i][j]
         #      print ('i=',i,'scenario=',i-1,'compartment',j,'prop_tests=',target)
               p['prop_tests'][j-1]=target
             beta=initial_beta.copy() #this is essential - otherwise the beta gets modified inside the simulation
             df = simulate(num_compartments,p,beta)
             dataframes.append(df)
             
             df.to_csv(filename,index=False)
             
             dfsum = df.groupby(['days']).sum().reset_index()
             dfsumcomp = df.groupby(['compartment']).sum().reset_index()
             dfmaxcomp = df.groupby(['compartment']).max().reset_index()
          
         ###########################################
         #In the next version we will make this calculation based on number of recorded tests
         # =============================================================================
         #     for i in range(0,num_compartments):
         #         prop_tests=float(p['prop_tests'][i]) #this seems to be defined twice
         #         for k in range(0,num_testkit_types): #need to derive num_testkit types
         #           #print('i=',i,'k=',k,'prop_tests=',p['prop_tests'][i],'testkitnumber=',testkits[k][1])
         #           #total_tests = total_tests + int(p['prop_tests'][i]*testkits[k][1]) 
         #           tests_available=int(p['num_tests'][k])
         #           num_tests_performed[i]=tests_available*prop_tests
         #         total_tests = total_tests + num_tests_performed[i] 
         # =============================================================================
             
             for j in range(0,num_compartments):
                comp = dfmaxcomp['compartment'][j]
                dfcomp = df.loc[df['compartment'] == comp]
                
               # print('num_daily tests in ',comp,' =', num_tests_performed[i])
                print('total tests in compartment',comp,'=',dfsumcomp['new_tested'][j])
         #        print('total_deaths in ',comp,'=',dfmax['total_deaths'][i])
                print('total_deaths in ',comp,'=', dfsumcomp['total_deaths'][j])
                print('max_infections in ',comp,'=',dfmaxcomp['total_infected'][j])
                print('max in isolation in ',comp,'=',dfmaxcomp['total_isolated'][j])
                print()
                plot_results(scenario_name,comp,int(num_tests_performed[i]),dfcomp['days'],dfcomp['total_isolated'],dfcomp['total_infected'],dfcomp['tested'],dfcomp['total_infected_notisolated'],dfcomp['total_confirmed'],dfcomp['total_deaths'],dfcomp['susceptibles'])
             #the million given in the second argument represents the number of tests - it is a dummy to be replaced by real number
             
             if not(expert_mode):
                 plot_results(scenario_name,'ALL',dfsumcomp['new_tested'],dfsum['days'],dfsum['total_isolated'],dfsum['total_infected'],dfsum['tested'],dfsum['total_infected_notisolated'],dfsum['total_confirmed'],dfsum['total_deaths'],dfsum['susceptibles'])
             
             print('************')
             total_tests_by_scenario[i]=dfsumcomp['new_tested'].sum()
             total_deaths_by_scenario[i]=dfsumcomp['total_deaths'].sum()
             max_infected_by_scenario[i]=dfsumcomp['total_infected'].sum().max()
             max_isolated_by_scenario[i]=dfsumcomp['total_isolated'].sum().max()
             print('Total tested  =',total_tests_by_scenario[i-1])
         #######################
             #In this version the maximum figures for infected and isolated are computed incorrectly
             # and are not printed. Function to be implemented in a future version
          
         # =============================================================================
          #   for i in range(0,num_compartments):
         #            if total_tests>0:
         #                print('   % tests in ',p['compartment'][i],'=',100*int(num_tests_performed[i])/total_tests,'%')  
         #            else:
         #                print('   % tests in ',p['compartment'][i],'=',0.0,'%')  
         # =============================================================================
         #    print('Max infected=',max_infected_by_scenario[i])
          #   print('Max isolated=',max_isolated_by_scenario[i])
            # print('Peak hospital degradation',100*(dfmax['total_infected'][0])/int(p['init_pop'][0]),'%')
             print('Total deaths=',total_deaths_by_scenario[i])
             print('************')
             print('')
         print('******************')
         print('Comparison between scenarios')
         print('******************')
         print('')
         print ('Total tests')
         print('')
         for i in range(1,num_scenarios+1):
             print('Scenario ',i,total_tests_by_scenario[i])
         print('')
         print('Total Deaths')
         print('')
         for i in range(1,num_scenarios+1):
             print('Scenario ',i,total_deaths_by_scenario[i])
          #=============================================================================
         print('')
         #plot_comparison_scenarios(scenario_names,total_tests_by_scenario,total_deaths_by_scenario)
         # =============================================================================
         # print('Max infected')
         # print('')
         # for i in range(1,num_scenarios+1):
         #     print('Scenario ',i,max_infected_by_scenario[i])
         # print('')
         # print('Max isolated')
         # for i in range(1,num_scenarios+1):
         #     print('Scenario ',i,max_isolated_by_scenario[i])
         # =============================================================================
         # =============================================================================
         return(dataframes, total_tests_by_scenario,total_deaths_by_scenario)
 
 

def simulate(num_compartments,params,beta):
    num_days = int(params['num_days'][0])
    inversion_date = int(params['inversion_date'][0])
    beta_pre_inversion = float(params['beta_pre_inversion'][0])
    alpha_post_inversion = float(params['alpha_post_inversion'][0])
    latent_period =  int(params['latent_period'][0])
    incubation_period =  int(params['incubation_period'][0])
    infective_period = int(params['infective_period'][0])
    confirmation_rate = float(params['confirmation_rate'][0])
    gamma = float(params['gamma'][0])
    recovery_period = int(params['recovery_period'] [0])
    tau = float(params['tau'][0])
    death_period = int(params['death_period'][0])
    test_start = int(params['test_start'][0])
    num_testkit_types=int(params['num_testkit_types'][0])
    test_symptomatic_only = params['test_symptomatic_only'][0].upper() == 'TRUE'
    p_positive_if_symptomatic = float(params['p_positive_if_symptomatic'][0])
    background_rate_symptomatic=float(params['background_rate_symptomatic'][0])
    compartment = []
    init_pop = np.zeros(num_days)
    init_infected = np.zeros(num_days)
    prop_tests = np.zeros(num_compartments)
    num_tests=np.zeros(num_compartments)
    sensitivity=np.zeros(num_testkit_types)
    selectivity=np.zeros(num_testkit_types)
    for i in range(0,num_compartments):
         compartment.append(params['compartment'][i])
         init_infected[i] = params['init_infected'][i] 
         prop_tests[i]=float(params['prop_tests'][i])
    for k in range(0,num_testkit_types):
         num_tests[k]=int(params['num_tests'][k])
 # ############
 # In this version of the code there are only compartments. 
 # The second compartment aggregates people in high risk professions and
 # People in degraded urban areas. 
 # It would probably be better to separate them into two compartments
 # #################
    if num_compartments!=3:
        print("Error!!! Current version only allows 3 compartments")
        sys.exit()
        
    init_pop[0]=int(params['init_pop'][0])
    high_risk_urban=int(params['total_pop'][0])*float(params['prop_urban'][0])*float(params['degraded'][0])
    other_high_risk=int(params['init_pop'][1] )                  
    init_pop[1]=high_risk_urban+other_high_risk
    init_pop[2]=int(params['total_pop'][0])-init_pop[0]+init_pop[1]
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
       newinfected[0,i]=init_infected[i] # note: orig code effectively has newinfected[0,i]=0
       population[0,i] = init_pop[i]
       susceptibles[0,i] = init_pop[i]-init_infected[i]
       if susceptibles[0,i]<0:
           susceptibles[0,i]=0
   #    susceptible_prop[0,i] = susceptibles[0,i]/population[0,i]
       infected[0,i] = newinfected[0,i]
       infectednotisolated[0,i]=init_infected[i]
   #    print('i=',i,'infectednotisolated)=',infectednotisolated[0,i],)
 
    alpha=beta/alpha_post_inversion
 
    totaldeaths=np.zeros(num_compartments)
    maxinfected=np.zeros(num_compartments)
    maxisolated=np.zeros(num_compartments)
    totalisolated=np.zeros(num_compartments)
   
     # calculate new infections day by day for each compartment
  #  print ('test_symptomatic_only',test_symptomatic_only)
    for t in range(1,num_days):
       days[t]=t
       #adjust value of betas - we assume they fall linearly with time after the intervention
       if t > inversion_date:
           for i in range (0,num_compartments):
               for j in range(0,num_compartments):
                   if beta[i,j]-alpha[i,j] > 0:
                       beta[i,j]=beta[i,j]-alpha[i,j]
                   else:
                       beta[i,j] = 0
       # add up number of new infected for each compartment - total correct at end of loops
       for i in range(0,num_compartments): #this is the compartment doing the infecting
           newinfected[t,i]=0
           for j in range(0, num_compartments):      
       # beta_arr[t] = beta #this is legacy code
             #This computes how many infections compart i will cause in compartment j 
               compart_newinfected[t,i,j] = infectednotisolated[t-1,i]*beta[i,j]*susceptible_prop[t-1,j] #this records how many new infections compart i will cause in compart j 
            #   print ('i=',i,'j=',j,'compart_new=', compart_newinfected[t,i,j])
         #following block is suprermely ugly - but I still haven't mastered numpy sums
       
       for i in range(0,num_compartments): #now each compartment adds up the total of new infections
     
           newinfected[t,i]=0
           for j in range(0,num_compartments):
             newinfected[t,i]=newinfected[t,i]+compart_newinfected[t,j,i]  
     
       for i in range(0,num_compartments): 
           true_positives=0
           false_positives=0
           for k in range(0,num_testkit_types): #accumulate true and false positives across different kinds of tests
 # =============================================================================
 #               num_tests[i]=prop_tests[i]*testkits[k][1]
 #               true_positive_rate=testkits[k][2]
 #               false_positive_rate=1-testkits[k][3]
 # =============================================================================
               tests_available=prop_tests[i]*num_tests[k]
       #        print('i=',i,'k=',k,'tests_available',tests_available,'prop_tests=', prop_tests[i],'num_tests',num_tests[k])
               true_positive_rate=float(params['sensitivity'][k])
       #        print ('true_positive_rate=',true_positive_rate)
               false_positive_rate=1-float(params['selectivity'][k])
         #      print('false_positive_rate=',false_positive_rate)
               false_positive_rate=0 #temporary for debugging purposes
               if t < test_start:
                  newtested[t,i] = 0
                  newisolated[t,i] = 0
                  newisolatedinfected[t,i] =  0
               else:
                  if population[t-1,i] >= tests_available:
                     newtested[t,i] = tests_available
                  else:
                     newtested[t,i] = population[t-1,i]
               if test_symptomatic_only:
                 total_symptomatic=population[t-1,i]*background_rate_symptomatic+infectednotisolated[t-1,i]
                 if total_symptomatic<tests_available:
                     newtested[t,i]=total_symptomatic
                 p_positive_if_symptomatic=infectednotisolated[t-1,i]/total_symptomatic
     #            print('total_symptomatic',total_symptomatic,'p_positive if',p_positive_if_symptomatic)
                 true_positives = true_positives+newtested[t,i] * p_positive_if_symptomatic * true_positive_rate
                 false_positives = false_positives+newtested[t,i] * (1-p_positive_if_symptomatic) * false_positive_rate
               else:
                 true_positives = true_positives+newtested[t,i] * infectednotisolated[t-1,i]/population[t-1,i] * true_positive_rate
                 if true_positives>infectednotisolated[t-1,i]:
                     true_positives=infectednotisolated[t-1,i]
                 false_positives=false_positives+newtested[t,i] * (1-infectednotisolated[t-1,i]/population[t-1,i]) * false_positive_rate
 
 
          # Put all positive cases into isolation
     
           newisolated[t,i] = true_positives+false_positives
           newisolatedinfected[t,i] = true_positives
           newrecovered[t,i] = 0
           if t >= recovery_period:
              newrecovered[t,i] = newinfected[t-recovery_period,i]*gamma
           newdeaths[t,i] = 0
           if t >= death_period:
               newdeaths[t,i] = newinfected[t-death_period,i]*tau
           else:
               newdeaths[t,i]=0
           newconfirmed[t,i] = newisolated[t,i]
           infected[t,i] = infected[t-1,i]+newinfected[t,i]-newrecovered[t,i]-newdeaths[t,i]
           if infected[t,i]<0:
               infected[t,i]=0
           recovered[t,i] = recovered[t-1,i]+newrecovered[t-1,i]
           susceptibles[t,i] = susceptibles[t-1,i]-newinfected[t-1,i]
           if susceptibles[t,i]<0:  #defensive programming - I don't know why they go negative but they do
               susceptibles[t,i]=0
           population[t,i] = population[t-1,i]-newdeaths[t,i]
           susceptible_prop[t,i] = susceptibles[t,i]/population[t,i]
           deaths[t,i] = deaths[t-1,i]+newdeaths[t,i]
 # =============================================================================
 #       newinfected[t] = new_infections
 #       newrecovered[t] = new_recoveries
 #       newdeaths[t] = new_deaths
 # =============================================================================
           tested[t,i] = tested[t-1,i] + newtested[t-1,i]
       #newconfirmed[t,i] = new_confirmed_cases
           confirmed[t,i]=confirmed[t-1,i] + newconfirmed[t,i]  # JPV changed
       #newisolated[t] = new_isolated
       #newisolatedinfected[t] = new_isolated_infected
           if t >= recovery_period:
              isolated[t,i] = isolated[t-1,i] + newisolated[t-1,i] - newisolated[t-recovery_period,i]
 # =============================================================================
 #              if i==0:
 #                  print('t=',t,'i=',i,'isolated_t=',isolated[t-1,i],'newisolated',newisolated[t-1,i],'recovered',newisolated[t-recovery_period,i])
 # =============================================================================
              isolatedinfected[t,i] = isolatedinfected[t-1,i] + newisolatedinfected[t-1,i] - newisolatedinfected[t-recovery_period,i] # JPV changed
           else:
              isolated[t,i] = isolated[t-1,i] + newisolated[t-1,i]
              isolatedinfected[t,i] = isolatedinfected[t-1,i] + newisolatedinfected[t-1,i]
              
           if infected[t,i] - isolated[t,i] > 0:
              infectednotisolated[t,i] = infected[t,i] - isolated[t,i]
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
          'num_deaths': np.round(newdeaths[:,0],1)
         })
    for i in range(1,num_compartments):
       print(compartment[i])
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
          'num_deaths': np.round(newdeaths[:,i],1)
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
     plt.title(compartment+' - Isolated')
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
     
 # =============================================================================
 # def plot_comparison_scenarios(scenario_names,tests_by_scenario, deaths_by_scenario):
 #     print('scenario_names=',scenario_names)
 #     plt.title('Comparison scenarios: deaths')
 #     plt.ylabel('Number')
 #     y_pos = np.arange(len(scenario_names))
 #     plt.bar(y_pos,deaths_by_scenario)
 #     plt.xticks(y_pos, scenario_names)
 #     plt.show()
 #     
 #     
 # =============================================================================
     
     
 
    
    
