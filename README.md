# animal-crossing-scraper
Python webscraper to extract data of the game Animal Crossing - New Horizons.

Scrapes and parses the data of bugs and fish to json.
For months, the program will return "True" if the critter is available, and "False" otherwise.

URLs to scrape from: 
- https://animalcrossing.fandom.com/wiki/Bugs_(New_Horizons)
- https://animalcrossing.fandom.com/wiki/Fish_(New_Horizons)

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

This will produce two outfiles: 
- fish.json
- bugs.json 
