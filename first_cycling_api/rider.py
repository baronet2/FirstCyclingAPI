"""
author: Ethan Baron
"""

from .rider_details import *
from .rider_results import *
from .utilities import *


class Rider:
    """
    Framework to store information about a particular rider.
    
    Attributes
    ----------
    rider_id : int
        FirstCycling.com id for the rider used in the url
    details : RiderDetails
        Rider's basic profile information
    year_details : dict(int : RiderYearDetails)
        Dictionary mapping years to rider's details for that year
    results : dict(int : ResultsTable)
        Dictionary mapping years to rider's results for that year
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

        # Verify passed rider ID
        try:
            rider_id = int(rider_id)
        except ValueError:
            print("Invalid rider ID")
            return
        self.rider_id = rider_id
        
        # Load rider page
        url = 'https://firstcycling.com/rider.php?r=' + str(rider_id) + (('&y=' + str(years[0])) if years else '')
        page = requests.get(url)
        soup = bs4.BeautifulSoup(page.text, 'html.parser')

        # Add basic details
        self.details = RiderDetails(rider_id, soup=soup)

        # Add yearly details and results
        self.year_details = {}
        self.results = {}
        if not years: # Get list of all years for which results available
            years = self.details.years_active
        year_showing = int(soup.find_all('h1')[1].text)
        years = [year for year in years if year != year_showing]

        # Load details and results from most recent year directly from soup (avoids repeating requests)
        self.year_details[year_showing] = RiderYearDetails(self.rider_id, year_showing, soup=soup)
        self.results[year_showing] = ResultsTable(self.rider_id, year_showing, soup=soup)
        
        for year in years: # Load details and results for other years (avoids repeating requests)
            url = 'https://firstcycling.com/rider.php?r=' + str(rider_id) + '&y=' + str(year)
            page = requests.get(url)
            soup = bs4.BeautifulSoup(page.text, 'html.parser')            
            self.year_details[year] = RiderYearDetails(self.rider_id, year, soup=soup)
            self.results[year] = ResultsTable(self.rider_id, year, soup=soup)


    def get_results_dataframe(self, expand=False):
        """ Return pd.DataFrame of all loaded result for rider, sorted in reverse chronological order """
        return pd.concat([result.to_dataframe(expand=expand) for result in self.results.values()]).sort_values('date', ascending=False)

    def __str__(self):
        return self.details.name

    def __repr__(self):
        return "Rider(" + str(self.rider_id) + ", " + self.details.name + ")"

    def get_json(self):
        return json.dumps(self, default=ComplexHandler)

    def to_json(self):
        d = vars(self).copy()
        return d