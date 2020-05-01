from bs4 import BeautifulSoup
import requests, io
from util import separateByBr, avaiConverter, getPriceWithBellsString, getImageLinks, dumpData

URLS = { 
    # --- New Horizons ---
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

    # --- New Leaf ---
    # "fish": "https://animalcrossing.fandom.com/wiki/Fish_(New_Leaf)",
    # "bugs": "https://animalcrossing.fandom.com/wiki/Bugs_(New_Leaf)",
}

def scrapeBugs(key): # take url and return object containing bugs data
    url = URLS.get(key)
    # create soup object
    response = (requests.get(url, timeout=5))
    soup = BeautifulSoup(response.content, "html.parser")
    # find the target table
    table = soup.find_all("table", {"class": "sortable"})

    items = {}
    # go through each tr in the table, ignoring the table header
    for tr in table[0].find_all("tr")[1:]:
        tableData = []
        # get rid of empty space
        for td in tr.find_all("td"):
            tableData.append(td.next.strip())
        # find data and save it into an object
        name = tr.findChildren("td")[0].a.text
        item = {
            "name": name,
            "imageLink": tr.findChildren("a")[1]['href'],
            "price": int(tableData[2]),
            "location": tr.findChildren("td")[3].text.strip('\n').strip(),
            "time": tr.findChildren("small")[0].text,
            "seasons-northern-hemisphere": {
                "jan": avaiConverter(tableData[5]),
                "feb": avaiConverter(tableData[6]),
                "mar": avaiConverter(tableData[7]),
                "apr": avaiConverter(tableData[8]),
                "may": avaiConverter(tableData[9]),
                "jun": avaiConverter(tableData[10]),
                "jul": avaiConverter(tableData[11]),
                "aug": avaiConverter(tableData[12]),
                "sep": avaiConverter(tableData[13]),
                "oct": avaiConverter(tableData[14]),
                "nov": avaiConverter(tableData[15]),
                "dec": avaiConverter(tableData[16])
            },
            "seasons-southern-hemisphere": { # shift northern hemisphere by 6 months
                "jan": avaiConverter(tableData[11]),
                "feb": avaiConverter(tableData[12]),
                "mar": avaiConverter(tableData[13]),
                "apr": avaiConverter(tableData[14]),
                "may": avaiConverter(tableData[15]),
                "jun": avaiConverter(tableData[16]),
                "jul": avaiConverter(tableData[5]),
                "aug": avaiConverter(tableData[6]),
                "sep": avaiConverter(tableData[7]),
                "oct": avaiConverter(tableData[8]),
                "nov": avaiConverter(tableData[9]),
                "dec": avaiConverter(tableData[10])
            }
        }
        items[name] = item
    dumpData(items, key)
    # return for debugging
    return items

def scrapeFish(key): # same logic as scrapeBugs
    url = URLS.get(key)
    response = (requests.get(url, timeout=5))
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find_all("table", {"class": "sortable"})
    items = {}
    for tr in table[0].find_all("tr")[1:]:
        tableData = []
        for td in tr.find_all("td"):
            tableData.append(td.next.strip())
        name = tr.findChildren("td")[0].a.text
        item = {
            "name": name,
            "imageLink": tr.findChildren("a")[1]['href'],
            "price": int(tableData[2]),
            "location": tr.findChildren("td")[3].text.strip('\n').strip(),
            "shadowSize": tableData[4], # specific to fish
            "time": tr.findChildren("small")[0].text, 
            "seasons-northern-hemisphere": {
                "jan": avaiConverter(tableData[6]),
                "feb": avaiConverter(tableData[7]),
                "mar": avaiConverter(tableData[8]),
                "apr": avaiConverter(tableData[9]),
                "may": avaiConverter(tableData[10]),
                "jun": avaiConverter(tableData[11]),
                "jul": avaiConverter(tableData[12]),
                "aug": avaiConverter(tableData[13]),
                "sep": avaiConverter(tableData[14]),
                "oct": avaiConverter(tableData[15]),
                "nov": avaiConverter(tableData[16]),
                "dec": avaiConverter(tableData[17])
            },
            "seasons-southern-hemisphere": {
                "jan": avaiConverter(tableData[12]),
                "feb": avaiConverter(tableData[13]),
                "mar": avaiConverter(tableData[14]),
                "apr": avaiConverter(tableData[15]),
                "may": avaiConverter(tableData[16]),
                "jun": avaiConverter(tableData[17]),
                "jul": avaiConverter(tableData[6]),
                "aug": avaiConverter(tableData[7]),
                "sep": avaiConverter(tableData[8]),
                "oct": avaiConverter(tableData[9]),
                "nov": avaiConverter(tableData[10]),
                "dec": avaiConverter(tableData[11])
            }
        }
        items[name] = item
    dumpData(items, key)
    return items

def scrapeFossils(key): # same logic as scrapeBugs and scrapeFish
    url = URLS.get(key)
    response = (requests.get(url, timeout=5))
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find_all("table", {"class": "sortable"})
    items = {}
    # Stand-alone fossils
    for tr in table[0].find_all("tr")[1:]:
        tableData = []
        for td in tr.find_all("td"):
            tableData.append(td.next.strip())
        name = tr.findChildren("td")[0].a.text
        item = {
            "name": name,
            "imageLink": tr.findChildren("a")[1]['href'],
            "price": getPriceWithBellsString(tableData[2]),
            "isMultipart": False
        }
        tableData.append(item)
        items[name] = item

    # Multi-part fossils
    for tr in table[1].find_all("tr")[1:]:
        tableData = []
        tds = tr.find_all("td")
        if not tds:
            currentCategory = tr.findChildren("a")[0].text
            continue
        for td in tr.find_all("td"):
            tableData.append(td.next.strip())
        name = tr.findChildren("td")[0].a.text
        item = {
            "name": name,
            "imageLink": tr.findChildren("a")[1]['href'],
            "price": getPriceWithBellsString(tableData[2]),
            "isMultipart": True,
            "category": currentCategory
        }
        items[name] = item
    dumpData(items, key)
    return items

def scrapeVillagers(key):
    url = URLS.get(key)
    response = (requests.get(url, timeout=5))
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find_all("table", {"class": "sortable"})
    items = {}
    for tr in table[0].find_all("tr")[1:]:
        name = tr.findChildren("td")[0].a.text
        print(tr.findChildren("td")[1].a['href'])
        item = {
            "name": name,
            "imageLink": tr.findChildren("td")[1].a['href'],
            "personality": tr.findChildren("td")[2].text.strip("\n")[1:],
            "species": tr.findChildren("td")[3].text.strip("\n")[1:],
            "birthday": tr.findChildren("td")[4].text.strip("\n")[1:],
            "catchPhrase": tr.findChildren("td")[5].text.strip("\n")[1:]
        }
        items[name] = item
    dumpData(items, key)
    return items

def scrapeDIYTools(key):
    url = URLS.get(key)
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
    url = URLS.get(key)
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
    url = URLS.get(key)
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
    # scrapeBugs("bugs")
    # scrapeFish("fish")
    # scrapeFossils("fossils")

    # -- Characters -- 
    scrapeVillagers("villagers")

    # -- DIY Recipes -- 
    # scrapeDIYTools("tools")
    # scrapeDIYEquipments("housewares")
    # scrapeDIYEquipments("equipments")
    # scrapeDIYEquipments("miscellaneous")
    # scrapeDIYEquipments("others")
    # scrapeDIYWalls("wallMounteds")
    # scrapeDIYWalls("wallpaperRugsFloorings")
    pass
