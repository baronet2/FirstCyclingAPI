from ..endpoints import ParsedEndpoint
from ..parser import parse_date

import pandas as pd
import bs4

class RiderEndpoint(ParsedEndpoint):
	def _parse_soup(self):
		self._get_years_active()
		self._get_header_details()
		self._get_sidebar_details()

	def _get_years_active(self):
		return [int(o['value']) for o in self.soup.find('select').find_all('option') if o['value']]

	def _get_header_details(self):
		self.header_details = {}
		self.header_details['current_team'] = self.soup.p.text.strip() if self.soup.p.text.strip() else None
		self.header_details['twitter_handle'] = self.soup.find('p', {'class': 'left'}).a['href'].split('/')[3] if self.soup.find('p', {'class': 'left'}).a else None
	
	def _get_sidebar_details(self):
		# Find table with rider details on right sidebar
		details_table = self.soup.find('table', {'class': 'tablesorter notOddEven'})
		details_df = pd.read_html(str(details_table))[0]
		details = pd.Series(details_df.set_index(0)[1])
		
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