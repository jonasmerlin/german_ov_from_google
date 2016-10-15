# This is a template for a Python scraper on morph.io (https://morph.io)
# including some code snippets below that you should find helpful

# import scraperwiki
# import lxml.html
#
# # Read in a page
# html = scraperwiki.scrape("http://foo.com")
#
# # Find something on the page using css selectors
# root = lxml.html.fromstring(html)
# root.cssselect("div[align='left']")
#
# # Write out to the sqlite database using scraperwiki library
# scraperwiki.sqlite.save(unique_keys=['name'], data={"name": "susan", "occupation": "software developer"})
#
# # An arbitrary query against the database
# scraperwiki.sql.select("* from data where 'name'='peter'")

# You don't have to do things with the ScraperWiki and lxml libraries.
# You can use whatever libraries you want: https://morph.io/documentation/python
# All that matters is that your final data is written to an SQLite database
# called "data.sqlite" in the current working directory which has at least a table
# called "data".

import re
import pickle
import datetime

from bs4 import BeautifulSoup
import scraperwiki
import requests

dates = {
    0: datetime.date.today(),
    1: datetime.date.today() + datetime.timedelta(1),
    2: datetime.date.today() + datetime.timedelta(2),
    3: datetime.date.today() + datetime.timedelta(3),
}

with open("cities.txt", "rb") as f:
    cities = pickle.load(f)
    for city in cities[:3]:
        for i in range(4):
            replaced_city = city.encode("utf-8").replace(" ", "+")
            url = "http://www.google.com/movies?near={}&date={}".format(replaced_city, i)
            page = requests.get(url)
            soup = BeautifulSoup(page.text, "html.parser")
            movies = soup.find_all(string=re.compile(".*\(OV\).*"))
            for movie in movies:
                complete_info = movie.find_parent('div', class_="movie")
                theater = movie.find_parent("div", class_="theater")
                data = {
                    "stadt": unicode(city),
                    "kino": unicode(theater.find("h2", class_="name").string),
                    "film": unicode(complete_info.find("div", class_="name").string),
                    "tag": dates[i],
                    "zeiten": ",".join([child.contents[2] for child in complete_info.find("div", class_="times").children])
                }
                # print data
                scraperwiki.sqlite.save(unique_keys=["stadt", "kino", "film", "tag"], data=data)
