from scrapy import scrape_bugs, scrape_fish, scrape_fossils, scrape_villagers, scrape_DIYtools
import unittest


class test_critters(unittest.TestCase):
    def test_bugs(self):
        result = scrape_bugs("bugs")
        self.assertEqual(result["Common butterfly"]["name"], "Common butterfly")
        self.assertEqual(result["Common butterfly"]["price"], 160)
        self.assertEqual(result["Common butterfly"]["location"], "Flying")
        self.assertEqual(result["Common butterfly"]["time"], "4 AM - 7 PM")

    def test_fish(self):
        result = scrape_fish("fish")
        self.assertEqual(result["Bitterling"]["name"], "Bitterling")
        self.assertEqual(result["Bitterling"]["price"], 900)
        self.assertEqual(result["Bitterling"]["location"], "River")
        self.assertEqual(result["Bitterling"]["shadowSize"], "1")
        self.assertEqual(result["Bitterling"]["time"], "All day")

    def test_fossils(self):
        result = scrape_fossils("fossils")
        self.assertEqual(result["Acanthostega"]["name"], "Acanthostega")
        self.assertEqual(result["Acanthostega"]["price"], 2000)


class test_characters(unittest.TestCase):
    def test_villagers(self):
        result = scrape_villagers("villagers")
        self.assertEqual(result["Admiral"]["name"], "Admiral")
        self.assertEqual(result["Admiral"]["personality"], "♂ Cranky")
        self.assertEqual(result["Admiral"]["species"], "Bird")
        self.assertEqual(result["Admiral"]["birthday"], "January 27th")
        self.assertEqual(result["Admiral"]["catchPhrase"], "\"aye aye\"")


# class TestDIYRecipes(unittest.TestCase):
#     def testDIYTools(self):
#         result = scrapeDIYTools("tools")
#         self.assertEqual(result[0]["name"], "Flimsy axe")
#         self.assertEqual(
#             result[0]["imageLink"], "https://vignette.wikia.nocookie.net/animalcrossing/images/1/13/NH-Flimsy_axe.png/revision/latest?cb=20200325181711")
#         self.assertEqual(result[0]["materials"], [
#                          "5x tree branch", "1x stone"])
#         self.assertEqual(result[0]["materialsImageLink"], ["https://vignette.wikia.nocookie.net/animalcrossing/images/4/4e/NH-tree_branch-icon.png/revision/latest/scale-to-width-down/18?cb=20200414015713",
#                                                            "https://vignette.wikia.nocookie.net/animalcrossing/images/0/01/NH-stone-icon.png/revision/latest/scale-to-width-down/18?cb=20200414012041"])
#         self.assertEqual(
#             result[0]["sizeLink"], "https://vignette.wikia.nocookie.net/animalcrossing/images/d/d7/NH1.0x1.0sq.jpg/revision/latest?cb=20200324214412")
#         self.assertEqual(result[0]["obtainedFrom"], "Tom Nook")
#         self.assertEqual(result[0]["price"], 200)
#         self.assertEqual(result[0]["isRecipeItem"], True)

#     def testDIYWallMounteds(self):
#         result = scrapeDIYWalls("wallMounteds")
#         self.assertEqual(result[0]["name"], "Bamboo wall decoration")
#         self.assertEqual(result[0]["materials"], ["1x bamboo piece"])
#         self.assertEqual(result[0]["obtainedFrom"], "Message in a bottle")
#         self.assertEqual(result[0]["price"], 160)


if __name__ == '__main__':
    unittest.main()
