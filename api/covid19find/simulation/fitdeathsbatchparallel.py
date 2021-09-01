


import pandas as pd
import optlib as opt
import cdata as cd
import numpy as np
import sys
from multiprocessing import Pool
from multiprocessing import cpu_count
from multiprocessing import set_start_method
from datetime import datetime
import os

a=10

cl_path_prefix = os.path.abspath(os.path.dirname(__file__))
        
def merge_files(in_name, out_name,out_name_long,n):
    df = pd.DataFrame(columns=['Code', 'Country', 'Severities', 'Trigger Dates', 'Score','Method'])
    dflong = pd.DataFrame(columns=['Code', 'Country', 'Severities', 'Trigger Dates', 'Score','Method', 'Long Sev', 'Long Trig'])
    for i in range(0,n):
        dbname=in_name+str(i)+'.csv'
        dbname_long=in_name+str(i)+'long.csv'
        dbfile=os.path.join(cl_path_prefix, 'results', dbname)
        dbfile_long=os.path.join(cl_path_prefix, 'results', dbname_long)
        in_df=pd.read_csv(dbfile,names=['Code', 'Country', 'Severities', 'Trigger Dates', 'Score','Method'],keep_default_na=False)
        in_df_long=pd.read_csv(dbfile_long,names=['Code', 'Country', 'Severities', 'Trigger Dates', 'Score','Method', 'Long Sev', 'Long Trig'],keep_default_na=False)
        df=df.append(in_df)
        dflong=dflong.append(in_df_long)
        #alist_long.append(origin_df_long)
    df.to_csv(out_name)
    dflong.to_csv(out_name_long)
#    out_dict_long.to_csv(out_name_long)
#    out_dict_long.to_csv(out_name_long)
    
    
    

def process_countries(a_tuple):
    filename ='db1.csv'
    filename_long ='db1_long.csv'
    figname = 'RUN12RW'
    dbname = 'dbx'
    start=a_tuple[0]
    finish=a_tuple[1]
    processor=a_tuple[2]
    testmode = False
    dbname = 'dbx_'+ str(processor)
    fname1 =os.path.join(cl_path_prefix, 'results', dbname+'.csv')
    fname2 = os.path.join(cl_path_prefix, 'results',dbname+'long.csv')
    df = pd.DataFrame(columns=['Code', 'Country', 'Severities', 'Trigger Dates', 'Score','Method'])
    dflong = pd.DataFrame(columns=['Code', 'Country', 'Severities', 'Trigger Dates', 'Score','Method',
                                   'Long Sev', 'Long Trig'])
    df_old_values=pd.read_csv(filename_long,keep_default_na=False)
    
# =============================================================================
#     i = 3
#     if testmode:
#        CDB = cd.gettestcountries()
#     else:
#        CDB = list(cd.getallcountrycodes())
#     df_old_values=pd.read_csv(filename_long,keep_default_na=False)
# =============================================================================
    
    for ccode in df_old_values['Code'][start:finish+1]:
          if cd.checkcountryparams(ccode) is  None:
             print('No data found ',ccode)
          else:
             cname = cd.getcountryname(ccode)
             old_sev,old_trig,old_long_sev, old_long_trig, old_score,method=opt.get_previous_parameters(df_old_values, cname)
             print("COUNTRY:",cname, '('+ccode+')')
             opt.setcountry(ccode)
             dfx,simulated_score=opt.simulate_with_old_parameters(old_sev,old_trig,cname)
             if simulated_score<0.05:
                 sev=old_sev
                 trig=old_trig
                 longsev=old_long_sev 
                 longtrig=old_long_trig
                 score=simulated_score
                 method='Result good without reoptimization'
             else:
                 opt.setlengths(7,28,50)
                 score1,dfx1,sev1,trig1,longsev1,longtrig1 = opt.computephases(ccode)
                 if score1<simulated_score:
                     dfx, sev, trig, score, method  = dfx1, sev1, trig1, score1, "Re-optimized;"#+str(diff)
                     longsev, longtrig = longsev1, longtrig1
                 else:
                     sev=old_sev
                     trig=old_trig
                     longsev=old_long_sev 
                     longtrig=old_long_trig
                     score=simulated_score
                     method='Old parameters retained - better results than new optimization'
                     
                     
      #           opt.setlengths(14,28,100)
       #          score2,dfx2,sev2,trig2,longsev2,longtrig2 = opt.computephases(ccode)
      #           diff = abs(score1-score2)
         #        if score1 < score2:
    # =============================================================================
    #                  dfx, sev, trig, score, method  = dfx1, sev1, trig1, score1, "horizon=50;"#+str(diff)
    #                  longsev, longtrig = longsev1, longtrig1
    # =============================================================================
                 #else:
                  #  dfx, sev, trig, score, method = dfx2, sev2, trig2, score2, "horizon=100"+str(diff)
                 #   longsev, longtrig = longsev2, longtrig2
             print("RESULT:",ccode,",",cname,",",sev,",",trig,",",score,",",method)
             opt.showthiscase(dfx,sev,trig,figname)
             df.loc[len(df.index)] = [ccode, cname, sev, trig, score, method]
             dflong.loc[len(dflong.index)] = [ccode, cname, sev, trig, score, method, longsev, longtrig]
             df.to_csv(fname1,index=False,header=False)
             dflong.to_csv(fname2,index=False,header=False)
                 #next statement used to be >=finish
    
#    dflong.loc[len(dflong.index)] = [ccode, cname, sev, trig, score, method, longsev, longtrig]
    
    
if __name__=='__main__':
    
   
   
    print('starting',datetime.now())
    filename ='db1.csv'
    db1_path=cl_path_prefix
    filename_long =os.path.join(db1_path, 'db1_long.csv')
#    CDB = cd.gettestcountries()
    df_old_values=pd.read_csv(filename_long,keep_default_na=False)
    n_processors=cpu_count()-2
    n_countries=len(df_old_values)
    countries_per_processor=int(n_countries/n_processors)+1
    tuples_list=[]
    last1=0
    last2=last1+countries_per_processor-1
    tuples_list.append((last1,last2,0))
    for i in range(1,n_processors):
        next1=last2+1
        next2=next1+countries_per_processor-1
        if next1>n_countries:
            next1=n_countries
        if next2>n_countries:
            next2=n_countries
        last1=next1
        last2=next2
        if next2>next1:
            tuples_list.append((next1,next2,i))
# multiprocessing temporarily disabled during development        
#    process_countries(tuples_list[0]) 
    if n_processors>len(tuples_list):
        n_processors=len(tuples_list)
    with Pool(n_processors) as p:
        p.map(process_countries,tuples_list)
    
    dbxname='dbx_'
    filename ='db1.csv'
    filename_long ='db1_long.csv'
    merge_files(dbxname,filename,filename_long,n_processors)
    print('ending',datetime.now())
