from bs4 import BeautifulSoup
import requests
import io

urls = {
	"fish": "https://animalcrossing.fandom.com/wiki/Fish_(New_Horizons)",
	# "fish": "https://animalcrossing.fandom.com/wiki/Fish_(New_Leaf)",
	"bugs": "https://animalcrossing.fandom.com/wiki/Bugs_(New_Horizons)"
}

def getBugs(url, output): 
	response = (requests.get(url, timeout=5))
	soup = BeautifulSoup(response.content, "html.parser")
	itemArr = []
	itemSoup = soup.find_all("table", {"class": "roundy sortable"})

	with io.open(output, "w", encoding="utf-8") as f:
		for item in itemSoup[0].find_all("tr")[1:]:  # first element is header, ignore
			itemInfo = []
			for td in item.find_all("td"):
				itemInfo.append(td.next.strip())
			itemObject = {
				"name":	item.findChildren("a")[0].text,
				"image": item.findChildren("a")[1]['href'],
				"price": itemInfo[2],
				"location": itemInfo[3],
				"shadow-size": itemInfo[4],
				"time": item.findChildren("small")[0].text,
				"jan": itemInfo[6],
				"feb": itemInfo[7],
				"mar": itemInfo[8],
				"apr": itemInfo[9],
				"may": itemInfo[10],
				"jun": itemInfo[11],
				"jul": itemInfo[12],
				"aug": itemInfo[13],
				"sep": itemInfo[14],
				"oct": itemInfo[15],
				"nov": itemInfo[16],
				"dec": itemInfo[17]
			}
			itemArr.append(itemObject)
		for i in itemArr:
			print(i, file=f)

def getFish(url, output): 
	response = (requests.get(url, timeout=5))
	soup = BeautifulSoup(response.content, "html.parser")
	itemSoup = soup.find_all("table", {"class": "roundy sortable"}) 
	itemArr = []

	with io.open(output, "w", encoding="utf-8") as f:
		for item in itemSoup[0].find_all("tr")[1:]:  # first element is header, ignore
			itemInfo = []
			for td in item.find_all("td"):
				itemInfo.append(td.next.strip())
			itemObject = {
				"name":	item.findChildren("a")[0].text,
				"image": item.findChildren("a")[1]['href'],
				"price": itemInfo[2],
				"location": itemInfo[3],
				"shadow-size": itemInfo[4],
				"time": item.findChildren("small")[0].text,
				"jan": itemInfo[6],
				"feb": itemInfo[7],
				"mar": itemInfo[8],
				"apr": itemInfo[9],
				"may": itemInfo[10],
				"jun": itemInfo[11],
				"jul": itemInfo[12],
				"aug": itemInfo[13],
				"sep": itemInfo[14],
				"oct": itemInfo[15],
				"nov": itemInfo[16],
				"dec": itemInfo[17]
			}
			itemArr.append(itemObject)
		for i in itemArr:
			print(i, file=f)

if __name__ == "__main__":
	getFish(urls["fish"], "fish.txt")
	# getBugs(urls["bugs"], "bugs.txt")

