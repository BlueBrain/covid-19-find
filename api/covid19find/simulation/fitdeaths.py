
import optlib as opt
import sys
import cdata as cd

ccode = 'IS'
if len(sys.argv) > 1:
   ccode = sys.argv[1]
   


cname = cd.getcountryname(ccode)
score,dfx,sev,trig,longsev,longtrig = opt.computephases(ccode)
print("RESULT:",cname,",",sev,",",trig,",",score)
opt.showthiscase(dfx,sev,trig,'TESTRW10')


