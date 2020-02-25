from bs4 import BeautifulSoup
import requests

urls = {
  "fish": "https://animalcrossing.fandom.com/wiki/Fish_(New_Horizons)",
  "bugs": "https://animalcrossing.fandom.com/wiki/Bugs_(New_Horizons)"
}

def scrape(key, url): 
  print(key, url)
  response = (requests.get(url, timeout=5))
  soup = BeautifulSoup(response.content, "html.parser").prettify()

  print(soup)

if __name__=="__main__":
  for key in urls:
    scrape(key, urls[key])

  

