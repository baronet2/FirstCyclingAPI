# FirstCyclingScraper

This repository provides a tool to scrape data from firstcycling.com.

## Usage
The relevant scripts are contained in `FirstCyclingScraper.py`. Import them by adding that file to your working directory and using:
```python
from SpotifyPlaylistScraper import *
```

To load data for a rider, you will need the rider id used by firstcycling.com in the url.
For example, for Primoz Roglic, the rider is 18655.
You can see this from the url of his profile page: https://firstcycling.com/rider.php?r=18655.

Riders are loaded into a `Rider` object. To load data for a rider, use:
```python
r = Rider(18655)
```

The script automatically loads rider's biographical information and the details and results for each season in which they were active.
The Python file provides documentation on how to use the `Rider` objects.
For instance, if you'd like to load a `pandas.DataFrame` of all the rider's results, you can use:

```python
df = r.get_full_results_dataframe()
```

## Contributing
If you would like to contribute to the code, please feel free to open a pull request. Feel free to open an issue to request features, identify bugs, or discuss the tool.
