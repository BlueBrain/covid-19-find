import pandas as pd
import optlib as opt
import countrydata as cd
import ast

dbdf = pd.read_csv("dbylong.csv")

df = pd.DataFrame(columns=['Code', 'Country', 'Severities', 'Trigger Dates', 'Score'])
dflong = pd.DataFrame(columns=['Code', 'Country', 'Severities', 'Trigger Dates', 'Score',
                               'Long Sev', 'Long Trig'])

for index, row in dbdf.iterrows():
    ccode = row['Code']
    cname = row['Country']
    print("COUNTRY:",cname, '('+ccode+')')
    sev = ast.literal_eval(row['Long Sev'])
    trig = ast.literal_eval(row['Long Trig'])
    score = row['Score']
    if len(sev) > 1:
       while (trig[-1] > 200):
          sev.pop()
          trig.pop()
       print(sev,trig)
       score,dfx,sev,trig,longsev,longtrig = opt.extendphases(ccode,sev,trig)
       print('extend attempted')
    print("RESULT:",ccode,",",cname,",",sev,",",trig,",",score)
    opt.showthiscase(dfx,sev,trig,'EXT')

    df.loc[len(df.index)] = [ccode, cname, sev, trig, score]
    dflong.loc[len(dflong.index)] = [ccode, cname, sev, trig, score, longsev, longtrig]

df.to_csv("dbnew.csv",index=False)
dflong.to_csv("dbnewlong.csv",index=False)
