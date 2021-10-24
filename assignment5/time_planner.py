from bs4 import BeautifulSoup
import requests as req

url = "https://en.wikipedia.org/wiki/List_of_soups"
request = req.get(url)

soup = BeautifulSoup(request.text , "html.parser")
print(soup.title)
soup_table = soup.find("table", {"class":"wikitable sortable"})