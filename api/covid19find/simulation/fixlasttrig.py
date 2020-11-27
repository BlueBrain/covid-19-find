import pandas as pd
import optlib as opt
import countrydata as cd
import ast

dbdf = pd.read_csv("dblong.csv")

lastday = 276

df = pd.DataFrame(columns=['Code', 'Country', 'Severities', 'Trigger Dates', 'Score'])
df2 = pd.DataFrame(columns=['Code', 'Country', 'Severities', 'Trigger Dates', 'Score', 'Long Sev', 'Long Trig'])

for index, row in dbdf.iterrows():
    ccode = str(row['Code'])
    print(ccode,row['Severities'],row['Trigger Dates'])
    cname = cd.getcountryname(ccode)
    print(ccode,cname)
    xsev = ast.literal_eval(row['Severities'])
    xtrig = ast.literal_eval(row['Trigger Dates'])
    last = xtrig[-1]
    if last > (lastday-56):
       print(last,xtrig[-2])
       xsev.pop()
       xtrig.pop()
    sev, trig = opt.packseverities(xsev,xtrig)
    opt.setcountry(ccode)
    dfx = opt.getactualdeaths(cname)
    result = opt.runandalignsim(dfx,sev,trig)
    absscore = opt.scorealignment(result,len(dfx))
    score = absscore/dfx['total_deaths'].mean()

    df.loc[len(df.index)] = [ccode, cname, sev, trig, score]
    df2.loc[len(df2.index)] = [ccode, cname, sev, trig, score, xsev, xtrig]

df.to_csv("db2.csv",index=False)
df2.to_csv("db1trunc.csv",index=False)
