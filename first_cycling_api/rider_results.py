"""
author: Ethan Baron
"""

from .utilities import *


class ResultsTable:
    """
    Attributes
    ----------
    rider_id : int
        FirstCycling.com id for the rider used in the url
    year : int
        Year data represents
    name : str
        Full rider name
    results : list[RaceResult]
        A list of the rider's results in the season

    Methods
    -------
    to_dataframe()
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

        # Get table of results
        results_table = soup.find('table', {'class': 'sortTabell tablesorter'})
        self.results = [RaceResult(row) for row in results_table.tbody.find_all('tr')] if results_table else []
        self.results = [x for x in self.results if vars(x)]

    def to_dataframe(self, expand=False):
        """
        Return pd.DataFrame of results table with attributes of RaceResults as column.
        
        Arguments
        ----------
        expand : bool
            Whether to include additional derived columns, such as boolean columns indicating what type of race each result is for
        """
        return pd.concat([result.to_series(expand=expand) for result in self.results], axis=1).transpose() if self.results else None

    def __str__(self):
        return 'ResultsTable(' + self.name + ', ' + str(self.year) + ')'

    def __repr__(self):
        return 'ResultsTable(' + self.name + ', ' + str(self.year) + ')'

    def get_json(self):
        return json.dumps(self, default=ComplexHandler)

    def to_json(self):
        d = vars(self).copy()
        return d


class RaceResult:
    """
    Framework to store information on one result for a rider.

    race_id : int
        ID used in URL for race
    name : str
        Race name excluding stage/edition/classification information, e.g. Tour de Pologne
    full_name : str
        Full race name as it appears in results table, e.g. Tour de Pologne | 1st stage
    race_country_code : str
        Three-letter code of country of race, or 'UCI' or 'OL' (Olympics)
    cat : str
        Race category
    stage_num : int
        Stage number, if applicable
    classification :
        Classification type, if applicable
        One of 'Points', 'Mountain', 'Sprint', or 'Youth'
        Note that 'General' (GC) not listed
    edition_country_code : str
        Three-letter code of country in which race edition held (e.g. for World Championships or Olympics)
    edition_city : str
        Name of city which hosted this race edition
    date : datetime.date
        Date of race
        If month unknown, set to January
        If day unknown, set to 1st
    icon : str
        File name of icon appearing before race name
        Contains either the jersey colour or profile type
    result : int or str
        Rider result in race or 'DNS', 'DNF', 'OOT', 'DSQ'
    uci_points : int
        Number of UCI points earned in race, None if prior to 2018
    gc_standing : int
        GC standing after stage or None if not applicable
    """
    
    def __init__(self, row):
        """
        Parameters
        ----------
        row : bs4.element.Tag
            tr from race results table
        """

        # Get tds from tr
        tds = row.find_all('td')
        if len(tds) < 7: # No data
            return
        elif len(tds) == 7: # Missing UCI points column - prior to 2018
            tds.append(None)
        date, date_alt, result, gc_standing, icon, race_td, cat, uci = tuple(tds)
        
        # Parse race date
        try:
            self.date = parse(date.text).date()
        except ParserError: # Result with uncertain date, use January/1st by default
            year, month, day = date.text.split('-')
            month = '01' if not int(month) else month
            day = '01' if not int(day) else day
            fixed_date = year + '-' + month + '-' + day
            self.date = parse(fixed_date).date()

        # Load basic result details
        self.result = int(result.text) if result.text.isnumeric() else result.text
        self.gc_standing = int(gc_standing.text) if gc_standing.text else None
        self.icon = icon.img['src'].split('/')[-1] if icon.img else None
        self.cat = cat.text
        self.uci_points = (float(uci.text) if uci.text != '-' else 0) if uci else None
        
        # Parse td containing race name
        links = race_td.find_all('a')
        self.race_id = race_link_to_race_id(links[0])
        imgs = race_td.find_all('img')
        self.race_country_code = img_to_country_code(imgs[0])
        self.full_name = race_td.text.strip().replace('\n', ' ').replace('\t', '').replace('\r', '')
        tokens = [x.strip() for x in self.full_name.split('|')]
        self.name = tokens[0]
        if len(imgs) == 2: # Championships edition
            self.edition_country_code = img_to_country_code(imgs[1])
            self.edition_city = tokens[1]
        else:
            if len(links) == 2: # Stage
                self.stage_num = race_link_to_stage_num(links[0])
            elif len(tokens) == 2: # Classification (except GC)
                self.classification = tokens[1]


    def __str__(self):
        return str(self.date.year) + ' ' + self.full_name

    def __repr__(self):
        return "RaceResult(" + self.full_name + ", " + str(self.date.year) + ")"

    def get_json(self):
        return json.dumps(self, default=ComplexHandler)

    def to_json(self):
        d = vars(self).copy()
        d['date'] = str(d['date'])
        return d

    def to_series(self, expand=False):
        """
        Return pd.Series representing race result.

        Arguments
        ----------
        expand : bool
            If True, include derived features such as booleans indicating race type and profile
        """
        series = pd.Series(vars(self))

        if expand:
            # Race type/category booleans
            series['uci_race'] = self.cat in uci_categories
            series['championship'] = self.cat in championships_categories
            series['u23'] = self.cat in U23_categories
            series['cx'] = self.name.startswith('CX -')
            series['juniors'] = self.cat.startswith('J')
            series['one_day'] = self.cat in one_day_categories

            # Parse icon for details on race type and profile using colours and icon_map static variables
            series['jersey_colour'] = None
            series['profile'] = None
            
            if self.icon:
                for col in colour_icons:
                    if (col + '.') in self.icon:
                        series['jersey_colour'] = col.capitalize()
                        break
                
                if not series['jersey_colour']:
                    if self.icon in profile_icon_map:
                        series['profile'] = profile_icon_map[self.icon]
       
            series['ttt'] = series['profile'] == 'TTT'
            series['itt'] = 'ITT' in series['profile'] if series['profile'] else None
            series['tt'] = series['itt'] or series['ttt']
            series['mtf'] = series['profile'].endswith(' MTF') if series['profile'] else None
            series['mountain'] = 'Mountain' in series['profile'] if series['profile'] else None
            series['hilly'] = 'Hilly' in series['profile'] if series['profile'] else None
            series['flat'] = 'Flat' in series['profile'] if series['profile'] else None
            series['cobbled'] = 'Cobbles' in series['profile'] if series['profile'] else None
        
        return series