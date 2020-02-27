from bs4 import BeautifulSoup
import requests

urls = {
  # "fish": "https://animalcrossing.fandom.com/wiki/Fish_(New_Horizons)",
  "fish": "https://animalcrossing.fandom.com/wiki/Fish_(New_Leaf)",
  "bugs": "https://animalcrossing.fandom.com/wiki/Bugs_(New_Horizons)"
}

def scrape(key, url): 
  response = (requests.get(url, timeout=5))
  soup = BeautifulSoup(response.content, "html.parser")
  tables = soup.find_all('table', {"class" : "roundy sortable"})
  # tables = soup.find_all('table', attrs={"style" : "background: #76acda"})

  f = open("output.txt",'w')
  print(tables, file=f)



if __name__=="__main__":
  # for key in urls:
  #   scrape(key, urls[key])

  scrape("fish", urls["fish"])

  

