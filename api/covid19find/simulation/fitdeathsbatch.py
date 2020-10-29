
import optlib as opt

CDB = opt.getallcountries()
for country in CDB:
   cname = country[0]
   print("COUNTRY:",cname)
   score,dfx,sev,trig = opt.computephases(cname)
   print("RESULT:",cname,",",sev,",",trig,",",score,",",score/dfx['total_deaths'].mean())
   opt.showthiscase(dfx,sev,trig,'FIG')
