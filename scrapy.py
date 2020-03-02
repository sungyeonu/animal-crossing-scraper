from bs4 import BeautifulSoup
import requests
import io

urls = {
    # "fish": "https://animalcrossing.fandom.com/wiki/Fish_(New_Leaf)",
    "fish": "https://animalcrossing.fandom.com/wiki/Fish_(New_Horizons)",
    # "bugs": "https://animalcrossing.fandom.com/wiki/Bugs_(New_Horizons)",
    "bugs": "https://animalcrossing.fandom.com/wiki/Bugs_(New_Leaf)"
}


def scrapeBugs(url, output):
    response = (requests.get(url, timeout=5))
    soup = BeautifulSoup(response.content, "html.parser")
    itemSoup = soup.find_all("table", {"class": "sortable"})
    itemArr = []
    with io.open(output, "w", encoding="utf-8") as f:
        for item in itemSoup[0].find_all("tr")[1:]:
            itemInfo = []
            for td in item.find_all("td"):
                itemInfo.append(td.next.strip())
            itemObject = {
                "name":	item.findChildren("a")[0].text,
                "image": item.findChildren("a")[1]['href'],
                "price": itemInfo[2],
                "location": itemInfo[3],
                "time": item.findChildren("small")[0].text,
                "jan": itemInfo[5],
                "feb": itemInfo[6],
                "mar": itemInfo[7],
                "apr": itemInfo[8],
                "may": itemInfo[9],
                "jun": itemInfo[10],
                "jul": itemInfo[11],
                "aug": itemInfo[12],
                "sep": itemInfo[13],
                "oct": itemInfo[14],
                "nov": itemInfo[15],
                "dec": itemInfo[16]
            }
            itemArr.append(itemObject)
        for i in itemArr:
            print(i, file=f)
    return itemArr

def scrapeFish(url, output):
    response = (requests.get(url, timeout=5))
    soup = BeautifulSoup(response.content, "html.parser")
    # test without "roundy"
    itemSoup = soup.find_all("table", {"class": "sortable"})
    itemArr = []
    with io.open(output, "w", encoding="utf-8") as f:
        for item in itemSoup[0].find_all("tr")[1:]:
            itemInfo = []
            for td in item.find_all("td"):
                itemInfo.append(td.next.strip())
            itemObject = {
                "name":	item.findChildren("a")[0].text,
                "image": item.findChildren("a")[1]['href'],
                "price": itemInfo[2],
                "location": itemInfo[3],
                "shadow-size": itemInfo[4],
                "time": item.findChildren("small")[0].text,
                "jan": itemInfo[6],
                "feb": itemInfo[7],
                "mar": itemInfo[8],
                "apr": itemInfo[9],
                "may": itemInfo[10],
                "jun": itemInfo[11],
                "jul": itemInfo[12],
                "aug": itemInfo[13],
                "sep": itemInfo[14],
                "oct": itemInfo[15],
                "nov": itemInfo[16],
                "dec": itemInfo[17]
            }
            itemArr.append(itemObject)
        for i in itemArr:
            print(i, file=f)
    return itemArr

def parseData(itemList): # turns list to json 
    with open('fishData.json', 'w') as outfile:
        json.dump(itemList, outfile) 
    

if __name__ == "__main__":
    t = scrapeBugs(urls["bugs"], "bugs.txt")
    #scrapeFish(urls["fish"], "fish.txt")
    parseData(t)
