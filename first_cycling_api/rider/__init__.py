"""
Rider
=====

Access rider details, including results and statistics.

Examples
--------
>>> Rider(18655).year_results(2020).results_df.iloc[0]
Date                        811
Pos                           1
GC                          NaN
Race            Vuelta a España
CAT                         GT2
UCI                         850
Icon                    red.png
Race_ID                      23
Race_Country                ESP
Name: 0, dtype: object
"""

from .rider import Rider