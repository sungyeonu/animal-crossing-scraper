from bs4 import BeautifulSoup, Tag
import requests, io
import simplejson as json

urls = { 
    # Urls for New Horizons
    # Collectables
    "fish": "https://animalcrossing.fandom.com/wiki/Fish_(New_Horizons)",
    "bugs": "https://animalcrossing.fandom.com/wiki/Bugs_(New_Horizons)",
    "fossils": "https://animalcrossing.fandom.com/wiki/Fossils_(New_Horizons)",

    # DIY Recipes
    "tools": "https://animalcrossing.fandom.com/wiki/DIY_recipes/Tools",
    "housewares": "https://animalcrossing.fandom.com/wiki/DIY_recipes/Housewares",
    "wallMounteds": "https://animalcrossing.fandom.com/wiki/DIY_recipes/Wall-mounted",
    "wallpaperRugsFloorings": "https://animalcrossing.fandom.com/wiki/DIY_recipes/Wallpaper,_rugs_and_flooring",
    "equipments": "https://animalcrossing.fandom.com/wiki/DIY_recipes/Equipment",
    "others": "https://animalcrossing.fandom.com/wiki/DIY_recipes/Other"

    # Urls for New Leaf
    # "fish": "https://animalcrossing.fandom.com/wiki/Fish_(New_Leaf)",
    # "bugs": "https://animalcrossing.fandom.com/wiki/Bugs_(New_Leaf)"
}

def separateByBr(tag, result=''):
    for c in tag.contents:
        if isinstance(c, Tag):  # check if content is a tag
            if c.name == 'br':  # if tag is <br> append it as string
                result += ","
            else:  # for any other tag, recurse
                result = separateByBr(c, result)
        else:  # if content is NavigableString (string), append
            result += c
    return result

def avaiConverter(str): # returns True if item is available, False otherwise
    if (str == "\u2713" or str == "✔"): # "\u2713" is a checkmark
        return True
    else:
        return False

def getPriceWithBellsString(str):
    return int(str.replace(',', '').replace(' Bells', ''))

def getImageLinks(images):
    result = []
    for image in images:
        t = image.get("src")
        if (t.startswith("https")):
            result.append(image.get("src"))
    return result

def parseData(itemList, outfile): # turns object to json 
    with open(outfile, 'w') as f:
        json.dump(itemList, f) 

def scrapeBugs(url): # take url and return object containing bugs data
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
    return itemList

def scrapeFish(url): # same logic as scrapeBugs
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
    return itemList

def scrapeFossils(url): # same logic as scrapeBugs and scrapeFish
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
    return itemList

def scrapeDIYTools(url):
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
    return itemList

def scrapeDIYEquipments(url):
    response = (requests.get(url, timeout=5))
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find_all("table", {"class": "sortable"})
    itemList = []
    for item in table[0].find_all("tr")[1:]: # change to [1:] when done
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
    return itemList

if __name__ == "__main__":

    # Completed, json has already been produced

    # -- Collectibles -- 
    # bugsList = scrapeBugs(urls["bugs"])
    # parseData(bugsList, "bugs.json")
    # fishList = scrapeFish(urls["fish"])
    # parseData(fishList, "fish.json")
    # fossilsList = scrapeFossils(urls["fossils"])
    # parseData(fossilsList, "fossils.json")

    # Incomplete, please run the script and update the jsons
    # -- DIY Recipes -- 
    toolsList = scrapeDIYTools(urls["tools"])
    parseData(toolsList, "tools.json")
    housewaresList = scrapeDIYEquipments(urls["housewares"])
    parseData(housewaresList, "housewares.json")
    equipmentsList = scrapeDIYEquipments(urls["equipments"])
    parseData(equipmentsList, "equipments.json")

    # # wallMountedsList = scrapeDIYRecipes(urls["wallMounteds"])
    # # parseData(wallMountedsList, "wallMounteds.json")
    # # wallpaperRugsFlooringsList = scrapeDIYRecipes(urls["wallpaperRugsFloorings"])
    # # parseData(wallpaperRugsFlooringsList, "wallpaperRugsFloorings.json")

    othersList = scrapeDIYEquipments(urls["others"])
    parseData(othersList, "others.json")
