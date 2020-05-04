from bs4 import Tag
import simplejson as json

def separateByBr(tag, result=''): # take html element and replace <br /> with comma, recursively
    for c in tag.contents:
        if isinstance(c, Tag):
            if c.name == 'br':
                result += ","
            else:
                result = separateByBr(c, result)
        else:
            result += c
    return result

def avaiConverter(str): # take str and returns True if str represents available. Return False otherwise
    if (str == "\u2713" or str == "✔"): # "\u2713" is a checkmark
        return True
    else:
        return False

def getPriceWithBellsString(str): # take str and return integer only
    return int(str.replace(',', '').replace(' Bells', ''))

def getImageLinks(images): # take html and return the imagelinks in a list
    result = []
    for image in images:
        t = image.get("src")
        if (t.startswith("https")):
            result.append(image.get("src"))
    return result

def dumpData(itemList, path): # turn object to json and dump it in data/
    with open(("data/" + path + ".json"), 'w') as f:
        json.dump(itemList, f, indent=4)
