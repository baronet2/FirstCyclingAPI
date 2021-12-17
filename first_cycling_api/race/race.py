from ..objects import FirstCyclingObject
from .endpoints import RaceEndpoint, RaceVictoryTable, RaceStageVictories, RaceEditionResults
from ..api import fc

class Race(FirstCyclingObject):
	"""
	Wrapper to access endpoints associated with races.

	Attributes
	----------
	ID : int
		The firstcycling.com ID for the race from the URL of the race page.
	"""

	_default_endpoint = RaceEndpoint

	def _get_response(self, **kwargs):
		return fc.get_race_endpoint(self.ID, **kwargs)

	def edition(self, year):
		"""
		Get RaceEdition instance for edition of race.

		Parameters
		----------
		year : int
			Year for edition of interest.

		Returns
		-------
		RaceEdition
		"""
		return RaceEdition(self.ID, year)

	def overview(self, classification_num=None):
		"""
		Get race overview for given classifications.

		Parameters
		----------
		classification_num : int
			Classification for which to collect information.
			See utilities.Classifications for possible inputs.

		Returns
		-------
		RaceEndpoint
		"""
		return self._get_endpoint(k=classification_num)

	def victory_table(self):
		"""
		Get race all-time victory table.

		Returns
		-------
		RaceVictoryTable
		"""
		return self._get_endpoint(endpoint=RaceVictoryTable, k='W')

	def year_by_year(self, classification_num=None):
		"""
		Get year-by-year race statistics for given classification.

		Parameters
		----------
		classification_num : int
			Classification for which to collect information.
			See utilities.Classifications for possible inputs.

		Returns
		-------
		RaceEndpoint
		"""
		return self._get_endpoint(k='X', j=classification_num)	
	
	def youngest_oldest_winners(self):
		"""
		Get race all-time victory table.

		Returns
		-------
		RaceYoungestOldestWinners
		"""
		return self._get_endpoint(k='Y')
	
	def stage_victories(self):
		"""
		Get race all-time stage victories.

		Returns
		-------
		RaceStageVictories
		"""
		return self._get_endpoint(endpoint=RaceStageVictories, k='Z')


class RaceEdition(FirstCyclingObject):
	"""
	Wrapper to access endpoints associated with specific editions of races.

	Attributes
	----------
	ID : int
		The firstcycling.com ID for the race from the URL of the race page.
	year : int
		The year of the race edition.
	"""

	_default_endpoint = RaceEndpoint
	
	def __init__(self, race_id, year):
		super().__init__(race_id)
		self.year = year

	def __repr__(self):
		return f"{self.__class__.__name__}({self.year} {self.ID})"

	def _get_response(self, **kwargs):
		return fc.get_race_endpoint(self.ID, y=self.year, **kwargs)

	def results(self, classification_num=None, stage_num=None):
		"""
		Get race edition results for given classification or stage.

		Parameters
		----------
		classification_num : int
			Classification for which to collect information.
			See utilities.Classifications for possible inputs.
		stage_num : int
			Stage number for which to collect results, if applicable.
			Input 0 for prologue.

		Returns
		-------
		RaceEditionResults
		"""
		zero_padded_stage_num = f'{stage_num:02}' if isinstance(stage_num, int) else None
		return self._get_endpoint(endpoint=RaceEditionResults, l=classification_num, e=zero_padded_stage_num)


	def stage_profiles(self):
		"""
		Get race edition stage profiles.

		Returns
		-------
		RaceEndpoint
		"""
		return self._get_endpoint(e='all')

	def startlist(self):
		"""
		Get race edition startlist in normal mode.

		Returns
		-------
		RaceEndpoint
		"""
		return self._get_endpoint(k=8)

	def startlist_extended(self):
		"""
		Get race edition startlist in extended mode.

		Returns
		-------
		RaceEndpoint
		"""
		return self._get_endpoint(k=9)