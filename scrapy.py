from bs4 import BeautifulSoup
import requests

urls = {
  "fish": "https://animalcrossing.fandom.com/wiki/Fish_(New_Horizons)",
  "bugs": "https://animalcrossing.fandom.com/wiki/Bugs_(New_Horizons)"
}

response = (requests.get(urls["fish"], timeout=5))
soup = BeautifulSoup(response.content, "html.parser").prettify()

print(soup)