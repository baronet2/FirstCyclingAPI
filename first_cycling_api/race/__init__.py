"""
Races
=====

Access race details, including results, statistics, startlists, and more.

Examples
--------
>>> RaceEdition(race_id=9, year=2019).results().results_table.iloc[0]
Pos                                01
Rider            Mathieu van der Poel
Team                Corendon - Circus
Time                          6:28:18
UCI                             500.0
Rider_ID                        16672
Rider_Country                     NED
Team_ID                         13279
Name: 0, dtype: object

"""


from .race import Race, RaceEdition