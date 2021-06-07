"""
Endpoints
=========

Provides classes for API objects.
"""

import bs4
import json
import pandas as pd
import datetime


class Endpoint:
	"""
	Generalized class to store endpoint responses.

	Attributes
	----------
	response : bytes
		Raw response from firstcycling.com
	"""

	def __init__(self, response):
		self.response = response
		""" Raw response from firstcycling.com. """

	def _to_json(self):
		return vars(self).copy()

	def get_json(self):
		""" Get JSON representation of endpoint response. """
		return json.dumps(self, default=ComplexHandler)


class ParsedEndpoint(Endpoint):
	def __init__(self, response):
		super().__init__(response)
		self._parse_result()

	def _parse_result(self):
		self.soup = bs4.BeautifulSoup(self.response, 'html.parser')
		self._parse_soup()
		del self.soup

	def _parse_soup(self):
		return


def ComplexHandler(obj):
	"""
	Customized handler to convert object to JSON by recursively calling to_json() method.
	Adapted from https://stackoverflow.com/questions/5160077/encoding-nested-python-object-in-json
	""" 
	if hasattr(obj, '_to_json'):
		return obj._to_json()
	elif isinstance(obj, datetime.date):
		return str(obj)
	elif isinstance(obj, pd.DataFrame):
		return obj.to_json()
	elif isinstance(obj, bytes):
		return obj.decode("utf-8")
	else:
		raise TypeError('Object of type %s with value of %s is not JSON serializable' % (type(obj), repr(obj)))