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

    test_dates = """
    13 October 2020
    Oct 14, 2021
    not 14, 2021
    2021 Dec 24
    2020-10-13
    """

    print(find_dates(test_dates))


if __name__ == "__main__":
    test_find_urls()
    test_find_dates()
