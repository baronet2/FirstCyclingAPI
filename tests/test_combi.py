#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 14 16:26:19 2023

@author: maxime
"""

from first_cycling_api.combi import combi_results_startlist
import numpy as np

def test_combi_2019_amstel(): 
    t = combi_results_startlist(9,2019)
    
    assert len(t.results_table) == 175
    assert t.results_table['Rider'].iloc[0] == 'Mathieu van der Poel'
    assert t.results_table['BIB'].iloc[0] ==181

def test_2022_TdF():
    t = combi_results_startlist(17,2022)

    assert len(t.results_table) == 176
    assert t.results_table['Rider'].iloc[0] == 'Jonas Vingegaard'
    assert t.results_table['BIB'].iloc[0] == 18
   
    t = combi_results_startlist(17,2022,classification_num=1)
    assert len(t.results_table) == 176
    assert t.results_table['Rider'].iloc[0] == 'Jonas Vingegaard'
    assert t.results_table['BIB'].iloc[0] == 18
    
    t = combi_results_startlist(17,2022,classification_num=2)
    assert len(t.results_table) == 26
    assert t.results_table['Rider'].iloc[0] == "Tadej Pogacar"
    assert t.results_table['Time'].iloc[0] == "79:36:03"
    
    

def test_combi_2023_itzulia(): 
    t = combi_results_startlist(14244,2023,stage_num=1)

    assert len(t.results_table) == 113
    assert t.results_table['Rider'].iloc[0] == 'Demi Vollering'
    assert t.results_table['BIB'].iloc[0] ==1
    
    assert 'gc' in t.standings
    assert 'point' in t.standings
    assert 'mountain' in t.standings
    assert 'youth' in t.standings
    
    t = combi_results_startlist(14244,2023,stage_num=1,classification_num=1)
    assert t.results_table['Rider'].iloc[0] == 'Demi Vollering'
    assert t.results_table['BIB'].iloc[0] ==1
    
    t = combi_results_startlist(14244,2023,stage_num=1,classification_num=3)
    assert t.results_table['Rider'].iloc[0] == 'Demi Vollering'
    assert t.results_table['BIB'].iloc[0] ==1
    
def test_combi_2023_gracia(): 
    t = combi_results_startlist(9549,2023,stage_num=3)

    assert len(t.results_table) == 128
    assert t.results_table['Rider'].iloc[0] == 'Jenny Rissveds'
    assert t.results_table['BIB'].iloc[0] ==73
    
    assert 'gc' in t.standings
    assert 'point' in t.standings
    assert 'mountain' in t.standings
    assert 'youth' in t.standings
    
    t = combi_results_startlist(9549,2023,stage_num=3,classification_num=3)
    assert t.results_table['Rider'].iloc[0] == 'Dominika Wlodarczyk'
    
def test_giro_donne_2001():
    t = combi_results_startlist(9064,2001,stage_num=1)
    assert len(t.results_table) == 10
    
    t = combi_results_startlist(9064,2001,stage_num=1,classification_num=3) #not existing
    assert t==None

    


    
