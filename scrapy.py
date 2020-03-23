from bs4 import BeautifulSoup
import requests
import io
import simplejson as json

urls = {
    "fish": "https://animalcrossing.fandom.com/wiki/Fish_(New_Horizons)",
    # "fish": "https://animalcrossing.fandom.com/wiki/Fish_(New_Leaf)",
    "bugs": "https://animalcrossing.fandom.com/wiki/Bugs_(New_Horizons)",
    # "bugs": "https://animalcrossing.fandom.com/wiki/Bugs_(New_Leaf)"
}


def scrapeBugs(url):
    response = (requests.get(url, timeout=5))
    soup = BeautifulSoup(response.content, "html.parser")
    itemSoup = soup.find_all("table", {"class": "sortable"})
    itemArr = []
    for item in itemSoup[0].find_all("tr")[1:]:
        # print(item)
    # for item in itemSoup[0].find_all("tr")[1:]:
        itemInfo = []
        for td in item.find_all("td"):
            itemInfo.append(td.next.strip())

        itemObject = {
            "price": itemInfo[2],
            "location": item.findChildren("td")[3].text.strip('\n').strip(),
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
        if (item.findChildren("td")[0].a is None):
            itemObject["name"] = "Unknown"
        else:
            itemObject["name"] = item.findChildren("td")[0].a.text
        try:
            itemObject["imageLink"] = item.findChildren("a")[1]['href']
        except: # KeyError || IndexError
            itemObject["imageLink"] = "Unknown"
        itemArr.append(itemObject)
    return itemArr

def scrapeFish(url):
    response = (requests.get(url, timeout=5))
    soup = BeautifulSoup(response.content, "html.parser")
    itemSoup = soup.find_all("table", {"class": "sortable"})
    itemArr = []
    for item in itemSoup[0].find_all("tr")[1:]:
        itemInfo = []
        for td in item.find_all("td"):
            itemInfo.append(td.next.strip())
        itemObject = {
            "name":	item.findChildren("a")[0].text,
            "imageLink": item.findChildren("a")[1]['href'],
            "price": itemInfo[2],
            "location": item.findChildren("td")[3].text.strip('\n').strip(),
            "shadowSize": itemInfo[4],
            "time": item.findChildren("small")[0].text, 
            # "time": itemInfo[5], 
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
    return itemArr

def parseData(itemList, outfile): # turns list to json 
    with open(outfile, 'w') as f:
        json.dump(itemList, f) 
    
if __name__ == "__main__":
    # bugsList = scrapeBugs(urls["bugs"])
    # parseData(bugsList, "bugs.json")


    fishList = scrapeFish(urls["fish"])
    parseData(fishList, "fish.json")
