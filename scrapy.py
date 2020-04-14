from bs4 import BeautifulSoup
import requests, io
import simplejson as json

urls = { 
    # Urls for New Horizons
    "fish": "https://animalcrossing.fandom.com/wiki/Fish_(New_Horizons)",
    "bugs": "https://animalcrossing.fandom.com/wiki/Bugs_(New_Horizons)",
    "fossils": "https://animalcrossing.fandom.com/wiki/Fossils_(New_Horizons)",

    # Urls for New Leaf
    # "fish": "https://animalcrossing.fandom.com/wiki/Fish_(New_Leaf)",
    # "bugs": "https://animalcrossing.fandom.com/wiki/Bugs_(New_Leaf)"
}

def avaiConverter(str): # returns True if item is available, False otherwise
    if (str == "\u2713"): # "\u2713" is a checkmark
        return True
    else:
        return False

def getPriceWithBellsString(str):
    return int(str.replace(',', '').replace(' Bells', ''))

def parseData(itemList, outfile): # turns object to json 
    with open(outfile, 'w') as f:
        json.dump(itemList, f) 

def scrapeBugs(url): # take url and return object containing bugs data
    # create soup object
    response = (requests.get(url, timeout=5))
    soup = BeautifulSoup(response.content, "html.parser")
    # find the target table
    itemSoup = soup.find_all("table", {"class": "sortable"})
    # contains all items
    itemArr = []
    # ignore first row as it just contains labels to the data
    for item in itemSoup[0].find_all("tr")[1:]:
        itemInfo = []
        for td in item.find_all("td"):
            itemInfo.append(td.next.strip())
        # find data and save it into an object
        itemObject = {
            "name": item.findChildren("td")[0].a.text,
            "imageLink": item.findChildren("a")[1]['href'],
            "price": int(itemInfo[2]),
            "location": item.findChildren("td")[3].text.strip('\n').strip(),
            "time": item.findChildren("small")[0].text,
            "jan": avaiConverter(itemInfo[5]),
            "feb": avaiConverter(itemInfo[6]),
            "mar": avaiConverter(itemInfo[7]),
            "apr": avaiConverter(itemInfo[8]),
            "may": avaiConverter(itemInfo[9]),
            "jun": avaiConverter(itemInfo[10]),
            "jul": avaiConverter(itemInfo[11]),
            "aug": avaiConverter(itemInfo[12]),
            "sep": avaiConverter(itemInfo[13]),
            "oct": avaiConverter(itemInfo[14]),
            "nov": avaiConverter(itemInfo[15]),
            "dec": avaiConverter(itemInfo[16])
        }
        itemArr.append(itemObject)
    return itemArr

def scrapeFish(url): # same logic as scrapeBugs
    response = (requests.get(url, timeout=5))
    soup = BeautifulSoup(response.content, "html.parser")
    itemSoup = soup.find_all("table", {"class": "sortable"})
    itemArr = []
    for item in itemSoup[0].find_all("tr")[1:]:
        itemInfo = []
        for td in item.find_all("td"):
            itemInfo.append(td.next.strip())
        itemObject = {
            "name": item.findChildren("a")[0].text,
            "imageLink": item.findChildren("a")[1]['href'],
            "price": int(itemInfo[2]),
            "location": item.findChildren("td")[3].text.strip('\n').strip(),
            "shadowSize": itemInfo[4], # specific to fish
            "time": item.findChildren("small")[0].text, 
            "jan": avaiConverter(itemInfo[6]),
            "feb": avaiConverter(itemInfo[7]),
            "mar": avaiConverter(itemInfo[8]),
            "apr": avaiConverter(itemInfo[9]),
            "may": avaiConverter(itemInfo[10]),
            "jun": avaiConverter(itemInfo[11]),
            "jul": avaiConverter(itemInfo[12]),
            "aug": avaiConverter(itemInfo[13]),
            "sep": avaiConverter(itemInfo[14]),
            "oct": avaiConverter(itemInfo[15]),
            "nov": avaiConverter(itemInfo[16]),
            "dec": avaiConverter(itemInfo[17])
        }
        itemArr.append(itemObject)
    return itemArr

def scrapeFossils(url): # same logic as scrapeBugs and scrapeFish
    response = (requests.get(url, timeout=5))
    soup = BeautifulSoup(response.content, "html.parser")
    itemSoup = soup.find_all("table", {"class": "sortable"})
    itemArr = []
    for item in itemSoup[0].find_all("tr")[1:]:
        itemInfo = []
        for td in item.find_all("td"):
            itemInfo.append(td.next.strip())

        itemObject = {
            "name": item.findChildren("a")[0].text,
            "imageLink": item.findChildren("a")[1]['href'],
            "price": getPriceWithBellsString(itemInfo[2]),
            "isMultipart": False
        }
        itemArr.append(itemObject)

    for item in itemSoup[1].find_all("tr")[1:]:
        itemInfo = []
        items = item.find_all("td")

        if not items:
            category = item.findChildren("a")[0].text
            continue

        for td in item.find_all("td"):
            itemInfo.append(td.next.strip())

        itemObject = {
            "name": item.findChildren("a")[0].text,
            "imageLink": item.findChildren("a")[1]['href'],
            "price": getPriceWithBellsString(itemInfo[2]),
            "isMultipart": True,
            "category": category
        }
        itemArr.append(itemObject)
    return itemArr
    
if __name__ == "__main__":
    bugsList = scrapeBugs(urls["bugs"])
    parseData(bugsList, "bugs.json")
    fishList = scrapeFish(urls["fish"])
    parseData(fishList, "fish.json")
    fossilsList = scrapeFossils(urls["fossils"])
    parseData(fossilsList, "fossils.json")
