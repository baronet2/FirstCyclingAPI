"""
Objects
=========

Provides base class for API objects.
"""

from .endpoints import Endpoint

class FirstCyclingObject:
	_default_endpoint = Endpoint

	def __init__(self, ID):
		self.ID = ID

	def __repr__(self):
		return f"{self.__class__.__name__}({self.ID})"

	def _get_response(self, **kwargs):
		return "That endpoint is not supported."

	def _get_endpoint(self, endpoint=None, **kwargs):
		endpoint = endpoint if endpoint else self._default_endpoint
		response = self._get_response(**kwargs)
		return endpoint(response)