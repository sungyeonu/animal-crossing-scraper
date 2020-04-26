# animal-crossing-scraper
Python webscraper to extract various data of the game Animal Crossing - New Horizons.

Data source: 
- https://animalcrossing.fandom.com/wiki/

## Output
All json files are stored in /data

Critters
- bugs.json
- fish.json
- fossils.json

Characters
- villagers.json

DIY Recipes
- tools.json
- equipments.json
- housewares.json
- miscellaneous.json
- wallMounteds.json
- wallpaperRugsFloorings.json
- others.json

## Set Up
1. In the animal-crossing-scraper root directory, clone the project using 
```
git clone https://github.com/sungyeonu/animal-crossing-scraper.git
```

2. Set up virtual environment
```
python -m venv venv
```

3. Activate the virtual environment
- Windows: `venv\Scripts\activate.bat`
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
