"""
author: Ethan Baron
"""

from .utilities import *


class RiderDetails:
    """
    Framework to store basic information about a particular rider.
    
    Attributes
    ----------
    id : int
        FirstCycling.com id for the rider used in the url
    name : str
        Full rider name
    nation : str
        Rider's nationality
    date_of_birth : datetime.date
        Date of rider's birth or None if not available
    current_team : str
        Current team of rider, or '' if no current team
    height : float
        Rider's height in meters or None if not available
    WT_wins : int
        Rider's number of World Tour wins
    UCI_wins : int
        Rider's number of UCI wins
    UCI_rank : int
        Rider's current UCI ranking or None if not available
    agency : str
        Agency representing the rider or None if not available
    twitter_handle : str
        The rider's Twitter handle or None if not available
    strengths : list[str]
        List of the rider's strengths, as listed by FirstCycling
    years_active : list[int]
        List of years for which rider results are available
    """

    def __init__(self, rider_id, soup=None, return_soup=False):
        """
        Parameters
        ----------
        rider_id : int
            FirstCycling.com id for the rider used in the url of their page
        soup : bs4.BeautifulSoup
            BeautifulSoup of page
        """
        
        # Load rider page
        if not soup:
            url = 'https://firstcycling.com/rider.php?r=' + str(rider_id)
            page = requests.get(url)
            soup = bs4.BeautifulSoup(page.text, 'html.parser')

        # Add basic rider information
        self.id = rider_id
        self.name = soup.h1.text
        self.current_team = soup.p.text.strip()
        self.current_team = soup.p.text.strip() if self.current_team else None
        self.twitter_handle = soup.find('p', {'class': 'left'}).a['href'].split('/')[3] if soup.find('p', {'class': 'left'}) else None
        
        # Find table with rider details on right sidebar
        details_table = soup.find('table', {'class': 'tablesorter notOddEven'})
        details_df = pd.read_html(str(details_table))[0]
        details = pd.Series(details_df.set_index(0)[1])
        
        # Load details from table into attributes
        self.nation = details['Nationality']
        self.date_of_birth = parse(details['Born'].rsplit(maxsplit=1)[0]).date() if 'Born' in details else None
        self.height = float(details['Height'].rsplit(maxsplit=1)[0]) if 'Height' in details else None
        self.WT_wins = int(details['WorldTour'].split()[0]) if 'WorldTour' in details else 0
        self.UCI_wins = int(details['UCI'].split()[0]) if 'UCI' in details else 0
        self.UCI_rank = int(details['UCI Ranking']) if 'UCI Ranking' in details else None
        self.agency = details['Agency'] if 'Agency' in details else None

        # Load rider's strengths from details table
        if 'Strengths' in details:
            tr = details_table.find_all('tr')[-1]
            td = tr.find_all('td')[1]
            self.strengths = [x.strip() for x in td if isinstance(x, bs4.element.NavigableString)]
        else:
            self.strengths = []
        
        # Get list of all years for which results available
        years = [o['value'] for o in soup.find('select').find_all('option')]
        self.years_active = [int(y) for y in years if y]

    def __str__(self):
        return self.name

    def __repr__(self):
        return "RiderDetails(" + str(self.id) + ", " + self.name + ")"

    def to_json(self):
        d = vars(self).copy()
        d['date_of_birth'] = str(d['date_of_birth']) if d['date_of_birth'] else None
        return d

    def get_json(self):
        return json.dumps(self, default=ComplexHandler)


class RiderYearDetails:
    """
    Framework to store general information about a particular rider in a particular season.
    
    Attributes
    ----------
    rider_id : int
        FirstCycling.com id for the rider used in the url
    year : int
        Year data represents
    name : str
        Full rider name
    team : str
        Team of rider in specific year or None if no team
    division : str
        Team's division in that season or None if not available
    UCI_rank : int
        Rider's UCI ranking in that season or None if not available
    UCI_points : int
        Rider's UCI points accumulated in that season or 0 if not available
    UCI_wins : int
        Rider's number of UCI wins in that season or None if not available
    race_days : int
        Rider's number of race days in that season or 0 if not available
    race_kms : int
        Distance covered by rider in races that season, in kilometers, or 0 if not available
    """
    
    def __init__(self, rider_id, year, soup=None):
        """
        Parameters
        ----------
        rider_id : int
            FirstCycling.com id for the rider used in the url of their page
        year : int
            Year for which to collect details
        soup : bs4.BeautifulSoup
            BeautifulSoup of page
        """

        # Load rider page
        if not soup:
            url = 'https://firstcycling.com/rider.php?r=' + str(rider_id) + '&y=' + str(year)
            page = requests.get(url)
            soup = bs4.BeautifulSoup(page.text, 'html.parser')

        self.rider_id = rider_id
        self.year = int(soup.find_all('h1')[1].text)
        self.name = soup.h1.text

        # Parse table with details
        details_table = soup.find('table', {'class': 'tablesorter notOddeven'})
        if details_table:
            rider_year_details = [s.strip() for s in details_table.text.replace('\n', '|').split('|') if s.strip()]
            rider_year_details = [x.split(':') if ':' in x else ['UCI Points', x.split()[0].replace('.', '')] for x in rider_year_details]
            rider_year_details = dict(rider_year_details)
        else:
            rider_year_details = {}

        # Load attributes
        self.team = rider_year_details['Team'].strip() if 'Team' in rider_year_details else None
        self.division = rider_year_details['Division'].strip() if 'Division' in rider_year_details else None
        self.UCI_rank = int(rider_year_details['UCI Ranking']) if 'UCI Ranking' in rider_year_details else None
        self.UCI_points = int(rider_year_details['UCI Points']) if 'UCI Points' in rider_year_details and rider_year_details['UCI Points'].strip() else 0
        self.UCI_wins = int(rider_year_details['UCI Wins'].replace('-', '0')) if 'UCI Wins' in rider_year_details and rider_year_details['UCI Wins'].strip() else 0
        self.race_days = int(rider_year_details['Race days'].replace('-', '0')) if 'Race days'in rider_year_details and rider_year_details['Race days'].strip() else 0
        self.race_kms = int(rider_year_details['Distance'].split()[0].replace('.', '').replace('-', '0')) if 'Distance' in rider_year_details else 0
            
    
    def __str__(self):
        return self.name + " (" + str(self.year) + ")"

    def __repr__(self):
        return "RiderYearDetails(" + str(self.rider_id) + ", " + self.name + ", " + str(self.year) + ")"

    def to_json(self):
        d = vars(self).copy()
        return d

    def get_json(self):
        return json.dumps(self, default=ComplexHandler)