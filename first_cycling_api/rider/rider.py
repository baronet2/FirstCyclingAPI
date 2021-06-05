from ..objects import FirstCyclingObject
from .endpoints import RiderEndpoint, RiderYearResults
from ..api import fc

class Rider(FirstCyclingObject):
	default_endpoint = RiderEndpoint

	def _get_response(self, **kwargs):
		return fc.get_rider_endpoint(self.ID, **kwargs)

	def year_results(self, year=None):
		""" Get rider details and results for given year. """
		return self._get_endpoint(endpoint=RiderYearResults, y=year)

	def best_results(self):
		""" Get the rider's best results. """
		return self._get_endpoint(high=1)

	def victories(self, world_tour=None, uci=None):
		""" Get the rider's victories. """
		return self._get_endpoint(high=1, k=1, uci=1 if uci else None, wt=1 if world_tour else None)

	def grand_tour_results(self):
		""" Get the rider's results in grand tours. """
		return self._get_endpoint(high=1, k=2)

	def monument_results(self):
		""" Get the rider's results in monuments. """
		return self._get_endpoint(high=1, k=3)

	def team_and_ranking(self):
		""" Get the rider's historical teams and rankings. """
		return self._get_endpoint(stats=1)

	def race_history(self, race_id=None):
		""" Get the rider's history at a certain race. """
		return self._get_endpoint(stats=1 if not race_id else None, k=1 if not race_id else None, ra=race_id if race_id else None)	

	def one_day_races(self):
		""" Get the rider's results at major one-day races. """
		return self._get_endpoint(stats=1, k=2)

	def stage_races(self):
		""" Get the rider's results at major stage races. """
		return self._get_endpoint(stats=1, k=3)

	def teams(self):
		""" Get the rider's historical teams. """
		return self._get_endpoint(teams=1)
