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
    i = 0
    for sibling in temp.tr.next_siblings:
      # if sibling == <td style="background-color:#ffffff; border-bottom: 1px 76acda; border-top-left-radius:10px;-moz-border-radius-topleft:10px;-webkit-border-top-left-radius:10px;-khtml-border-top-left-radius:10px;-icab-border-top-left-radius:10px;-o-border-top-left-radius:10px;border-bottom-left-radius:10px;-moz-border-radius-bottomleft:10px;-webkit-border-bottom-left-radius:10px;-khtml-border-bottom-left-radius:10px;-icab-border-bottom-left-radius:10px;-o-border-bottom-left-radius:10px;"> <a href="/wiki/Bitterling" title="Bitterling">Bitterling</a>
      # if (sibling.)
      # print(sibling.name)
      if (sibling.name == "tr"):
        i += 1 # there are 72 tr's
      # print(sibling, file = f1)
      print(repr(sibling), file=f1)
    print(i)




  

if __name__=="__main__":
  # for key in urls:
  #   scrape(key, urls[key])
  scrape("fish", urls["fish"])

  

