# Glycemic Index Database 

## Instructions:
1. Install Python 3
2. Open the project in your favorite CLI
3. Check if Python 3 is installed
		python --version
4. If python is > 3.X run the following commands:  
python -m venv venv  
python -m pip install -r packages.txt
5. Pull Data  
		python pull_data.py

[Database Source](http://www.glycemicindex.com/foodSearch.php)

### Modules
#### check-for_missing.ids.py
Checks for missing ids from database

#### pull.data.py
Scrapes the date from the source and inserts the data into our database.