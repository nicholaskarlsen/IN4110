from requesting_urls import get_html
import re


def find_urls(html_str, base_url=None):
    """Parses a string containing HTML and returns any urls that are enclosed in <a> tag.
    We then further filter and modify the resultant matches to fit the following criteria:

    - Relative URLS are transformed to full urls given that base_url is defined. Else, they are deleted.
      i.e '/relative/url' would be transformed to 'https://www.base_url.org/relative/url'

    - Fragments are stripped from urls
      i.e 'https://www.base_url.org/relative/url#fragment' -> 'https://www.base_url.org/relative/url'

    - Matches that are composed only of a fragment are simply removed
      i.e '#fragment' -> DELETE

    - Matches which contains a colon AFTER the https:// part of the url are deleted
      i.e 'https://en.wikipedia.org/wiki/Avengers:_Endgame' -> DELETE

    Arguments:
        html_str (String): A string ideally containing valid HTML.
        base_url (list<String>):  Base url address of the website i.e https://www.base_url.org

    Returns:
        urls (list<String>): List of matched, and sanitized urls
    """
    # match must start with <a ...href=" and end with "...</a>, return what's in between.
    urls = re.findall(pattern=r"<a\s.*href=\"(?!#)(.*?)[\?#\"].*</a>", string=html_str)

    # Loop through the matches and clean them up, filter out unwanted entries etc.
    for i in range(len(urls)):
        # if the url starts with // (partial url)
        urls[i] = re.sub(pattern=("^(//)"), repl="https://", string=urls[i])

        # for relative urls starting with a single /
        # if base_url is not defined, delete the entry and print a warning message in the terminal.
        if re.match("^(/(?!/))", string=urls[i]):
            if base_url is None:
                print(
                    "[WARNING] Found relative url: %s\n%sbase_url argument not supplied. Deleting entry."
                    % (urls[i], (len("[WARNING] ")) * " ")
                )
                urls[i] = "DELETE"
            else:
                urls[i] = re.sub(
                    pattern="^(/(?!/))", repl=base_url + "/", string=urls[i]
                )

        # Remove any urls with a colon https://en.wikipedia.org/wiki/Avengers:_Endgame
        # urls[i] = re.sub(pattern="^https://.*:.*", repl="DELETE", string=urls[i])
        # If URL contains a get query, delete it.
        # urls[i] = re.sub(pattern=".*\?.*", repl="DELETE", string=urls[i])

    # Remove all entries that are marked for deletion
    urls = [url for url in urls if url != "DELETE"]

    return urls


def find_articles(url):
    html_str = get_html(url)
    base_url = re.findall(pattern="(.*wikipedia.org)(?:/.*)", string=url)[0]
    urls = find_urls(html_str=html_str, base_url=base_url)
    urls = "\n".join(urls)
    articles = re.findall(pattern="https://[a-z]*.wikipedia.org/wiki/.*", string=urls)
    return articles


if __name__ == "__main__":
    urls = [
        "https://en.wikipedia.org/wiki/Nobel_Prize",
        "https://en.wikipedia.org/wiki/Bundesliga",
        "https://en.wikipedia.org/wiki/2019%E2%80%9320_FIS_Alpine_Ski_World_Cup",
    ]

    for u in find_articles(urls[1]):
        print("-",u)
