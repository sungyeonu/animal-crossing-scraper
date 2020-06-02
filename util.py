from bs4 import Tag
import simplejson as json
import re

def separate_by_br(tag, result=''): # take html element and replace <br/> tag with comma
    for c in tag.contents:
        if isinstance(c, Tag):
            if c.name == 'br' or c.name == "\n":
                result += "|"
            else:
                result = separate_by_br(c, result)
        else:
            result += c
    return result

def convert_checkmark(string): # take str and returns True if str represents available. Return False otherwise
    if (string == "\u2713" or string == "✔"):  # "\u2713" is a checkmark
        return True
    else:
        return False

def parse_price(string): # take str and return integer only
    try: 
        return int(''.join(filter(str.isdigit, string)))
    except:
        return -1


def get_image_urls(images): # take html and return all imageLinks in a list. Strip out downscale property
    result = []
    for image in images:
        t = image.get("src")
        if (t.startswith("https")):
            result.append(image.get("src").replace(
                "/scale-to-width-down/18", "").replace("/scale-to-width-down/50", ""))
    return result

def parse_variations(tag):
    if tag.text.strip() == "N/A":
        return []
    return separate_by_br(tag).strip().split(", ")

def parse_source(tag):
    if tag.text.strip() == "*" or tag.text.strip() == "N/A":
        return []
    if tag.img:
        if tag.img['alt'] == "NH-Inventory Icons-DIY Recipe" or tag.img['alt'] == "DIY Icon":
            return ["DIY Recipes"]
        if tag.img['alt'] == "72px-Timmy Icon" or tag.img['alt'] == "NH-Icon-Timmy":
            return ["Nook's Cranny"]
        if tag.img['alt'] == "FishIconTest":
            return ["Fishing Tourney"]
        if tag.img['alt'] == "BugIconTest":
            return ["Bug Off"]
        if tag.img['alt'] == "NH-Icon-Flick":
            return ["Flick"]
        if tag.img['alt'] == "NH-Icon-CJ":
            return ["C.J."]
        if tag.img['alt'] == "NHnookstop":
            return ["Nook Stop"]
        if tag.img['alt'] == "NH-Icon-Gulliver":
            return ["Gulliver"]
        if tag.img['alt'] == "HHA logo":
            return ["Happy Home Academy"]
        if tag.img['alt'] == "NH-Icon-Saharah":
            return ["Saharah"]
        if tag.img['alt'] == "NH-Icon-Present":
            return ["Mom"]
    return []


def parse_personality(tag): 
    return tag.text.strip()[2:]


def parse_gender(tag):
    if tag.text.strip()[0] == "♂":
        return "male"
    elif tag.text.strip()[0] == "♀":
        return "female"
    return None    


def parse_image_URLs(tag):
    result = []
    for image in tag("img"):
        if image.get("data-src") is not None:
            result.append(image.get("data-src").replace("/scale-to-width-down/24", ""))
    return result


def parse_months(months):
    result = []
    counter = 1
    for m in months:
        if convert_checkmark(m.text.strip()):
            result.append(counter)
        counter += 1
    return (result)


def parse_rose_image_URLs(tags):
    result = []
    for tag in tags:
        result.append(tag.get("data-src").replace("/scale-to-width-down/50", ""))
    return result


def parse_hybridization_children(tag):
    result = []
    abbrs = tag("abbr")
    percentages = [i for i in tag.text.split("\n") if i]
    counter = 0
    for abbr in abbrs:
        child = {
            "image_url": abbr("img")[0].get("data-src").replace("/scale-to-width-down/30", ""),
            # return percentage in int
            "gene": abbr.get("title"),
            "probability": float(percentages[counter].strip("%"))/100
        }
        counter += 1
        result.append(child)
    return result

def parse_materials(tag):
    items = {}
    materials_separated = separate_by_br(tag).strip().split("|")
    counter = 0
    image_urls = get_image_urls(tag("img"))
    for material in materials_separated:
        if (material != ""):
            item = {
                "amount": int(re.sub("\D", "", material.split(" ")[0])), # scrape only digits
            }
            try: 
                item["image_url"] = image_urls[counter]
            except IndexError:
                item["image_url"] = None

            name = material.replace(material.split(" ")[0], "").strip()
            counter += 1
            items[name] = item
    return items

def parse_customization(tag):
    if tag.text.strip() == "N/A": 
        return None
    if tag.text.strip() == "': Custom Design":
        return None
    try:

        item = {}
        item["detail"] = tag.text.strip().split()[0]
        item["number_kits"] = int(re.sub("\D", "", tag.text.strip()))
        return item
    except:
        return None

def parse_image_url(tag):
    try: 
        img_url = tag("img")[1]["src"]
        if img_url[:5] == "https":
            return img_url.replace("/scale-to-width-down/30", "")
    except:
        return None

def parse_furniture_variations(tag):
    if tag.text.strip() == "N/A":
        return None
    text = tag.text.strip()
    if ":" in text: # remove header
        text = text.split(":", 1)[-1].strip()
    text = text.split(",")
    return [t.strip() for t in text]


def parse_obtained_from(tag):
    if "\n" in tag.text: # some pages use \n to break, some use <br> 
        return tag.text.strip().split("\n")
    return separate_by_br(tag).strip().split(",")

def parse_image_img_url(tag):
    try:
        return tag.img.get("data-src")
    except:
        return None


def dump_data(itemList, path): # turn object to json and dump it in data/
    with open(("data/" + path + ".json"), 'w', encoding='utf-8') as f:
        json.dump(itemList, f, ensure_ascii=False, indent=4)

