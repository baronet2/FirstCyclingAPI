"""
Ranking
=======

Access race details, including statistics and results.

Initialize a `Ranking` instance and load ranking endpoints using its `ranking()` method.


Examples
--------
>>> Ranking().ranking(h=1, rank=1, y=2020, page=2).table.iloc[0]
Pos                          101
Rider                Egan Bernal
Nation                  Colombia
Team            INEOS Grenadiers
Points                       426
Rider_ID                   58275
Team_ID                    17536
Team_Country                 GBR
Name: 0, dtype: object
"""

from .ranking import Ranking