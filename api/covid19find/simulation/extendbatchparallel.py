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

def extendbatchparallel(db1_path, temp_path, n_processors):
    #This method reads the current db1_long from directory db1_path
    # and writes a new db1.csv and db1_long.csv in the same directory
    # In the process it generates temporary files in the directory defined by temp_path
    # On correct completion the method returns a value of 1

    n_countries=175
    countries_per_processor=int(n_countries/n_processors)+1
    dbx_name= os.path.join(temp_path,'dbextend_')
    filename =os.path.join(db1_path, 'db1.csv')
    filename_long =os.path.join(db1_path, 'db1_long.csv')
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
    process_countries(tuples_list[0])
    with Pool(n_processors) as p:
        p.map(process_countries,tuples_list)
    merge_files(dbx_name,filename,filename_long,n_processors)
    return(1)



def merge_files(in_name, out_name,out_name_long,n):
    df = pd.DataFrame(columns=['Code', 'Country', 'Severities', 'Trigger Dates', 'Score','Method'])
    dflong = pd.DataFrame(columns=['Code', 'Country', 'Severities', 'Trigger Dates', 'Score', 'Long Sev', 'Long Trig'])
    for i in range(0,n):
        dbname=in_name+str(i)+'.csv'
        dbname_long=in_name+str(i)+'long.csv'
        dbfile=os.path.join(cl_path_prefix, 'results', dbname)
        dbfile_long=os.path.join(cl_path_prefix, 'results', dbname_long)
        in_df=pd.read_csv(dbfile,names=['Code', 'Country', 'Severities', 'Trigger Dates', 'Score','Method'],keep_default_na=False)
        in_df_long=pd.read_csv(dbfile_long,names=['Code', 'Country', 'Severities', 'Trigger Dates', 'Score', 'Long Sev', 'Long Trig'],keep_default_na=False)
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
    df = pd.DataFrame(columns=['Code', 'Country', 'Severities', 'Trigger Dates', 'Score'])
    dflong = pd.DataFrame(columns=['Code', 'Country', 'Severities', 'Trigger Dates', 'Score', 'Long Sev', 'Long Trig'])
    dbdf = pd.read_csv(db1_long_name,keep_default_na=False)
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
    #         sev = json.loads(a_row['Long Sev'].tolist()[0])
             if not type(pd.eval(a_row['Long Sev'])) is list:
                 sev=pd.eval(a_row['Long Sev']).tolist()
             else:
                sev=pd.eval(a_row['Long Sev'])
             if not type(pd.eval(a_row['Long Trig'])) is list:
                 trig=pd.eval(a_row['Long Trig']).tolist()
             else:
                trig=pd.eval(a_row['Long Trig'])
   #          trig = json.loads(a_row['Long Trig'].tolist()[0])
   #currently there is no long trig for this to read
             score = a_row['Score']
             if len(sev) > 1:
               while (trig[-1] > start_extend):
                  sev.pop()
                  trig.pop()
               score,dfx,sev,trig,longsev,longtrig = opt.extendphases(ccode,sev,trig)
            
              # opt.showthiscase(dfx,sev,trig,'EXT')
               #problem in line below - 'cannot set a row with misplaced columns
               df.loc[len(df.index)] = [ccode, cname, sev, trig, score]
               dflong.loc[len(dflong.index)] = [ccode, cname, sev, trig, score, longsev, longtrig]
               df.to_csv(fname1,index=False,header=False)
               dflong.to_csv(fname2,index=False,header=False)


if __name__=='__main__':
    db1_path=cl_path_prefix
    temp_path=os.path.join(cl_path_prefix,'results')
    n_processors=10
    extendbatchparallel(db1_path, temp_path, n_processors)

   
 