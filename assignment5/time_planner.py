import os
import requests as req
from bs4 import BeautifulSoup
from requesting_urls import get_html


def extract_events(url):
    """Extract date, venue and type (discipline) for competitions and return them in a dictionary
    containing lists

    Args:
        url (str): The url to extract events from.
    Returns:
        table_info (dict of lists): the keys are: [Date, Venue, Type], and each entry contains a list
    """
    disciplines = {
        "DH": "Downhill",
        "SL": "Slalom",
        "GS": "Giant Slalom",
        "SG": "Super Giant Slalom",
        "AC": "Alpine Combined",
        "PG": "Parallel Giant Slalom",
    }

    html = get_html(url)
    soup = BeautifulSoup(html, "html.parser")
    soup_table = soup.find("table", {"class": "wikitable sortable"})
    rows = soup_table.find_all("tr")

    table = {"Date": [], "Venue": [], "Type": []}
    table_col = {"Date": None, "Venue": None, "Type": None}

    # First row of the table consists of the headers. Find which columns contains the relevant entries
    headers = rows[0].findAll("th")
    for (i, header) in enumerate(headers):
        header = header.text.strip()
        if header in table.keys():
            table_col[header] = i

    # Number of columns in a regular row
    num_cols = len(headers)

    for (i, row) in enumerate(rows[1:]):  # Skip the first row (containing the headers)
        columns = row.findAll("td")

        # Regular rows
        if len(columns) == num_cols:
            for key in table.keys():
                col = table_col[key]
                content = columns[col].text.strip()
                if key == "Type":
                    content = content.split()[0]
                    content = disciplines[content]
                table[key].append(content)

        # Irregular row where venue + slope entries spans multiple rows require special treatment.
        elif 1 < len(columns) < num_cols:
            # Date is in the usual form
            table["Date"].append(columns[table_col["Date"]].text.strip())

            # Venue is repeated from the previous row
            table["Venue"].append(table["Venue"][-1])

            # The type/discipline is the "num_cols-len(columns)" column for these type of rows.
            type_content = (
                columns[table_col["Type"] - (num_cols - len(columns))]
                .text.strip()
                .split()[0]
            )
            type_content = disciplines[type_content]
            table["Type"].append(type_content)

        # If there is only a single column, skip to the next row (as is done by not matching the above ifs)
        # i.e the rows containing "2022 Winter Olympics" and "World Cup Season Final "
    return table


def create_betting_slip(events, save_as):
    """Saves a markdown format betting slip to the location'./ datetime_filter/<save_as >.md'.

    Args:
        events (dict): takes a dict of lists containing date, venue and type for each event.
        save_as (string): filename to save the markdown betting slip as.
    """
    # ensure directory exists
    os.makedirs("datetime_filter", exist_ok=True)

    with open(f"./datetime_filter/{save_as}.md", "w") as out_file:
        out_file.write(f"# BETTING SLIP ({ save_as })\n\nName:\n\n")

        out_file.write("| Date | Venue | Discipline | Who Wins? |\n")
        out_file.write("|---|---|---|---|\n")
        for e in zip(events["Date"], events["Venue"], events["Type"]):
            date, venue, type = e
            out_file.write(f"| {date} | {venue} | {type} | |\n")


if __name__ == "__main__":
    url = "https://en.wikipedia.org/wiki/2021%E2%80%9322_FIS_Alpine_Ski_World_Cup"
    events = extract_events(url)
    create_betting_slip(events, "betting_slip_empty")
