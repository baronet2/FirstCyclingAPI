from ..endpoints import ParsedEndpoint
from ..parser import parse_table

class RankingEndpoint(ParsedEndpoint):
	"""
	Rakings page response.

	Attributes
	----------
	table : pd.DataFrame
		Rankings table.
	"""
	def _parse_soup(self):
		self._get_rankings_table()

	def _get_page_nums(self):
		# TODO <p class="right" style="margin-top:-15px;" -> find all a -> text
		return

	def _get_rankings_table(self):
		rankings_table = self.soup.find('table', {'class': 'tablesorter sort'})
		if not rankings_table:
			rankings_table = self.soup.find('table', {'class': 'tablesorter'})
		self.table = parse_table(rankings_table)