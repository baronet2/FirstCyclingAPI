# First Cycling API
[![Documentation Status](https://readthedocs.org/projects/firstcyclingapi/badge/?version=latest)](https://firstcyclingapi.readthedocs.io/en/latest/?badge=latest)
[![GitHub license](https://img.shields.io/github/license/Naereen/StrapDown.js.svg)](https://github.com/Naereen/StrapDown.js/blob/master/LICENSE)
[![GitHub Repo stars](https://img.shields.io/github/stars/baronet2/FirstCyclingAPI)](https://github.com/baronet2/FirstCyclingAPI/stargazers)

An unofficial Python API wrapper for https://firstcycling.com/.

## Usage

The API wrapper currently supports the following endpoints:

- Race pages
- Rider pages
- Rankings pages

A few examples are shown below.

For full documentation, see https://firstcyclingapi.readthedocs.io/en/latest/.

**Race Results:**
```python
>>> from first_cycling_api import RaceEdition
>>> amstel_2019 = RaceEdition(race_id=9, year=2019) # The race_id comes from the race page URL
>>> amstel_2019.results().results_table.head() # A pandas DataFrame of the race results
```

|    |   Pos | Rider                 | Team                    | Time    |   UCI |   Rider_ID | Rider_Country   |   Team_ID |
|---:|------:|:----------------------|:------------------------|:--------|------:|-----------:|:----------------|----------:|
|  0 |    01 | van der Poel Mathieu  | Corendon - Circus       | 6:28:18 |   500 |      16672 | NED             |     13279 |
|  1 |    02 | Clarke Simon          | EF Education First      | + 00    |   400 |        568 | AUS             |     13208 |
|  2 |    03 | Fuglsang Jakob        | Astana Pro Team         | + 00    |   325 |        264 | DEN             |     13198 |
|  3 |    04 | Alaphilippe Julian    | Deceuninck - Quick Step | + 00    |   275 |      12474 | FRA             |     13206 |
|  4 |    05 | Schachmann Maximilian | Bora - Hansgrohe        | + 00    |   225 |      16643 | GER             |     13200 |

**Rider Results:**
```python
>>> from first_cycling_api import Rider
>>> roglic = Rider(18655) # The rider ID comes from the rider page URL
>>> roglic.year_results(2020).results_df.head() # A pandas DataFrame of Roglic's 2020 results
```

|    |   Date |   Pos |   GC | Race_Country   | Race                  | CAT   |   UCI | Unnamed: 8   |   Race_ID |
|---:|-------:|------:|-----:|:---------------|:----------------------|:------|------:|:-------------|----------:|
|  0 |   8.11 |     1 |  nan | ESP            | Vuelta a España       | 2.UWT |   850 | Show more    |        23 |
|  1 |   4.1  |     1 |  nan | BEL            | Liège-Bastogne-Liège  | 1.UWT |   500 | Show more    |        11 |
|  2 |  20.09 |     2 |  nan | FRA            | Tour de France        | 2.UWT |   800 | Show more    |        17 |
|  3 |  27.09 |     6 |  nan | UCI            | World Championship RR | WCRR  |   225 | Show more    |        26 |
|  4 |   9.08 |     1 |  nan | FRA            | Tour de l'Ain         | 2.1   |   125 | Show more    |        63 |

**Rankings Pages:**
```python
>>> from first_cycling_api import Ranking
>>> ranking = Ranking(h=1, rank=1, y=2020, page=2) # Parameters from corresponding URL
>>> ranking.table.head() # A pandas DataFrame of the rankings table
```

|    |   Pos | Rider         | Nation      | Team                  |   Points |   Rider_ID |   Team_ID | Team_Country   |
|---:|------:|:--------------|:------------|:----------------------|---------:|-----------:|----------:|:---------------|
|  0 |   101 | Egan Bernal   | Colombia    | INEOS Grenadiers      |      425 |      58275 |     17536 | GBR            |
|  1 |   102 | Bauke Mollema | Netherlands | Trek-Segafredo        |      420 |        581 |     17540 | USA            |
|  2 |   103 | Tim Declercq  | Belgium     | Deceuninck-Quick Step |      415 |       1970 |     17529 | BEL            |
|  3 |   104 | Oliver Naesen | Belgium     | AG2R La Mondiale      |      411 |      22682 |     17524 | FRA            |
|  4 |   105 | Alex Aranburu | Spain       | Astana Pro Team       |      410 |      27307 |     17525 | KAZ            |

## Contributing
Contributions are welcome! Please feel free to open issues, pull requests, and/or discussions.

Especially, there is room to help with:
- Mapping additional endpoints (e.g. pages starting with https://firstcycling.com/team.php?)
- Parsing results from additional pages (e.g. race startlists, race statistics)

To run tests, first `pip install pytest` and `pip install vcrpy`. Then run `py.test` in a shell from the root directory.

## License
See the file called LICENSE. This project is not affiliated in any way with firstcycling.com.
