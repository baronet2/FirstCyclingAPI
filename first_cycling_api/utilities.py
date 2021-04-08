"""
author: Ethan Baron
"""

# Import packages ----

import requests
import bs4
import pandas as pd
from dateutil.parser import parse
import json
import re


# Global constants ----

colour_icons = ('green', 'red', 'yellow', 'pink', 'violet', 'blue', 'black', 'orange', 'lightblue', 'white') # TODO Any more?

profile_icon_map = {'Bakketempo.png': 'Mountain ITT',
            'Fjell-MF.png': 'Mountain MTF',
            'Fjell.png': 'Mountain',
            'Flatt.png': 'Flat',
            'Smaakupert-MF.png': 'Hilly MTF',
            'Smaakupert.png': 'Hilly',
            'Tempo.png': 'Flat ITT',
            'Brosten.png': 'Cobbles',
            'Lagtempo.png': 'TTT'} # TODO Any more?

uci_categories = ['2.2', '2.1', '2.HC', '2.WT1', '2.WT2', '2.WT3', '2.Pro', 'GT1', 'GT2', '1.2', '1.1', '1.HC', '1.WT1', '1.WT2', '1.WT3', '1.Pro']
one_day_categories = ['1.2', '1.1', '1.HC', '1.WT1', '1.WT2', '1.WT3', '1.Pro']
championships_categories = ['CN', 'CCRR', 'CCTT', 'CCU', 'CCUT', 'WCRR', 'WCTT', 'WCU', 'WCUT']
U23_categories = ['1.2U', '2.2U', '1.NC', '2.NC']


# Useful functions ----

def ComplexHandler(obj):
    """
    Customized handler to convert object to JSON by recursively calling to_json() method.
    Adapted from https://stackoverflow.com/questions/5160077/encoding-nested-python-object-in-json
    """ 
    if hasattr(obj, 'to_json'):
        return obj.to_json()
    else:
        raise TypeError('Object of type %s with value of %s is not JSON serializable' % (type(obj), repr(obj)))

def rider_link_to_id(a):
    return int(a['href'].split('r=')[1])

def team_link_to_id(a):
    return int(a['href'].split('l=')[1])

def img_to_country_code(img):
    """ Obtain three-letter country code, or 'UCI' or 'OL' from html img tag """
    return img['src'].split('/')[-1].split('.')[0]

def race_link_to_race_id(a):
    """ Obtain race id from html a tag containing link to race page """
    return int(a['href'].split('r=')[1].split('&')[0])

def race_link_to_stage_num(a):
    """ Obtain stage number from html a tag containing link to race stage page """
    return int(a['href'].split('e=')[1])

def img_to_profile(img):
    """ Return profile type for image """
    return profile_icon_map[img['src'].split('/')[-1]]

def table_of_riders_to_df(rankings_table):
    """ Convert HTML table containing rankings/results table from bs4 to pandas DataFrame. Return None if no data. """

    # Load pandas DataFrame from raw text only
    out_df = pd.read_html(str(rankings_table), thousands='.')[0].dropna(how='all', axis=1)
    if out_df.iat[0, 0] == 'No data': # No data
        return None

    # Parse soup to add information hidden in tags/links
    headers = [th.text for th in rankings_table.tr.find_all('th')]
    trs = rankings_table.find_all('tr')[1:]
    soup_df = pd.DataFrame([tr.find_all('td') for tr in trs], columns=headers)

    # Add information hidden in tags/links
    if 'Rider' in headers:
        out_df['Rider_ID'] = soup_df['Rider'].apply(lambda td: rider_link_to_id(td.a))
        try:
            out_df['Rider_Country'] = soup_df['Rider'].apply(lambda td: img_to_country_code(td.img))
        except TypeError:
            pass
    if 'Team' in headers:
        out_df['Team_ID'] = soup_df['Team'].apply(lambda td: team_link_to_id(td.a) if td.a else None)
        out_df['Team_Country'] = soup_df['Team'].apply(lambda td: img_to_country_code(td.img) if td.img else None)
    return out_df