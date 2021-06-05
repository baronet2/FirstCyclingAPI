from ..objects import FirstCyclingObject
from .endpoints import RaceEndpoint
from ..api import fc

class Race(FirstCyclingObject):
	default_endpoint = RaceEndpoint

	def _get_response(self, **kwargs):
		return fc.get_race_endpoint(self.ID, **kwargs)

	def edition(self, year):
		return RaceEdition(self.ID, year)

	def overview(self, classification_num=None):
		return self._get_endpoint(k=classification_num)

	def victory_table(self):
		return self._get_endpoint(k='W')

	def year_by_year(self, classification_num=None):
		return self._get_endpoint(k='X', j=classification_num)	
	
	def youngest_oldest_winners(self):
		return self._get_endpoint(k='Y')
	
	def stage_victories(self):
		return self._get_endpoint(k='Z')


class RaceEdition(FirstCyclingObject):
	default_endpoint = RaceEndpoint
	
	def __init__(self, race_id, year):
		super().__init__(race_id)
		self.year = year

	def __repr__(self):
		return f"{self.__class__.__name__}({self.year} {self.ID})"

	def _get_response(self, **kwargs):
		return fc.get_race_endpoint(self.ID, y=self.year, **kwargs)

	def results(self, classification_num=None, stage_num=None):
		return self._get_endpoint(l=classification_num, e=stage_num)

	def stage_profiles(self):
		return self._get_endpoint(e='all')

	def startlist(self):
		return self._get_endpoint(k=8)

	def startlist_extended(self):
		return self._get_endpoint(k=9)