from .utilities import *

# Endpoints ----
class RiderEndpoint(Endpoint):
	base_url = 'https://firstcycling.com/rider.php'

	def _get_years_active(self):
		soup = bs4.BeautifulSoup(self.response, 'html.parser')
		return [int(o['value']) for o in soup.find('select').find_all('option') if o['value']]

	def _get_header_details(self):
		soup = bs4.BeautifulSoup(self.response, 'html.parser')
		header_details = {}
		header_details['name'] = soup.h1.text
		header_details['current_team'] = soup.p.text.strip() if soup.p.text.strip() else None
		header_details['twitter_handle'] = soup.find('p', {'class': 'left'}).a['href'].split('/')[3] if soup.find('p', {'class': 'left'}).a else None
		return header_details
	
	def _get_sidebar_details(self):
		soup = bs4.BeautifulSoup(self.response, 'html.parser')

		# Find table with rider details on right sidebar
		details_table = soup.find('table', {'class': 'tablesorter notOddEven'})
		details_df = pd.read_html(str(details_table))[0]
		details = pd.Series(details_df.set_index(0)[1])
		
		# Load details from table into attributes
		sidebar_details = {}
		sidebar_details['nation'] = details['Nationality']
		sidebar_details['date_of_birth'] = parse_date(details['Born'].rsplit(maxsplit=1)[0]) if 'Born' in details else None
		sidebar_details['height'] = float(details['Height'].rsplit(maxsplit=1)[0]) if 'Height' in details else None
		sidebar_details['WT_wins'] = int(details['WorldTour'].split()[0]) if 'WorldTour' in details else 0
		sidebar_details['UCI_wins'] = int(details['UCI'].split()[0]) if 'UCI' in details else 0
		sidebar_details['UCI_rank'] = int(details['UCI Ranking']) if 'UCI Ranking' in details else None
		sidebar_details['agency'] = details['Agency'] if 'Agency' in details else None

		# Load rider's strengths from details table
		if 'Strengths' in details:
			tr = details_table.find_all('tr')[-1]
			td = tr.find_all('td')[1]
			sidebar_details['strengths'] = [x.strip() for x in td if isinstance(x, bs4.element.NavigableString)]
		else:
			sidebar_details['strengths'] = []

		return sidebar_details

class RiderYearResults(RiderEndpoint):
	def __init__(self, rider_id, year=None):
		params = {'r': rider_id, 'y': year}
		self.make_request(params)

		self.soup = bs4.BeautifulSoup(self.response, 'html.parser')
		self.year = int(self.soup.find('option', selected=True)['value'])
		self._get_year_details()
		self._get_year_results()
		del self.soup

	def _get_year_details(self):
		# Find table with details
		details_table = self.soup.find('table', {'class': 'tablesorter notOddeven'})

		# Parse table with details
		if details_table:
			rider_year_details = [s.strip() for s in details_table.text.replace('\n', '|').split('|') if s.strip()]
			rider_year_details = [x.split(':') if ':' in x else ['UCI Points', x.split()[0].replace('.', '')] for x in rider_year_details]
			rider_year_details = dict(rider_year_details)
		else:
			rider_year_details = {}

		# Load attributes
		self.year_details = {}
		self.year_details['Team'] = rider_year_details['Team'].strip() if 'Team' in rider_year_details else None
		self.year_details['Division'] = rider_year_details['Division'].strip() if 'Division' in rider_year_details else None
		self.year_details['UCI Ranking'] = int(rider_year_details['UCI Ranking']) if 'UCI Ranking' in rider_year_details else None
		self.year_details['UCI Points'] = int(rider_year_details['UCI Points']) if 'UCI Points' in rider_year_details and rider_year_details['UCI Points'].strip() else 0
		self.year_details['UCI Wins'] = int(rider_year_details['UCI Wins'].replace('-', '0')) if 'UCI Wins' in rider_year_details and rider_year_details['UCI Wins'].strip() else 0
		self.year_details['Race days'] = int(rider_year_details['Race days'].replace('-', '0')) if 'Race days'in rider_year_details and rider_year_details['Race days'].strip() else 0
		self.year_details['Distance'] = int(rider_year_details['Distance'].split()[0].replace('.', '').replace('-', '0')) if 'Distance' in rider_year_details else 0

	def _get_year_results(self):
		# Find table with results
		table = self.soup.find('table', {'class': "sortTabell tablesorter"})
		self.results_df = table_parser(table)

class RiderBestResults(RiderEndpoint):
	def __init__(self, rider_id):
		params = {'r': rider_id, 'high': 1}
		self.make_request(params)

class RiderVictories(RiderEndpoint):
	def __init__(self, rider_id, uci=0):
		params = {'r': rider_id, 'high': 1, 'k': 1, 'uci': uci}
		self.make_request(params)

class RiderMonumentResults(RiderEndpoint):
	def __init__(self, rider_id):
		params = {'r': rider_id, 'high': 1, 'k': 3}
		self.make_request(params)

class RiderRaceHistory(RiderEndpoint):
	def __init__(self, rider_id, race_id):
		params = {'r': rider_id, 'ra': race_id}
		self.make_request(params)

class RiderTeamAndRanking(RiderEndpoint):
	def __init__(self, rider_id):
		params = {'r': rider_id, 'stats': 1}
		self.make_request(params)

class RiderRaceHistory(RiderEndpoint):
	def __init__(self, rider_id):
		params = {'r': rider_id, 'stats': 1, 'k': 1}
		self.make_request(params)

class RiderOneDayRaces(RiderEndpoint):
	def __init__(self, rider_id):
		params = {'r': rider_id, 'stats': 1, 'k': 2}
		self.make_request(params)

class RiderStageRaces(RiderEndpoint):
	def __init__(self, rider_id):
		params = {'r': rider_id, 'stats': 1, 'k': 3}
		self.make_request(params)

class RiderTeams(RiderEndpoint):
	def __init__(self, rider_id):
		params = {'r': rider_id, 'teams': 1}
		self.make_request(params)


# Rider ----
class Rider(FirstCyclingObject):
	def __init__(self, rider_id):
		self.ID = rider_id
		self.header_details = None
		self.sidebar_details = None
		self.years_active = None
		self.results = {}
		self.race_history = {}

	def _get_general_info(self, endpoint):
		if not self.header_details:
			self.header_details = endpoint._get_header_details()
			self.sidebar_details = endpoint._get_sidebar_details()
			self.years_active = endpoint._get_years_active()

	def get_years(self, years=None):
		if years is None:
			if not self.years_active: # Get first unloaded year
				self.get_year()
			years = [year for year in self.years_active if year not in self.results]
		for year in years:
			self.get_year(year)

	def get_year(self, year=None):
		""" If None, loads most recent unloaded year. """
		if year:
			return self._get_endpoint(RiderYearResults, 'results', year, year)
		elif self.years_active: # Get first unloaded year
			year = [year for year in self.years_active if year not in self.results][0]
			return self._get_endpoint(RiderYearResults, 'results', year, year)
		else:
			year_results = RiderYearResults(self.ID)
			self.results[year_results.year] = year_results
			self._get_general_info(year_results)
			return year_results

	def get_best_results(self):
		return self._get_endpoint(RiderBestResults, 'best_results')

	def get_victories(self):
		return self._get_endpoint(RiderVictories, 'victories')

	def get_uci_victories(self):
		return self._get_endpoint(RiderVictories, 'uci_victories', uci=1)

	def get_monument_results(self):
		return self._get_endpoint(RiderMonumentResults, 'monument_results')

	def get_race_history(self, race_id):
		return self._get_endpoint(RiderRaceHistory, 'race_history', race_id, race_id)

	def get_team_and_ranking(self):
		return self._get_endpoint(RiderTeamAndRanking, 'team_and_ranking')

	def get_race_history(self):
		return self._get_endpoint(RiderRaceHistory, 'race_history')

	def get_one_day_races(self):
		return self._get_endpoint(RiderOneDayRaces, 'one_day_races')

	def get_stage_races(self):
		return self._get_endpoint(RiderStageRaces, 'stage_races')

	def get_teams(self):
		return self._get_endpoint(RiderTeams, 'teams')