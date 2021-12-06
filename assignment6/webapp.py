import uvicorn
from typing import Optional
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from webvisualization_plots import (
    plot_reported_cases_per_million,
    get_countries,
    get_yaxis_cols,
)

# create app variable (FastAPI instance)
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# mount one or more static directories,
# e.g. your auto-generated Sphinx documentation with html files
app.mount(
    # the URL where these files will be available
    "/sphinx_docs",
    StaticFiles(
        # the directory the files are in
        directory="docs/_build/html/",
        html=True,
    ),
    # an internal name for FastAPI
    name="sphinx_docs",
)


@app.get("/")
def plot_reported_cases_per_million_html(request: Request):
    """
    Root route for the web application.
    Handle requests that go to the path "/".
    """
    return templates.TemplateResponse(
        "plot_reported_cases_per_million.html",
        {
            "request": request,
            "countries": get_countries(),
            "yaxis_names": get_yaxis_cols(),
            # further template inputs here
        },
    )


@app.get("/plot_reported_cases_per_million.json")
def plot_reported_cases_per_million_json(
    countries: Optional[str] = None,
    start: Optional[str] = None,
    end: Optional[str] = None,
    yaxis: Optional[str] = None,
):
    """Return json chart from altair"""

    if countries:
        countries = countries.split(",")

    figure = plot_reported_cases_per_million(countries=countries, yaxis=yaxis)
    return figure.to_dict()


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
