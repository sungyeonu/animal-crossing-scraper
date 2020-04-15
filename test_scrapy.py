from scrapy import scrapeBugs, scrapeFish, scrapeFossils, scrapeDIYRecipes
import unittest

class TestSum(unittest.TestCase):
    def test_DIY_Tools(self):
        url = "https://animalcrossing.fandom.com/wiki/DIY_recipes/Tools"
        result = scrapeDIYRecipes(url)
        self.assertEqual(result[0]["name"], "Flimsy axe", "Should be 6")

if __name__ == '__main__':
    unittest.main()

