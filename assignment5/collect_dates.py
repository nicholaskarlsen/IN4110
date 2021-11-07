import re
from requesting_urls import get_html


def get_months_str():
    """Utility function that returns a list of all months as list of strings in the correct order.

    Returns:
        list<String>: List of strings containing the name of all months.
    """
    months = [
        "January",
        "Februrary",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]
    return months


def get_months_abbr_str():
    """Utility function that returns a list of all months in an abbreviated form as list of strings
    in the correct order.

    Returns:
        list<String>: List of strings containing the name of all months in an abbreviated form.
    """
    months_abbr = [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
    ]
    return months_abbr


def num_to_day_str(num):
    """converts a number to a string, adding a leading 0 if the number is smaller than 10
        1 -> 01

    Returns:
        String representing a number, with a leading 0 if  <10
    """
    str = "%s" % num
    if int(num) < 10:
        str = "0" + str
    return str


def get_month_hash():
    """Generate a hashmap that maps months to their respective numbers, both in an abbreviated
    and unabbreviated form.

    Returns:
        dictionary: Hashmap which maps the name of months to their corresponding numbers
    """
    months = get_months_str()
    months_abbr = get_months_abbr_str()
    month_hash = {}
    # Populate the hash by assigning keys from both lists (which are ordered from Jan - Dec)
    for (i, month) in enumerate(months):
        month_hash[month] = num_to_day_str(i + 1)
    for (i, month) in enumerate(months_abbr):
        month_hash[month] = num_to_day_str(i + 1)

    return month_hash


def convert_DMY(dates_DMY):
    """Converts the entries in a list containing dates in the DMY format to our desired format, an ISO-like
    format delimited by / rather than -

    Returns:
        List of dates in YYYY/MM/DD format
    """
    output = []
    # create list of months & their abbreviations and join them with | acting as a separator; ie jan|feb|...
    months = "|".join(get_months_str() + get_months_abbr_str())
    # fetch hash that maps month names to numbers
    month_hash = get_month_hash()
    # compile pattern with 3 return groups corresponding to Day, Month and Year.
    pattern = re.compile("([0-9]{1,2}) (%s) ([0-9]{4})" % months)
    for date in dates_DMY:
        match = pattern.match(date)
        D = match.group(1)
        M = match.group(2)
        Y = match.group(3)
        output.append("%s/%s/%s" % (Y, month_hash[M], num_to_day_str(D)))
    return output


def convert_MDY(dates_MDY):
    """Converts the entries in a list containing dates in the MDY format to our desired format, an ISO-like
    format delimited by / rather than -.

    Returns:
        List of dates in YYYY/MM/DD format
    """
    output = []
    # create list of months & their abbreviations and join them with | acting as a separator; ie jan|feb|...
    months = "|".join(get_months_str() + get_months_abbr_str())
    # fetch hash that maps month names to numbers
    month_hash = get_month_hash()
    # compile pattern with 3 return groups corresponding to Day, Month and Year.
    pattern = re.compile("(%s) ([0-9]{1,2}), ([0-9]{4})" % months)
    for date in dates_MDY:
        match = pattern.match(date)
        M = match.group(1)
        D = match.group(2)
        Y = match.group(3)
        output.append("%s/%s/%s" % (Y, month_hash[M], num_to_day_str(D)))
    return output


def convert_YMD(dates_YMD):
    """Converts the entries in a list containing dates in the YMD format to our desired format, an ISO-like
    format delimited by / rather than -.

    Returns:
        List of dates in YYYY/MM/DD format
    """
    output = []
    # create list of months & their abbreviations and join them with | acting as a separator; ie jan|feb|...
    months = "|".join(get_months_str() + get_months_abbr_str())
    # fetch hash that maps month names to numbers
    month_hash = get_month_hash()
    # compile pattern with 3 return groups corresponding to Day, Month and Year.
    pattern = re.compile("([0-9]{4}) (%s) ([0-9]{1,2})" % months)
    for date in dates_YMD:
        match = pattern.match(date)
        Y = match.group(1)
        M = match.group(2)
        D = match.group(3)
        output.append("%s/%s/%s" % (Y, month_hash[M], num_to_day_str(D)))
    return output


def convert_ISO(dates_ISO):
    """Converts the entries in a list containing dates in the ISO format to our desired format, an ISO-like
    format delimited by / rather than -.

    Returns:
        List of dates in YYYY/MM/DD format
    """
    output = []
    for date in dates_ISO:
        output.append(re.sub(pattern="-", repl="/", string=date))
    return output


def find_dates(html_string, output=None):
    """
    Finds all dates in a html string.

    The returned list is in the following format:
    - 1998/10/12
    - 1998/11/04
    - 1999/01/13

    The following formats are considered when searching:
    DMY: 13 Oct(ober) 2020
    MDY: Oct(ober) 13, 2020
    YMD: 2020 Oct(ober) 13
    ISO: 2020-10-13

    # Finish Docstrng Here

    NOTE: Explanation of regex pattern used to catch days: (?:[1-9]|[1-2]?[0-9]|3?[01])
    - [1-9] : Numbers from 1-9, self explanatory
    - [1-2]?[0-9] : numbers 1 or 2 followed by 0-9 -> 10-29
    - 3?[01] : the number 3 followd by 0 or 1 -> 30-31
    => only complete numbers in the range 1-31 are caught.


    patterns used in ISO format follows from the same logic.

    Returns:
        results (list): A list with all the dates found in Y/M/D format
    """
    # create list of months & their abbreviations and join them with | acting as a separator; ie jan|feb|...
    months = "|".join(get_months_str() + get_months_abbr_str())

    # Expected format i.e 13 Oct(ober) 2020
    dates_DMY = re.findall(
        pattern="((?:[1-9]|[1-2]?[1-9]|3?[12]) (?:%s) [0-9]{4})" % months,
        string=html_string,
    )

    # Expected format i.e Oct(ober) 13, 2020
    dates_MDY = re.findall(
        pattern="((?:%s) (?:[1-9]|[1-2]?[1-9]|3?[01]), [0-9]{4})" % months,
        string=html_string,
    )

    # Expected format i.e 2020 Oct(ober) 13
    # NOTE: Extra (?:[^0-9]) needed at end to avoid returning only a single digit instead of the full number
    dates_YMD = re.findall(
        pattern="([0-9]{4} (?:%s) (?:[1-9]|[1-2]?[1-9]|3?[01]))(?:[^0-9])" % months,
        string=html_string,
    )

    # Expected format i.e YYYY-MM-DD
    dates_ISO = re.findall(
        pattern="([0-9]{4}-(?:0?[1-9]|1?[0-2])-(?:0?[0-9]|[1-2]?[0-9]|3?[01]))(?:[^0-9])",
        string=html_string,
    )

    # Convert all of the matches to the YYYY/MM/DD format
    result = []
    result += convert_DMY(dates_DMY)
    result += convert_MDY(dates_MDY)
    result += convert_YMD(dates_YMD)
    result += convert_ISO(dates_ISO)

    if output:
        outfile = open(output, "w")
        outfile.write("\n".join(result))
        outfile.close

    return result


if __name__ == "__main__":
    dir = "collect_dates_regex/"
    urls = [
        "https://en.wikipedia.org/wiki/J._K._Rowling",
        "https://en.wikipedia.org/wiki/Richard_Feynman",
        "https://en.wikipedia.org/wiki/Hans_Rosling",
    ]
    for url in urls:
        html = get_html(url)
        find_dates(html, output="%soutput_%s.txt" % (dir, url.split("/wiki/")[-1]))
