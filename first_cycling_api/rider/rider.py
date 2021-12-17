from ..objects import FirstCyclingObject
from .endpoints import RiderEndpoint, RiderYearResults
from ..api import fc

class Rider(FirstCyclingObject):
	"""
	Wrapper to load information on riders.

	Attributes
	----------
	ID : int
		The firstycling.com ID for the rider from the URL of their profile page.
	"""
	_default_endpoint = RiderEndpoint

	def _get_response(self, **kwargs):
		return fc.get_rider_endpoint(self.ID, **kwargs)

	def year_results(self, year=None):
		"""
		Get rider details and results for given year.

		Parameters
		----------
		year : int
			Year for which to collect information.
			If None, collects information for latest unloaded year in which rider was active.

		Returns
		-------
		RiderYearResults
		"""
		return self._get_endpoint(endpoint=RiderYearResults, y=year)

	def best_results(self):
		"""
		Get the rider's best results.

		Returns
		-------
		RiderEndpoint
		"""
		return self._get_endpoint(high=1)

	def victories(self, world_tour=None, uci=None):
		"""
		Get the rider's victories.

		Parameters
		----------
		world_tour : bool
			True if only World Tour wins wanted
		uci : bool
			True if only UCI wins wanted

		Returns
		-------
		RiderEndpoint
		"""
		return self._get_endpoint(high=1, k=1, uci=1 if uci else None, wt=1 if world_tour else None)

	def grand_tour_results(self):
		"""
		Get the rider's results in grand tours.

		Returns
		-------
		RiderEndpoint
		"""
		return self._get_endpoint(high=1, k=2)

	def monument_results(self):
		"""
		Get the rider's results in monuments.

		Returns
		-------
		RiderEndpoint
		"""
		return self._get_endpoint(high=1, k=3)

	def team_and_ranking(self):
		"""
		Get the rider's historical teams and rankings.

		Returns
		-------
		RiderEndpoint
		"""
		return self._get_endpoint(stats=1)

	def race_history(self, race_id=None):
		"""
		Get the rider's history at a certain race.

		Parameters
		----------
		race_id : int
			The firstcycling.com ID for the desired race, from the race profile URL.
			If None, loads rider's race history at UCI races.

		Returns
		-------
		RiderEndpoint
		"""
		return self._get_endpoint(stats=1 if not race_id else None, k=1 if not race_id else None, ra=race_id if race_id else None)	

	def one_day_races(self):
		"""
		Get the rider's results at major one-day races.

		Returns
		-------
		RiderEndpoint
		"""
		return self._get_endpoint(stats=1, k=2)

	def stage_races(self):
		"""
		Get the rider's results at major stage races.

		Returns
		-------
		RiderEndpoint
		"""
		return self._get_endpoint(stats=1, k=3)

	def teams(self):
		"""
		Get the rider's historical teams.

		Returns
		-------
		RiderEndpoint
		"""
		return self._get_endpoint(teams=1)