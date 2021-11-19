import optlib as opt
import pandas as pd
import cdata as cd
import ast
import os
import json
import numpy as np
from multiprocessing import Pool
from multiprocessing import cpu_count
from datetime import datetime
import sys

cl_path_prefix = os.path.abspath(os.path.dirname(__file__))

def extendbatchparallel(db1_path, temp_path, n_processors):
    #This method reads the current db1_long from directory db1_path
    # and writes a new db1.csv and db1_long.csv in the same directory
    # In the process it generates temporary files in the directory defined by temp_path
    # On correct completion the method returns a value of 1
    dbx_name= os.path.join(temp_path,'dbextend_')
    filename =os.path.join(db1_path, 'db1.csv')
    filename_long =os.path.join(db1_path, 'db1_long.csv')
    df_old_values=pd.read_csv(filename_long,keep_default_na=False)
    n_countries=len(df_old_values)
    countries_per_processor=int(n_countries/n_processors)+1
    tuples_list=[]
    last1=0
    last2=last1+countries_per_processor-1
    tuples_list.append((last1,last2,0,filename_long,dbx_name))
    for i in range(1,n_processors):
        next1=last2+1
        next2=next1+countries_per_processor-1
        if next1>n_countries:
            next1=n_countries
        if next2>n_countries:
            next2=n_countries
        last1=next1
        last2=next2
        tuples_list.append((next1,next2,i,filename_long,dbx_name))
  #  process_countries(tuples_list[0])
 #   process_countries(tuples_list[0])
    if n_processors>len(tuples_list):
        n_processors=len(tuples_list)
    if n_processors==1:
        process_countries(tuples_list[0])
    else:
        with Pool(n_processors) as p:
            p.map(process_countries,tuples_list)
    merge_files(dbx_name,filename,filename_long,n_processors)
    return(1)



def merge_files(in_name, out_name,out_name_long,n):
    df = pd.DataFrame(columns=['Code', 'Country', 'Severities', 'Trigger Dates', 'Score','Method'])
    dflong = pd.DataFrame(columns=['Code', 'Country', 'Severities', 'Trigger Dates', 'Score', 'Long Sev', 'Long Trig','Method'])
    for i in range(0,n):
        dbname=in_name+str(i)+'.csv'
        dbname_long=in_name+str(i)+'long.csv'
        dbfile=os.path.join(cl_path_prefix, 'results', dbname)
        dbfile_long=os.path.join(cl_path_prefix, 'results', dbname_long)
        in_df=pd.read_csv(dbfile,names=['Code', 'Country', 'Severities', 'Trigger Dates', 'Score','Method'],keep_default_na=False)
        in_df_long=pd.read_csv(dbfile_long,names=['Code', 'Country', 'Severities', 'Trigger Dates', 'Score', 'Long Sev', 'Long Trig','Method'],keep_default_na=False)
        df=df.append(in_df)
        dflong=dflong.append(in_df_long)
        #alist_long.append(origin_df_long)
    df.to_csv(out_name)
    dflong.to_csv(out_name_long)
#    out_dict_long.to_csv(out_name_long)
#    out_dict_long.to_csv(out_name_long)


def process_countries(a_tuple):
    dbname = 'dbextend_'
    start=a_tuple[0]
    finish=a_tuple[1]
    processor=a_tuple[2]
    db1_long_name=a_tuple[3]
    dbx_name=a_tuple[4]
    testmode = False
    dbname = dbx_name+ str(processor)
    fname1 =dbname+'.csv'
    fname2 =dbname+'long.csv'
    df = pd.DataFrame(columns=['Code', 'Country', 'Severities', 'Trigger Dates', 'Score','Method'])
    dflong = pd.DataFrame(columns=['Code', 'Country', 'Severities', 'Trigger Dates', 'Score', 'Long Sev', 'Long Trig','Method'])
    df_old_values = pd.read_csv(db1_long_name,keep_default_na=False)
# =============================================================================
#     if testmode:
#        CDB = cd.gettestcountries()
#     else:
#        CDB = list(cd.getallcountrycodes()) 
#     localCDB=CDB#for index, row in dbdf.iterrows():
# =============================================================================
    #for ccode in CDB[start-1:finish]:
    today=datetime.now()
    day1= datetime.strptime('2019-11-23',"%Y-%m-%d")
    sim_days=(today-day1).days
    start_extend=sim_days-350 # uaed to be 60
    for ccode in df_old_values['Code'][start:finish+1]:
        if cd.checkcountryparams(ccode) is not None:
             cname = cd.getcountryname(ccode)
             print("COUNTRY:",cname, '('+ccode+')')
             opt.setcountry(ccode)
             print ('Currently processing', ccode)
             old_sev,old_trig,old_long_sev, old_long_trig, old_score,method=opt.get_previous_parameters(df_old_values, cname)
             dfx,simulated_score=opt.simulate_with_old_parameters(old_sev,old_trig,cname)
             if simulated_score<0.02:
                 sev=old_sev
                 trig=old_trig
                 longsev=old_long_sev 
                 longtrig=old_long_trig
                 score=simulated_score
                 method='Old result good enough'
             else:
                 opt.setlengths(7,28,50)
                 if len(old_long_sev) > 1:
                  while (old_long_trig[-1] > start_extend):
                    old_long_sev.pop()
                    old_long_trig.pop()
                 score,dfx,sev,trig,longsev,longtrig = opt.extendphases(ccode,old_long_sev,old_long_trig)
                 method='reoptimized on extend'
                 if score>simulated_score:
                     sev=old_sev
                     trig=old_trig
                     longsev=old_long_sev 
                     longtrig=old_long_trig
                     score=simulated_score
                     method='Old result retained on extend - better than new '
             opt.showthiscase(dfx,sev,trig,'EXT')
              #problem in line below - 'cannot set a row with misplaced columns
             df.loc[len(df.index)] = [ccode, cname, sev, trig, score, method]
             dflong.loc[len(dflong.index)] = [ccode, cname, sev, trig, score, longsev, longtrig,method]
             df.to_csv(fname1,index=False,header=False)
             dflong.to_csv(fname2,index=False,header=False)

if __name__=='__main__':
    print('starting',datetime.now())
    a=1
    db1_path=cl_path_prefix
    temp_path=os.path.join(cl_path_prefix,'results')
    n_processors=cpu_count()-2
    if n_processors<1:
        n_processors=1
    extendbatchparallel(db1_path, temp_path, n_processors)
    print('finished',datetime.now())
    

   
 