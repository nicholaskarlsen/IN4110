import os
import re
import requests as req
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from requesting_urls import get_html


def get_teams(url):
    """ Extract team names and urls from the NBA playoff bracket selection table
    Args:
        url (str): URL of the wiki page containing the table
    Returns:
        teams (list<String>): A list of team names that made it to the conference semifinals
        teams_url (list<String>): A list of the absolute wikipedia urls corresponding to the team names

    """
    teams = []
    teams_url = []

    html = get_html(url)
    soup = BeautifulSoup(html, "html.parser")
    soup_table = soup.find(
        "table",
        {
            "style": r"font-size: 90%; margin:1em 2em 1em 1em;",
            "cellspacing": "0",
            "cellpadding": "0",
            "border": "0",
        },
    )
    rows = soup_table.find_all("tr")

    for (i, row) in enumerate(rows[4:]):
        columns = row.findAll("td")
        if len(columns) >= 5:
            hyperlink = columns[3].find("a")
            if hyperlink != None:
                title = hyperlink.get("title")
                title = " ".join(title.split()[1:-1])
                if title not in teams:
                    teams.append(title)
                    teams_url.append("https://en.wikipedia.org" + hyperlink.get("href"))

    return teams, teams_url


def get_players(url):
    """ Extract players that played for a specific team in the NBA playoffs
    Args:
        url (str): URL to the wikipedia article of the season for a given team
    Returns:
        players (list<str>): A list of players names corresponding to the team whos URL was passed.
        players_url (list<str>): A list of wikipedia urls corresponding to player_names of the team
            whos url was passed
    """
    players = []
    players_url = []

    html = get_html(url)
    soup = BeautifulSoup(html, "html.parser")
    # Table containing table of players + list of coaches
    soup_table = soup.find("table", {"class": "toccolours"})
    # Extract table of players
    soup_table = soup_table.find(
        "table",
        {
            "class": "sortable",
            "style": "background: transparent; margin: 0px; width: 100%;",
        },
    )

    rows = soup_table.findAll("tr")
    for row in rows[1:]:
        columns = row.findAll("td")
        player_col = columns[2]
        player_hyperlink = player_col.find("a")
        players.append(
            player_hyperlink.get("title").replace("(basketball)", "").strip()
        )
        players_url.append("https://en.wikipedia.org" + player_hyperlink.get("href"))

    return players, players_url


def get_player_statistics(url, year="2020–21"):
    """Extract player statistics for NBA player.

    Args:
        url (str) : URL to the wikipedia article of a player

    Returns:
        ppg (float) : Points per game
        bpg (float) : Blocks per game
        rpg (float) : Rebounds per game
    """
    # Some of the players havent got the NBA table yet (i.e Charles Bassey, who joined the NBA recently)
    # In this case, simply return 0 under the assumption that they wont be a top-scorer yet anyway.
    # ppg = 0.0
    # bpg = 0.0
    # rpg = 0.0

    statistics = {"PPG": 0.0, "BPG": 0.0, "RPG": 0.0}
    statcolumn = {"PPG": None, "BPG": None, "RPG": None}

    html = get_html(url)

    soup = BeautifulSoup(html, "html.parser")
    nba_header = soup.find(id="NBA_career_statistics")

    # if no headers are found, try another possible id
    if nba_header == None:
        nba_header = soup.find(id="NBA")
    # if a header is still not found assume the entry isn't there and return the default statistics
    if nba_header == None:
        return statistics

    regular_season_header = nba_header.find_next(id="Regular_season")

    if regular_season_header == None:
        return statistics

    nba_table = regular_season_header.find_next("table")

    # if no table is found, return default statistics
    if nba_table == None:
        return statistics

    # Determine the columns in which the desired statistics are located
    table_header = nba_table.findAll("th")
    for (i, header) in enumerate(table_header):
        header = header.text.strip()
        if header in statcolumn.keys():
            statcolumn[header] = i

    # Loop through the rows in the table
    for row in nba_table.findAll("tr")[1:]:
        cols = row.findAll("td")

        # Check if the 0th column containing the date matches the desired year
        datelink = cols[0].find("a")
        if datelink != None:
            season = datelink.get("title")
            if re.match(year, season):
                # Extract statistics from the relevant columns
                for key in statistics:
                    statistics[key] = float(cols[statcolumn[key]].text.replace("*", ""))

    return statistics


def get_best_players(url, metric="PPG"):
    teams, teams_url = get_teams(url)
    data = {}

    for (t, t_url) in zip(teams, teams_url):
        data[t] = {"name": [], metric: []}
        players, players_url = get_players(t_url)

        for (p, p_url) in zip(players, players_url):
            stats = get_player_statistics(p_url)
            data[t]["name"].append(p)
            data[t][metric].append(stats[metric])

        data[t][metric], data[t]["name"] = zip(
            *sorted(zip(data[t][metric], data[t]["name"]))
        )
        data[t][metric] = data[t][metric][-3:]
        data[t]["name"] = data[t]["name"][-3:]

    return data


def plot_best_players(data, metric):
    """ 
    Args:
        data (Dict) :
        metric (str) :
    """
    # Dictionary to translate basketball jargon to plain english
    jargon = {
        "PPG": "Points per game",
        "BPG": "Blocks per game",
        "RPG": "Rebounds per game",
    }

    # keep a record of the widest bar to add a bit of padding at the end
    xmax = 0

    plt.figure(figsize=(8, 8))
    for (i, t) in enumerate(data.keys()):
        plots = plt.barh(data[t]["name"], data[t][metric], ec="black")

        # Annotate the bars with the team name
        for bar in plots.patches:
            # Add the team name to the bar
            plt.annotate(2 * " " + t, xy=(0, bar.get_y() + bar.get_height() / 3))
            # Add the metric at the end of the bar
            plt.annotate(
                bar.get_width(),
                xy=(bar.get_width() * 1.01, bar.get_y() + bar.get_height() / 3),
            )
            # Keep track of the highest metric
            xmax = bar.get_width() if bar.get_width() > xmax else xmax

    # add a bit of extra padding for to accomodate for the metric annotation at the end of the bars
    plt.xlim(0, xmax * 1.1)
    plt.ylabel("Player")
    plt.xlabel(jargon[metric])
    plt.tight_layout()
    plt.savefig("NBA_player_statistics/players_over_%s.png" % metric)
    plt.close()
    return


if __name__ == "__main__":
    url = "https://en.wikipedia.org/wiki/2021_NBA_playoffs"

    for metric in ["PPG", "BPG", "RPG"]:
        stats = get_best_players(url, metric)
        plot_best_players(stats, metric)
