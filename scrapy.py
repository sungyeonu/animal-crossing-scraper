from bs4 import BeautifulSoup
import requests
import io

urls = {
	# "fish": "https://animalcrossing.fandom.com/wiki/Fish_(New_Horizons)",
	"fish": "https://animalcrossing.fandom.com/wiki/Fish_(New_Leaf)",
	"bugs": "https://animalcrossing.fandom.com/wiki/Bugs_(New_Horizons)"
}


def scrape(url, output):  # fish
	response = (requests.get(url, timeout=5))
	soup = BeautifulSoup(response.content, "html.parser")
	itemArr = []
	itemSoup = soup.find_all("table", {"class": "roundy sortable"})

	with io.open(output, "w", encoding="utf-8") as f:
		temp = itemSoup[0]  # the data is in the first table
		for item in temp.find_all("tr")[1:10]:  # ignore the first element
			itemInfo = []
			for td in item.find_all("td", text=True):
				itemInfo.append(td.next.strip())
				# print(td.next.strip(), file=f)

			itemObject = {
				"name":	item.findChildren("a")[0].text,
				"image": item.findChildren("a")[1]['href'],
				"price": itemInfo[0],
				"location": itemInfo[1],
				"shadow-size": itemInfo[2], # needs fix
				"time": item.findChildren("small")[0].text,
				"jan": itemInfo[3],
				"feb": itemInfo[4],
				"mar": itemInfo[5],
				"apr": itemInfo[6],
				"may": itemInfo[7],
				"jun": itemInfo[8],
				"jul": itemInfo[9],
				"aug": itemInfo[10],
				"sep": itemInfo[11],
				"oct": itemInfo[12],
				"nov": itemInfo[13],
				"dec": itemInfo[14]
			}
			itemArr.append(itemObject)

		for i in itemArr:
			print(i, file=f)

if __name__ == "__main__":
	scrape(urls["fish"], "fish.txt")

