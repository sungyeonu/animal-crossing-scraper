from bs4 import BeautifulSoup
import requests
import io

urls = {
	"fish": "https://animalcrossing.fandom.com/wiki/Fish_(New_Horizons)",
	# "fish": "https://animalcrossing.fandom.com/wiki/Fish_(New_Leaf)",
	"bugs": "https://animalcrossing.fandom.com/wiki/Bugs_(New_Horizons)"
}
fname = "output.txt"


def scrape(url, output):  # fish
	response = (requests.get(url, timeout=5))
	soup = BeautifulSoup(response.content, "html.parser")
	itemArr = []
	itemSoup = soup.find_all("table", {"class": "roundy sortable"})

	with io.open(output, "w", encoding="utf-8") as f:
		temp = itemSoup[0]  # the data is in the first table
		for item in temp.find_all("tr")[1:]:  # ignore the first element
			picture = item.findChildren("a")
			location = item.findChildren("small")
			temp = []
			for td in item.find_all("td", text=True):
				temp.append(td.next.strip)
				print(td.next.strip(), file=f)

			itemObject = {
				"picture": picture,
				"location": location
			}
			print("----------", file=f)
			itemArr.append(itemObject)
			# print(itemArr)

if __name__ == "__main__":
	scrape(urls["fish"], "fish.txt")

