# animal-crossing-scraper
Python webscraper to extract various data of the game Animal Crossing - New Horizons.

Data source: https://animalcrossing.fandom.com/wiki/

Feel free to use the JSON files! Some of the pages on the wiki are incomplete, so if some data is missing please check back later. 

## Output
All JSON files are stored in /data

*-- Completed --*  
/museums
- bugs.json
- fish.json
- fossils.json
- artwork.json

/characters
- villagers.json

*-- Incomplete --*  
/crafting
- tools.json
- equipments.json
- housewares.json
- miscellaneous.json
- wallMounteds.json
- wallpaperRugsFloorings.json
- others.json

/clothing
- tops.json
- bottoms.json

## JSON fields
-1 for price means the data is not available yet. 

## Set Up
1. In the animal-crossing-scraper root directory, clone the project using 
```
git clone https://github.com/sungyeonu/animal-crossing-scraper.git
```

2. Set up a virtual environment
```
python -m venv venv
```

3. Activate the virtual environment
- Windows: `venv\Scripts\activate`
- Linux/Mac: `source venv/bin/activate`

4. Install required packages
```
pip install -r requirements.txt
```

## Usage
To run:
```
python scrapy.py
```

To test:
```
python test_scrapy.py
```
