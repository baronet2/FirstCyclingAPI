from ..endpoints import ParsedEndpoint
from ..parser import parse_date, parse_table, team_link_to_id, img_to_country_code, link_to_twitter_handle

import pandas as pd
import bs4


class RiderEndpoint(ParsedEndpoint):
	"""
	Rider profile page response. Extends Endpoint.

	Attributes
	----------
	years_active : list[int]
		List of years in which rider was active.
	header_details : dict
		Details from page header, including rider name and external links.
	sidebar_details : dict
		Details from right sidebar, including nation, date of birth, height, and more.
	"""

	def _parse_soup(self):
		self._get_years_active()
		self._get_header_details()
		self._get_sidebar_details()

	def _get_years_active(self):
		# TODO make this more robust, fails when too many active years (e.g. Anna Van Der Breggen)
		try:
			self.years_active = [int(a.text) for a in self.soup.find('p', {'class': "sidemeny2"}).find_all('a')]
		except ValueError:
			print("Warning: could not collect rider's years active.")
			self.years_active = []

	def _get_header_details(self):
		self.header_details = {}
		self.header_details['current_team'] = self.soup.p.text.strip() if self.soup.p.text.strip() else None
		self.header_details['twitter_handle'] = link_to_twitter_handle(self.soup.find('p', {'class': 'left'}).a) if self.soup.find('p', {'class': 'left'}) and self.soup.find('p', {'class': 'left'}).a else None
	
	def _get_sidebar_details(self):
		# Find table with rider details on right sidebar
		details_table = self.soup.find('table', {'class': 'tablesorter'})
		details_df = pd.read_html(str(details_table))[0]
		details = pd.Series(details_df.set_index('Information')['Information.1'])
		
		# Load details from table into attributes
		self.sidebar_details = {}
		self.sidebar_details['nation'] = details['Nationality']
		self.sidebar_details['date_of_birth'] = parse_date(details['Born'].rsplit(maxsplit=1)[0]) if 'Born' in details else None
		self.sidebar_details['height'] = float(details['Height'].rsplit(maxsplit=1)[0]) if 'Height' in details else None
		self.sidebar_details['WT_wins'] = int(details['WorldTour'].split()[0]) if 'WorldTour' in details else 0
		self.sidebar_details['UCI_wins'] = int(details['UCI'].split()[0]) if 'UCI' in details else 0
		self.sidebar_details['UCI_rank'] = int(details['UCI Ranking']) if 'UCI Ranking' in details else None
		self.sidebar_details['agency'] = details['Agency'] if 'Agency' in details else None

		# Load rider's strengths from details table
		if 'Strengths' in details:
			tr = details_table.find_all('tr')[-1]
			td = tr.find_all('td')[1]
			self.sidebar_details['strengths'] = [x.strip() for x in td if isinstance(x, bs4.element.NavigableString)]
		else:
			self.sidebar_details['strengths'] = []


class RiderYearResults(RiderEndpoint):
	"""
	Rider's results in a certain year. Extends RiderEndpoint.

	Attributes
	----------
	year_details : dict
		The year-specific rider details from the page, including the team, division, UCI points, and more.
	results_df : pd.DataFrame
		Table of rider's results from the year.
	"""

	def _parse_soup(self):
		super()._parse_soup()
		self._get_year_details()
		self._get_year_results()

	def _get_year_details(self):
		# Find table with details
		details_table = self.soup.find('table', {'class': 'tablesorter notOddEven'})

		spans = details_table.find_all('span')

		self.year_details = {}
		for span in spans:
			if span.img: # Team details
				self.year_details['Team'] = span.text.split('(')[0].strip()
				self.year_details['Team ID'] = team_link_to_id(span.a)
				self.year_details['Team Country'] = img_to_country_code(span.img)
				self.year_details['Division'] = span.text.split('(')[1].split(')')[0]
			elif 'Ranking' in span.text:
				self.year_details['UCI Ranking'] = int(span.text.split(': ')[1])
			elif 'Wins' in span.text:
				self.year_details['UCI Wins'] = int(span.text.split(': ')[1])
			elif 'Racedays' in span.text:
				self.year_details['Race days'] = int(span.text.split(': ')[1])
			elif 'Distance' in span.text:
				self.year_details['Distance'] = int(span.text.split(': ')[1].replace('.', '').split('km')[0])
		

	def _get_year_results(self):
		# Find table with results
		table = self.soup.find('table', {'class': "sortTabell tablesorter"})
		self.results_df = parse_table(table)