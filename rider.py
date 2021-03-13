"""
author: Ethan Baron
"""

from rider_details import *
from rider_results import *


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
        # Add basic details
        self.id = rider_id
        self.details = RiderDetails(rider_id)

        # Add yearly details and results
        self.year_details = {}
        self.results = {}
        if not years: # Get list of all years for which results available
            years = self.details.years_active
        for year in years:
            self.year_details[year] = RiderYearDetails(self.id, year)
            self.results[year] = ResultsTable(self.id, year)

        # TODO Reuse soup across functions - provide alternative __init__ from soup

    def __str__(self):
        return self.details.name

    def __repr__(self):
        return "Rider(" + str(self.id) + ", " + self.details.name + ")"

    def get_json(self):
        return json.dumps(self, default=ComplexHandler)

    def to_json(self):
        d = vars(self).copy()
        return d