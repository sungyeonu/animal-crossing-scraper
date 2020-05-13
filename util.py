from bs4 import Tag
import simplejson as json

def separate_by_br(tag, result=''): # take html element and replace <br/> tag with comma
    for c in tag.contents:
        if isinstance(c, Tag):
            if c.name == 'br':
                result += ","
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

def strip_price(string): # take str and return integer only
    return int(''.join(filter(str.isdigit, string)))
    # return int(str.replace(',', '').replace(' Bells', ''))

def get_image_links(images): # take html and return all imageLinks in a list. Strip out downscale property
    result = []
    for image in images:
        t = image.get("src")
        if (t.startswith("https")):
            result.append(image.get("src").replace("/scale-to-width-down/18", ""))
    return result

def dump_data(itemList, path): # turn object to json and dump it in data/
    with open(("data/" + path + ".json"), 'w') as f:
        json.dump(itemList, f, indent=4)
