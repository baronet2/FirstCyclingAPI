from .utilities import *

# Race Endpoints ----
class RaceEndpoint(Endpoint):
	base_url = 'https://firstcycling.com/race.php'

	def _get_header_details(self):
		soup = bs4.BeautifulSoup(self.response, 'html.parser')
		header_details = {}
		header_details['name'] = soup.h1.text.rsplit(' - ', maxsplit=1)[0] # Get race name, excluding year
		header_details['links'] = {a.img['src'].rsplit('/', maxsplit=1)[1][:-7]: a['href'] for a in soup.h1.parent.find_all('a')}
		if 'www' in header_details['links']:
			header_details['links']['website'] = header_details['links'].pop('www')
		return header_details

	def _get_editions(self):
		soup = bs4.BeautifulSoup(self.response, 'html.parser')
		return [int(o['value']) for o in soup.find('select', {'name': 'y'}).find_all('option') if o['value']]

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
		self.soup = bs4.BeautifulSoup(self.response, 'html.parser')
		self._get_victory_table()
		del self.soup

	def _get_victory_table(self):
		victory_table = self.soup.find('table', {'class': 'tablesorter'})
		self.table = table_parser(victory_table)

class RaceStageVictories(RaceEndpoint):
	def __init__(self, race_id):
		params = {'r': race_id, 'k': 'Z'}
		self.make_request(params)

class RaceYoungestOldestWinners(RaceEndpoint):
	def __init__(self, race_id):
		params = {'r': race_id, 'k': 'Y'}
		self.make_request(params)

# Race Edition Endpoints ----
class RaceEditionInformation(RaceEndpoint):
	def __init__(self, race_id, year):
		params = {'r': race_id, 'y': year, 'k': 2}
		self.make_request(params)

class RaceEditionResults(RaceEndpoint):
	def __init__(self, race_id, year, classification_num=None, stage_num=None):
		params = {'r': race_id, 'y': year, 'l': classification_num, 'e': stage_num}
		self.make_request(params)
		self.soup = bs4.BeautifulSoup(self.response, 'html.parser')
		self._get_results_table()
		self._get_sidebar_information()
		del self.soup

	def _get_results_table(self):
		results_table = self.soup.find('table', {'class': 'sortTabell tablesorter'})
		self.results_table = table_parser(results_table)

	def _get_sidebar_information(self):
		return

class RaceEditionStageProfiles(RaceEndpoint):
	def __init__(self, race_id, year):
		params = {'r': race_id, 'y': year, 'e': 'all'}
		self.make_request(params)

class RaceEditionStartlistNormal(RaceEndpoint):
	def __init__(self, race_id, year):
		params = {'r': race_id, 'y': year, 'k': 8}
		self.make_request(params)

class RaceEditionStartlistExtended(RaceEndpoint):
	def __init__(self, race_id, year):
		params = {'r': race_id, 'y': year, 'k': 9}
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

	def _get_edition_endpoint(self, endpoint, year, destination_key, *args, **kwargs):
		""" Generalized method to load endpoints for race edition """
		endpoint = endpoint(self.ID, year, *args, **kwargs)
		self._get_general_info(endpoint)
		if year in self.editions:
			self.editions[year][destination_key] = endpoint
		else:
			self.editions[year] = {destination_key: endpoint}
		return endpoint

	def get_edition_information(self, year):
		return self._get_edition_endpoint(RaceEditionInformation, year, 'information')

	def get_edition_results(self, year, classification_num=None, stage_num=None): # Also upddate information from right sidebar if missing
		return self._get_edition_endpoint(RaceEditionResults, year, 'results', classification_num=classification_num, stage_num=stage_num)

	def get_edition_stage_profiles(self, year):
		self._get_edition_endpoint(RaceEditionStageProfiles, year, 'stage_profiles')

	def get_edition_startlist_normal(self, year):
		self._get_edition_endpoint(RaceEditionStartlistNormal, year, 'startlist_normal')

	def get_edition_startlist_extended(self, year):
		self._get_edition_endpoint(RaceEditionStartlistExtended, year, 'startlist_extended')