from bs4 import Tag
import simplejson as json

def separateByBr(tag, result=''): # recursive, take html element and separate text by <br/>
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

def getImageLinks(images): # return list of imagelinks 
    result = []
    for image in images:
        t = image.get("src")
        if (t.startswith("https")):
            result.append(image.get("src"))
    return result

def dumpData(itemList, path): # turns object to json and dump it in the data/
    with open(("data/" + path + ".json"), 'w') as f:
        json.dump(itemList, f) 


