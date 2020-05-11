from bs4 import BeautifulSoup
import requests, io
from util import separateByBr, avaiConverter, getPriceWithBellsString, getImageLinks, dumpData

URLS = {
    # --- New Horizons ---
    # Museum
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
        # scrape each item
        name = tr.findChildren("td")[0].a.text
        item = {
            "name": name,
            "imageLink": tr.findChildren("a")[1]['href'],
            "price": int(tableData[2]),
            "location": tr.findChildren("td")[3].text.strip('\n').strip(),
            "time": tr.findChildren("small")[0].text,
            "seasonsNorthernHemisphere": {
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
            "seasonsSouthernHemisphere": { # shift northern hemisphere by 6 months
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
    dumpData(items, "museum/" + key)
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
            "seasonsNorthernHemisphere": {
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
            "seasonsSouthernHemisphere": {
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
    dumpData(items, "museum/" + key)
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
    dumpData(items, "museum/" + key)
    return items

def scrapeVillagers(key):
    url = URLS.get(key)
    response = (requests.get(url, timeout=5))
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find_all("table", {"class": "sortable"})
    items = {}
    for tr in table[0].find_all("tr")[1:]:
        name = tr.findChildren("td")[0].a.text
        item = {
            "name": name,
            "imageLink": tr.findChildren("td")[1].a['href'],
            "personality": tr.findChildren("td")[2].text.strip("\n").lstrip(),
            "species": tr.findChildren("td")[3].text.strip("\n").lstrip(),
            "birthday": tr.findChildren("td")[4].text.strip("\n").lstrip(),
            "catchPhrase": tr.findChildren("td")[5].text.strip("\n").lstrip()
        }
        items[name] = item
    dumpData(items, key)
    return items

def scrapeDIYTools(key):
    url = URLS.get(key)
    response = (requests.get(url, timeout=5))
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find_all("table", {"class": "sortable"})
    items = {}
    for tr in table[0].find_all("tr")[1:]:
        name = tr.findChildren("td")[0].a.text
        item = {
            "name": name,
        }
        if tr.findChildren("a")[1]['href']:
            item["imageLink"] = tr.findChildren("a")[1]['href']
        if tr.findChildren("td")[2]:
            item["materials"] = separateByBr(tr.findChildren("td")[2]).strip("\n").split(",")
        if tr.findChildren("td")[2].find_all("img"):
            item["materialsImageLink"] = getImageLinks(tr.findChildren("td")[2].find_all("img"))
        if tr.findChildren("td")[3].img.get("data-src"):
            item["sizeImageLink"] = tr.findChildren("td")[3].img.get("data-src")
        if tr.findChildren("td")[4].text:
            item["obtainedFrom"] = tr.findChildren("td")[4].text.strip("\n").splitlines()
        if tr.findChildren("td")[5]:
            item["price"] = int(tr.findChildren("td")[5].next.strip().replace(",", ""))
        # if tr.findChildren("td")[6]:
        #     item["isRecipeItem"] = avaiConverter(tr.findChildren("td")[6].next.strip("\n"))
        items[name] = item
    dumpData(items, "crafting/" + key)
    return items

def scrapeDIYEquipments(key):
    url = URLS.get(key)
    response = (requests.get(url, timeout=5))
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find_all("table", {"class": "sortable"})
    items = {}
    for tr in table[0].find_all("tr")[1:]:
        name = tr.findChildren("td")[0].a.text
        item = {
            "name": name,
        }
        if tr.findChildren("a")[1]['href']:
            item["imageLink"] = tr.findChildren("a")[1]['href']
        if tr.findChildren("td")[2]:
            item["materials"] = separateByBr(tr.findChildren("td")[2]).strip("\n").split(",")
        if tr.findChildren("td")[2].find_all("img"):
            item["materialsImageLink"] = getImageLinks(tr.findChildren("td")[2].find_all("img"))
        if tr.findChildren("td")[3].img.get("data-src"):
            item["sizeImageLink"] = tr.findChildren("td")[3].img.get("data-src")
        if tr.findChildren("td")[4].text:
            item["obtainedFrom"] = tr.findChildren("td")[4].text.strip("\n").splitlines()
        if tr.findChildren("td")[5]:
            item["price"] = int(tr.findChildren("td")[5].next.strip().replace(",", ""))
        items[name] = item
    dumpData(items, "crafting/" + key)
    return items

def scrapeDIYWallpapers(key):
    url = URLS.get(key)
    response = (requests.get(url, timeout=5))
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find_all("table", {"class": "sortable"})
    items = {}
    for tr in table[0].find_all("tr")[1:]:
        name = tr.findChildren("td")[0].a.text
        item = {
            "name": name,
        }
        if tr.findChildren("a")[1]['href']:
            item["imageLink"] = tr.findChildren("a")[1]['href']
        if tr.findChildren("td")[2]:
            item["materials"] = separateByBr(tr.findChildren("td")[2]).strip("\n").split(",")
            item["materialsImageLink"] = getImageLinks(tr.findChildren("td")[2].find_all("img"))
        if tr.findChildren("td")[3].findChildren("a"):
            item["sizeLink"] = tr.findChildren("td")[3].findChildren("a")[0]['href']
        if tr.findChildren("td")[4].text:
            item["obtainedFrom"] = tr.findChildren("td")[4].text.strip('\n').splitlines()
        if tr.findChildren("td")[5].text.strip().replace(",", ""):
            item["price"] = int(tr.findChildren("td")[5].text.strip().replace(",", ""))
        items[name] = item
    dumpData(items, "crafting/" + key)
    return items

def scrapeDIYOthers(key):
    url = URLS.get(key)
    response = (requests.get(url, timeout=5))
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.findChildren("table", {"class": "roundy"})
    items = {}
    for tr in table[0].find_all("tr")[1:]:
        name = tr.findChildren("td")[0].a.text
        # print(tr)
        item = {
            "name": name,
        }
        items[name] = item
        if tr.findChildren("a")[1]['href']:
            item["imageLink"] = tr.findChildren("a")[1]['href']
        # if tr.findChildren("td")[2]:
        #     item["materials"] = separateByBr(tr.findChildren("td")[2]).strip("\n").split(",")
        # if tr.findChildren("td")[2].find_all("img"):
        #     item["materialsImageLink"] = getImageLinks(tr.findChildren("td")[2].find_all("img"))
        # if tr.findChildren("td")[3].img.get("data-src"):
        #     item["sizeImageLink"] = tr.findChildren("td")[3].img.get("data-src")
        # if tr.findChildren("td")[4].text:
        #     item["obtainedFrom"] = tr.findChildren("td")[4].text.strip("\n").splitlines()
        # if tr.findChildren("td")[5]:
        #     item["price"] = int(tr.findChildren("td")[5].next.strip().replace(",", ""))
    dumpData(items, "crafting/" + key)
    return items

if __name__ == "__main__":
    # -- Museum --
    # scrapeBugs("bugs")
    # scrapeFish("fish")
    # scrapeFossils("fossils")

    # -- Characters --
    scrapeVillagers("villagers")

    # -- Crafting --
    # scrapeDIYTools("tools")
    # scrapeDIYTools("housewares")
    # scrapeDIYEquipments("equipments")
    # scrapeDIYTools("miscellaneous")
    # scrapeDIYOthers("others")
    # scrapeDIYEquipments("wallMounteds")
    # scrapeDIYWallpapers("wallpaperRugsFloorings")
    pass
