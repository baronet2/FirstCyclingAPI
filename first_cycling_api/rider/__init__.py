"""
Riders
======

Access rider details, including results and statistics.

Examples
--------
>>> Rider(18655).year_results(2020).results_df.iloc[0]
Date                     9.08
Pos                         1
GC                        NaN
Race            Tour de l'Ain
CAT                       2.1
UCI                     125.0
Unnamed: 7          Show more
Race_ID                    63
Race_Country              FRA
Name: 0, dtype: object

"""

from .rider import Rider