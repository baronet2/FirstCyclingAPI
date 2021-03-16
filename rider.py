"""
author: Ethan Baron
"""

from rider_details import *
from rider_results import *
from utilities import *


class Rider:
    """
    Framework to store information about a particular rider.
    
    Attributes
    ----------
    id : int
        FirstCycling.com id for the rider used in the url
    details : RiderDetails
        Rider's basic profile information
    year_details : dict(int : RiderYearDetails)
        Dictionary mapping years to rider's details for that year
    results : dict(int : ResultsTable)
        Dictionary mapping years to rider's results for that year

    Methods
    -------
    get_results_dataframe()
    get_json()
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
        # Load rider page
        url = 'https://firstcycling.com/rider.php?r=' + str(rider_id) + ('&y=' + str(years[0])) if years else ''
        page = requests.get(url)
        soup = bs4.BeautifulSoup(page.text, 'html.parser')

        # Add basic details
        self.id = rider_id
        self.details = RiderDetails(rider_id, soup=soup)

        # Add yearly details and results
        self.year_details = {}
        self.results = {}
        if not years: # Get list of all years for which results available
            years = self.details.years_active
        year_showing = int(soup.find_all('h1')[1].text)
        years = [year for year in years if year != year_showing]

        # Load details and results from most recent year directly from soup (avoids repeating requests)
        self.year_details[year_showing] = RiderYearDetails(self.id, year_showing, soup=soup)
        self.results[year_showing] = ResultsTable(self.id, year_showing, soup=soup)
        
        for year in years: # Load details and results for other years (avoids repeating requests)
            url = 'https://firstcycling.com/rider.php?r=' + str(rider_id) + '&y=' + str(year)
            page = requests.get(url)
            soup = bs4.BeautifulSoup(page.text, 'html.parser')            
            self.year_details[year] = RiderYearDetails(self.id, year, soup=soup)
            self.results[year] = ResultsTable(self.id, year, soup=soup)


    def get_results_dataframe(self):
        """ Return pd.DataFrame of all loaded result for rider, sorted in reverse chronological order """
        return pd.concat([result.to_dataframe() for result in self.results.values()]).sort_values('date', ascending=False)

    def __str__(self):
        return self.details.name

    def __repr__(self):
        return "Rider(" + str(self.id) + ", " + self.details.name + ")"

    def get_json(self):
        return json.dumps(self, default=ComplexHandler)

    def to_json(self):
        d = vars(self).copy()
        return d