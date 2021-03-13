# First Cycling API

This repository provides a tool to obtain data from firstcycling.com.

## Usage
The relevant scripts are contained in `first_cycling_api.py`. Import them by adding this repository to your working directory and using:
```python
from first_cycling_api import *
```

To load data for a rider, you will need the rider id used by firstcycling.com in the url.
For example, for Primoz Roglic, the rider is 18655.
You can see this from the url of his profile page: https://firstcycling.com/rider.php?r=18655.

Rider information can be loaded into a `Rider` object. To load data for a rider, use:
```python
r = Rider(18655)
```

The script automatically loads rider's biographical information and the details and results for each season in which they were active.
To only load data for specific years, pass a list of years to the `years` attribute.

`Rider` and other objects can be obtained in JSON format using:
```python
r.get_json()
```

## Contributing
If you would like to contribute to the code, please feel free to open a pull request. Feel free to open an issue to request features, identify bugs, or discuss the tool.
