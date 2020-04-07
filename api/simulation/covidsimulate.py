
# usage: python covidsimulate.py <simfile.csv>
# author:  JP Vergara

import sys
import pandas as pd
import numpy as np
from covidlib import simulate,plot_results

simsfile = 'compart_params.csv'
betafile = 'betas.csv'
if len(sys.argv) > 1:
   simsfile = sys.argv[1]
if len(sys.argv) > 2:
   betafile = sys.argv[2]
sims = pd.read_csv(simsfile,header=None)
(rows,cols) = sims.shape
print('parameter file: {:d} rows, {:d} cols'.format(rows,cols))

p = {}
for i in range(0,rows):
   p[sims.iloc[i,0]] = []
   for j in range(1,cols):
      p[sims.iloc[i,0]].append(sims.iloc[i,j])

num_compartments = cols-1

beta_table = pd.read_csv(betafile,header=None)
(rows,cols) = beta_table.shape
print('beta file: {:d} rows, {:d} cols'.format(rows,cols))
beta = np.zeros((num_compartments,num_compartments))
for i in range(1,num_compartments+1):
   for j in range(1,num_compartments+1):
      beta[i-1,j-1] = beta_table.iloc[i,j]

df = simulate(num_compartments,p,beta)

filename = 'out.csv'
df.to_csv(filename,index=False)

dfsum = df.groupby(['days']).sum().reset_index()
dfsumcomp = df.groupby(['compartment']).sum().reset_index()
dfmax = df.groupby(['compartment']).max().reset_index()

total_tests=0
for i in range(0,num_compartments):
    total_tests = total_tests + int(p['num_tests'][i])

for i in range(0,num_compartments):
   comp = dfmax['compartment'][i]
   dfcomp = df.loc[df['compartment'] == comp]
   print('num_daily tests in ',comp,' =', p['num_tests'][i])
   print('total_deaths in ',comp,'=',dfmax['total_deaths'][i])
   print('max_infections in ',comp,'=',dfmax['total_infected'][i])
   print('max in isolation in ',comp,'=',dfmax['total_isolated'][i])
   print()
   plot_results(comp,int(p['num_tests'][i]),dfcomp['days'],dfcomp['total_isolated'],dfcomp['total_infected'],dfcomp['tested'],dfcomp['total_infected_notisolated'],dfcomp['total_confirmed'],dfcomp['total_deaths'],dfcomp['susceptibles'])

plot_results('OVERALL',total_tests,dfsum['days'],dfsum['total_isolated'],dfsum['total_infected'],dfsum['tested'],dfsum['total_infected_notisolated'],dfsum['total_confirmed'],dfsum['total_deaths'],dfsum['susceptibles'])

print('************')
print('Total tests per day =',total_tests)
for i in range(0,num_compartments):
   print('   % tests in ',p['compartment'][i],'=',100*int(p['num_tests'][i])/total_tests,'%')  
print('Total infected=',dfsum['num_infected'].sum())
print('Total isolated=',dfsum['num_isolated'].sum())
print('Hospital degradation',100*(dfsumcomp['num_deaths'][0]+dfsumcomp['num_isolated'][0])/int(p['init_pop'][0]),'%')
print('************')
print('TOTAL DEATHS=',dfsum['num_deaths'].sum())
print('************')
print('')
