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

	with io.open("output.txt", "w", encoding="utf-8") as f1:
		for item in itemSoup[0].find_all("tr")[11:12]:  # ignore the first element
			print(item, file=f1)
			pass
	with io.open(output, "w", encoding="utf-8") as f:
		for item in itemSoup[0].find_all("tr")[11:12]:  # ignore the first element
			itemInfo = []
			for td in item.find_all("td", text=True): # maybe look here?
				itemInfo.append(td.next.strip())
				print(td.next.strip(), file=f)
			# print(itemInfo[0]) # price
			# print(itemInfo[1]) # loc
			# print(itemInfo[2]) # size
			# print(itemInfo[3]) # 1
			# print(itemInfo[4]) # 2
			# print(itemInfo[5]) # 3
			# print("v", itemInfo[6]) # 4 
			# print("v", itemInfo[7]) # 5 
			# print("v", itemInfo[8]) # 6 
			# print("v", itemInfo[9]) # 7
			# print("v", itemInfo[10]) # 8
			# print("v", itemInfo[11]) # 9 
			# print(itemInfo[12]) # 10
			# print(itemInfo[13]) # 11
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
				# "dec": itemInfo[14]
			}
			itemArr.append(itemObject)

		for i in itemArr:
			pass
			# print(i, file=f)

if __name__ == "__main__":
	scrape(urls["fish"], "fish.txt")

