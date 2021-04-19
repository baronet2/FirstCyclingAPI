from .utilities import *

# Endpoints ----
class Ranking(Endpoint):
	"""
	Return Ranking table.
	Use the `table` attribute to obtain a pandas DataFrame of the ranking table.
	"""
	base_url = 'https://firstcycling.com/ranking.php?'

	def __init__(self, params):
		"""
		Parameters:
		-----------
		params : dict {str: str or int or None}
			The query parameters to add to the rankings URL.

			For UCI Ranking:
				'rank': int
					The ranking type (1: 'World', 2: 'One-day race', 3: 'Stage race', 4: 'Africa Tour', 5: 'America Tour', 6: 'Europe Tour', 7: 'Asia Tour', 8: 'Oceania Tour', 99: 'Women')
				'h': int
					The ranking category (1: 'Riders', 2: 'Teams', 3: 'Nations')
				'y': int or str
					If int, returns ranking for that particular year, e.g. 2021
					If str, format as "yyyy-w" with year and week, e.g. '2021-7' returns the rankings in week 7 of 2021
				'cnat': str, optional
					The three-letter code for the country to filter results to, e.g. 'BEL'
				'u23': {1, None}, optional, default None
					If 1, include results for under-23 riders only
				'page_num': int, optional, default 1
					The desired page number of the ranking

			For National Ranking:
				'k': {'nat'}
				'nation': {'bel', 'den', 'fra', 'ita', 'ned', 'nor'}
					The three-letter code for the country {'bel', 'den', 'fra', 'ita', 'ned', 'nor'}
				'y': int
					Year of rankings
				'race': {1, None}, optional, default None
					If 1, return races considered in ranking

			For FirstCycling Ranking:
				'k': {'fc'}
				'rank': {'el', 'jr', 'wel', 'wjr'}
					Category of rankings {'el': Men Elite, 'jr': Men Junior, 'wel': Women Elite, 'wjr': Women Junior}
				'y': int or 'all'
					Year of rankings, 'all' returns podium finishers per year
				'U23': {1, None}, optional, default None
					If 1, include U23 riders only. Not valid if 'y' = 'all' or junior rankings requested.

			For FirstCycling Amateur:
				'k': {'ama'}
				'nat': {'aus', bel', 'den', 'fra', 'ita', 'jpn', 'nor', 'esp', 'gbr', 'usa'}
					The three-letter code for the country
				'y': int
					Year of rankings
				'cnat': str, optional, default None
					The three-letter code, capitalized, for the country of riders to filter
				'U23': {1, None}, optional, default None
					If 1, include U23 riders only.
		
		"""

		self.make_request(params)
		self.soup = bs4.BeautifulSoup(self.response, 'html.parser')
		self._get_page_nums()
		self._get_rankings_table()
		del self.soup

	def _get_page_nums(self):
		# TODO <p class="right" style="margin-top:-15px;" -> find all a -> text
		return

	def _get_rankings_table(self):
		rankings_table = self.soup.find('table', {'class': 'tablesorter sort'})
		if not rankings_table:
			rankings_table = self.soup.find('table', {'class': 'tablesorter'})
		self.table = table_parser(rankings_table)