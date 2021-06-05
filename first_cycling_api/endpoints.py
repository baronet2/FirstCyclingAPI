"""
Endpoints
=========

Provides classes for API objects.
"""

import bs4

class Endpoint:
	def __init__(self, response):
		self.response = response

	def get_json(self):
		return vars(self).copy()


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