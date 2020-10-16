
import optlib as opt
import sys

cname = 'Switzerland'
if len(sys.argv) > 1:
   cname = sys.argv[1]

score,dfx,sev,trig = opt.computephases(cname)
print("RESULT:",cname,",",sev,",",trig,",",score,",",score/dfx['total_deaths'].mean())
opt.showthiscase(dfx,sev,trig,'PLOT')

