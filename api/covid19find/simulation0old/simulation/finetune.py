
import optlib as opt

sev = [0.0, 0.85, 0.95, 1.0, 0.85, 1.0, 0.9, 0.75, 0.95]
trig = [1, 46, 63, 81, 106, 123, 150, 204, 220]
ccode ='CH'
# sev = [0.0, 0.1, 0.0, 0.75, 0.7, 0.8, 0.75, 0.7, 0.9, 0.8, 0.75, 0.9, 0.75, 0.95, 0.55, 1.0, 0.8]
# trig = [1, 17, 31, 47, 61, 75, 90, 104, 118, 132, 146, 160, 174, 188, 202, 216, 230]
# ccode ='IN'

oldsev = sev.copy()
oldtrig = trig.copy()
score, relscore, newsev, newtrig = opt.finetune(ccode, sev, trig )
opt.plotcase(ccode,oldsev,oldtrig,'BEFORE')
opt.plotcase(ccode,newsev,newtrig,'AFTER')
print('BEFORE:',oldsev,oldtrig)
print('AFTER:',newsev,newtrig,relscore)
