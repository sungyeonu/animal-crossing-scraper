from bs4 import BeautifulSoup
import requests
import io
from util import separate_by_br, convert_checkmark, strip_price, get_image_links, dump_data

URLS = {
    # --- New Horizons ---
    # Museum
    "fish": "https://animalcrossing.fandom.com/wiki/Fish_(New_Horizons)",
    "bugs": "https://animalcrossing.fandom.com/wiki/Bugs_(New_Horizons)",
    "fossils": "https://animalcrossing.fandom.com/wiki/Fossils_(New_Horizons)",
    "artworks": "https://animalcrossing.fandom.com/wiki/Artwork_(New_Horizons)",

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


def scrape_bugs(key):  # take url and return object containing bugs data
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
        name = tr.find_all("td")[0].a.text
        item = {
            "name": name,
            "imageLink": tr.find_all("a")[1]['href'],
            "price": int(tableData[2]),
            "location": tr.find_all("td")[3].text.strip('\n').strip(),
            "time": tr.find_all("small")[0].text,
            "seasonsNorthernHemisphere": {
                "jan": convert_checkmark(tableData[5]),
                "feb": convert_checkmark(tableData[6]),
                "mar": convert_checkmark(tableData[7]),
                "apr": convert_checkmark(tableData[8]),
                "may": convert_checkmark(tableData[9]),
                "jun": convert_checkmark(tableData[10]),
                "jul": convert_checkmark(tableData[11]),
                "aug": convert_checkmark(tableData[12]),
                "sep": convert_checkmark(tableData[13]),
                "oct": convert_checkmark(tableData[14]),
                "nov": convert_checkmark(tableData[15]),
                "dec": convert_checkmark(tableData[16])
            },
            "seasonsSouthernHemisphere": {  # shift northern hemisphere by 6 months
                "jan": convert_checkmark(tableData[11]),
                "feb": convert_checkmark(tableData[12]),
                "mar": convert_checkmark(tableData[13]),
                "apr": convert_checkmark(tableData[14]),
                "may": convert_checkmark(tableData[15]),
                "jun": convert_checkmark(tableData[16]),
                "jul": convert_checkmark(tableData[5]),
                "aug": convert_checkmark(tableData[6]),
                "sep": convert_checkmark(tableData[7]),
                "oct": convert_checkmark(tableData[8]),
                "nov": convert_checkmark(tableData[9]),
                "dec": convert_checkmark(tableData[10])
            }
        }
        # add to the json
        items[name] = item
    dump_data(items, "museum/" + key)
    # return for debugging
    return items


def scrape_fish(key):  # same logic as scrapeBugs
    url = URLS.get(key)
    response = (requests.get(url, timeout=5))
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find_all("table", {"class": "sortable"})
    items = {}
    for tr in table[0].find_all("tr")[1:]:
        tableData = []
        for td in tr.find_all("td"):
            tableData.append(td.next.strip())
        name = tr.find_all("td")[0].a.text
        item = {
            "name": name,
            "imageLink": tr.find_all("a")[1]['href'],
            "price": strip_price(tableData[2]),
            "location": tr.find_all("td")[3].text.strip('\n').strip(),
            "shadowSize": tableData[4],
            "time": tr.find_all("small")[0].text,
            "seasonsNorthernHemisphere": {
                "jan": convert_checkmark(tableData[6]),
                "feb": convert_checkmark(tableData[7]),
                "mar": convert_checkmark(tableData[8]),
                "apr": convert_checkmark(tableData[9]),
                "may": convert_checkmark(tableData[10]),
                "jun": convert_checkmark(tableData[11]),
                "jul": convert_checkmark(tableData[12]),
                "aug": convert_checkmark(tableData[13]),
                "sep": convert_checkmark(tableData[14]),
                "oct": convert_checkmark(tableData[15]),
                "nov": convert_checkmark(tableData[16]),
                "dec": convert_checkmark(tableData[17])
            },
            "seasonsSouthernHemisphere": {
                "jan": convert_checkmark(tableData[12]),
                "feb": convert_checkmark(tableData[13]),
                "mar": convert_checkmark(tableData[14]),
                "apr": convert_checkmark(tableData[15]),
                "may": convert_checkmark(tableData[16]),
                "jun": convert_checkmark(tableData[17]),
                "jul": convert_checkmark(tableData[6]),
                "aug": convert_checkmark(tableData[7]),
                "sep": convert_checkmark(tableData[8]),
                "oct": convert_checkmark(tableData[9]),
                "nov": convert_checkmark(tableData[10]),
                "dec": convert_checkmark(tableData[11])
            }
        }
        items[name] = item
    dump_data(items, "museum/" + key)
    return items


def scrape_fossils(key):  # same logic as scrapeBugs and scrapeFish
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
        name = tr.find_all("td")[0].a.text
        item = {
            "name": name,
            "imageLink": tr.find_all("a")[1]['href'],
            "price": strip_price(tableData[2]),
            "isMultipart": False
        }
        tableData.append(item)
        items[name] = item
    # Multi-part fossils
    for tr in table[1].find_all("tr")[1:]:
        tableData = []
        tds = tr.find_all("td")
        if not tds:
            currentCategory = tr.find_all("a")[0].text
            continue
        for td in tr.find_all("td"):
            tableData.append(td.next.strip())
        name = tr.find_all("td")[0].a.text
        item = {
            "name": name,
            "imageLink": tr.find_all("a")[1]['href'],
            "price": strip_price(tableData[2]),
            "isMultipart": True,
            "category": currentCategory
        }
        items[name] = item
    dump_data(items, "museum/" + key)
    return items


def scrape_artworks(key):
    url = URLS.get(key)
    response = requests.get(url, timeout=5)
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find_all("table", {"class": "wikitable"})
    items = {}
    for tr in table[0].find_all("tr")[1:]:
        name = tr.find_all("td")[0].a.text
        item = {
            "name": name,
        }
        if tr.find_all("td")[1].a:
            item["fakeImageLink"] = tr.find_all("td")[1].a['href']
        if tr.find_all("td")[2].a:
            item["realImageLink"] = tr.find_all("td")[2].a['href']
        if tr.find_all("td")[3]:
            item["description"] = tr.find_all("td")[3].text.strip('\n').lstrip()
        items[name] = item
    for tr in table[1].find_all("tr")[1:]:
        name = tr.find_all("td")[0].a.text
        item = {
            "name": name,
        }
        if tr.find_all("td")[1].a:
            item["fakeImageLink"] = tr.find_all("td")[1].a['href']
        if tr.find_all("td")[2].a:
            item["realImageLink"] = tr.find_all("td")[2].a['href']
        if tr.find_all("td")[3]:
            item["description"] = tr.find_all("td")[3].text.strip('\n').lstrip()
        items[name] = item
    dump_data(items, "museum/" + key)
    return items


def scrape_villagers(key):
    url = URLS.get(key)
    response = (requests.get(url, timeout=5))
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find_all("table", {"class": "sortable"})
    items = {}
    for tr in table[0].find_all("tr")[1:]:
        name = tr.find_all("td")[0].a.text
        item = {
            "name": name,
            "imageLink": tr.find_all("td")[1].a['href'],
            "personality": tr.find_all("td")[2].text.strip("\n").lstrip(),
            "species": tr.find_all("td")[3].text.strip("\n").lstrip(),
            "birthday": tr.find_all("td")[4].text.strip("\n").lstrip(),
            "catchPhrase": tr.find_all("td")[5].text.strip("\n").lstrip()
        }
        items[name] = item
    dump_data(items, "characters/" + key)
    return items


def scrape_tools(key):
    url = URLS.get(key)
    response = (requests.get(url, timeout=5))
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find_all("table", {"class": "sortable"})
    items = {}
    for tr in table[0].find_all("tr")[1:]:
        name = tr.find_all("td")[0].a.text
        item = {
            "name": name,
        }
        if tr.find_all("a")[1]['href']:
            item["imageLink"] = tr.find_all("a")[1]['href']
        if tr.find_all("td")[2]:
            item["materials"] = separate_by_br(tr.find_all("td")[2]).lstrip().strip("\n").split(",")
        if tr.find_all("td")[2].find_all("img"):
            item["materialsImageLink"] = get_image_links(tr.find_all("td")[2].find_all("img"))
        if tr.find_all("td")[3].img.get("data-src"):
            item["sizeImageLink"] = tr.find_all("td")[3].img.get("data-src")
        if tr.find_all("td")[4].text:
            item["obtainedFrom"] = tr.find_all("td")[4].text.strip().strip("\n").splitlines()
        if tr.find_all("td")[5]:
            item["price"] = strip_price(tr.find_all("td")[5].text)
        items[name] = item
    dump_data(items, "crafting/" + key)
    return items


def scrape_equipments(key):
    url = URLS.get(key)
    response = (requests.get(url, timeout=5))
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find_all("table", {"class": "sortable"})
    items = {}
    for tr in table[0].find_all("tr")[1:]:
        name = tr.find_all("td")[0].a.text
        item = {
            "name": name,
            "imageLink": tr.find_all("a")[1]['href'],
            "materials": separate_by_br(tr.find_all("td")[2]).lstrip().strip("\n").split(","),
            "materialsImageLink": get_image_links(tr.find_all("td")[2].find_all("img")),
            "sizeImageLink": tr.find_all("td")[3].img.get("data-src"),
            "obtainedFrom": tr.find_all("td")[4].text.strip().strip("\n").splitlines(),
            "price": strip_price(tr.find_all("td")[5].text)
        }
        items[name] = item
    dump_data(items, "crafting/" + key)
    return items


def scrape_wallpapers(key):
    url = URLS.get(key)
    response = (requests.get(url, timeout=5))
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find_all("table", {"class": "sortable"})
    items = {}
    for tr in table[0].find_all("tr")[1:]:
        name = tr.find_all("td")[0].a.text
        item = {
            "name": name,
        }
        if tr.find_all("a")[1]['href']:
            item["imageLink"] = tr.find_all("a")[1]['href']
        if tr.find_all("td")[2]:
            item["materials"] = separate_by_br(
                tr.find_all("td")[2]).strip("\n").split(",")
            item["materialsImageLink"] = get_image_links(
                tr.find_all("td")[2].find_all("img"))
        if tr.find_all("td")[3].find_all("a"):
            item["sizeLink"] = tr.find_all(
                "td")[3].find_all("a")[0]['href']
        if tr.find_all("td")[4].text:
            if (tr.find_all("td")[4].text.strip('\n').splitlines() == []):
                pass
            else:
                item["obtainedFrom"] = tr.find_all("td")[4].text.strip('\n').splitlines()
        if tr.find_all("td")[5].text.strip().replace(",", ""):
            item["price"] = int(tr.find_all(
                "td")[5].text.strip().replace(",", ""))
        items[name] = item
    dump_data(items, "crafting/" + key)
    return items


def scrape_DIYothers(key):
    url = URLS.get(key)
    response = (requests.get(url, timeout=5))
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find_all("table", {"class": "roundy"})
    items = {}
    for tr in table[2].find_all("tr")[1:]:
        name = tr.find_all("td")[0].a.text
        item = {
            "name": name,
            "imageLink": tr.find_all("a")[1]['href'],
            "materials": separate_by_br(tr.find_all("td")[2]).lstrip().strip("\n").split(","),
            "materialsImageLink": get_image_links(tr.find_all("td")[2].find_all("img")),
            "sizeImageLink": tr.find_all("td")[3].img.get("data-src"),
            "obtainedFrom": tr.find_all("td")[4].text.strip().strip("\n").splitlines(),
            "price": strip_price(tr.find_all("td")[5].text)
        }
        if (item["obtainedFrom"] == ["Nook Stop (1,000 )"]): # TODO: rewrite this lazy code
            item["obtainedFrom"] = ["Nook Stop (1,000 Nook Miles)"]
        items[name] = item
    dump_data(items, "crafting/" + key)
    return items


if __name__ == "__main__":
    # -- Museum --
    # scrape_bugs("bugs")
    # scrape_fish("fish")
    # scrape_fossils("fossils")
    # scrape_artworks("artworks")

    # -- Characters --
    # scrape_villagers("villagers")

    # -- Crafting --
    # scrape_equipments("tools")
    # scrape_equipments("housewares")
    # scrape_equipments("equipments")
    # scrape_equipments("miscellaneous")
    # scrape_equipments("wallMounteds")
    # scrape_DIYothers("others")
    # scrape_wallpapers("wallpaperRugsFloorings")
    pass
