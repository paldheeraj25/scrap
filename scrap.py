# module to fetch the url
import urllib3
# module to query the page
from bs4 import BeautifulSoup

# url to be scraped
wiki = "https://en.wikipedia.org/wiki/List_of_state_and_union_territory_capitals_in_India"

# query the url and return the object in the variable page
http = urllib3.PoolManager()

response = http.request('GET', wiki)
soup = BeautifulSoup(response.data, 'html.parser')
