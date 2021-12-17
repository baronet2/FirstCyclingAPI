"""
API
=========

Provides tools to access the FirstCycling API.
"""

from slumber import API

class FirstCyclingAPI(API):
    """ Wrapper for FirstCycling API """
    def __init__(self):
        super().__init__("https://firstcycling.com", append_slash=False)
        
    def __getitem__(self, key):
        return getattr(self, key)
    
    def _fix_kwargs(self, **kwargs):
        return {k: v for k, v in kwargs.items() if v}
    
    def _get_resource_response(self, resource, **kwargs):
        return self._store['session'].get(resource.url(), params=self._fix_kwargs(**kwargs)).content

    def get_rider_endpoint(self, rider_id, **kwargs):
        return self._get_resource_response(self['rider.php'], r=rider_id, **kwargs)

    def get_race_endpoint(self, race_id, **kwargs):
        return self._get_resource_response(self['race.php'], r=race_id, **kwargs)

    def get_ranking_endpoint(self, **kwargs):
        return self._get_resource_response(self['ranking.php'], **kwargs)

fc = FirstCyclingAPI()