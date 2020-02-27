from bs4 import BeautifulSoup
import requests
import io
urls = {
  # "fish": "https://animalcrossing.fandom.com/wiki/Fish_(New_Horizons)",
  "fish": "https://animalcrossing.fandom.com/wiki/Fish_(New_Leaf)",
  "bugs": "https://animalcrossing.fandom.com/wiki/Bugs_(New_Horizons)"
}
fname = "output.txt"

def scrape(key, url): 
  response = (requests.get(url, timeout=5))
  soup = BeautifulSoup(response.content, "html.parser")
  itemArr = []
  itemSoup = soup.find_all('table', {"class" : "roundy sortable"})

  with io.open(fname, "w", encoding="utf-8") as f:
    print(itemSoup, file=f)

  with io.open("test.txt", "w", encoding="utf-8") as f1:
    temp = itemSoup[0]

    for sibling in itemSoup[0].tr.next_siblings:
      print(repr(sibling), file=f1)




  

if __name__=="__main__":
  # for key in urls:
  #   scrape(key, urls[key])
  scrape("fish", urls["fish"])

  

