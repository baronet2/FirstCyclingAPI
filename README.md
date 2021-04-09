# First Cycling API

An unofficial Python API to obtain data from https://firstcycling.com/.

## Usage

The following pages are currently mapped by the API:
- Rider profile pages (e.g. https://firstcycling.com/rider.php?r=18655)
- UCI Ranking pages (e.g. https://firstcycling.com/ranking.php?rank=1&y=2021-12)
- Race results pages (e.g. https://firstcycling.com/race.php?r=9&y=2019)

### Rider Profiles
Rider information can be loaded into a `Rider` object with the rider id from the URL.

```python
from first_cycling_api import *
r = Rider(18655)
r.get_json() # Get the rider's attributes in JSON format
r.get_results_dataframe() # Get a DataFrame with the rider's results
help(Rider) # For more complete documentation on the Rider class
```

### UCI Rankings
Ranking tables can be loaded into `Ranking` objects using either the URL or a combination of arguments.

```python
from first_cycling_api import *
ranking = Ranking(url='https://firstcycling.com/ranking.php?rank=2&h=1&y=2020&u23=&page=2') # Using the URL
ranking = Ranking(ranking_type=2, ranking_category=1, year=2020, page_num=2) # Using arguments
ranking.get_json() # Get the Ranking object in JSON format
ranking.df # Rankings table in pandas.DataFrame format
help(Ranking) # For more complete documentation on the Ranking class
```

### Race Results
Race results can be loaded into `RaceResults` objects using either the URL or a combination of arguments.

```python
from first_cycling_api import *
results = RaceResults(race_id=9, year=2019) # Using arguments
results = RaceResults(url='https://firstcycling.com/race.php?r=9&y=2019&l=1') # Using the URL
results.get_json() # Get the RaceResults object in JSON format
results.df # Results table in pandas.DataFrame format
help(RaceResults) # For more complete documentation on the Ranking class
```

## Contributing
Contributions are welcome! Please feel free to open issues, pull requests, and/or discussions.

## License
See the file called LICENSE. This project is not affiliated in any way with firstcycling.com.
