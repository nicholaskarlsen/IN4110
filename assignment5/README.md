# Assignment 5: Regular Expressions & Web Scraping

You may (re)generate all of the data produced in this assignment by running each of the python files whilst in this directory. Alternatively, i have included a convenient makefile so that you can also just call `make` to run all the scripts.

The dependencies to run the files in this project can be installed by running
```
python3 -m pip install numpy matplotlib requests beautifulsoup4
```
## Tests

A subset of the implemented functions have tests asociated with them. These can be ran using pytest like
```
pytest tests.py
```
or alternatively using the makefile like
```
make test
```

## Short description of the Python scripts 
|File|Description| 
|---|---|
|`requesting_urls.py`| Request the HTML code from a given URL |
|`filter_urls.py`| Parses websites using REGEX to extract hyperlinks and links to other articles on wikipedia pages |
|`collect_dates.py`| Parse a website and extract all dates (in various formats) from the HTML using REGEX and gather them in a list |
|`time_planner.py`| Parses the wiki page of the Alpine world cup and generates a nicely formatted betting slip in markdown for all of the events|
|`fetch_player_statistics.py`| Fetches player statistics from the top 3 players of each team that made it to the semi-finals in the 2021 NBA playoffs and generates a bar-chart for easy comparisons |
|`tests.py`| Some simple unit tests that ensure the functionality (of some) of the functions implemented |
