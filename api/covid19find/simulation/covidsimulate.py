
# usage: python covidsimulate.py <simfile.csv>
# author:  JP Vergara

class covid_simulator:

    def run_simulation():
        import sys
        import pandas as pd
        import numpy as np
        from covidlib import simulate,plot_results
        simsfile = 'compart_params.csv'
        
        betafile = 'betas.csv'
        testkitfile='test_kits.csv'
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
            
            plot_results(scenario_name,'ALL',dfsumcomp['new_tested'],dfsum['days'],dfsum['total_isolated'],dfsum['total_infected'],dfsum['tested'],dfsum['total_infected_notisolated'],dfsum['total_confirmed'],dfsum['total_deaths'],dfsum['susceptibles'])
            
            print('************')
            total_tests_by_scenario[i]=dfsumcomp['new_tested'].sum()
            total_deaths_by_scenario[i]=dfsumcomp['total_deaths'].sum()
            max_infected_by_scenario[i]=dfsumcomp['total_infected'].sum().max()
            max_isolated_by_scenario[i]=dfsumcomp['total_isolated'].sum().max()
            print('Total tested  =',total_tests_by_scenario[i])
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

    
