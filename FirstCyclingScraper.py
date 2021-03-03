"""
author: Ethan Baron

This file provides tools used to collect data from FirstCycling.com.
"""

import requests
import bs4
import pandas as pd
from dateutil.parser import parse

class YearDetails:
    """
    Framework to store information about a particular rider.
    
    Attributes
    ----------
    team : str
        Team of rider in specific year or None if no team
    division : str
        Team's division in that season or None if not available
    UCI_rank : int
        Rider's UCI ranking in that season or None if not available
    UCI_points : int
        Rider's UCI points accumulated in that season or None if not available
    UCI_rank : int
        Rider's number of UCI wins in that season or None if not available
    race_days : int
        Rider's number of race days in that season or None if not available
    race_kms : int
        Distance covered by rider in races that season in kilometers or None if not available
    """
    
    def __init__(self, table):
        """
        Parameters
        ----------
        table : bs4.element.Tag
            Table containing year information of rider
        """
        
        if table:
            rider_year_details = [s.strip() for s in table.text.replace('\n', '|').split('|') if s.strip()]
            rider_year_details = [x.split(':') if ':' in x else ['UCI Points', x.split()[0].replace('.', '')] for x in rider_year_details]
            rider_year_details = dict(rider_year_details)

            self.team = rider_year_details['Team'].strip() if 'Team' in rider_year_details else None
            self.division = rider_year_details['Division'] if 'Division' in rider_year_details else None
            self.UCI_rank = int(rider_year_details['UCI Ranking']) if 'UCI Ranking' in rider_year_details else None
            self.UCI_points = int(rider_year_details['UCI Points']) if 'UCI Points' in rider_year_details and rider_year_details['UCI Points'].strip() else None
            self.UCI_wins = int(rider_year_details['UCI Wins'].replace('-', '0')) if 'UCI Wins' in rider_year_details and rider_year_details['UCI Wins'].strip() else None
            self.race_days = int(rider_year_details['Race days'].replace('-', '0')) if 'Race days'in rider_year_details and rider_year_details['Race days'].strip() else None
            self.race_kms = int(rider_year_details['Distance'].split()[0].replace('.', '').replace('-', '0')) if 'Distance' in rider_year_details else None
        
        else:
            self.team = None
            self.division = None
            self.UCI_rank = None
            self.UCI_points = None
            self.UCI_wins = None
            self.race_days = None
            self.race_kms = None
    
    def __str__(self):
        return str(vars(self))

    def __repr__(self):
        return str(vars(self))
     
        
class Rider:
    """
    Framework to store information about a particular rider.
    
    Attributes
    ----------
    id : int
        FirstCycling.com id for the rider used in the url
    name : str
        Full rider name
    current_team : str
        Current team of rider
    nation : str
        Rider's nationality
    date_of_birth : datetime.datetime
        Date of rider's birth
    height : float
        Rider's height in meters or None if not available
    WT_detail : str
        WorldTour detail provided for rider or None if not available
    UCI_detail : str
        UCI detail provided for rider or None if not available
    UCI_rank : int
        Rider's current UCI ranking or None if not available
    agency : str
        Agency representing the rider or None if not available
    strengths : list[str]
        List of the rider's strengths, as determined by FirstCycling
    year_details : dict[int, YearDetails]
        Dictionary mapping years to YearDetails object including rider's details for that year
    """

    def __init__(self, rider_id):
        """
        Parameters
        ----------
        rider_id : int
            FirstCycling.com id for the rider used in the url of their page
        """
        
        url = 'https://firstcycling.com/rider.php?r=' + str(rider_id)
        page = requests.get(url)
        soup = bs4.BeautifulSoup(page.text, 'html.parser')
        
        # Add basic rider information
        self.id = rider_id
        self.name = soup.h1.text
        self.current_team = soup.p.text.strip()
        
        # Find table with rider details on right sidebar
        details_table = soup.find('table', {'class': 'tablesorter notOddEven'})
        details_df = pd.read_html(str(details_table))[0]
        details = pd.Series(details_df.set_index(0)[1])
        
        # Load details from table into attributes
        self.nation = details['Nationality']
        self.date_of_birth = parse(details['Born'].rsplit(maxsplit=1)[0]) #datetime
        self.height = float(details['Height'].rsplit(maxsplit=1)[0]) if 'Height' in details else None
        self.WT_detail = details['WorldTour'] if 'WorldTour' in details else None
        self.UCI_detail = details['UCI'] if 'UCI' in details else None
        self.UCI_rank = int(details['UCI Ranking']) if 'UCI Ranking' in details else None
        self.agency = details['Agency'] if 'Agency' in details else None

        tr = details_table.find_all('tr')[-1]
        if 'Strengths' in tr.find('td'):
            td = tr.find_all('td')[1]
            self.strengths = [x.strip() for x in td if isinstance(x, bs4.element.NavigableString)]
        else:
            self.strengths = []
        
        # Get list of years for which results are available
        years = [o['value'] for o in soup.find('select').find_all('option')]
        years = [int(y) for y in years if y]

        # Load year-by-year details
        self.year_details = {}
        for year in years:
            self.add_year_details(year)


    def add_year_details(self, year):
        """ Add year-by-year details for rider.

        Parameters
        ----------
        year : int
            Year for which to collect details.
        """
        url = 'https://firstcycling.com/rider.php?r=' + str(self.id) + '&y=' + str(year)
        page = requests.get(url)
        soup = bs4.BeautifulSoup(page.text, 'html.parser')
        rider_year_details_table = soup.find('table', {'class': 'tablesorter notOddeven'})
        self.year_details[year] = YearDetails(rider_year_details_table)

    def __str__(self):
        return self.name

    def __repr__(self):
        return (self.id, self.name)