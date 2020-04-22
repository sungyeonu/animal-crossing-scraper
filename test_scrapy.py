from scrapy import scrapeBugs, scrapeFish, scrapeFossils, scrapeVillagers, scrapeDIYTools
import unittest

class TestCritters(unittest.TestCase):
    def testBugs(self):
        result = scrapeBugs("bugs")
        self.assertEqual(result[0]["name"], "Common butterfly")
        self.assertEqual(result[0]["price"], 160)
        self.assertEqual(result[0]["location"], "Flying")
        self.assertEqual(result[0]["time"], "4 AM - 7 PM")

    def testFish(self):
        result = scrapeFish("fish")
        self.assertEqual(result[0]["name"], "Bitterling")
        self.assertEqual(result[0]["price"], 900)
        self.assertEqual(result[0]["location"], "River")
        self.assertEqual(result[0]["shadowSize"], "1")
        self.assertEqual(result[0]["time"], "All day")
    
    def testFossils(self):
        result = scrapeFossils("fossils")
        self.assertEqual(result[0]["name"], "Acanthostega")
        self.assertEqual(result[0]["price"], 2000)

class TestCharacters(unittest.TestCase):
    def testVillagers(self):
        result = scrapeVillagers("villagers")
        self.assertEqual(result[0]["name"], "Admiral")
        self.assertEqual(result[0]["personality"], "♂ Cranky")
        self.assertEqual(result[0]["species"], "Bird")
        self.assertEqual(result[0]["birthday"], "January 27th")
        self.assertEqual(result[0]["catchPhrase"], "\"aye aye\"")

class TestDIYRecipes(unittest.TestCase):
    def testDIYTools(self):
        result = scrapeDIYTools("tools")
        self.assertEqual(result[0]["name"], "Flimsy axe")
        self.assertEqual(result[0]["imageLink"], "https://vignette.wikia.nocookie.net/animalcrossing/images/1/13/NH-Flimsy_axe.png/revision/latest?cb=20200325181711")
        self.assertEqual(result[0]["materials"], ["5x tree branch", "1x stone"])
        self.assertEqual(result[0]["materialsImageLink"], ["https://vignette.wikia.nocookie.net/animalcrossing/images/4/4e/NH-tree_branch-icon.png/revision/latest/scale-to-width-down/18?cb=20200414015713", "https://vignette.wikia.nocookie.net/animalcrossing/images/0/01/NH-stone-icon.png/revision/latest/scale-to-width-down/18?cb=20200414012041"])
        self.assertEqual(result[0]["sizeLink"], "https://vignette.wikia.nocookie.net/animalcrossing/images/d/d7/NH1.0x1.0sq.jpg/revision/latest?cb=20200324214412")
        self.assertEqual(result[0]["obtainedFrom"], "Tom Nook")
        self.assertEqual(result[0]["price"], 200)
        self.assertEqual(result[0]["isRecipeItem"], True)

    def testDIYEquipments(self):
        pass

if __name__ == '__main__':
    unittest.main()

