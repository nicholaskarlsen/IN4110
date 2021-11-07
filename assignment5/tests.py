from re import I
from filter_urls import find_urls
from collect_dates import find_dates


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



if __name__ == "__main__":
    test_find_urls()
    test_find_dates()
