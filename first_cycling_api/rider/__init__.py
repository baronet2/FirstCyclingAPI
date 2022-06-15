"""
Riders
======

Access rider details, including results and statistics.

Examples
--------
>>> Rider(18655).year_results(2020).results_df.iloc[0]
Date                       8.11
Pos                           1
GC                          NaN
Race_Country                ESP
Race            Vuelta a España
CAT                       2.UWT
UCI                       850.0
Unnamed: 8            Show more
Race_ID                      23
Name: 0, dtype: object

"""

from .rider import Rider