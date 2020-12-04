import optlib as opt

ccode = 'CH'
sev =[0.0, 0.9, 1.0, 0.85, 1.0, 0.9, 0.7, 0.9, 0.0]
trig = [1, 47, 73, 100, 120, 147, 203, 218, 246] 
sev.pop()
trig.pop()
dfx,score = opt.plotcase(ccode,sev,trig,'BEFORE')
print("BEFORE:",ccode,",",sev,",",trig,",",score)
score,dfx,nsev,ntrig,lsev,ltrig = opt.extendphases(ccode,sev,trig)
print('extend attempted')
print("AFTER:",ccode,",",nsev,",",ntrig,",",score)
opt.plotcase(ccode,nsev,ntrig,'PLOT')
