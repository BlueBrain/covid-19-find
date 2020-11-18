import pandas as pd
import optlib as opt
import countrydata as cd
import ast
import sys

dbdf = pd.read_csv("db1trunc.csv")

ccode = 'CH'
if len(sys.argv) > 1:
   ccode = sys.argv[1]

cname = cd.getcountryname(ccode)

onerow = dbdf[dbdf.Code==ccode]

for index, row in onerow.iterrows():
    ccode = row['Code']
    cname = row['Country']
    print("COUNTRY:",cname, '('+ccode+')')
    sev = ast.literal_eval(row['Long Sev'])
    trig = ast.literal_eval(row['Long Trig'])
    score = row['Score']
    print("BEFORE:",ccode,",",cname,",",sev,",",trig,",",score)
    if len(sev) > 1:
       score,dfx,sev,trig = opt.extendphases(ccode,sev,trig)
       score = score/dfx['total_deaths'].mean()
       print('extend attempted')
    print("RESULT:",ccode,",",cname,",",sev,",",trig,",",score)
    opt.showthiscase(dfx,sev,trig,'PLOT')
