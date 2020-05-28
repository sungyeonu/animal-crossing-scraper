from bs4 import BeautifulSoup
import requests
import io
from util import separate_by_br, parse_obtained_from, parse_materials, parse_price, get_image_urls, parse_hybridization_children, parse_months, parse_variations, parse_source, parse_image_URLs, parse_rose_image_URLs, dump_data


URLS = {
    # --- New Horizons ---
    # Characters
    "villagers": "https://animalcrossing.fandom.com/wiki/Villager_list_(New_Horizons)",

    # Museum
    "fish": "https://animalcrossing.fandom.com/wiki/Fish_(New_Horizons)",
    "bugs": "https://animalcrossing.fandom.com/wiki/Bugs_(New_Horizons)",
    "fossils": "https://animalcrossing.fandom.com/wiki/Fossils_(New_Horizons)",
    "artworks": "https://animalcrossing.fandom.com/wiki/Artwork_(New_Horizons)",

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
    
    # Furnitures
    "furniture_housewares": "https://animalcrossing.fandom.com/wiki/Furniture_(New_Horizons)/Housewares",
    
    # Flowers
    "flowers": "https://animalcrossing.fandom.com/wiki/Flower/New_Horizons_mechanics"
    # --- New Leaf ---
    # "fish": "https://animalcrossing.fandom.com/wiki/Fish_(New_Leaf)",
    # "bugs": "https://animalcrossing.fandom.com/wiki/Bugs_(New_Leaf)",
}


def scrape_villagers(key):
    # get list of villager urls
    url = URLS.get(key)
    response = (requests.get(url, timeout=5))
    soup = BeautifulSoup(response.content, "html.parser")
    tables = soup("table", {"class": "sortable"})
    villagers_urls = []
    for tr in tables[0]("tr")[1:]:
        villagers_urls.append("https://animalcrossing.fandom.com" + tr("td")[0].a.get("href"))
    # scrape each villager page
    villagers_info = {}
    for vu in villagers_urls:
        response = requests.get(vu, timeout=5)
        soup = BeautifulSoup(response.content, "html.parser")
        asides = soup("aside")
        name = asides[0]("h2")[0].text
        item = {}
        item["image_url"] = asides[0]("img")[0].get("src").replace("/scale-to-width-down/350", "")
        if len(asides[0]("figcaption")) > 0:
            item["caption"] = asides[0]("figcaption")[0].text
        else:
            item["caption"] = None
        for div in asides[0]("div", {"class": "pi-item"}):
            if div.find("div").text == "Unknown":
                item[div("h3")[0].text.lower().replace(" ", "_")] = None
            else:
                item[div("h3")[0].text.lower().replace(" ", "_")] = div.find("div").text
        villagers_info[name] = item
    dump_data(villagers_info, "characters/villagers")


def scrape_bugs(key):  # take url and return object containing bugs data
    url = URLS.get(key)
    # create soup object
    response = (requests.get(url, timeout=5))
    soup = BeautifulSoup(response.content, "html.parser")
    # find the target table

    tables = soup("table", {"class": "sortable"})
    items = {}
    # go through each tr in the table, ignoring the table header
    for tr in tables[0]("tr")[1:]:

        # scrape each item
        name = tr("td")[0].a.text
        item = {
            "image_url": tr("a")[1]['href'],
            "price": parse_price(tr("td")[2].text),
            "location": tr("td")[3].text.strip(),
            "time": tr("small")[0].text,
            "months": {
                "northern": parse_months([tr("td")[5], tr("td")[6], tr("td")[7], tr("td")[8], tr("td")[9], tr("td")[10], tr("td")[11], tr("td")[12], tr("td")[13], tr("td")[14], tr("td")[15], tr("td")[16]]),
                "southern": parse_months([tr("td")[11], tr("td")[12], tr("td")[13], tr("td")[14], tr("td")[15], tr("td")[16], tr("td")[5], tr("td")[6], tr("td")[7], tr("td")[8], tr("td")[9], tr("td")[10]]),
            }
        }
        items[name] = item
    # dump data in a json
    dump_data(items, "museum/" + key)
    # return for debugging
    return items


def scrape_fish(key):  # same logic as scrapeBugs
    url = URLS.get(key)
    response = (requests.get(url, timeout=5))
    soup = BeautifulSoup(response.content, "html.parser")
    tables = soup("table", {"class": "sortable"})
    items = {}
    for tr in tables[0]("tr")[1:]:

        name = tr("td")[0].a.text
        item = {
            "image_url": tr("a")[1]['href'],
            "price": parse_price(tr("td")[2].text),
            "location": tr("td")[3].text.strip(),
            "shadow_size": tr("td")[4].text.strip(),
            "time": tr("small")[0].text,
            "months": {
                "northern": parse_months([tr("td")[6], tr("td")[7], tr("td")[8], tr("td")[9], tr("td")[10], tr("td")[11], tr("td")[12], tr("td")[13], tr("td")[14], tr("td")[15], tr("td")[16], tr("td")[17]]),
                "southern": parse_months([tr("td")[12], tr("td")[13], tr("td")[14], tr("td")[15], tr("td")[16], tr("td")[17], tr("td")[6], tr("td")[7], tr("td")[8], tr("td")[9], tr("td")[10], tr("td")[11]]),
            }
        }
        items[name] = item
    dump_data(items, "museum/" + key)
    return items


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
    url = URLS.get(key)
    response = (requests.get(url, timeout=5))
    soup = BeautifulSoup(response.content, "html.parser")
    tables = soup("table", {"class": "roundy"})
    items = {}
    print(len(tables))
    # for tr in table[3]("tr")[2:]:
    #     name = tr.find_all("td")[1].text.strip()
    #     item = {
    #         "name": name,
    #         # "imageLink": tr.find_all("td")[1].find_all("a")[0]["href"],
    #         "priceBuy": parse_price(tr.find_all("td")[2].text),
    #         "priceSell": parse_price(tr.find_all("td")[3].text),
    #         "source": parse_source(tr.find_all("td")[4]),
    #         "variations": parse_variations(tr.find_all("td")[5]),
    #         "customization": False,
    #         "sizeLink": tr.find_all("td")[6].img.get("data-src")
    #     }
    #     if tr.find_all("td")[1].find_all("a"):
    #         item["imageLink"] = tr.find_all("td")[0].find_all("a")[0]["href"]
    #     items[name] = item
    # dump_data(items, "furniture/" + key)
    # return items


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


if __name__ == "__main__":
    # -- Characters --
    # scrape_villagers("villagers")

    # -- Museum --
    # scrape_bugs("bugs")
    # scrape_fish("fish")
    # scrape_fossils("fossils")
    # scrape_artworks("artworks")

    # -- Crafting --
    scrape_tools("tools")
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
    # scrape_furniture_housewares("furniture_housewares")

    # -- Flower -- 
    # scrape_flowers("flowers")
    pass
