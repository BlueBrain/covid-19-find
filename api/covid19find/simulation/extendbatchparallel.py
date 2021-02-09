import pandas as pd
import optlib as opt
import cdata as cd
import ast
import os
import json
from multiprocessing import Pool
from multiprocessing import cpu_count
from datetime import datetime
import sys

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
    figname = 'RUN12RW'
    dbname = 'dbextend_'
    start=a_tuple[0]
    finish=a_tuple[1]
    processor=a_tuple[2]
    testmode = False
    dbname = 'dbextend_'+ str(processor)
    fname1 =os.path.join(cl_path_prefix, 'results', dbname+'.csv')
    fname2 = os.path.join(cl_path_prefix, 'results',dbname+'long.csv')
    df = pd.DataFrame(columns=['Code', 'Country', 'Severities', 'Trigger Dates', 'Score'])
    dflong = pd.DataFrame(columns=['Code', 'Country', 'Severities', 'Trigger Dates', 'Score', 'Long Sev', 'Long Trig'])
    dbdf = pd.read_csv("db1_long.csv",keep_default_na=False)
    if testmode:
       CDB = cd.gettestcountries()
    else:
       CDB = list(cd.getallcountrycodes())   
    #for index, row in dbdf.iterrows():
    #for ccode in CDB[start-1:finish]:
    today=datetime.now()
    day1= datetime.strptime('2019-11-23',"%Y-%m-%d")
    sim_days=(today-day1).days
    start_extend=sim_days-60 #should be 56 - have made it bigger for safety
    for index,a_row in dbdf.iterrows():
          #if cd.checkcountryparams(ccode) is not None:
          #   row=dbdf.loc[dbdf['Code']==ccode]
          if index>=start and index<=finish:
             #print('row=',a_row)
             cname = a_row['Country']
             ccode=a_row['Code']
             print("COUNTRY:",cname, '('+cname+')')
    #         sev = json.loads(a_row['Long Sev'].tolist()[0])
             sev=pd.eval(a_row['Long Sev']).tolist()
             print('sev=',sev)
   #          trig = json.loads(a_row['Long Trig'].tolist()[0])
             trig=pd.eval(a_row['Long Trig']).tolist()
             score = a_row['Score']
             if len(sev) > 1:
               while (trig[-1] > start_extend):
                  sev.pop()
                  trig.pop()
               print(sev,trig)
               score,dfx,sev,trig,longsev,longtrig = opt.extendphases(ccode,sev,trig)
               print('extend attempted')
               print("RESULT:",ccode,",",cname,",",sev,",",trig,",",score)
               opt.showthiscase(dfx,sev,trig,'EXT')
               #problem in line below - 'cannot set a row with misplaced columns
               df.loc[len(df.index)] = [ccode, cname, sev, trig, score]
               dflong.loc[len(dflong.index)] = [ccode, cname, sev, trig, score, longsev, longtrig]
               df.to_csv(fname1,index=False,header=False)
               dflong.to_csv(fname2,index=False,header=False)



if __name__=='__main__':
   
  #  CDB = cd.gettestcountries()
    print('starting',datetime.now())
    n_processors=cpu_count()-2
    #this is hard coded - will need to be dynamic
    n_countries=175
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
        tuples_list.append((next1,next2,i))
    with Pool(n_processors) as p:
        p.map(process_countries,tuples_list)
    filename ='db1.csv'
    filename_long ='db1_long.csv'
    dbxname='dbextend_'
    merge_files(dbxname,filename,filename_long,n_processors)
    print('ending',datetime.now())