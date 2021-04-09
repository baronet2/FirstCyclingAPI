"""
author: Ethan Baron
"""

from .utilities import *

class Ranking:
	"""
	A framework to store Ranking data.

	Attributes
	----------
	url : str
		The url for the rankings page
	df : pd.DataFrame
		A dataframe containing the rankings from the page, or None if there is no data for that page
	"""

	def __init__(self, url=None, ranking_type=1, ranking_category=1, year=2021, country=None, u23='', page_num=1):
		"""
		Initialize a Ranking object.

		Arguments
		---------
		url : str
			url for rankings page
			If url is provided, all other arguments are ignored
		ranking_type : int
			The ranking type (1: 'World', 2: 'One-day race', 3: 'Stage race', 4: 'Africa Tour', 5: 'America Tour', 6: 'Europe Tour', 7: 'Asia Tour', 8: 'Oceania Tour', 99: 'Women')
		ranking_category : int
			The ranking category (1: 'Riders', 2: 'Teams', 3: 'Nations')
		year : int or str
			If int, returns ranking for that particular year, e.g. '2021'
			If str, format as "yyyy-w" with year and week, e.g. '2021-7' returns the rankings in week 7 of 2021
		country : str
			The three-letter code for the country to filter results to, e.g. 'BEL'
		u23 : int
			If 1, include results for under-23 riders only
		page_num : int
			The page number of the ranking desired
		"""

		if not url: # Prepare URL with appropriate headers
			url = "https://firstcycling.com/ranking.php?"
			url += 'rank=' + str(ranking_type)
			url += '&h=' + str(ranking_category)
			url += '&y=' + str(year)
			url += ('&cnat=' + str(country)) if country else ''
			url += '&u23=' + str(u23)
			url += '&page=' + str(page_num)

		# Load webpage
		self.url = url
		page = requests.get(url)
		soup = bs4.BeautifulSoup(page.text, 'html.parser')

		# Parse rankings from page
		rankings_table = soup.find('table', {'class': 'tablesorter sort'})
		self.df = table_of_riders_to_df(rankings_table)

	def __repr__(self):
		return "Ranking(" + self.url + ")"

	def get_json(self):
		return json.dumps(self, default=ComplexHandler)

	def to_json(self):
		d = vars(self).copy()
		d['df'] = self.df.to_json() if self.df is not None else None
		return d