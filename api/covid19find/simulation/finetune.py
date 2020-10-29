
import optlib as opt

sev = [0.0, 0.2, 0.9, 1.0, 0.9, 0.85, 1.0, 0.0]
trig = [1, 29, 49, 71, 160, 210, 224, 238]
oldsev = sev.copy()
oldtrig = trig.copy()
opt.plotcase('Switzerland',sev,trig,'BEFORE')
score, newsev, newtrig = opt.finetune('Switzerland', sev, trig )
print('score:',score)
opt.plotcase('Switzerland',newsev,newtrig,'AFTER')
print('BEFORE:',oldsev,oldtrig)
print('AFTER:',newsev,newtrig)
