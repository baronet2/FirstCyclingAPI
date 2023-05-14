#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 14 15:39:13 2023

@author: maxime
"""
from .race.race import RaceEdition

def combi_results_startlist(race_id, year,**kwargs):
    try:
        r=RaceEdition(race_id=race_id,year=year)
        t=r.results(**kwargs)
        if t is None:
            return None
        else:
            results_table=t.results_table
            
            start_list=r.startlist()
            
            """ Convert HTML table from bs4 to pandas DataFrame. Return None if no data. """
            # TODO for rider results, format dates nicely with hidden column we are throwing away
            for i in results_table.index:
                try:
                    results_table.loc[i,"BIB"]=start_list.bib_df.loc[results_table.loc[i,"Inv name"]]["BIB"]
                except:
                    print(results_table.loc[i,"Inv name"] + " not found in the start list")
                    results_table.loc[i,"BIB"]=0
            
            t.results_table=results_table
        
            return t
    except Exception as msg:
        import sys
        _, _, exc_tb = sys.exc_info()
        print("line " + str(exc_tb.tb_lineno))
        print(msg)

