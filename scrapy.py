from bs4 import BeautifulSoup
import requests

url = 'https://animalcrossing.fandom.com/wiki/Fish_(New_Horizons)'
response = (requests.get(url, timeout=5))
content = BeautifulSoup(response.content, "html.parser").prettify()

print(content)