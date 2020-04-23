from bs4 import BeautifulSoup
import requests, io
from util import separateByBr, avaiConverter, getPriceWithBellsString, getImageLinks, dumpData

urls = { 
    # Urls for New Horizons
    # Critters
    "fish": "https://animalcrossing.fandom.com/wiki/Fish_(New_Horizons)",
    "bugs": "https://animalcrossing.fandom.com/wiki/Bugs_(New_Horizons)",
    "fossils": "https://animalcrossing.fandom.com/wiki/Fossils_(New_Horizons)",

    # Characters
    "villagers": "https://animalcrossing.fandom.com/wiki/Villager_list_(New_Horizons)",

    # DIY Recipes
    "tools": "https://animalcrossing.fandom.com/wiki/DIY_recipes/Tools",
    "housewares": "https://animalcrossing.fandom.com/wiki/DIY_recipes/Housewares",
    "miscellaneous": "https://animalcrossing.fandom.com/wiki/DIY_recipes/Miscellaneous",
    "equipments": "https://animalcrossing.fandom.com/wiki/DIY_recipes/Equipment",
    "others": "https://animalcrossing.fandom.com/wiki/DIY_recipes/Other",
    "wallMounteds": "https://animalcrossing.fandom.com/wiki/DIY_recipes/Wall-mounted",
    "wallpaperRugsFloorings": "https://animalcrossing.fandom.com/wiki/DIY_recipes/Wallpaper,_rugs_and_flooring",

    # Urls for New Leaf
    # "fish": "https://animalcrossing.fandom.com/wiki/Fish_(New_Leaf)",
    # "bugs": "https://animalcrossing.fandom.com/wiki/Bugs_(New_Leaf)"
}

def scrapeBugs(key): # take url and return object containing bugs data
    url = urls.get(key)
    # create soup object
    response = (requests.get(url, timeout=5))
    soup = BeautifulSoup(response.content, "html.parser")
    # find the target table
    table = soup.find_all("table", {"class": "sortable"})
    # contains all items
    itemList = []
    # ignore first row as it just contains labels to the data
    for item in table[0].find_all("tr")[1:]:
        itemInfo = []
        # get rid of empty space
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
        itemList.append(itemObject)
    dumpData(itemList, key)
    return itemList

def scrapeFish(key): # same logic as scrapeBugs
    url = urls.get(key)
    response = (requests.get(url, timeout=5))
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find_all("table", {"class": "sortable"})
    itemList = []
    for item in table[0].find_all("tr")[1:]:
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
        itemList.append(itemObject)
    dumpData(itemList, key)

    return itemList

def scrapeFossils(key): # same logic as scrapeBugs and scrapeFish
    url = urls.get(key)
    response = (requests.get(url, timeout=5))
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find_all("table", {"class": "sortable"})
    itemList = []

    # Stand-alone fossils
    for item in table[0].find_all("tr")[1:]:
        itemInfo = []
        for td in item.find_all("td"):
            itemInfo.append(td.next.strip())
        itemObject = {
            "name": item.findChildren("a")[0].text,
            "imageLink": item.findChildren("a")[1]['href'],
            "price": getPriceWithBellsString(itemInfo[2]),
            "isMultipart": False
        }
        itemList.append(itemObject)

    # Multi-part fossils
    for item in table[1].find_all("tr")[1:]:
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
        itemList.append(itemObject)
    dumpData(itemList, key)
    return itemList

def scrapeVillagers(key):
    url = urls.get(key)
    response = (requests.get(url, timeout=5))
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find_all("table", {"class": "sortable"})
    itemList = []
    for item in table[0].find_all("tr")[1:]:
        itemObject = {
            "name": item.findChildren("td")[0].a.text,
            "imageLink": item.findChildren("a")[1]['href'],
            "personality": item.findChildren("td")[2].text.strip("\n")[1:],
            "species": item.findChildren("td")[3].text.strip("\n")[1:],
            "birthday": item.findChildren("td")[4].text.strip("\n")[1:],
            "catchPhrase": item.findChildren("td")[5].text.strip("\n")[1:]
        }
        itemList.append(itemObject)
    dumpData(itemList, key)
    return itemList

def scrapeDIYTools(key):
    url = urls.get(key)
    response = (requests.get(url, timeout=5))
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find_all("table", {"class": "sortable"})
    itemList = []
    for item in table[0].find_all("tr")[1:]:
        itemInfo = []
        for td in item.find_all("td"):
            if not td.string is None:
                itemInfo.append(td.next.strip())
            else:
                itemInfo.append(td.next)
        itemObject = {
            "name": item.findChildren("td")[0].a.text,
        }
        try:
            itemObject["imageLink"] = item.findChildren("a")[1]['href']
        except AttributeError:
            itemObject["imageLink"] = None
        try:
            itemObject["materials"] = separateByBr(item.findChildren("td")[2]).strip("\n").split(",")
        except AttributeError:
            itemObject["materials"] = []
        try:
            itemObject["materialsImageLink"] = getImageLinks(item.findChildren("td")[2].find_all("img"))
        except AttributeError:
            itemObject["materialsImageLink"] = []
        try:
            itemObject["sizeLink"] = itemInfo[3].img.get("data-src")
        except AttributeError:
            itemObject["sizeLink"] = None
        try:
            itemObject["obtainedFrom"] = itemInfo[4].text
        except AttributeError:
            itemObject["obtainedFrom"] = None
        try:
            itemObject["price"] = int(itemInfo[5].strip().replace(",", ""))
        except: 
            itemObject["price"] = None
        try:
            itemObject["isRecipeItem"] = avaiConverter(itemInfo[6])
        except: 
            itemObject["isRecipeItem"] = None
        itemList.append(itemObject)
    dumpData(itemList, key)
    return itemList

def scrapeDIYEquipments(key):
    url = urls.get(key)
    response = (requests.get(url, timeout=5))
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find_all("table", {"class": "sortable"})
    itemList = []
    for item in table[0].find_all("tr")[1:]:
        itemInfo = []
        for td in item.find_all("td"):
            if not td.string is None:
                itemInfo.append(td.next.strip())
            else:
                itemInfo.append(td.next)
        itemObject = {
            "name": item.findChildren("td")[0].a.text,
        }
        try:
            itemObject["imageLink"] = item.findChildren("a")[1]['href']
        except AttributeError:
            itemObject["imageLink"] = None
        try:
            itemObject["materials"] = separateByBr(item.findChildren("td")[2]).strip("\n").split(",")
        except AttributeError:
            itemObject["materials"] = []
        try:
            itemObject["materialsImageLink"] = getImageLinks(item.findChildren("td")[2].find_all("img"))
        except AttributeError:
            itemObject["materialsImageLink"] = []
        try:
            itemObject["sizeLink"] = itemInfo[3].findChildren("a")[0]['href']
        except AttributeError:
            itemObject["sizeLink"] = None
        try:
            itemObject["obtainedFrom"] = itemInfo[4].text
        except AttributeError:
            itemObject["obtainedFrom"] = None
        try:
            itemObject["price"] = int(itemInfo[5].strip().replace(",", ""))
        except: 
            itemObject["price"] = None
        itemList.append(itemObject)
    dumpData(itemList, key)
    return itemList


def scrapeDIYWalls(key):
    url = urls.get(key)
    response = (requests.get(url, timeout=5))
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find_all("table", {"class": "sortable"})
    itemList = []
    for item in table[0].find_all("tr")[1:]: # change to [1:] when done
        itemObject = {
            "name": item.findChildren("td")[0].text.strip("\n")
        }
        if item.findChildren("a")[1]['href']:
            itemObject["imageLink"] = item.findChildren("a")[1]['href']
        if item.findChildren("td")[2]:
            itemObject["materials"] = separateByBr(item.findChildren("td")[2]).strip("\n").split(",")
            itemObject["materialsImageLink"] = getImageLinks(item.findChildren("td")[2].find_all("img"))
        if item.findChildren("td")[3].findChildren("a"):
            itemObject["sizeLink"] = item.findChildren("td")[3].findChildren("a")[0]['href']
        if item.findChildren("td")[4].text:
            itemObject["obtainedFrom"] = item.findChildren("td")[4].text.strip('\n')
        if item.findChildren("td")[5].text.strip().replace(",", ""):
            itemObject["price"] = int(item.findChildren("td")[5].text.strip().replace(",", ""))
        itemList.append(itemObject)
    dumpData(itemList, key)
    return itemList


if __name__ == "__main__":
    # -- Critters -- 
    scrapeBugs("bugs")
    scrapeFish("fish")
    scrapeFossils("fossils")

    # -- Characters -- 
    scrapeVillagers("villagers")

    # -- DIY Recipes -- 
    scrapeDIYTools("tools")
    scrapeDIYEquipments("housewares")
    scrapeDIYEquipments("equipments")
    scrapeDIYEquipments("miscellaneous")
    scrapeDIYEquipments("others")
    scrapeDIYWalls("wallMounteds")
    scrapeDIYWalls("wallpaperRugsFloorings")
