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
        Team of rider in specific year
    division : str
        Team's division in that season
    UCI_rank : int
        Rider's UCI ranking in that season
    UCI_points : int
        Rider's UCI points accumulated in that season
    UCI_rank : int
        Rider's number of UCI wins in that season
    race_days : int
        Rider's number of race days in that season
    race_kms : int
        Distance covered by rider in races that season, in kilometers
    """
    
    def __init__(self, table):
        """
        Parameters
        ----------
        table : bs4.element.Tag
            Table containing year information of rider
        """
        
        rider_year_details = [s.strip() for s in table.text.replace('\n', '|').split('|') if s.strip()]
        self.team = rider_year_details[0].split(maxsplit=1)[-1]
        self.division = rider_year_details[1].split(maxsplit=1)[-1]
        self.UCI_rank = int(rider_year_details[2].rsplit(maxsplit=1)[-1])
        self.UCI_points = int(rider_year_details[3].split(maxsplit=1)[0].replace('.', ''))
        self.UCI_wins = int(rider_year_details[4].rsplit(maxsplit=1)[-1])
        self.race_days = int(rider_year_details[5].rsplit(maxsplit=1)[-1])
        self.race_kms = int(rider_year_details[6].rsplit(maxsplit=2)[-2].replace('.', ''))
        
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