"""
author: Ethan Baron
"""

# Import packages ----

import requests
import bs4
import pandas as pd
from dateutil.parser import parse
import json


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
        raise TypeError('Object of type %s with value of %s is not JSON serializable' % (type(Obj), repr(Obj)))


def img_to_country_code(img):
    """ Obtain three-letter country code, or 'UCI' or 'OL' from html img tag """
    return img['src'].split('/')[-1].split('.')[0]


def race_link_to_race_id(a):
    """ Obtain race id from html a tag containing link to race page """
    return int(a['href'].split('r=')[1].split('&')[0])


def race_link_to_stage_num(a):
    """ Obtain stage number from html a tag containing link to race stage page """
    return int(a['href'].split('e=')[1])