from bs4 import BeautifulSoup
import html5lib
import requests
import io
import urllib.request
import json
from util import parse_personality, parse_gender, parse_image_img_url, parse_image_url, parse_customization, parse_obtained_from, parse_furniture_variations, parse_materials, parse_price, get_image_urls, parse_hybridization_children, parse_months, parse_variations, parse_source, parse_image_URLs, parse_rose_image_URLs, dump_data



URLS = {
    "wiki": "https://animalcrossing.fandom.com",
    "api": "https://acnhapi.com/v1",

    # --- New Horizons ---
    "character": {
        "villagers": "https://animalcrossing.fandom.com/wiki/Villager_list_(New_Horizons)",
    },

    "museum": {
        "fish": "https://animalcrossing.fandom.com/wiki/Fish_(New_Horizons)",
        "bugs": "https://animalcrossing.fandom.com/wiki/Bugs_(New_Horizons)",
        "fossils": "https://animalcrossing.fandom.com/wiki/Fossils_(New_Horizons)",
        "artworks": "https://animalcrossing.fandom.com/wiki/Artwork_(New_Horizons)",
    },

    # Crafting
    "tools": "https://animalcrossing.fandom.com/wiki/DIY_recipes/Tools",
    "housewares": "https://animalcrossing.fandom.com/wiki/DIY_recipes/Housewares",
    "miscellaneous": "https://animalcrossing.fandom.com/wiki/DIY_recipes/Miscellaneous",
    "equipments": "https://animalcrossing.fandom.com/wiki/DIY_recipes/Equipment",
    "others": "https://animalcrossing.fandom.com/wiki/DIY_recipes/Other",
    "wall_mounteds": "https://animalcrossing.fandom.com/wiki/DIY_recipes/Wall-mounted",
    "wallpaper_rugs_floorings": "https://animalcrossing.fandom.com/wiki/DIY_recipes/Wallpaper,_rugs_and_flooring",

    # Clothing
    "tops": "https://animalcrossing.fandom.com/wiki/Clothing_(New_Horizons)/Tops",
    "bottoms": "https://animalcrossing.fandom.com/wiki/Clothing_(New_Horizons)/Bottoms",
    "dresses": "https://animalcrossing.fandom.com/wiki/Clothing_(New_Horizons)/Dresses",
    "hats": "https://animalcrossing.fandom.com/wiki/Clothing_(New_Horizons)/Hats",
    "accessories": "https://animalcrossing.fandom.com/wiki/Clothing_(New_Horizons)/Accessories",
    "socks": "https://animalcrossing.fandom.com/wiki/Clothing_(New_Horizons)/Socks",
    "shoes": "https://animalcrossing.fandom.com/wiki/Clothing_(New_Horizons)/Shoes",
    "bags": "https://animalcrossing.fandom.com/wiki/Clothing_(New_Horizons)/Bags",
    "umbrellas": "https://animalcrossing.fandom.com/wiki/Clothing_(New_Horizons)/Umbrellas",
    
    "furniture": {
        "housewares": "https://animalcrossing.fandom.com/wiki/Furniture_(New_Horizons)/Housewares",
        "miscellaneous": "https://animalcrossing.fandom.com/wiki/Furniture_(New_Horizons)/Miscellaneous",
        "wall_mounted": "https://animalcrossing.fandom.com/wiki/Furniture_(New_Horizons)/Wall-mounted",
        "wallpapers": "https://animalcrossing.fandom.com/wiki/Furniture_(New_Horizons)/Wallpaper",
        "floorings": "https://animalcrossing.fandom.com/wiki/Furniture_(New_Horizons)/Flooring",
        "rugs": "https://animalcrossing.fandom.com/wiki/Furniture_(New_Horizons)/Rugs"
    },
    
    # Flowers
    "flowers": "https://animalcrossing.fandom.com/wiki/Flower/New_Horizons_mechanics",
    
    # Music
    "music": "https://animalcrossing.fandom.com/wiki/Music_(New_Horizons)"

    # --- New Leaf ---
    # "fish": "https://animalcrossing.fandom.com/wiki/Fish_(New_Leaf)",
    # "bugs": "https://animalcrossing.fandom.com/wiki/Bugs_(New_Leaf)",
}

 
def scrape_villagers(url_key):
    url = URLS["character"][url_key]
    response = requests.get(url, timeout=5)
    soup = BeautifulSoup(response.content, "html.parser")
    tables = soup("table", {"class": "sortable"})
    items = {}
    # these headers must be scraped from their individual wiki page
    headers = ["initial_clothes", "caption", "home_request", "skill", "goal", "coffee", "style", "favorite_song", "appearances"]
    for tr in tables[0]("tr")[1:]:
        name = tr("td")[0].text.strip()
        item = {
            "wiki_url": "https://animalcrossing.fandom.com" + tr("td")[0].a.get("href"),
            "image_url": tr("td")[1]("a")[0]("img")[-1]["src"].replace("scale-to-width-down/100", ""), # fix data:images
            "gender": parse_gender(tr("td")[2]),
            "personality": parse_personality(tr("td")[2]),
            "species": tr("td")[3].text.strip(),
            "birthday": tr("td")[4].text.strip(),
            "initial_phrase": tr("td")[5].text.strip().replace("\"", ""),
            "hobbies": tr("td")[6].text.strip(),
        }
        # scrape additional information from the character's page
        for header in headers: 
            item[header] = None
        villager_response = requests.get(item["wiki_url"], timeout=5)
        villager_soup = BeautifulSoup(villager_response.content, "html.parser")
        aside = villager_soup("aside")[0]
        if len(aside("figcaption")) > 0:
            item["caption"] = aside("figcaption")[0].text.replace("“", "").replace("”", "")
        for div in aside("div", {"class": "pi-item"}):
            if not div.find("div").text == "Unknown":
                if div("h3")[0].text.lower().replace(" ", "_") in headers:
                    item[div("h3")[0].text.lower().replace(" ", "_")] = div.find("div").text
        # format unformatted text 
        if not item["coffee"] is None: 
            coffee = item["coffee"].split(",")
            item["coffee"]  = {
                "type": coffee[0],
                "milk": coffee[1],
                "sugar": coffee[2]
            }
        if not item["appearances"] is None:
            item["appearances"] = item["appearances"].split(", ")
        if not item["favorite_song"] is None:
            item["favorite_song"] = item["favorite_song"].replace("[[", "").replace("]]", "")
        items[name] = item
    dump_data(items, "character/villagers")

def scrape_bugs(url_key):
    # contains all bugs
    items = {}
    # get response from url and create soup
    url = URLS["museum"][url_key]
    response = requests.get(url, timeout=5)
    soup = BeautifulSoup(response.content, "html.parser")
    # find the table to scrape from
    table = soup("table", {"class": "sortable"})[0]
    item_id = 1
    for tr in table("tr")[1:]:
        name = tr("td")[0].text.strip()
        item_key = name.replace(" ", "_").replace("-", "_")
        acnhapi_url = URLS["api"] + "/bugs/" + str(item_id)
        acnhapi_response = urllib.request.urlopen(acnhapi_url)
        acnhapi_data = json.loads(acnhapi_response.read())
        item = {
            "name": name,
            "id": item_id,
            "wiki_url": URLS["wiki"] + tr("td")[0].find("a")["href"],
            "icon_url": tr("a")[1]['href'],
            "image_url": URLS["api"] + "/images/bugs/" + str(item_id),
            "price": parse_price(tr("td")[2].text),
            "location": tr("td")[3].text.strip(),
            "time": tr("small")[0].text.split(" & "),
            "months": {
                "northern": parse_months([tr("td")[5], tr("td")[6], tr("td")[7], tr("td")[8], tr("td")[9], tr("td")[10], tr("td")[11], tr("td")[12], tr("td")[13], tr("td")[14], tr("td")[15], tr("td")[16]]),
                "southern": parse_months([tr("td")[11], tr("td")[12], tr("td")[13], tr("td")[14], tr("td")[15], tr("td")[16], tr("td")[5], tr("td")[6], tr("td")[7], tr("td")[8], tr("td")[9], tr("td")[10]]),
            },
            "catch_phrase": acnhapi_data["catch-phrase"],
            "museum_phrase": acnhapi_data["museum-phrase"],
        }
        item_id += 1
        items[item_key] = item
    dump_data(items, "museum/bugs")

def scrape_fish(url_key): 
    items = {}
    url = URLS["museum"][url_key]
    response = (requests.get(url, timeout=5))
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup("table", {"class": "sortable"})[0]
    item_id = 1
    for tr in table("tr")[1:]:
        name = tr("td")[0].text.strip()
        item_key = name.replace(" ", "_").replace("-", "_")
        acnhapi_url = URLS["api"] + "/fish/" + str(item_id)
        acnhapi_response = urllib.request.urlopen(acnhapi_url)
        acnhapi_data = json.loads(acnhapi_response.read())
        item = {
            "name": name,
            "id": item_id,
            "wiki_url": "https://animalcrossing.fandom.com" + tr("td")[0].find("a")["href"],
            "icon_url": tr("a")[1]['href'],
            "image_url": URLS["api"] + "/images/fish/" + str(item_id),
            "price": parse_price(tr("td")[2].text),
            "location": tr("td")[3].text.strip(),
            "shadow_size": tr("td")[4].text.strip(),
            "time": tr("small")[0].text.split(" & "),
            "months": {
                "northern": parse_months([tr("td")[6], tr("td")[7], tr("td")[8], tr("td")[9], tr("td")[10], tr("td")[11], tr("td")[12], tr("td")[13], tr("td")[14], tr("td")[15], tr("td")[16], tr("td")[17]]),
                "southern": parse_months([tr("td")[12], tr("td")[13], tr("td")[14], tr("td")[15], tr("td")[16], tr("td")[17], tr("td")[6], tr("td")[7], tr("td")[8], tr("td")[9], tr("td")[10], tr("td")[11]]),
            },
            "catch_phrase": acnhapi_data["catch-phrase"],
            "museum_phrase": acnhapi_data["museum-phrase"],
        }
        item_id += 1
        items[item_key] = item
    dump_data(items, "museum/fish")

def scrape_fossils(key):
    url = URLS.get(key)
    response = (requests.get(url, timeout=5))
    soup = BeautifulSoup(response.content, "html.parser")
    tables = soup("table", {"class": "sortable"})
    items = {}
    # Stand-alone fossils
    items["stand_alone"] = {}
    for tr in tables[0]("tr")[1:]:
        name = tr("td")[0].a.text
        item = {
            "image_url": tr("a")[1]['href'],
            "price": parse_price(tr("td")[2].text),
        }
        items["stand_alone"][name] = item
    # Multi-part fossils
    items["multi_part"] = {}
    for tr in tables[1]("tr")[1:]:
        tds = tr("td")
        if not tds:
            currentCategory = tr("a")[0].text
            continue
        name = tr("td")[0].a.text
        item = {
            "image_url": tr("a")[1]['href'],
            "price": parse_price(tr("td")[2].text),
            "category": currentCategory
        }
        items["multi_part"][name] = item
    dump_data(items, "museum/" + key)
    return items


def scrape_artworks(key):
    url = URLS.get(key)
    response = requests.get(url, timeout=5)
    soup = BeautifulSoup(response.content, "html.parser")
    tables = soup("table", {"class": "wikitable"})
    items = {}
    # paintings
    items["paintings"] = {}
    for tr in tables[0]("tr")[1:]:
        name = tr("td")[0].a.text
        item = {
            "description": tr("td")[3].text.strip(),
        }
        if tr("td")[1].a:
            item["fake_image_url"] = tr("td")[1].a['href']
        else:
            item["fake_image_url"] = None
        if tr("td")[2].a:
            item["real_image_url"] = tr("td")[2].a['href']
        else:
            item["real_image_url"] = None
        items["paintings"][name] = item
    # sculptures
    items["sculptures"] = {}
    for tr in tables[1]("tr")[1:]:
        name = tr("td")[0].a.text
        item = {
            "description": tr("td")[3].text.strip(),
        }
        if tr("td")[1].a:
            item["fake_image_url"] = tr("td")[1].a['href']
        else:
            item["fake_image_url"] = None
        if tr("td")[2].a:
            item["real_image_url"] = tr("td")[2].a['href']
        else:
            item["real_image_url"] = None
        items["sculptures"][name] = item
    dump_data(items, "museum/" + key)
    return items

def scrape_tools(key):
    url = URLS.get(key)
    response = (requests.get(url, timeout=5))
    soup = BeautifulSoup(response.content, "html.parser")
    tables = soup("table", {"class": "sortable"})
    items = {}
    for tr in tables[0]("tr")[1:]:
        name = tr("td")[0].a.text
        item = {
            "image_url": tr("a")[1]['href'],
            "materials": parse_materials(tr("td")[2]),
            "size_image_url": tr("td")[3].img.get("data-src"),
            "obtained_from": parse_obtained_from(tr("td")[4]),
            "price": parse_price(tr("td")[5].text)
        }
        items[name] = item
    dump_data(items, "crafting/" + key)
    return items

def scrape_wallpapers(key):
    url = URLS.get(key)
    response = (requests.get(url, timeout=5))
    soup = BeautifulSoup(response.content, "html.parser")
    tables = soup("table", {"class": "sortable"})
    items = {}
    for tr in tables[0]("tr")[1:]:
        name = tr("td")[0].a.text
        item = {
            "image_url": tr("a")[1]['href'],
            "materials": parse_materials(tr("td")[2]),
            "obtained_from": parse_obtained_from(tr("td")[4]),
            "price": parse_price(tr("td")[5].text)
        }
        if tr("td")[3].img:
            item["size_image_url"] = tr("td")[3].img.get("src")
        else:
            item["size_image_url"] = None
        items[name] = item
    dump_data(items, "crafting/" + key)
    return items


def scrape_crafting_others(key):
    url = URLS.get(key)
    response = (requests.get(url, timeout=5))
    soup = BeautifulSoup(response.content, "html.parser")
    tables = soup("table", {"class": "roundy"})
    items = {}
    for tr in tables[2]("tr")[1:]:
        name = tr("td")[0].a.text
        item = {
            "image_url": tr("a")[1]['href'],
            "materials": parse_materials(tr("td")[2]),
            "obtained_from": parse_obtained_from(tr("td")[4]), # TODO add nook miles  .replace(")", "Nook Miles)")
            "price": parse_price(tr("td")[5].text)
        }
        if tr("td")[3].img.get("data-src"):
            item["size_image_url"] = tr("td")[3].img.get("data-src")
        elif tr("td")[3].img:
            item["size_image_url"] = tr("td")[3].img.get("src") # ????
        else:
            item["size_image_url"] = None

        
        items[name] = item
    dump_data(items, "crafting/" + key)
    return items


def scrape_tops(key):
    url = URLS.get(key)
    response = (requests.get(url, timeout=5))
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find_all("table", {"class": "roundy"})
    items = {}
    for tr in table[2].find_all("tr")[2:]:
        name = tr.find_all("td")[0].text.strip()
        item = {
            "name": name,
            # "imageLink": tr.find_all("td")[1].find_all("a")[0]["href"],
            "priceBuy": parse_price(tr.find_all("td")[2].text),
            "priceSell": parse_price(tr.find_all("td")[3].text),
            "source": parse_source(tr.find_all("td")[4]),
            "variations": parse_variations(tr.find_all("td")[5]),
            "variationImageLinks": get_image_urls(tr.find_all("td")[5].find_all("img"))
        }
        if tr.find_all("td")[1].find_all("a"):
            item["imageLink"] = tr.find_all("td")[1].find_all("a")[0]["href"]
        items[name] = item
    dump_data(items, "clothing/" + key)
    return items


def scrape_hats(key):
    url = URLS.get(key)
    response = (requests.get(url, timeout=5))
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find_all("table", {"class": "roundy"})
    items = {}
    for tableNumber in range(2,10):
        for tr in table[tableNumber].find_all("tr")[2:]:
            name = tr.find_all("td")[0].text.strip()
            item = {
                "name": name,
                # "imageLink": tr.find_all("td")[1].find_all("a")[0]["href"],
                "priceBuy": parse_price(tr.find_all("td")[2].text),
                "priceSell": parse_price(tr.find_all("td")[3].text),
                "source": parse_source(tr.find_all("td")[4]),
                "variations": parse_variations(tr.find_all("td")[5]),
                "variationImageLinks": get_image_urls(tr.find_all("td")[5].find_all("img"))
            }
            if tr.find_all("td")[1].find_all("a"):
                item["imageLink"] = tr.find_all("td")[1].find_all("a")[0]["href"]
            items[name] = item
    dump_data(items, "clothing/" + key)
    return items


def scrape_shoes(key):
    url = URLS.get(key)
    response = (requests.get(url, timeout=5))
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find_all("table", {"class": "roundy"})
    items = {}
    for tableNumber in range(2,8):
        for tr in table[tableNumber].find_all("tr")[2:]:
            name = tr.find_all("td")[0].text.strip()
            item = {
                "name": name,
                # "imageLink": tr.find_all("td")[1].find_all("a")[0]["href"],
                "priceBuy": parse_price(tr.find_all("td")[2].text),
                "priceSell": parse_price(tr.find_all("td")[3].text),
                "source": parse_source(tr.find_all("td")[4]),
                "variations": parse_variations(tr.find_all("td")[5]),
                "variationImageLinks": get_image_urls(tr.find_all("td")[5].find_all("img"))
            }
            if tr.find_all("td")[1].find_all("a"):
                item["imageLink"] = tr.find_all(
                    "td")[1].find_all("a")[0]["href"]
            items[name] = item
    dump_data(items, "clothing/" + key)
    return items


def scrape_umbrellas(key):
    url = URLS.get(key)
    response = (requests.get(url, timeout=5))
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find_all("table", {"class": "roundy"})
    items = {}
    for tr in table[2].find_all("tr")[2:]:
        name = tr.find_all("td")[0].text.strip()
        item = {
            "name": name,
            "imageLink": tr.find_all("td")[1].find_all("a")[0]["href"],
            "source": parse_source(tr.find_all("td")[2]),
            "priceBuy": parse_price(tr.find_all("td")[3].text),
            "priceSell": parse_price(tr.find_all("td")[4].text),
        }
        items[name] = item
    dump_data(items, "clothing/" + key)
    return items


def scrape_furniture_housewares(key):
    url = URLS["furniture"][key]
    response = requests.get(url, timeout=5)
    soup = BeautifulSoup(response.content, "html5lib") # html.parser does not scrape all html contents
    tables = soup("table", {"class": "roundy"})
    items = {}
    for table_number in range(3, 29): # a - z
        if len(tables[table_number]("tr")) > 3: # some tables are empty
            for tr in tables[table_number]("tr")[2:]:
                name = tr("td")[1].text.strip()
                item = {
                    "image_url": parse_image_url(tr("td")[0]),
                    "price": {
                        "buy": parse_price(tr("td")[2].text),
                        "sell": parse_price(tr("td")[3].text)
                    },
                    "source": parse_source(tr("td")[4]),
                    "variations": parse_furniture_variations(tr("td")[5]),
                    "customization": parse_customization(tr("td")[6]),
                    "size_image_url": parse_image_img_url(tr("td")[7]),
                }
                items[name] = item
    dump_data(items, "furniture/" + key)
    return items


def scrape_furniture_wallpapers(key):
    url = URLS["furniture"][key]
    response = requests.get(url, timeout=5)
    soup = BeautifulSoup(response.content, "html5lib") # html.parser does not scrape all html contents
    tables = soup("table", {"class": "roundy"})
    items = {}
    for tr in tables[3]("tr")[2:]:
        name = tr("td")[1].text.strip()
        item = {
            "image_url": parse_image_url(tr("td")[0]),
            "price": {
                "buy": parse_price(tr("td")[2].text),
                "sell": parse_price(tr("td")[3].text)
            },
            "source": parse_source(tr("td")[4]),
        }
        items[name] = item
    dump_data(items, "furniture/" + key)
    return items


def scrape_furniture_rugs(key):
    url = URLS["furniture"][key]
    response = requests.get(url, timeout=5)
    # html.parser does not scrape all html contents
    soup = BeautifulSoup(response.content, "html5lib")
    tables = soup("table", {"class": "roundy"})
    items = {}
    for tr in tables[3]("tr")[2:]:
        name = tr("td")[1].text.strip()
        item = {
            "image_url": parse_image_url(tr("td")[0]),
            "price": {
                "buy": parse_price(tr("td")[2].text),
                "sell": parse_price(tr("td")[3].text)
            },
            "source": parse_source(tr("td")[4]),
            "size_image_url": parse_image_img_url(tr("td")[5]),

        }
        items[name] = item
    dump_data(items, "furniture/" + key)
    return items

def scrape_flowers(key):
    url = URLS.get(key)
    response = (requests.get(url, timeout=5))
    soup = BeautifulSoup(response.content, "html.parser")
    tables = soup("table")

    # availability
    items = {}
    for tr in tables[0]("tr")[2:10]:
        name = tr("td")[0].text.strip()
        t = tables[0]("tr")[2]("td")
        item = {
            "color_image_urls": parse_image_URLs(tr("td")[1]),
            "months": {
                "northern": parse_months([tr("td")[2], tr("td")[3], tr("td")[4], tr("td")[5], tr("td")[6], tr("td")[7], tr("td")[8], tr("td")[9], tr("td")[10], tr("td")[11], tr("td")[12], tr("td")[13]]),
                "southern": parse_months([tr("td")[8], tr("td")[9], tr("td")[10], tr("td")[11], tr("td")[12], tr("td")[13], tr("td")[2], tr("td")[3], tr("td")[4], tr("td")[5], tr("td")[6], tr("td")[7]])
            }
        }
        items[name] = item
    dump_data(items, "flower/availability")

    # genetics_rose
    items = []
    for tr in tables[5]("tr")[2:29]:
        item = {
            "genotype": {
                "red": int(tr("td")[0].text.strip()),
                "yellow": int(tr("td")[1].text.strip()),
                "white": int(tr("td")[2].text.strip())
            },
            "phenotypes_image_url": parse_rose_image_URLs([tr("td")[3].img, tr("td")[4].img, tr("td")[5].img])
        }
        items.append(item)
    dump_data(items, "flower/genetics_rose")
    
    # genetics_others
    items = []
    for tr in tables[6]("tr")[3:30]:
        item = {
            "genotype": {
                "red": int(tr("td")[0].text.strip()),
                "yellow": int(tr("td")[1].text.strip()),
                "white": int(tr("td")[2].text.strip())
            },
            "phenotypes_image_url": {
                "tulips": tr("td")[3].img.get("data-src").replace("/scale-to-width-down/50", ""),
                "pansies": tr("td")[4].img.get("data-src").replace("/scale-to-width-down/50", ""),
                "cosmos": tr("td")[5].img.get("data-src").replace("/scale-to-width-down/50", ""),
                "lilies": tr("td")[6].img.get("data-src").replace("/scale-to-width-down/50", ""),
                "hyacinths": tr("td")[7].img.get("data-src").replace("/scale-to-width-down/50", ""),
                "windflowers": tr("td")[8].img.get("data-src").replace("/scale-to-width-down/50", ""),
                "mums": tr("td")[9].img.get("data-src").replace("/scale-to-width-down/50", "")
            }
        }
        items.append(item)
    dump_data(items, "flower/genetics_others")

    # hybridization_simple
    items = {}
    for table_number in range(7, 15):
        temp = []
        species = tables[table_number]("tr")[0].text.strip()
        for tr in tables[table_number]("tr")[2:8]:
            if len(tr("abbr")) > 0: # some trs do not contain hybridization data
                item = {
                    "parent_a": {
                        "gene": tr("abbr")[0].get("title"),
                        "image_url": tr("abbr")[0]("img")[0].get("data-src").replace("/scale-to-width-down/50", "")
                    },
                    "parent_b": {
                        "gene": tr("abbr")[1].get("title"),
                        "image_url": tr("abbr")[1]("img")[0].get("data-src").replace("/scale-to-width-down/50", "")
                    },
                    "children": parse_hybridization_children(tr("td")[2])
            }
            temp.append(item)
        items[species] = temp
    dump_data(items, "flower/hybridization_simple")

    # hybridization_advanced
    items = {}
    for table_number in range(15, 17):
        temp = []
        species = tables[table_number]("tr")[0].text.strip()
        for tr in tables[table_number]("tr")[2:6]:
            if len(tr("abbr")) > 0:
                item = {
                    "parent_a": {
                        "gene": tr("abbr")[0].get("title"),
                        "image_url": tr("abbr")[0]("img")[0].get("data-src").replace("/scale-to-width-down/50", "")
                    },
                    "parent_b": {
                        "gene": tr("abbr")[1].get("title"),
                        "image_url": tr("abbr")[1]("img")[0].get("data-src").replace("/scale-to-width-down/50", "")
                    },
                    "children": parse_hybridization_children(tr("td")[2])
                }
            temp.append(item)
        items[species] = temp
    dump_data(items, "flower/hybridization_advanced")


def scrape_music(key):
    url = URLS.get(key)
    response = requests.get(url, timeout=5)
    soup = BeautifulSoup(response.content, "html.parser")
    tables = soup("table", {"class": "article-table"})
    items = {}
    for tr in tables[0]("tr")[1:]:
        name = tr("td")[0].text.strip()
        item_key = name.replace(" ", "_").replace("-", "_")
        item = {
            "name": name,
            "image_url": parse_image_url(tr.find_all("td")[1]),
            "priceBuy": parse_price(tr.find_all("td")[2].text),
            "priceSell": parse_price(tr.find_all("td")[3].text),
            "source": parse_source(tr.find_all("td")[4])
        }
        items[item_key] = item
    dump_data(items, "music/" + key)
    return items


if __name__ == "__main__":
    # -- Characters --
    # scrape_villagers("villagers")

    # -- Museum --
    scrape_bugs("bugs")
    scrape_fish("fish")
    # scrape_fossils("fossils")
    # scrape_artworks("artworks")

    # -- Crafting --
    # scrape_tools("tools")
    # scrape_tools("housewares")
    # scrape_tools("equipments")
    # scrape_tools("miscellaneous")
    # scrape_tools("wall_mounteds")
    # scrape_crafting_others("others")
    # scrape_wallpapers("wallpaper_rugs_floorings")

    # -- Clothing --
    # scrape_tops("tops")
    # scrape_tops("bottoms")
    # scrape_tops("dresses")
    # scrape_hats("hats")
    # scrape_tops("accessories")
    # scrape_tops("socks")
    # scrape_shoes("shoes")
    # scrape_tops("bags")
    # scrape_umbrellas("umbrellas")

    # -- Furniture --
    # scrape_furniture_housewares("housewares")
    # scrape_furniture_housewares("miscellaneous")
    # scrape_furniture_housewares("wall_mounted")
    # scrape_furniture_wallpapers("wallpapers")
    # scrape_furniture_wallpapers("floorings")
    # scrape_furniture_rugs("rugs")

    # -- Flower -- 
    # scrape_flowers("flowers")

    # -- Music --
    # scrape_music("music")

    pass
