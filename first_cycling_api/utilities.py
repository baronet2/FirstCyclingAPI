"""
author: Ethan Baron
"""

# Import packages ----

import requests
import bs4
import pandas as pd
from dateutil.parser import parse as date_parse, ParserError
from datetime import date
import json
import re
from urllib import parse as url_parse

# Base classes ----

class Endpoint:
    base_url = None
    
    def make_request(self, parameters):
        page = requests.get(self.base_url, params=parameters)
        self.url = page.url
        self.response = page.text
    
    def _to_json(self):
        d = vars(self).copy()
        del d['response']
        return d

    def get_json(self):
        return json.dumps(self, default=ComplexHandler)

    def __repr__(self):
        return self.__class__.__name__ + '(' + self.url + ')'


class FirstCyclingObject:
    def __init__(self, ID, name):
        self.ID = ID

    def __repr__(self):
        return self.__class__.__name__ + '(' + str(self.ID) + ')'

    def get_json(self):
        return json.dumps(self, default=ComplexHandler)

    def _to_json(self):
        d = vars(self).copy()
        return d

    def _get_general_info(self, endpoint):
        """ Function called after loading any endpoint """
        return

    def _get_endpoint(self, endpoint, destination, destination_key=None, *args, **kwargs):
        """ Generalized method to load endpoints """
        endpoint = endpoint(self.ID, *args, **kwargs)
        self._get_general_info(endpoint)
        if destination_key:
            getattr(self, destination)[destination_key] = endpoint
        else:
            setattr(self, destination, endpoint)
        return endpoint


# Global constants ----

# TODO all countries and country codes? - enum?

classifications = {1: 'general', 2: 'youth', 3: 'points', 4: 'mountain', 6: 'sprint'}

current_year = date.today().year

colour_icons = ('green', 'red', 'yellow', 'pink', 'violet', 'blue', 'black', 'orange', 'lightblue', 'white', 'polka', 'maillotmon') # TODO Any more?

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


# JSON Serialization ----

def ComplexHandler(obj):
    """
    Customized handler to convert object to JSON by recursively calling to_json() method.
    Adapted from https://stackoverflow.com/questions/5160077/encoding-nested-python-object-in-json
    """ 
    if hasattr(obj, '_to_json'):
        return obj._to_json()
    elif isinstance(obj, date):
        return str(obj)
    elif isinstance(obj, pd.DataFrame):
        return obj.to_json()
    else:
        raise TypeError('Object of type %s with value of %s is not JSON serializable' % (type(obj), repr(obj)))

# Parsing dates ----

def parse_date(date_text):
    try:
        return date_parse(date_text).date()
    except ParserError: # Result with uncertain date, use January/1st by default
        year, month, day = date_text.split('-')
        month = '01' if not int(month) else month
        day = '01' if not int(day) else day
        fixed_date = year + '-' + month + '-' + day
        return date_parse(fixed_date).date()

# Parsing links ----

def get_url_parameters(url): # Adapted from https://stackoverflow.com/questions/21584545/url-query-parameters-to-dict-python
    return dict(url_parse.parse_qsl(url_parse.urlsplit(url).query))

def rider_link_to_id(a):
    return get_url_parameters(a['href'])['r']

def team_link_to_id(a):
    return get_url_parameters(a['href'])['l']

def race_link_to_race_id(a):
    return get_url_parameters(a['href'])['r']

def race_link_to_stage_num(a):
    return get_url_parameters(a['href'])['e']

# Parsing icons ----

def get_img_name(img):
    return img['src'].split('/')[-1]

def img_to_country_code(img):
    """ Obtain three-letter country code, or 'UCI' or 'OL' from html img tag """
    return get_img_name(img).split('.')[0]

def img_to_profile(img):
    """ Return profile type for image """
    return profile_icon_map[get_img_name(img)]


# Parsing tables ----

def table_parser(table):
    """ Convert HTML table from bs4 to pandas DataFrame. Return None if no data. """

    # Load pandas DataFrame from raw text only
    out_df = pd.read_html(str(table), thousands='.')[0]

    if out_df.iat[0, 0] == 'No data': # No data
        return None

    # Parse soup to add information hidden in tags/links
    headers = [th.text for th in table.tr.find_all('th')]
    trs = table.find_all('tr')[1:]
    soup_df = pd.DataFrame([tr.find_all('td') for tr in trs], columns=headers)

    # Add information hidden in tags
    for col, series in soup_df.iteritems():
        if col in ('Rider', 'Winner', 'Second', 'Third'):
            out_df[col + '_ID'] = series.apply(lambda td: rider_link_to_id(td.a))
            try:
                out_df[col + '_Country'] = series.apply(lambda td: img_to_country_code(td.img))
            except TypeError:
                pass

        elif col == 'Team':
            out_df['Team_ID'] = series.apply(lambda td: team_link_to_id(td.a) if td.a else None)
            out_df['Team_Country'] = series.apply(lambda td: img_to_country_code(td.img) if td.img else None)

        elif col == 'Race':
            out_df['Race_ID'] = series.apply(lambda td: get_url_parameters(td.a['href'])['r'] if td.a else None)
            out_df['Race_Country'] = series.apply(lambda td: img_to_country_code(td.img) if td.img else None)

        elif col == '':
            try:
                out_df['Icon'] = series.apply(lambda td: get_img_name(td.img) if td.img else None)
            except AttributeError:
                pass

    out_df = out_df.replace({'-': None}).dropna(how='all', axis=1)
    return out_df