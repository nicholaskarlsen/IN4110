"""
Module used to generate interactive plots displaying statistics pertaining to the COVID-19 pandemic
"""

from datetime import datetime

import altair as alt
import pandas as pd
import numpy as np

# Suppress warning to avoid clutter in terminal
pd.options.mode.chained_assignment = None  # default='warn'


def get_data_from_csv(
    filename,
    countries=None,
    start=None,
    end=None,
    extra_columns=[
        "new_deaths",
        "new_deaths_per_million",
        "reproduction_rate",
        "people_fully_vaccinated_per_hundred",
    ],
):
    """Creates pandas dataframe from .csv file.

    Data will be filtered based on data column name, list of countries to be plotted and
    time frame chosen.

    As a bare minimum, the columns: "date", "continent", "location", "new_cases", "new_cases_per_million"
    are included, as these are required to satisfy the basic functionality of the website. However,
    you may freely add additional columns, as is done by default, that may also be displayed on the webpage.

    This function also computes and  adds an additional column containing the 7-day running average to 
    the dataframe.

    Args:
        filename (str): Filename of the CSV file

        columns (list(string), optional): a list of additional data columns you want to include

        countries ((list(string), optional): List of countries you want to include.
        If none is passed, dataframe should be filtered for the 6 countries with the highest
        number of cases per million at the last current date available in the timeframe chosen.

        start (string, optional): The first date to include in the returned dataframe.
            If specified, records earlier than this will be excluded.
            Default: include earliest date
            Example format: "2021-10-10"

        end (string, optional): The latest date to include in the returned data frame.
            If specified, records later than this will be excluded.
            Example format: "2021-10-10"

        extra_columns (list(string)): any additional data columns that you wish to include in the dataframe
        
    Returns:
        cases_df (dataframe): returns dataframe for the timeframe, columns, and countries chosen
    """
    # read .csv file, define which columns to read
    df = pd.read_csv(
        filename,
        sep=",",
        usecols=["date", "continent", "location", "new_cases", "new_cases_per_million"]
        + extra_columns,
        parse_dates=["date"],
        date_parser=lambda col: pd.to_datetime(col, format="%Y-%m-%d"),
    )
    if countries is None or countries == "":
        # no countries specified, pick 6 countries with the highest case count at end_date
        if end is None:
            # no end date specified, pick latest date available
            end_date = df.date.iloc[-1]
        else:
            end_date = datetime.strptime(end, "%Y-%m-%d")
        # df_latest_dates = df[df.date.isin([end_date])]

        # identify the 6 countries with the highest case count on the last included day by:
        # -> Filter down to rows corresponding to end date
        # -> sort by new cases in descending order
        # -> drop rows with NaN in the continent columns (corresponding to i.e World, Europe etc.)
        # -> keep only the 6 first rows
        # -> convert the location column to a numpy array of strings
        countries = (
            df[df.date == end_date]
            .sort_values(by="new_cases", ascending=False)
            .dropna(subset=["continent"])
            .head(6)
            .location.to_numpy()
        )

    # now filter to include only the selected countries
    cases_df = df.loc[df.location.isin(countries)]

    # apply date filters
    if start is not None:
        start_date = datetime.strptime(start, r"%Y-%m-%d")
        # exclude records earlier than start_date
        cases_df = cases_df[start <= cases_df.date]

    if end is not None:
        end_date = datetime.strptime(end, r"%Y-%m-%d")
        if start_date is not None and start_date >= end_date:
            raise ValueError("The start date must be earlier than the end date.")

        # exclude records later than end date
        cases_df = cases_df[end >= cases_df.date]

    # Compute the rolling average for each country
    for c in cases_df.location.unique():
        cases_df.loc[
            cases_df.location == c, "new_cases_per_million (7 day rolling average)"
        ] = (
            cases_df.loc[cases_df.location == c, "new_cases_per_million"]
            .rolling(7)
            .mean()
        )

    return cases_df


def get_countries(filename="data/owid-covid-data.csv"):
    """ Generate a list of all the countries present in the .csv file
    
    Args:
        filename (str): Filename of the CSV file

    Returns:
        (array) List of all the countries present in the dataset
    """
    df = pd.read_csv(filename, sep=",", usecols=["continent", "location"])
    # Filter out rows where "continent" is undefined, as these correspond to bulk statistics i.e "World" etc.
    return df.dropna(subset=["continent"]).location.unique()


def get_yaxis_cols(
    filename="data/owid-covid-data.csv", filter_out=["continent", "location", "date"]
):
    """ Get a list of the columns containing data in the dataframe. i.e excluding things like 
    "continent", "location", "date". What columns are excluded may be specified by setting the filter_out
    variable. The returned list is used to populate the drop-down menu on the website.

    Args:
        filename (str): Filename of the CSV file
        filter_out (list(str)): Which columns to exclude in the returned list

    Returns:
        (Array) List of all data columns in the dataset
    """
    cols = get_data_from_csv(filename=filename).columns
    cols = cols[np.isin(cols, filter_out, invert=True)]
    return cols


def plot_reported_cases_per_million(
    filename="data/owid-covid-data.csv",
    countries=None,
    start=None,
    end=None,
    yaxis="new_cases_per_million",
):
    """Plots data of reported covid-19 cases per million using altair.
    Calls the function get_data_from_csv to receive a dataframe used for plotting.

    Args:
        countries ((list(string), optional): List of countries you want to filter.
            If none is passed, dataframe will be filtered for the 6 countries with the highest
            number of cases per million at the last current date available in the timeframe chosen.

        start (string, optional): a string of the start date of the table, none
            of the dates will be older then this on

        end (string, optional): a string of the en date of the table, none of
            the dates will be newer then this one

        yaxis (String): Pick which dataset to display. i.e which column of the dataframe will be plotted on 
            the y-axis. This parameter is intended to be used to allow the user to select a dataset from
            the drop-down menu on the webpage.

    Returns:
        altair Chart of number of reported covid-19 cases over time.
    """
    # create dataframe
    cases_df = get_data_from_csv(
        filename=filename, countries=countries, start=start, end=end
    )

    # Note: when you want to plot all countries simultaneously while enabling checkboxes, you might need to disable altairs max row limit by commenting in the following line
    alt.data_transformers.disable_max_rows()

    chart = (
        alt.Chart(cases_df, title="Reported Cases of COVID-19")
        .mark_line(size=2)
        .encode(
            x=alt.X(
                "date:T",
                axis=alt.Axis(
                    format="%b, %Y", title="Date", titleFontSize=14, tickCount=20
                ),
            ),
            y=alt.Y(
                yaxis, axis=alt.Axis(title=yaxis, titleFontSize=14, tickCount=10,),
            ),
            color=alt.Color("location:N", legend=alt.Legend(title="Country")),
        )
    )

    return (chart).properties(height=400, width=600).interactive()


if __name__ == "__main__":
    chart = plot_reported_cases_per_million("data/owid-covid-data.csv")
    chart.show()
