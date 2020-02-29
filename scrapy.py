from bs4 import BeautifulSoup
import requests
import io
urls = {
	# "fish": "https://animalcrossing.fandom.com/wiki/Fish_(New_Horizons)",
	"fish": "https://animalcrossing.fandom.com/wiki/Fish_(New_Leaf)",
	"bugs": "https://animalcrossing.fandom.com/wiki/Bugs_(New_Horizons)"
}
fname = "output.txt"


def scrape(key, url):
  # need to take account of different formats. Fish has shadow size but bug doesnt.
	response = (requests.get(url, timeout=5))
	soup = BeautifulSoup(response.content, "html.parser")
	itemArr = []
	itemSoup = soup.find_all("table", {"class": "roundy sortable"})

	with io.open("test.txt", "w", encoding="utf-8") as f1:
		temp = itemSoup[0]  # the data is in the first table
		for item in temp.find_all("tr")[1:]:  # ignore the first element
			picture = item.findChildren("a")
			location = item.findChildren("small")
			for td in item.find_all("td", text=True):
				print(td.next.strip(), file=f1)
			itemObject = {
				"picture": picture,
				"location": location
			}
			print("----------", file=f1)
			itemArr.append(itemObject)
	with io.open(fname, "w", encoding="utf-8") as f:
		print(itemArr, file=f)
if __name__ == "__main__":
	# for key in urls:
	#   scrape(key, urls[key])
	scrape("fish", urls["fish"])
