from .utilities import *
from .race_edition import RaceEdition

# Endpoints ----
class RaceEndpoint(Endpoint):
	base_url = 'https://firstcycling.com/race.php'

	def _get_header_details(self):
		soup = bs4.BeautifulSoup(self.response, 'html.parser')
		header_details = {}
		header_details['name'] = soup.h1.text
		header_details['links'] = {a.img['src'].rsplit('/', maxsplit=1)[1][:-7]: a['href'] for a in soup.h1.parent.find_all('a')}
		if 'www' in header_details['links']:
			header_details['links']['website'] = header_details['links'].pop('www')
		return header_details

	def _get_editions(self):
		soup = bs4.BeautifulSoup(self.response, 'html.parser')
		return [int(o['value']) for o in soup.find('select').find_all('option') if o['value']]

class RaceOverview(RaceEndpoint):
	def __init__(self, race_id, classification_num=None):
		params = {'r': race_id, 'k': classification_num}
		self.make_request(params)

class RaceYearByYear(RaceEndpoint):
	def __init__(self, race_id, classification_num=None):
		params = {'r': race_id, 'k': 'X', 'j': classification_num}
		self.make_request(params)

class RaceVictoryTable(RaceEndpoint):
	def __init__(self, race_id):
		params = {'r': race_id, 'k': 'W'}
		self.make_request(params)

class RaceStageVictories(RaceEndpoint):
	def __init__(self, race_id):
		params = {'r': race_id, 'k': 'Z'}
		self.make_request(params)

class RaceYoungestOldestWinners(RaceEndpoint):
	def __init__(self, race_id):
		params = {'r': race_id, 'k': 'Y'}
		self.make_request(params)

# Race ----
class Race(FirstCyclingObject):
	def __init__(self, race_id):
		self.ID = race_id
		self.header_details = None
		self.edition_years = None
		self.editions = {}

	def _get_general_info(self, endpoint):
		if not self.header_details:
			self.header_details = endpoint._get_header_details()
			self.edition_years = endpoint._get_editions()

	def get_overview(self, classifications=[0]):
		for classification_num in classifications:
			self._get_endpoint(RaceOverview, 'overview', classification_num, classification_num)

	def get_year_by_year(self, classifications=[0]):
		for classification_num in classifications:
			self._get_endpoint(RaceYearByYear, 'year_by_year', classification_num, classification_num)

	def get_victory_table(self):
		return self._get_endpoint(RaceVictoryTable, 'victory_table')

	def get_stage_victories(self):
		return self._get_endpoint(RaceStageVictories, 'stage_victories')

	def get_youngest_oldest_winners(self):
		return self._get_endpoint(RaceYoungestOldestWinners, 'youngest_oldest_winners')

	def add_edition(self, year, edition):
		self.editions[year] = edition

	def get_edition(self, year):
		if year in self.editions:
			return self.editions[year]
		else:
			self.editions[year] = RaceEdition(self.ID, year)
			return self.editions[year]