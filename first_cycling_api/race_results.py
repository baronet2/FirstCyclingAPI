"""
author: Ethan Baron
"""

from .utilities import *


class RaceResults:
	"""
	A framework to store Results from a race edition.

	Attributes
	----------
	url : str
		The url for the race results page
	race_id : int
		The firstcycling.com ID for the race
	classification : str
		The name of the classification for which results are loaded
	race_name : str
		The name of the race
	year : int
		The year for the race edition
	links : dict {str : str}
		A dictionary of external links for the race's social media and website, where available
	nation : str
		Three-letter code for country in which race took place
	start_city : str
		City in which race started, if available
	end_city : str
		City in which race ended, if available
	start_date : datetime.date
		The date on which the race started
	end_date : datetime.date
		The date on which the race ended. If the race is a one-day race, this will be the same as start_date
	distance : float
		The race distance in kilometres or None if not available
	cat : str
		The race category or None if not available
	profile : str
		The race profile or None if not available
	df : pd.DataFrame
		A dataframe containing the results from the race, or None if there is no data for that page
	stage_num : int
		The stage number or None if not applicable. 0 indicates prologue.
	classification_leaders : dict {str : int}
		A dictionary mapping classification to the rider ID of the leader after the stage, if applicable
		For 'Combative', shows the rider ID for the rider who won the combative award in the stage.
	standings : dict {str : pandas.DataFrame}
		A dictionary mapping classifications to a pandas DataFrame containing the standings for the classification after the stage, if applicable
	"""

	def __init__(self, url=None, race_id=None, year=None, classification_num=None, stage_num=None):
		"""
		Initialize a RaceResults object.

		Arguments
		---------
		url : str
			url for race results page
			If url is provided, all other arguments are ignored
		race_id : int
			The firstcycling.com ID for the race
		year : int
			The year for the edition of interest
		classification_num : int
			The argument apssed to the 'l' argument in the URL
			{1: 'GC', 2: 'Youth', 3: 'Points', 4: 'Mountain', 7: 'Combined'}
		stage_num : int
			The stage number for the stage of interest
		"""

		if not url: # Prepare URL with appropriate headers
			if not race_id or not year:
				raise TypeError('Must provide url or both race_id and year.')

			url = "https://firstcycling.com/race.php?r=" + str(race_id) + '&y=' + str(year)
			url += '&l=' + str(classification_num) if classification_num else ''
			url += '&e=' + str(stage_num) if stage_num else ''

		# Load webpage
		self.url = url
		page = requests.get(url)
		soup = bs4.BeautifulSoup(page.text, 'html.parser')

		# Get race information from header
		self.race_id = int(url.split('r=')[1].split('&')[0])
		self.race_name, self.year = tuple(soup.h1.text.rsplit(' - ', maxsplit=1))
		self.year = int(self.year)
		self.links = {a.img['src'].rsplit('/', maxsplit=1)[1][:-7]: a['href'] for a in soup.h1.parent.find_all('a')}
		if 'www' in self.links:
			self.links['website'] = self.links.pop('www')

		# Parse results table
		results_table = soup.find('table', {'class': 'sortTabell2 tablesorter'})
		if not results_table:
			results_table = soup.find('table', {'class': 'sortTabell tablesorter'})
		self.df = table_of_riders_to_df(results_table)

		# Classification name
		self.classification = soup.find('li', {'class': 'current'}).text if soup.find('li', {'class': 'current'}) else None

		# Standings after stage
		divs = soup.find_all('div', {'class': "tab-content dummy"})
		self.standings = {div['id']: table_of_riders_to_df(div.table) for div in divs}

		# Load information on right sidebar
		info_table = soup.find('table', {'class': 'tablesorter notOddEven'})
		details_df = pd.read_html(str(info_table))[0]
		details = pd.Series(details_df['Information.1'].values, index=details_df['Information'])
		soup_details = pd.Series(info_table.find_all('tr')[1:], index=details.index)

		# Get nation and start/end cities
		self.nation = img_to_country_code(soup_details['Nation' if 'Nation' in details.index else 'Where'].img)

		if 'Where' in details.index:
			if ' -> ' in details['Where']:
				self.start_city, self.end_city = details['Where'].split(' -> ')
			else:
				self.start_city = self.end_city = details['Where']
		else:
			self.start_city = self.end_city = None

		if 'Nation' in details.index and len(soup_details['Nation'].find_all('img')) > 1: # Edge case: olympic games
			self.nation = img_to_country_code(soup_details['Nation'].find_all('img')[-1])
			self.start_city = self.end_city = soup_details['Nation'].find_all('img')[-1].next_sibling.strip()

		# Get date
		if 'Date' in details.index:
			if ' - ' in details['Date']:
				self.start_date, self.end_date = tuple([parse(x + ', ' + str(self.year)).date() for x in details['Date'].split(' - ')])
			else:
				self.start_date = self.end_date = parse(details['Date'] + ', ' + str(self.year)).date()
		else:
			self.start_date = self.end_date = None

		# Get additional race information
		self.distance = float(details['Distance'].split()[0]) if 'Distance' in details.index else None
		self.cat = details['CAT'] if 'CAT' in details.index else None
		self.stage_num = int(''.join([x for x in details['What'] if x.isnumeric()])) if 'What' in details.index else None
		
		if 'What' in details.index and 'Prologue' in details['What']:
			self.stage_num = 0

		# Find profile information
		self.profile = None
		if 'Distance' in details.index:
			self.profile = img_to_profile(soup_details['Distance'].img) if soup_details['Distance'].img else None
		elif 'What' in details.index:
			self.profile = img_to_profile(soup_details['What'].img) if soup_details['What'].img else None

		# Classification leaders after stage
		self.classification_leaders = {}
		for classification in ['Leader', 'Youth', 'Points', 'Mountain', 'Combative']: # TODO Any others?
			if classification in details:
				self.classification_leaders[classification] = rider_link_to_id(soup_details[classification].a) # TODO save as Rider without loading page?

	def __repr__(self):
		return "Results(" + self.race_name + ", " + str(self.year) + ")"

	def get_json(self):
		return json.dumps(self, default=ComplexHandler)

	def to_json(self):
		d = vars(self).copy()
		d['start_date'] = str(d['start_date'])
		d['end_date'] = str(d['end_date'])
		d['df'] = self.df.to_json() if self.df is not None else None
		d['standings'] = {k: v.to_json() for k, v in d['standings'].items()}
		return d