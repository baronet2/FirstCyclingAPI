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
	params = {'k': 0}

class RaceYearByYear(RaceEndpoint):
	params = {'k': 'X', 'j': 0}

class RaceVictoryTable(ParsedEndpoint, RaceEndpoint):
	params = {'k': 'W'}

	def parse_soup(self):
		self._get_victory_table()

	def _get_victory_table(self):
		victory_table = self.soup.find('table', {'class': 'tablesorter'})
		self.table = parse_table(victory_table)

class RaceStageVictories(RaceEndpoint):
	params = {'k': 'Z'}

class RaceYoungestOldestWinners(RaceEndpoint):
	params = {'k': 'Y'}

# Race Edition Endpoints ----
class RaceEditionInformation(RaceEndpoint):
	params = {'k': 2}

class RaceEditionResults(ParsedEndpoint, RaceEndpoint):
	params = {'l': None, 'e': None}

	def parse_soup(self):
		self._get_results_table()
		self._get_sidebar_information()

	def _get_results_table(self):
		results_table = self.soup.find('table', {'class': 'sortTabell tablesorter'})
		if not results_table:
			results_table = self.soup.find('table', {'class': 'sortTabell2 tablesorter'})
		self.results_table = parse_table(results_table)

		# Load all classification standings after stage
		divs = self.soup.find_all('div', {'class': "tab-content dummy"})
		self.standings = {div['id']: parse_table(div.table) for div in divs}

	def _get_sidebar_information(self):
		return

class RaceEditionStageProfiles(RaceEndpoint):
	params = {'e': 'all'}

class RaceEditionStartlistNormal(RaceEndpoint):
	params = {'k': 8}

class RaceEditionStartlistExtended(RaceEndpoint):
	params = {'k': 9}

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

	def _prepare_endpoint_params(self, kwargs):
		kwargs['r'] = self.ID
		return kwargs

	def get_overview(self, classifications=[0]):
		for classification_num in classifications:
			self._get_endpoint(RaceOverview, 'overview', classification_num, k=classification_num)

	def get_year_by_year(self, classifications=[0]):
		for classification_num in classifications:
			self._get_endpoint(RaceYearByYear, 'year_by_year', classification_num, j=classification_num)

	def get_victory_table(self):
		return self._get_endpoint(RaceVictoryTable, 'victory_table')

	def get_stage_victories(self):
		return self._get_endpoint(RaceStageVictories, 'stage_victories')

	def get_youngest_oldest_winners(self):
		return self._get_endpoint(RaceYoungestOldestWinners, 'youngest_oldest_winners')

	def _get_edition_endpoint(self, year, method, **kwargs):
		""" Generalized method to load endpoints for race edition """
		if year not in self.editions:
			self.editions[year] = RaceEdition(self.ID, year)
		return method(self.editions[year], **kwargs)

	def get_edition_information(self, year):
		return self._get_edition_endpoint(year, RaceEdition.get_information)

	def get_edition_results(self, year, classification_num=None, stage_num=None): # Also update information from right sidebar if missing
		return self._get_edition_endpoint(year, RaceEdition.get_results, classification_num=classification_num, stage_num=stage_num)

	def get_edition_stage_profiles(self, year):
		return self._get_edition_endpoint(year, RaceEdition.get_stage_profiles)

	def get_edition_startlist_normal(self, year):
		return self._get_edition_endpoint(year, RaceEdition.get_startlist_normal)

	def get_edition_startlist_extended(self, year):
		return self._get_edition_endpoint(year, RaceEdition.get_startlist_extended)


# RaceEdition ----
class RaceEdition(FirstCyclingObject):
	def __init__(self, race_id, year):
		self.ID = race_id
		self.year = year

	def _prepare_endpoint_params(self, kwargs):
		kwargs['r'] = self.ID
		kwargs['y'] = self.year
		return kwargs

	def get_information(self):
		return self._get_endpoint(RaceEditionInformation, 'information')

	def get_results(self, classification_num=None, stage_num=None): # Also update information from right sidebar if missing
		key = 'results' + ('_' + classifications[classification_num] if classification_num else ('_stage_' + str(stage_num) if stage_num else ''))
		return self._get_endpoint(RaceEditionResults, key, l=classification_num, e=stage_num)

	def get_stage_profiles(self):
		self._get_endpoint(RaceEditionStageProfiles, 'stage_profiles')

	def get_startlist_normal(self):
		self._get_endpoint(RaceEditionStartlistNormal, 'startlist_normal')

	def get_startlist_extended(self):
		self._get_endpoint(RaceEditionStartlistExtended, 'startlist_extended')