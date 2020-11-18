
import pandas as pd
import optlib as opt
import cdata as cd
import sys


figname = 'RUN4'
dbname = 'dbx'
start=1
finish=182
testmode = False
if len(sys.argv) > 1:
   if sys.argv[1] == 'test':
      testmode = True
   else:
      start = int(sys.argv[1])	
      if len(sys.argv) > 2:
         finish = int(sys.argv[2])  
      if len(sys.argv) > 3:
         dbname = sys.argv[3]  

fname1 = dbname+'.csv'
fname2 = dbname+'long.csv'
df = pd.DataFrame(columns=['Code', 'Country', 'Severities', 'Trigger Dates', 'Score','Method'])
dflong = pd.DataFrame(columns=['Code', 'Country', 'Severities', 'Trigger Dates', 'Score','Method',
                               'Long Sev', 'Long Trig'])

i = 1
if testmode:
   CDB = cd.gettestcountries()
else:
   CDB = cd.getallcountrycodes()
for ccode in CDB:
   if i >= start:
      print('INDEX:',i)
      if cd.checkcountryparams(ccode) is not None:
         cname = cd.getcountryname(ccode)
         print("COUNTRY:",cname, '('+ccode+')')
         opt.setlengths(14,28,50)
         absscore1,dfx1,sev1,trig1,longsev1,longtrig1 = opt.computephases(ccode)
         score1 = absscore1/dfx1['total_deaths'].mean()
         opt.setlengths(14,28,100)
         absscore2,dfx2,sev2,trig2,longsev2,longtrig2 = opt.computephases(ccode)
         score2 = absscore2/dfx2['total_deaths'].mean()
         if score1 < score2:
            dfx, sev, trig, score, method  = dfx1, sev1, trig1, score1, "horizon=50"
            longsev, longtrig = longsev1, longtrig1
         else:
            dfx, sev, trig, score, method = dfx2, sev2, trig2, score2, "horizon=100"
            longsev, longtrig = longsev2, longtrig2
         print("RESULT:",ccode,",",cname,",",sev,",",trig,",",score,",",method)
         opt.showthiscase(dfx,sev,trig,figname)
         df.loc[len(df.index)] = [ccode, cname, sev, trig, score, method]
         dflong.loc[len(dflong.index)] = [ccode, cname, sev, trig, score, method, longsev, longtrig]
   if i >= finish:
   	  break
   i = i + 1

df.to_csv(fname1,index=False)
dflong.to_csv(fname2,index=False)
