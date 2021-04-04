# First Cycling API

An unofficial API to obtain data from https://firstcycling.com/.

## Usage

Rider information can be loaded into a `Rider` object. To load data for a rider, use the rider id from the rider's firstcycling.com page URL.
For example, the id for Primoz Roglic is 18655 (see https://firstcycling.com/rider.php?r=18655)

```python
from first_cycling_api import *
r = Rider(18655)
print(vars(r)) # Shows all the attributes of the Rider object
```

The script loads rider's biographical information and the details and results for each season in which they were active.
To only load data for specific years, pass a list of years to the `years` attribute.

`Rider` and other objects can be obtained in JSON format using:
```python
r.get_json()
```

A `pandas.DataFrame` with a rider's results can be obtained by calling:
```python
r.get_results_dataframe()
```

More complete documentation on each class and its attributes can be obtained using:
```python
help(r)
```

## Contributing
Contributions are welcome! Please feel free to open issues, pull requests, and/or discussions.

## License
See the file called LICENSE. This project is not affiliated in any way with firstcycling.com.
