"""
API
=========

Provides tools to access the FirstCycling API.
"""

from agithub.base import API, ConnectionProperties, Client

class FirstCyclingAPI(API):
	""" Wrapper for FirstCycling API """
	def __init__(self):
		props = ConnectionProperties(api_url='firstcycling.com', secure_http=True)
		self.setClient(Client())
		self.setConnectionProperties(props)

	def _fix_kwargs(self, **kwargs):
		return {k: v for k, v in kwargs.items() if v}
		
	def get_rider_endpoint(self, rider_id, **kwargs):
		return self['rider.php'].get(r=rider_id, **self._fix_kwargs(**kwargs))[1]
	
	def get_race_endpoint(self, race_id, **kwargs):
		return self['race.php'].get(r=race_id,**self._fix_kwargs(**kwargs))[1]

	def get_ranking_endpoint(self, **kwargs):
		return self['ranking.php'].get(**self._fix_kwargs(**kwargs))[1]

fc = FirstCyclingAPI()