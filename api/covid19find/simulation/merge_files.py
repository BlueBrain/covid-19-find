#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 09:08:09 2020

@author: richard
"""

import pandas as pd
from multiprocessing import cpu_count
import os

cl_path_prefix = os.path.abspath(os.path.dirname(__file__))

def merge_files(in_name, out_name,out_name_long,n):
    df = pd.DataFrame(columns=['Code', 'Country', 'Severities', 'Trigger Dates', 'Score','Method'])
    dflong = pd.DataFrame(columns=['Code', 'Country', 'Severities', 'Trigger Dates', 'Score','Method', 'Long Sev', 'Long Trig'])
    for i in range(0,n):
        dbname=in_name+str(i)+'.csv'
        dbname_long=in_name+str(i)+'long.csv'
        dbfile=os.path.join(cl_path_prefix, 'results', dbname)
        dbfile_long=os.path.join(cl_path_prefix, 'results', dbname_long)
        in_df=pd.read_csv(dbfile,names=['Code', 'Country', 'Severities', 'Trigger Dates', 'Score','Method'])
        in_df_long=pd.read_csv(dbfile_long,names=['Code', 'Country', 'Severities', 'Trigger Dates', 'Score','Method', 'Long Sev', 'Long Trig'])
        df=df.append(in_df)
        dflong=dflong.append(in_df_long)
        #alist_long.append(origin_df_long)
    df.to_csv(out_name)
    dflong.to_csv(out_name_long)
#    out_dict_long.to_csv(out_name_long)
#    out_dict_long.to_csv(out_name_long)
    
if __name__=='__main__':
    
    n_processors=cpu_count()-2
    merge_files('dbx_','finaldb.csv','finaldb_long.csv',n_processors)