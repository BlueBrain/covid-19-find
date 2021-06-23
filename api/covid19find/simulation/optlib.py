
import matplotlib.pyplot as plt
import covidlib as cl
import pandas as pd
import math
import numpy as np
import sys
import os
import json
import cdata as cd
import datetime as dt

a=9
minphaselength = 14
maxphaselength = 28
lag = 26
sample =30
#shiftlag=56
shiftlag = lag+sample
horizon = 50

#countryname = 'Switzerland'
#countrycode = 'CH'
#country_df = cd.getcountrydata(countrycode)

#country_df = cl.getcountrydata('Switzerland.csv')[['Date','accumulated_deaths','tests','accumulated_cases']]

epsilon = 0.0001

def setlengths(minp,maxp,hor):
   global minphaselength
   global maxphaselength
   global horizon
   minphaselength = minp
   maxphaselength = maxp
   horizon = hor

def aligntotest(dfactual,dfsimdeaths):
   simdeaths = dfsimdeaths['total_deaths'].tolist()
   day1 = dt.datetime.strptime(dfactual.iloc[0]['Date'],"%Y-%m-%d")-dt.timedelta(days=60)
   empty_df=cl.create_empty_country_df(day1, 60)
   frames=[empty_df,dfactual]
   results_df=pd.concat(frames)[0:len(simdeaths)]
 #  actdeaths = dfactual['total_deaths'].tolist()
#   aligneddeaths, shift = cl.aligndeaths(actdeaths,simdeaths)
 #  dfactual['sim_total_deaths'] = aligneddeaths
 #lengths do not match
   results_df['sim_total_deaths'] = simdeaths[0:len(results_df)]
   # day0 = dfactual.iloc[shift]['Date']
   return results_df

def getsimdeaths(dfx,sev,trig):

   test_directory = 'scratch2'
   fixed_params=cl.get_system_params(test_directory)
   country_params=cd.getcountryparams(countrycode)
   if not(country_params==None):
       fixed_params.update(cd.getcountryparams(countrycode))
   else:
       print('Country files need to be updated')
       print('Please run bbpsetup.py')
       sys.exit()
   fixed_params['test_directory'] = test_directory
   fixed_params['past_severities'] = sev
   fixed_params['past_dates'] = trig
   fixed_params['expert_mode'] = False
   fixed_params['save_results'] = "False"
   fixed_params['run_multiple_test_scenarios'] = False
#   local_df=dfx
#   fixed_params['fatality_reduction'] = 0.35
   day1 = dt.datetime.strptime(dfx.iloc[0]['Date'],"%Y-%m-%d")-dt.timedelta(days=60)
   simphase,lastday=cl.computetoday(day1,trig)
   span=lookahead(trig[-1], horizon,lastday)
   fixed_params['num_days']=span
   end_day=span
# =============================================================================
#    fixed_params['num_days'] = len(country_df)+60
#    end_day=len(country_df)+60
# =============================================================================
#   print(len(country_df))
   
   scenario_params=[]
   scenario_params=cl.get_next_phases_scenarios(fixed_params['test_directory'])
   try:
       filename=os.path.join(fixed_params['test_directory'],'parameters.json')
   except FileNotFoundError:
       print('')
       print('parameters file in ', fixed_params['test_directory'], ' not found')
       sys.exit()
       cl.write_parameters(filename,fixed_params,scenario_params)
# =============================================================================
#    #I try to end the simulation ends 56 days after last day in simulation but this has bad effects
#    endsim=trig[len(trig)-1]+56
#    if endsim>fixed_params['num_days']:
#        endsim=fixed_params['num_days']-1
# =============================================================================
   dataframes, test_df,results_dict=\
                   cl.run_simulation(country_df,fixed_params,scenarios=scenario_params,end_day=end_day)
   firstdf = dataframes[1].rename(columns = {'deaths': 'total_deaths', 'newdeaths': 'new_deaths'}, inplace = False)
   dfsum = firstdf.groupby(['days']).sum().reset_index()
   
   deaths = dfsum[['total_deaths', 'new_deaths']]
   return deaths

def scorealignment(result,span):
   totweight=0.3
   denom1 = result['total_deaths'].head(span).mean()
   if abs(denom1) < 1:
      denom1 = 1
   meanreldev1 = result['absdiff'].head(span).mean()/denom1
   denom2 = result['new_deaths'].head(span).mean()
   if abs(denom2) < 1:
      denom2 = 1
   meanreldev2 = result['absdiff_new_deaths'].head(span).mean()/denom2
   return (meanreldev1*totweight+meanreldev2*(1-totweight))

# =============================================================================
# def scorealignment(result,span):
#    # meandev1 = result['absdiff'].head(span).mean()
#    meanreldev1 = result['absdiff'].head(span).mean()/result['total_deaths'].head(span).mean()
#    meanreldev2 = result['absdiff_new_deaths'].head(span).mean()/result['new_deaths'].head(span).mean()
#    return (meanreldev1*0.7+meanreldev2*0.3)
# =============================================================================

# =============================================================================
# def scorealignment(result,span):
#    # meandev1 = result['absdiff'].head(span).mean()
#    if result['total_deaths'].head(span).mean()>0:
#        meanreldev1 = result['absdiff'].head(span).mean()/result['total_deaths'].head(span).mean()
#    else:
#        meanreldev1=0
#    if result['new_deaths'].head(span).mean()>0:
#        meanreldev2 = result['absdiff_new_deaths'].head(span).mean()/result['new_deaths'].head(span).mean()
#    else:
#        meanreldev2=0
#    return (meanreldev1*0.9+meanreldev2*0.1)
# =============================================================================

# =============================================================================
# def scorealignment(result,span):
#    #totweight is temporary. John defines it as a global in his code.
#    totweight=0.7
#    denom1 = result['total_deaths'].head(span).mean()
#    if abs(denom1) < 1:
#       denom1 = 1
#    meanreldev1 = result['absdiff'].head(span).mean()/denom1
#    denom2 = result['new_deaths'].head(span).mean()
#    if abs(denom2) < 1:
#       denom2 = 1
#    meanreldev2 = result['absdiff_new_deaths'].head(span).mean()/denom2
#    return (meanreldev1*totweight+meanreldev2*(1-totweight))
# =============================================================================

def runandalignsim(dfx,sev,trig):
   simdeaths = getsimdeaths(dfx,sev,trig)
   result = aligntotest(dfx,simdeaths)
#   result['sim_new_deaths'] = result['sim_total_deaths'].diff().fillna(result['sim_total_deaths'].iloc[0]).rolling(7,center=True).mean()
   result['sim_new_deaths'] = result['sim_total_deaths'].diff().fillna(result['sim_total_deaths'].iloc[0]).rolling(7).mean()
   result['sim_growth'] = getgrowthrate(result['sim_total_deaths'],7)
   # result['absdiff'] = abs(result.growth - result.sim_growth)
   result['absdiff'] = abs(result.total_deaths - result.sim_total_deaths)
   result['absdiff_new_deaths'] = abs(result.new_deaths - result.sim_new_deaths)
   result['roll'] = result['absdiff'].rolling(3).mean()
   result['roll_new_deaths'] = result['absdiff_new_deaths'].rolling(3).mean()
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

def getactualdeaths(countryname):
  # dfactual = cd.getdeathdata(countryname)
  # can i get the same stuff from country_df?
  # yes! next three lines
  dfactual = country_df.rename(columns = {'accumulated_deaths': 'total_deaths'}, inplace = False)
  dfactual["New deaths"] = dfactual['total_deaths'].diff().fillna(dfactual['total_deaths'].iloc[0])
  dfactual["New deaths"] = dfactual["New deaths"].astype(float)
  dfx = pd.DataFrame()
  dfx['Date'] = dfactual['Date']
  dfx['orig_new_deaths'] = dfactual['New deaths']
#  dfx['new_deaths'] = dfactual['New deaths'].rolling(28,center=True).mean()
  dfx['new_deaths'] = dfactual['New deaths'].rolling(28).mean()
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
   print('.')
#   lastday = len(dfx)+60
# No reason for this - correct last day is really +60
   lastday = len(dfx)+60
   sev.append(0.00)
   trig.append(lastday)
   sevsteps = 20
   sevmult = 1.0/(sevsteps)
   bestscore = 100000
   bests = 0
   besttrig = lastday # doesnt matter
   lowerbound = trig[trignum-1]+minphaselength
   upperbound = trig[trignum-1]+maxphaselength # should not go beyond lastday-shiftlag+30
   if upperbound > lastday-shiftlag+30:
      upperbound = lastday-shiftlag+30
 #  print("trigger index:",trignum)
#   print("try from",lowerbound,"to",upperbound)
   span = lastday
   for s in range(0,sevsteps+1):
      currsev = round(s*sevmult,2)
 #     print(">severity:",currsev)
      scorerun = 0
      score = 0
      for t in range(lowerbound,upperbound,2):
         lastscore = score
         sev[trignum] = currsev
         trig[trignum] = t
         #have taken 14 off this on John's suggestion
    #     span = lookahead(t,horizon,lastday-14)
         # as an experiment put it back to see if we now get better result for Peru
         span = lookahead(t,horizon,lastday)
         result = runandalignsim(dfx,sev,trig)
         score = scorealignment(result,span) # span vs lastday
         if abs(score - lastscore)<epsilon:
            scorerun = scorerun + 1
         else:
            scorerun = 0
         if scorerun == 5:
            break
 #        print(currsev,t,score)
         if score < bestscore:
            bestscore = score
            bests = currsev
            besttrig = t
#      print(bestscore,bests,besttrig)
#   print(">>best:",bests,besttrig,bestscore,"*",span)
   sev[trignum] = bests
   trig[trignum] = besttrig
   return bestscore, sev, trig

def findnexttrig_finetune(dfx, sev, trig, trignum, sevguide, trigguide):
   lastday = len(dfx)
   sev.append(0.00)
   trig.append(lastday)
   sevsteps = 5
   sevmult = 0.01
   trigsteps = 1
   bestscore = 100000
   bests = 0
   besttrig = lastday # doesnt matter
   lowerbound = trigguide[trignum]-trigsteps
   upperbound = trigguide[trignum]+trigsteps # should not go beyond lastday-shiftlag
   if upperbound > lastday-shiftlag:
      upperbound = lastday-shiftlag
   print("trigger index:",trignum)
   midsev = sevguide[trignum]
   midtrig = trigguide[trignum]
   for s in range(-sevsteps,sevsteps+1):
      currsev = round(midsev+s*sevmult,2)
      if currsev < 0:
         continue
      if currsev > 1:
         continue 
      print(">severity:",currsev)
      scorerun = 0
      score = 0
      for t in range(lowerbound,upperbound+1):
         lastscore = score
         sev[trignum] = currsev
         trig[trignum] = t
         span = lookahead(t,horizon,lastday)
         result = runandalignsim(dfx,sev,trig)
         score = scorealignment(result,span) # span vs lastday
         if abs(score - lastscore)<epsilon:
            scorerun = scorerun + 1
         else:
            scorerun = 0
         if scorerun == 5:
            break
         print(currsev,t,score)
         if score < bestscore:
            bestscore = score
            bests = currsev
            besttrig = t
#      print(bestscore,bests,besttrig)
   print(">>best:",bests,besttrig,bestscore)
   sev[trignum] = bests
   trig[trignum] = besttrig
   return bestscore, sev, trig

def getbestfit(dfx, sev, trig):
   sc = 0
   #This is addition to compensate for added extra frame - previously 60
   lastday = len(dfx)+60
   i = len(sev)
   print(trig[-1],(lastday-shiftlag))
   while trig[-1] < (lastday-shiftlag):
      sc, sev, trig = findnexttrig(dfx,sev,trig,i)
      i = i + 1
   return sc, sev, trig

def getbestfit_finetune(dfx, sev, trig, sevguide, trigguide):
   sc = 0
   lastday = len(dfx) - 1
   n = len(trigguide)
   for i in range(1,n):
      sc, sev, trig = findnexttrig_finetune(dfx,sev,trig,i, sevguide, trigguide)
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

def setcountry(ccode):
   global countryname
   global country_df
   global countrycode
#   earlystarters=['CN']
   n_records=60
   countrycode = ccode
   countryname = cd.getcountryname(countrycode)
   country_df = cd.getcountrydata(countrycode)

   
def checkenoughdeaths(ccode):
   setcountry(ccode)
   dfx = getactualdeaths(countryname)
   zerodeathsprefix = dfx['total_deaths'].head(shiftlag).mean() < epsilon
   lessthantwenty = dfx['new_deaths'].sum() < 20
   return dfx,zerodeathsprefix,lessthantwenty

def computephases(ccode):
   initsev = [0.0]
   dfx,zerodeaths,lessthantwenty = checkenoughdeaths(ccode)
# =============================================================================
#    if zerodeaths:
#       initsev = [1.0]
#    if lessthantwenty:
#       return 1.0,dfx,[1.0],[1],[1.0],[1]
# =============================================================================
   score, dfx, sev, trig, longsev, longtrig = extendphases(ccode, initsev, [1])
   if np.isnan(score)or not isinstance(score,float):
       score=0.0
   return score, dfx, sev, trig, longsev, longtrig

# =============================================================================
# def computephases(ccode):
#    score, dfx, sev, trig, longsev, longtrig = extendphases(ccode, [0.0], [1])
#    return score, dfx, sev, trig, longsev, longtrig
# =============================================================================

def extendphases(ccode, sev, trig):
   setcountry(ccode)
   dfx = getactualdeaths(countryname)
   score, sev, trig = getbestfit(dfx, sev, trig)
   print('LAST SCORE',sev,trig,score)
   result = runandalignsim(dfx,sev,trig)
   score = scorealignment(result,len(dfx))
   print('RESCORE',sev,trig,score)
   nsev, ntrig = packseverities(sev, trig)
   result = runandalignsim(dfx,nsev,ntrig)
   score = scorealignment(result,len(dfx))
   print('PACKED SCORE',nsev,ntrig,score)
   if np.isnan(score) or not isinstance(score,float):
       score=0.0
   return score, dfx, nsev, ntrig, sev, trig

def finetune(ccode, sevguide, trigguide):
   sev = [sevguide[0]]   # always 0.0
   trig = [trigguide[0]] # always 1
   setcountry(ccode)
   dfx = getactualdeaths(countryname)
   score, sev, trig = getbestfit_finetune(dfx, sev, trig, sevguide, trigguide)
   sev, trig = packseverities(sev, trig)
   result = runandalignsim(dfx,sev,trig)
   score = scorealignment(result,len(dfx))
   return score,sev, trig

def finetune1(ccode, origsev, origtrig):
   sev = [0.0]
   trig = [1]
   setcountry(ccode)
   dfx = getactualdeaths(countryname)
   lastday = len(dfx)
   sevsteps = 20
   sevmult = 0.01
   trigsteps = 10
   n = len(origtrig)
   bestscore = 0
   for i in range(1,n):
      sev.append(origsev[i])
      trig.append(origtrig[i])
      midsev = sev[i]
      midtrig = trig[i]
      # severity
      bestsev = midsev
      bestscore = 10000000
#      print(">severity:",i,midsev)
      for j in range(-sevsteps,sevsteps):
         trysev = round(midsev + j*sevmult,2)
         if trysev < 0:
            trysev = 0
         if trysev > 1:
            trysev = 1
         sev[i] = trysev
         result = runandalignsim(dfx,sev,trig)
         span = lookahead(trig[i],horizon,lastday)
         score = scorealignment(result,span)
 #        print('-',trysev,score)
         if score < bestscore:
            bestscore = score
            bestsev = trysev
#      print(">>best:",bestsev,trig[i],bestscore)
      sev[i] = bestsev
      # trig
      if i > 0:
        besttrig = midtrig
        bestscore = 10000000
 #       print(">trig:",i,midtrig)
        for j in range(-trigsteps,trigsteps):
           trytrig = midtrig + j
           trig[i] = trytrig
           result = runandalignsim(dfx,sev,trig)
           span = lookahead(trig[i],horizon,lastday)
           score = scorealignment(result,span)
   #        print('-',trytrig,score)
           if score < bestscore:
              bestscore = score
              besttrig = trytrig
#        print(">>best:",sev[i],besttrig,bestscore)
        trig[i] = besttrig

   return bestscore, sev, trig

def plotresult(result,figname,titlestr):
# Length of plot reduced by 1 to get rid of anomalous last result
  cl_path_prefix = os.path.abspath(os.path.dirname(__file__))
  n = len(result['sim_total_deaths'])
  # fig = plt.figure()
  plt.title(titlestr)
  plt.plot(range(0,n),result['sim_total_deaths'],label='sim')
  plt.plot(range(0,n),result['total_deaths'],label='actual')
  plt.legend();
  filename=os.path.join(cl_path_prefix, 'results',figname+countrycode+'TotalDeaths.png' )
  plt.savefig(filename)
  if figname == 'PLOT':
    plt.show()
  plt.clf()
  plt.title(titlestr)
  plt.plot(range(0,n),result['sim_new_deaths'],label='sim')
  plt.plot(range(0,n),result['new_deaths'],label='actual')
  plt.legend()
  filename=os.path.join(cl_path_prefix, 'results',figname+countrycode+'NewDeaths.png' )
  plt.savefig(filename)
  if figname == 'PLOT':
    plt.show()
  plt.close()

def showthiscase(dfx,sev,trig,figname):
#  print(sev)
#  print(trig)
  result = runandalignsim(dfx,sev,trig)
#  result.to_csv('onecase.csv',index=False)
  score = scorealignment(result,len(dfx))
#  print("SCORE:", score)
  plotresult(result,figname,countryname+'\n'+str(sev)+'\n'+str(trig))
  return score

def plotcase(ccode,sev,trig,figname):
   setcountry(ccode)
   dfx = getactualdeaths(countryname)
#   print("LAST DAY:",len(dfx))
   score = showthiscase(dfx,sev,trig,figname)
   return dfx, score

def get_previous_parameters(df_old_values, country_name):
# Having problems with pd.eval
    
    a_row=df_old_values.loc[df_old_values['Country']==country_name]
    if not type(pd.eval(a_row['Severities'])) is list:
            sev=pd.eval(a_row['Severities']).tolist()[0]
    else:
            sev=pd.eval(a_row['Severities'])
    if not type(pd.eval(a_row['Long Sev'])) is list:
            long_sev=pd.eval(a_row['Long Sev']).tolist()[0]
    else:
            long_sev=pd.eval(a_row['Long Sev'])
    if not type(pd.eval(a_row['Trigger Dates'])) is list:
            trig=pd.eval(a_row['Trigger Dates']).tolist()[0]
    else:
           trig=pd.eval(a_row['Trigger Dates'])
    if not type(pd.eval(a_row['Long Trig'])) is list:
            long_trig=pd.eval(a_row['Long Trig']).tolist()[0]
    else:
           long_trig=pd.eval(a_row['Long Trig'])
    score=float(a_row['Score'])
    if np.isnan(score):
        score=0.0
  #  method=a_row['Method']
    method=''
    return(sev,trig,long_sev, long_trig,score,method)

def simulate_with_old_parameters(sev,trig,country_name):
    dfx_actuals=getactualdeaths(country_name)
    result=runandalignsim(dfx_actuals,sev,trig)
    score=scorealignment(result, len(dfx_actuals))
    if score==None or np.isnan(score):
        score=0.0
    return(dfx_actuals,score)
    
