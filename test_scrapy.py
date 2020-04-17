from scrapy import scrapeBugs, scrapeFish, scrapeFossils, scrapeDIYRecipes
import unittest

class TestDIYRecipes(unittest.TestCase):
    def test_DIY_Tools(self):
        url = "https://animalcrossing.fandom.com/wiki/DIY_recipes/Tools"
        result = scrapeDIYRecipes(url)
        # first item
        self.assertEqual(result[0]["name"], "Flimsy axe")
        self.assertEqual(result[0]["imageLink"], "https://vignette.wikia.nocookie.net/animalcrossing/images/1/13/NH-Flimsy_axe.png/revision/latest?cb=20200325181711")
        self.assertEqual(result[0]["materials"], ["5x tree branch", "1x stone"])
        self.assertEqual(result[0]["materialsImageLink"], ["https://vignette.wikia.nocookie.net/animalcrossing/images/4/4e/NH-tree_branch-icon.png/revision/latest/scale-to-width-down/18?cb=20200414015713", "https://vignette.wikia.nocookie.net/animalcrossing/images/0/01/NH-stone-icon.png/revision/latest/scale-to-width-down/18?cb=20200414012041"])
        self.assertEqual(result[0]["sizeLink"], "https://vignette.wikia.nocookie.net/animalcrossing/images/d/d7/NH1.0x1.0sq.jpg/revision/latest?cb=20200324214412")
        self.assertEqual(result[0]["obtainedFrom"], "Tom Nook")
        self.assertEqual(result[0]["price"], 200)
        self.assertEqual(result[0]["isRecipeItem"], True)

if __name__ == '__main__':
    unittest.main()

