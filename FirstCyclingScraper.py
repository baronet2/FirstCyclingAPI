"""
author: Ethan Baron

This file provides tools used to collect data from FirstCycling.com.
"""

import requests
import bs4
import pandas as pd
from dateutil.parser import parse, ParserError


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
    results_df : pd.DataFrame
        DataFrame with the following columns:
        Date : datetime.datetime
            Date of result
        Result : int or str
            Rider's result in race, e.g. 5 or 'DNF'
        GC Standing : int
            Rider's GC standings after stage, or None if not applicable
        Race : Race
            Race object including details on race
        UCI Points : float
            Number of UCI points earned by rider in race
    """
    
    def __init__(self, details_table, results_table):
        """
        Parameters
        ----------
        details_table : bs4.element.Tag
            Table containing year information of rider
        results_table : bs4.element.Tag
            Table containing race results of rider in year
        """
        
        def parse_row(row):
            """ Parse one row from rider's race results table

            Parameters
            ----------
            row : bs4.element.Tag
                tr from race results table

            Returns
            -------
            date : datetime.datetime
                Date of race
            pos : int or str
                Rider's result in race, e.g. 5 or 'DNF'
            gc : int
                Rider's GC standing at end of stage or None if not applicable
            race : Race
                Object representing race
            uci : float
                UCI points earned by rider in race
            """
            tds = row.find_all('td')
            if len(tds) == 7:
                tds.append(None)
            date, date_alt, pos, gc, icon, race, cat, uci = tuple(tds)
            try:
                date = parse(date.text)
            except ParserError:
                year, month, day = date.text.split('-')
                month = '01' if not int(month) else month
                day = '01' if not int(day) else day
                fixed_date = year + '-' + month + '-' + day
                date = parse(fixed_date)

            pos = int(pos.text) if pos.text.isnumeric() else pos.text
            gc = int(gc.text) if gc.text else None
            race = Race(icon, race, cat.text.strip(), date)
            uci = (float(uci.text) if uci.text != '-' else 0) if uci else None
            return date, pos, gc, race, uci   
            
        if details_table:
            rider_year_details = [s.strip() for s in details_table.text.replace('\n', '|').split('|') if s.strip()]
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

        if results_table:
            result_rows = results_table.find_all('tr')[1:]
            self.results_df = pd.DataFrame([parse_row(row) for row in result_rows], columns = ['Date', 'Result', 'GC Standing', 'Race', 'UCI Points'])
        else:
            self.results_df = pd.DataFrame(columns = ['Date', 'Result', 'GC Standing', 'Race', 'UCI_Points'])
    
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

    Methods
    -------
    get_full_results_dataframe()
        Loads pd.DataFrame() of all rider's race results
    """

    def __init__(self, rider_id, years=None):
        """
        Parameters
        ----------
        rider_id : int
            FirstCycling.com id for the rider used in the url of their page
        years : list[int]
            List of years for which to collect data, default is None
            If None, collect all years for which rider results are available
        """
        
        url = 'https://firstcycling.com/rider.php?r=' + str(rider_id) + (('&y=' + str(years[0])) if years else '')

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

        # Load rider's strengths from details table
        tr = details_table.find_all('tr')[-1]
        if 'Strengths' in tr.find('td'):
            td = tr.find_all('td')[1]
            self.strengths = [x.strip() for x in td if isinstance(x, bs4.element.NavigableString)]
        else:
            self.strengths = []
        
        # Add yearly details
        self.year_details = {}
        if not years: # Get list of all years for which results available
            years = [o['value'] for o in soup.find('select').find_all('option')]
            years = [int(y) for y in years if y]
        self.year_details[years[0]] = self.__year_details_from_soup(soup) # Add year from current page
        for year in years[1:]:
            self.add_year_details(year) # Add other requested years


    def __year_details_from_soup(self, soup):
        """ Return year details for rider from soup.

        Parameters
        ----------
        soup : bs4.BeautifulSoup
            BeautifulSoup for page
        """
        rider_year_details_table = soup.find('table', {'class': 'tablesorter notOddeven'})
        rider_results_table = soup.find('table', {'class': 'sortTabell tablesorter'})
        return YearDetails(rider_year_details_table, rider_results_table)

    
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
        self.year_details[year] = self.__year_details_from_soup(soup)

    
    def get_full_results_dataframe(self):
        """ Return pd.DataFrame() of all rider's race results """
        teams = {k: v.team for k, v in self.year_details.items()}
        df = pd.concat([v.results_df for v in self.year_details.values()]).reset_index(drop=True)
        df['Year'] = df['Date'].apply(lambda x: x.year)
        df['Team'] = df['Year'].apply(lambda x: teams[x])
        df['Race Name'] = df['Year'].astype(str) + ' ' + df['Race'].apply(lambda x: x.name)
        race_details_df = pd.concat([pd.Series(vars(race)) for race in df['Race']], axis=1).transpose()
        race_details_df.columns = [' '.join([w[0].capitalize() + w[1:] for w in c.replace('_', ' ').split()]) for c in race_details_df.columns]
        df = pd.concat([df, race_details_df], axis=1)
        df = df.loc[:,~df.columns.duplicated()] # Remove second 'Date' column
        return df

    def __str__(self):
        return self.name

    def __repr__(self):
        return str((self.id, self.name))


class Race:
    """
    Framework to store one race day / classification information

    Attributes
    ----------
    id : int
        FirstCycling.com id for the race used in URLs
    name : str
        Race name, e.g. 'Tour de France'
    full_name : str
        Full Race name as it appears in the race results table, e.g. 'Tour de France | 17th stage'
    date : datetime.datetime
        Date of race result
    cat : str
        The race category/division
    championship : bool
        Whether the race is a national, continental, or world championships event
    country : str
        Three-letter code for country in which race held or 'UCI' or 'OL' (Olympics) for races which change countries
    edition_country : str
        Three-letter code for country in which race edition held
        May be different from self.country for races which change countries
    edition_name : str
        Details about this edition of a race which changes countries, e.g. host city for World Championships, or None if not available
    classification : str
        The classification type ('General', 'Points', 'Mountain', 'Sprint', or 'Youth') or None if not applicable
    jersey_colour :  str
        The colour of the jersey for the race's classification, if available
    stage_num : int
        The stage number or 0 for a prologue None if not applicable
    one_day : bool
        Whether race is a one-day race
    ITT : bool
        Whether the race is an inidividual time trial
    TTT : bool
        Whether the race is a team time trial
    TT : bool
        Whether the race is a time trial
    MTF : bool
        Whether the race has a mountain-top finish
    mountain : bool
        Whether the race is on mountainous terrain, or is a mountain individual time trial
    hilly : bool
        Whether the race is on hilly terrain
    flat : bool
        Whether the race is on flat terrain, or is a non-mountain individual time trial
    cobbled : bool
        Whether the race is a cobbled race
    icon : str
        The filename for the icon which appears before the race country flag, for debugging purposes
    """

    colours = ('green', 'red', 'yellow', 'pink', 'violet', 'blue', 'black', 'orange', 'lightblue', 'white') # TODO Any more?
    icon_map = {'Bakketempo.png': 'Mountain ITT',
                'Fjell-MF.png': 'Mountain MTF',
                'Fjell.png': 'Mountain',
                'Flatt.png': 'Flat',
                'Smaakupert-MF.png': 'Hilly MTF',
                'Smaakupert.png': 'Hilly',
                'Tempo.png': 'Flat ITT',
                'Brosten.png': 'Cobbles',
                'Lagtempo.png': 'TTT'} # TODO Any more?

    def __init__(self, icon, race, cat, date):
        """
        Parameters
        ----------
        icon : bs4.element.Tag
            td from race results table which includes the icon before the race country flag
        race : bs4.element.Tag
            td from race results table which includes the race name
        cat : str
            Race category/division, e.g. '2.WT3' or '1.1'
        date : datetime.datetime
            Date of race
        """

        # Initialize variables
        self.cat = cat
        self.championship = cat in ('CN', 'CCRR', 'CCTT', 'WCRR', 'WCTT')
        self.classification = None
        self.stage_num = None
        self.jersey_colour = None
        self.TTT = False
        self.ITT = False
        self.TT = False
        self.MTF = False
        self.mountain = False
        self.hilly = False
        self.flat = False
        self.cobbled = False
        
        # Parse icon for details on race type and profile using colours and icon_map static variables  
        icon = icon.img['src'].split('/')[-1] if icon.img else icon.text
        self.icon = icon
        if icon:
            for col in Race.colours:
                if (col + '.') in icon:
                    self.classification = True
                    self.jersey_colour = col.capitalize()
                    icon = col.capitalize()
                    break
            icon = Race.icon_map[icon] if icon in Race.icon_map else icon
       
            self.TTT = icon == 'TTT'
            self.ITT = 'ITT' in icon
            self.TT = self.ITT or self.TTT
            self.MTF = icon.endswith(' MTF')
            self.mountain = 'Mountain' in icon
            self.hilly = 'Hilly' in icon
            self.flat = 'Flat' in icon
            self.cobbled = 'Cobbles' in icon
        
        # Basic race details
        self.name = race.a.text
        self.id = int(race.a['href'].split('?r=')[1].split('&')[0])
        self.full_name = race.text.strip().replace('\n', ' ').replace('\t', '').replace('\r', '')
        
        # Country flags for race
        imgs = race.find_all('img')
        self.country = imgs[0]['src'].split('/')[-1][:-4]
        self.edition_country = self.country
        self.edition_name = None
        
        # Additional information in full race name
        tokens = self.full_name.split(' | ')
        if len(imgs) > 1:
            self.edition_country = imgs[1]['src'][-7:-4]
            self.edition_name = tokens[1].strip()
        if self.classification:
            # TODO we miss general classification with missing jerseys
            self.classification = 'General' if len(tokens) == 1 else tokens[1]
        elif ' | Mountain' in self.full_name:
            self.classification = 'Mountain'
        elif ' | Points' in self.full_name:
            self.classification = 'Points'
        elif ' | Youth' in self.full_name:
            self.classification = 'Youth'
        elif ' | Sprint' in self.full_name:
            self.classification = 'Sprint'
        elif len(tokens) > 1:
            self.stage_num = '0' if tokens[1] == 'Prologue' else ''.join([c for c in tokens[1] if c.isnumeric()])
            self.stage_num = None if not self.stage_num.strip() else int(self.stage_num)
        self.one_day = not (self.classification or self.stage_num)

    def __str__(self):
        return self.full_name
    
    def __repr__(self):
        return 'Race(' + self.full_name + ')'