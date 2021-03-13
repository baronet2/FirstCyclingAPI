"""
author: Ethan Baron
"""

import requests
import bs4
import pandas as pd
from dateutil.parser import parse
import json


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