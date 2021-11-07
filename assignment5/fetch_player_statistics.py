import os
import requests as req
from bs4 import BeautifulSoup
from requesting_urls import get_html


def get_teams(url):
    """
    Arguments:
        url String :
    Returns:
        teams list<String> :
        teams_url list<String> :

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


def get_player_statistics(url):
    html = get_html(url)
    # Some of the players havent got the NBA table yet (i.e Charles Bassey, who joined the NBA recently)    
    # In this case, simply return 0 under the assumption that they wont be a top-scorer yet anyway.
    #if r'<span id="NBA" class="mw-headline">NBA</span>' not in html:
        #return 0 


    soup = BeautifulSoup(html, "html.parser")
    soup_table = soup.find("table")
    print(soup_table)

    return


if __name__ == "__main__":
    url = "https://en.wikipedia.org/wiki/2021_NBA_playoffs"
    teams, teams_url = get_teams(url)

    for (t, tu) in zip(teams, teams_url):
        print("%20s -  %s" % (t, tu))
        players, players_url = get_players(tu)
        for (p, pu) in zip(players, players_url):
            print("  ---> %40s - %s" % (p, pu))
            break
        break

    ppg = get_player_statistics("https://en.wikipedia.org/wiki/Seth_Curry")
    print(ppg)