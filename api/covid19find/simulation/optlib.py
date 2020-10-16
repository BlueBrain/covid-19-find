
import matplotlib.pyplot as plt
import covidlib as cl
import pandas as pd
import math
import numpy as np
import getdeaths as gd
import sys
import os
import json

countryname = 'Switzerland'
DB = [
      ['Philippines','PH'],
      ['Switzerland','CH'],
      ['Italy','IT'],
      ['France','FR'],
      ['US','US'],
      ['India','IN'],
      ['Brazil','BR'],
      ['United Kingdom','GB'],
      ['Sweden','SE'],
      ['Spain','ES'],
      ['Peru','PE'],
      ['Canada','CA']
     ]

def getallcountries():
   return DB

def getcountrycode(countryname):
   global DB
   for country in DB:
     if country[0] == countryname:
        return country[1]
   return 'XX'

countrycode = getcountrycode(countryname)

def fixparamnames(dict):
   params={'total_pop':dict['population'],
    'hospital_beds':dict['hospitalBeds'],
    'prop_15_64':dict['activePopulationProportion'],
    'age_gt_64':dict['over64Proportion'],
    'prop_urban':dict['urbanPopulationProportion'],
    'prop_below_pl':0.05,
    'prop_woh':0.4,
    'staff_per_bed':2.5
   }
   return params

def getcountryparams(countrycode):

   countrydata = [ {'countryCode': 'CH', 'population': 8655000, 'activePopulationProportion': 0.66, 'urbanPopulationProportion': 0.73, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.20232131715771232, 'hospitalBeds': 34620, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
   {'countryCode': 'PH', 'population': 109581000, 'activePopulationProportion': 0.63, 'urbanPopulationProportion': 0.46, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.060647064728374445, 'hospitalBeds': 109581, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
   {'countryCode': 'IT', 'population': 60462000, 'activePopulationProportion': 0.63, 'urbanPopulationProportion': 0.7, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.2453680989712547, 'hospitalBeds': 181386, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
   {'countryCode': 'FR', 'population': 65274000, 'activePopulationProportion': 0.62, 'urbanPopulationProportion': 0.8, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.2194590189049238, 'hospitalBeds': 391644, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
   {'countryCode': 'US', 'population': 331003000, 'activePopulationProportion': 0.65, 'urbanPopulationProportion': 0.82, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.17824813068159504, 'hospitalBeds': 662006, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
   {'countryCode': 'IN', 'population': 1380004000, 'activePopulationProportion': 0.66, 'urbanPopulationProportion': 0.34, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.07224416813284598, 'hospitalBeds': 1380004, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None},
   {'countryCode': 'BR', 'population': 212559000, 'activePopulationProportion': 0.69, 'urbanPopulationProportion': 0.86, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.10405319934700485, 'hospitalBeds': 425118, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
   {'countryCode': 'GB', 'population': 67886000, 'activePopulationProportion': 0.63, 'urbanPopulationProportion': 0.83, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.19727496096396904, 'hospitalBeds': 135772, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
   {'countryCode': 'SE', 'population': 10099000, 'activePopulationProportion': 0.62, 'urbanPopulationProportion': 0.87, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.21408812753737994, 'hospitalBeds': 20198, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
   {'countryCode': 'ES', 'population': 46755000, 'activePopulationProportion': 0.65, 'urbanPopulationProportion': 0.8, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.21135401561330344, 'hospitalBeds': 140265, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
   {'countryCode': 'PE', 'population': 32972000, 'activePopulationProportion': 0.66, 'urbanPopulationProportion': 0.77, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.09428448380444011, 'hospitalBeds': 32972, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
   {'countryCode': 'CA', 'population': 37742000, 'activePopulationProportion': 0.66, 'urbanPopulationProportion': 0.81, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.19382738063695618, 'hospitalBeds': 75484, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ]

   for c in countrydata:
     if c['countryCode'] == countrycode:
       return fixparamnames(c)
   print("fix country params function - no matching country")
   return {}

def getdeathdata(countryname):
   df = gd.get_death_data_by_country(countryname)
   return df.fillna(0)

def getcountrydata(countryname):
   df = getdeathdata(countryname)
   n = len(df)
   newdf = df.rename(columns = {'total_deaths': 'accumulated_deaths'}, inplace = False)
   newdf['tests'] = 0
   filename = countryname+'.csv'
   resultdf = newdf.reset_index()[['Date','accumulated_deaths','tests']]
   # print("df1")
   # print(resultdf.reset_index()[['Date','accumulated_deaths','tests']])
   # resultdf.to_csv(filename,index=False)
   # resultdf2 = cl.getcountrydata(filename)
   # print("df2")
   # print(resultdf2)
   return resultdf

# functions for determining shift

epsilon = 0.0001
def zero(x):
   return abs(x-0) < epsilon

def positive(x):
   return x > epsilon

def negative(x):
   epsilon = 0.0000001
   return x < -epsilon

def getshiftswin(df,win):
   columndata = df.rolling(win,win_type='triang',center=True).mean().tolist()
   n = len(columndata)
   shifts = []
   deltas = [0]
   prevdelta = 0
   sign = 1
   for i in range(1,n):
      newdelta = columndata[i]-columndata[i-1]
      deltas.append(newdelta)
      if zero(newdelta):
         sign = sign # nochange
      elif positive(newdelta) and sign == -1:
         sign = 1
         shifts.append(i)
      elif negative(newdelta) and sign == 1:
         sign = -1
         shifts.append(i)
   return shifts

def checkgaps(shifts):
   n = len(shifts)
   min = shifts[0]
   for i in range(1,n):
      gap = shifts[i]-shifts[i-1]
      if gap < min:
         min = gap
   return min

def getshifts(df):
   max = 20
   thresh = 14
   shifts = []
   for win in range(1,max):
      shifts = getshiftswin(df,win)
      mingap = checkgaps(shifts)
      if mingap >= thresh:
         return shifts
   return shifts

def aligntotest(dfactual,dfsimdeaths):
   simdeaths = dfsimdeaths['total_deaths'].tolist()
   actdeaths = dfactual['total_deaths'].tolist()
   aligneddeaths, shift = cl.aligndeaths(actdeaths,simdeaths)
   dfactual['sim_total_deaths'] = aligneddeaths
   # day0 = dfactual.iloc[shift]['Date']
   return dfactual

country_df = getcountrydata(countryname)[['Date','accumulated_deaths','tests']]
#country_df = cl.getcountrydata('Switzerland.csv')[['Date','accumulated_deaths','tests']]
#country_df = cl.getcountrydata('swiss.csv')[['Date','accumulated_deaths','tests']]
#country_df['tests'] = 0
# country_df.to_csv('country.csv',index=False)
end_date=len(country_df)-1

def getsimdeaths(sev,trig):

   fixed_params = getcountryparams(countrycode)
   fixed_params['test_directory'] = 'scratch1'
   fixed_params['past_severities'] = sev
   fixed_params['past_dates'] = trig
   fixed_params['expert_mode'] = 'FALSE'

   scenario_params=[]

# scenario 0

   scenario_params.append({   
    'symptomatic_only':['True','True'], \
    'prop_hospital': [0.3, 0.3],\
    'prop_other_hc':[0.3,0.3],\
    'prop_rop':[0.4,0.4],\
    'severity':[0.8, 0.8],\
    'trig_values':['2020-09-11','2020-12-30'],\
    'trig_def_type':['date','date'],\
    'trig_op_type':['=','='],\
    'num_tests_mitigation':[13000,13000],\
    'type_test_mitigation':['PCR','PCR'],\
    'sensitivity':[0.95,0.95],\
    'specificity':[0.95,0.95],\
    'num_tests_care':[0,0],\
    'type_tests_care':['PCR','PCR'],\
    'prop_contacts_traced':[0.25,0.25],\
    'imported_infections_per_day':[50,50],
    'requireddxtests':[1,2],
    'is_counterfactual':['False','False'],
    'test_strategy':['open public testing','open public testing'],
    'results_period':[1,1],
    'prop_asymptomatic_tested':[0.01,0.01]
    })

   filename=os.path.join(fixed_params['test_directory'],'parameters.json')
   cl.write_parameters(filename,fixed_params,scenario_params)

   dataframes, test_df,results_dict=\
                   cl.run_simulation(country_df,fixed_params,scenarios=scenario_params,end_date=end_date)
   firstdf = dataframes[1].rename(columns = {'deaths': 'total_deaths', 'newdeaths': 'new_deaths'}, inplace = False)
   dfsum = firstdf.groupby(['days']).sum().reset_index()
   
   deaths = dfsum[['total_deaths', 'new_deaths']]
   return deaths

def scorealignment(result,span):
   meandev = result['absdiff'].head(span).sum()/span
   return meandev

def runandalignsim(dfx,sev,trig):
   simdeaths = getsimdeaths(sev,trig)
   result = aligntotest(dfx,simdeaths)
   result['sim_new_deaths'] = result['sim_total_deaths'].diff().fillna(result['sim_total_deaths'].iloc[0]).rolling(7,center=True).mean()
   result['sim_growth'] = getgrowthrate(result['sim_total_deaths'],7)
   # result['absdiff'] = abs(result.growth - result.sim_growth)
   result['absdiff'] = abs(result.total_deaths - result.sim_total_deaths)
   result['absdiff_deaths'] = abs(result.new_deaths - result.sim_new_deaths)
   result['roll'] = result['absdiff'].rolling(3).mean()
   result['roll_deaths'] = result['absdiff_deaths'].rolling(3).mean()
   return result

def growth(x,y,roll):
  if x == 0 or roll == 0:
     return 0
  else:
     return (y/x)**(1/roll) - 1

def getgrowthrate(deaths,roll):
   vals = deaths.tolist()
   ans = vals.copy()
   n = len(vals)
   for i in range(n):
      if i < roll:
         ans[i] = growth(vals[0],vals[i],i)
      else:
         ans[i] = growth(vals[i-roll],vals[i],roll)
   return ans

def plotresult(result,figname,titlestr):
# Length of plot reduced by 0 to get rid of anomalous last result
  n = len(result['sim_total_deaths'])-10
  fig = plt.figure()
  plt.title(titlestr)
  plt.plot(range(0,n),result['sim_total_deaths'][0:n],label='sim')
  plt.plot(range(0,n),result['total_deaths'][0:n],label='actual')
  plt.legend();
  if figname == 'PLOT':
    plt.show()
  plt.savefig(figname+countryname+'TotalDeaths.png')
  plt.clf()
  plt.title(titlestr)
  plt.plot(range(0,n),result['sim_new_deaths'][0:n],label='sim')
  plt.plot(range(0,n),result['new_deaths'][0:n],label='actual')
  plt.legend()
  if figname == 'PLOT':
    plt.show()
  plt.savefig(figname+countryname+'NewDeaths.png')

def showthiscase(dfx,sev,trig,figname):
  print(sev)
  print(trig)
  result = runandalignsim(dfx,sev,trig)
#  result.to_csv('onecase.csv',index=False)
  plotresult(result,figname,countryname+':'+str(sev)+','+str(trig))

def getactualdeaths(countryname):
  dfactual = getdeathdata(countryname)
  dfx = pd.DataFrame()
  dfx['Date'] = dfactual['Date']
  dfx['orig_new_deaths'] = dfactual['New deaths']
  dfx['new_deaths'] = dfactual['New deaths'].rolling(7,center=True).mean().rolling(10).mean()
  dfx['total_deaths'] = dfx['new_deaths'].cumsum()
  dfx['growth'] = getgrowthrate(dfx['total_deaths'],7)
  # dfx.to_csv('actualdeaths.csv',index=False)
  return dfx.fillna(0)

def lookahead(base,inc,bound):
    ans = base+inc
    if (ans > bound):
       return bound
    else:
       return ans

def findnexttrig(dfx, sev, trig, trignum):
   lastday = len(dfx)-1
   sev.append(0.00)
   trig.append(lastday)
   sevsteps = 20
   sevmult = 1.0/(sevsteps)
   minphaselength = 14
   maxphaselength = 90

   bestscore = 100000
   bests = 0
   besttrig = lastday # doesnt matter
   lowerbound = trig[trignum-1]+minphaselength
   upperbound = trig[trignum-1]+maxphaselength
   if upperbound>lastday-56:
       upperbound=lastday-56
 #  span = lookahead(trig[trignum-1]+1,maxphaselength+50,lastday) # EXP1
   print("trigger index:",trignum)
   stopcounter=0
   for t in range(lowerbound,upperbound):
      print('t=',t)
      trig[trignum] = t
      maxsev=1
      minsev=0
      sev[trignum]=1
      maxresult = runandalignsim(dfx,sev,trig)
      maxsevscore = scorealignment(maxresult,lastday) # span vs lastday
      sev[trignum]=0
      minresult=runandalignsim(dfx,sev,trig)
      minsevscore=scorealignment(minresult,lastday)
      while maxsev-minsev>0.001:
  #       print('minsev=',minsev,'maxsev=',maxsev)
         if maxsevscore<minsevscore:
             minsev=minsev+0.382*(maxsev-minsev)
             sev[trignum]=minsev
             minresult=runandalignsim(dfx,sev,trig)
             minsevscore=scorealignment(minresult,lastday)
         else:
             maxsev=minsev+0.618*(maxsev-minsev)
             sev[trignum]=maxsev
             maxresult=runandalignsim(dfx,sev,trig)
             maxsevscore=scorealignment(maxresult,lastday)
 #        span = lookahead(t,20,lastday)
      if minsevscore < bestscore:
         stopcounter=0
         bestscore = minsevscore
         bests =minsev 
         besttrig = t
      else:
          stopcounter=stopcounter+1
      if stopcounter>=7:
          break
      print('bestscore=',bestscore,'best severity=',bests,'besttrigger=',besttrig)
 #  print(">>best:",bests,besttrig,bestscore)
   sev[trignum] = bests
   trig[trignum] = besttrig
   return bestscore, sev, trig

def finetune(cname, sev, trig):
   setcountry(cname)
   dfx = getactualdeaths(cname)
   lastday = len(dfx)
   sevsteps = 20
   sevmult = 0.01
   trigsteps = 10
   n = len(trig)
   bestscore = 0
   for i in range(0,n):
      midsev = sev[i]
      midtrig = trig[i]
      # severity
      bestsev = midsev
      bestscore = 1000
      print(">severity:",i,midsev)
      for j in range(-sevsteps,sevsteps):
         trysev = round(midsev + j*sevmult,2)
         if trysev < 0:
            trysev = 0
         if trysev > 1:
            trysev = 1
         sev[i] = trysev
         result = runandalignsim(dfx,sev,trig)
         span = lookahead(trig[i],100,lastday)
         score = scorealignment(result,lastday)
         print('-',trysev,score)
         if score < bestscore:
            bestscore = score
            bestsev = trysev
      print(">>best:",i,bestsev,bestscore)
      sev[i] = bestsev
      # trig
      if i > 0:
        besttrig = midtrig
        bestscore = 1000
        print(">trig:",i,midtrig)
        for j in range(-trigsteps,trigsteps):
           trytrig = midtrig + j
           trig[i] = trytrig
           result = runandalignsim(dfx,sev,trig)
           span = lookahead(trig[i],50,lastday)
           score = scorealignment(result,lastday)
           print('-',trytrig,score)
           if score < bestscore:
              bestscore = score
              besttrig = trytrig
        print(">>best:",i,besttrig,bestscore)
        trig[i] = besttrig

   return bestscore, sev, trig

def getbestfitwithtrig(dfx):
   sev = [0.0]
   trig = [1]
   minphaselength = 14
   sc = 0
   lastday = len(dfx)-1
   i = 1
   while trig[-1]+minphaselength < (lastday-56):
      sc, sev, trig = findnexttrig(dfx,sev,trig,i)
      i = i + 1
   return sc, sev, trig

def packseverities(sev,trig):
   n = len(sev)
   newsev = [sev[0]]
   newtrig = [trig[0]]
   j = 0
   for i in range(1,n):
      if sev[i] == newsev[j]:
         continue
      else:
         newsev.append(sev[i])
         newtrig.append(trig[i])
         j = j + 1
   return newsev,newtrig

def setcountry(cname):
   global countryname
   global countrydf
   global countrycode
   countryname = cname
   countrycode = getcountrycode(countryname)
   country_df = getcountrydata(countryname)

def computephases(cname):
   setcountry(cname)
   dfx = getactualdeaths(cname)
   score, sev, trig = getbestfitwithtrig(dfx)
   sev, trig = packseverities(sev, trig)
   return score, dfx, sev, trig

def plotcase(cname,sev,trig,figname):
   setcountry(cname)
   dfx = getactualdeaths(cname)
   showthiscase(dfx,sev,trig,figname)


