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
        Distance covered by rider in races that season, in kilometers or None if not available
    """
    
    def __init__(self, table):
        """
        Parameters
        ----------
        table : bs4.element.Tag
            Table containing year information of rider
            If table not on page, pass None and YearDetails will load with default values
        """
        
        if table:
            rider_year_details = [s.strip() for s in table.text.replace('\n', '|').split('|') if s.strip()]
            rider_year_details = [x.split(': ') if ': ' in x else ['UCI Points', x.split()[0].replace('.', '')] for x in rider_year_details]
            rider_year_details = dict(rider_year_details)

            self.team = rider_year_details['Team'].strip() if 'Team' in rider_year_details else None
            self.division = rider_year_details['Division'] if 'Division' in rider_year_details else None
            self.UCI_rank = int(rider_year_details['UCI Ranking']) if 'UCI Ranking' in rider_year_details else None
            self.UCI_points = int(rider_year_details['UCI Points']) if 'UCI Points' in rider_year_details else None
            self.UCI_wins = int(rider_year_details['UCI Wins']) if 'UCI Wins' in rider_year_details else None
            self.race_days = int(rider_year_details['Race days']) if 'Race days' in rider_year_details else None
            self.race_kms = int(rider_year_details['Distance'].split()[0].replace('.', '')) if 'Distance' in rider_year_details else None
        
        else:
            self.team = None
            self.division = None
            self.UCI_rank = None
            self.UCI_points = None
            self.UCI_wins = None
            self.race_days = None
            self.race_kms = None

        
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
        Rider's height, in meters
    WT_detail : str
        WorldTour detail provided for rider
    UCI_detail : str
        UCI detail provided for rider
    UCI_rank : int
        Rider's current UCI ranking
    agency : str
        Agency representing the rider
    strengths : list[str]
        List of the rider's strengths, as determined by FirstCycling
    year_details : dict[int, YearDetails]
        Dictionary mapping years to YearDetails object including rider's details for that year
    """

    def __init__(self, rider_id, year=None):
        """
        Parameters
        ----------
        rider_id : int
            FirstCycling.com id for the rider used in the url of their page
        year : int, optional
            Year for which to collect details.
            If None, no yearly details collected (default is None).
        """
        
        url = 'https://firstcycling.com/rider.php?r=' + str(rider_id) + ('&y=' + str(year)) if year else ''
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
        self.height = float(details['Height'].rsplit(maxsplit=1)[0]) #in m
        self.WT_detail = details['WorldTour']
        self.UCI_detail = details['UCI']
        self.UCI_rank = int(details['UCI Ranking'])
        self.agency = details['Agency']
        td = details_table.find_all('tr')[-1].find_all('td')[1]
        self.strengths = [x.strip() for x in td if isinstance(x, bs4.element.NavigableString)]
        
        # Load information for selected year
        self.year_details = {}
        if year:
            rider_year_details_table = soup.find('table', {'class': 'tablesorter notOddeven'})
            self.year_details[year] = YearDetails(rider_year_details_table)