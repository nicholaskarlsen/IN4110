import numpy as np
from re import I
from filter_urls import find_urls
from collect_dates import find_dates
from fetch_player_statistics import get_teams, get_players, get_player_statistics


def test_find_urls():
    html = """
    <a href="#fragment-only">anchor link </a>
    <a id="some-id" href="/relative/path#fragment">relative link </a>
    <a href="//other.host/same-protocol">same-protocol link </a>
    <a href="https://example.com">absolute URL </a>
    """
    urls = find_urls(html, base_url="https://en.wikipedia.org")

    assert urls == [
        "https://en.wikipedia.org/relative/path",
        "https://other.host/same-protocol",
        "https://example.com",
    ]

    return


def test_find_dates():
    """
    Tests the find_dates function against two simple test cases, with both single and double digit days.
    Where the former is an important test case to ensure proper conversion of i.e the day "4" to "04".
    across all the functions.
    """

    test_dates = """
    13 Oct 2020
    13 October 2020
    Oct 13, 2020
    October 13, 2020
    2020 Oct 13
    2020 October 13
    2020-10-13
    """
    test_results = find_dates(test_dates)
    target = "2020/10/13"

    for test in test_results:
        assert test == target

    # Test a case with a single-digit day as well
    test_dates = """
    2 Nov 2020
    2 November 2020
    Nov 2, 2020
    November 2, 2020
    2020 Nov 2
    2020 November 2
    2020-11-02
    """
    test_results = find_dates(test_dates)
    target = "2020/11/02"

    for test in test_results:
        assert test == target

    return


def test_get_teams():
    """
    tests the get_teams function by ensuring that it extracts all of the teams that made it to the semifinals
    in 2021.
    """

    # List of teams that made it to the semifinals
    teams_ground_truth = [
        "Philadelphia 76ers",
        "Atlanta Hawks",
        "Milwaukee Bucks",
        "Brooklyn Nets",
        "Utah Jazz",
        "Los Angeles Clippers",
        "Denver Nuggets",
        "Phoenix Suns",
    ]

    # Attempt to extract the same list automagically using a script
    teams, _ = get_teams("https://en.wikipedia.org/wiki/2021_NBA_playoffs")

    # The lists are not necessarily in the same order -> sort them with numpy.
    teams_ground_truth = np.sort(teams_ground_truth)
    teams = np.sort(teams)

    # Check that both of these sorted arrays are equal
    np.testing.assert_array_equal(teams_ground_truth, teams)

    return


def test_get_players():
    """
    tests the get_players function by ensuring that it sextracts all of the players that play for the
    Philadelphia 76ers
    """
    # List of players in the Philadelphia 76ers
    players_ground_truth = [
        "Charles Bassey",
        "Seth Curry",
        "Andre Drummond",
        "Joel Embiid",
        "Danny Green",
        "Tobias Harris",
        "Aaron Henry",
        "Isaiah Joe",
        "Furkan Korkmaz",
        "Tyrese Maxey",
        "Shake Milton",
        "Georges Niang",
        "Paul Reed",
        "Grant Riller",
        "Ben Simmons",
        "Jaden Springer",
        "Matisse Thybulle",
    ]

    # Attempt to extract the same list automagically using a script
    players, _ = get_players(
        "https://en.wikipedia.org/wiki/2020%E2%80%9321_Philadelphia_76ers_season"
    )

    # The lists are not necessarily in the same order -> sort them with numpy.
    players_ground_truth = np.sort(players_ground_truth)
    players = np.sort(players)

    # Check that both of these sorted arrays are equal
    np.testing.assert_array_equal(players_ground_truth, players)
    return


def test_get_player_statistics():
    """
    Tests the get_player statistics by testing it on two players. One of which should return "default" values
    of 0 for each metric, since he does not have the correct table on the wikipedia page.
    """
    # Charles Bassey does not have the table on his wiki page (yet?)
    bassey = get_player_statistics("https://en.wikipedia.org/wiki/Charles_Bassey")
    # so all  metrics should return as 0.0 by default
    assert bassey["PPG"] == 0.0
    assert bassey["BPG"] == 0.0
    assert bassey["RPG"] == 0.0

    # Seth Curry does have the table, so check that the function retuns the correct values
    curry = get_player_statistics("https://en.wikipedia.org/wiki/Seth_Curry")
    assert curry["PPG"] == 12.5
    assert curry["BPG"] == 0.1
    assert curry["RPG"] == 2.4

    return


if __name__ == "__main__":
    test_find_urls()
    test_find_dates()
    test_get_teams()
    test_get_players()
    test_get_player_statistics()
