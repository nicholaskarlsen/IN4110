import requests as req


def get_html(url, params=None, output=None):
    """Fetch the HTML code from a given URL using requests. May also optionally write the HTML to file.

    Args:
        url (str): URL of the website from which you want the HTML
        params (dict): Dict containing any get requests
        output (str): Filename of the optional outfile

    Returns:
        A string containing the HTML code from the requested URL
    """
    # passing the optional parameters argument to the get function
    if params != None:
        url += "/get"

    response = req.get(url, params=params)

    # if output is specified, the response txt and url get printed to a txt file with the name in 'output'
    if output != None:
        outfile = open(output, "w")
        # outfile.write("URL: %s\n" % response.url)
        outfile.write(response.text)

    return response.text


if __name__ == "__main__":
    # Generate the output for problem 5.1

    get_html(
        url="https://en.wikipedia.org/wiki/Studio_Ghibli",
        output="requesting_urls/output_Studio_Ghibli.txt",
    )

    get_html(
        url="https://en.wikipedia.org/wiki/Star_Wars",
        output="requesting_urls/output_Star_Wars.txt",
    )

    get_html(
        url="https://en.wikipedia.org/w/index.php",
        params={"title": "Main_Page", "action": "info"},
        output="requesting_urls/output_index.txt",
    )
