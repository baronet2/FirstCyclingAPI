from .endpoints import RankingEndpoint
from ..api import fc

class Ranking:
	"""
	Object to retrieve rankings pages.

	Examples
	--------
	>>> Ranking(h=1, rank=1, y=2020, page=2)
	<first_cycling_api.ranking.endpoints.RankingEndpoint at 0x295caddccd0>
	"""
	def __new__(cls, **kwargs):
		"""
		Obtain a ranking endpoint.

		Parameters
		----------
		rank : int or str
			For UCI Ranking, {1: 'World', 2: 'One-day race', 3: 'Stage race', 4: 'Africa Tour', 5: 'America Tour', 6: 'Europe Tour', 7: 'Asia Tour', 8: 'Oceania Tour', 99: 'Women'}.
			For FirstCycling Ranking, {'el': Men Elite, 'jr': Men Junior, 'wel': Women Elite, 'wjr': Women Junior}.
		h : int
			For UCI Ranking, {1: 'Riders', 2: 'Teams', 3: 'Nations'}.
		y : int or str
			If int, returns ranking for that particular year, e.g. 2021.
			For UCI Ranking, if str, format as 'yyyy-w' with year and week, e.g. '2021-7' returns the rankings in week 7 of 2021.
			For FirstCycling Ranking, 'all' returns podium finishers per year.
		cnat : str
			For UCI Ranking and FirstCycling Amateur, the three-letter code for the country to filter riders to, e.g. 'BEL'.
		u23 : int
			For UCI Ranking, if 1 include results for under-23 riders only.
		page_num : int
			The desired page number of the ranking.
		k : str
			For National Ranking, 'nat'.
			For FirstCycling Ranking, 'fc'.
			For FirstCycling Amateur, 'ama'.
		nation : str
			For National Ranking, the three-letter code for the country, one of {'bel', 'den', 'fra', 'ita', 'ned', 'nor'}.
		race : int
			For National Ranking, if 1, load races considered in ranking.
		U23 : int
			For FirstCycling Ranking and FirstCycling Amateur, if 1 include results for under-23 riders only.
		nat : str
			For FirstCycling Amateur, three-letter code for country, one of {'aus', bel', 'den', 'fra', 'ita', 'jpn', 'nor', 'esp', 'gbr', 'usa'}.
			If women's amateur ranking is desired, add a 'w' to the country code, yielding one of {'denw', 'norw'}.

		Returns
		-------
		RankingEndpoint
		"""
		return RankingEndpoint(fc.get_ranking_endpoint(**kwargs))