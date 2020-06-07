import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl, re
import sqlite3


conn = sqlite3.connect('food_data.sqlite')
cur = conn.cursor()

cur.execute('''
  CREATE TABLE IF NOT EXISTS GI (
  id 			INTEGER NOT NULL PRIMARY KEY UNIQUE,
  food_name		TEXT,
  food_man		TEXT,
  gi_vs_gluc		INTEGER,
  st_serv_size		INTEGER,
  carb_per_serv		INTEGER,
  gl_load			INTEGER,
  country			TEXT,
  prod_cat		TEXT,
  year_test		INTEGER,
  sem			TEXT,
  time_period_test	TEXT,
  num_of_sub		INTEGER,
  type_of_sub		TEXT,
  source_of_data		TEXT,
  url TEXT
  )
''')

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


# How many ID's to check?
count = 3000

# Loop starts here:
# Check all ids in count
for i in range(count):

# URL constructor
  url = 'http://www.glycemicindex.com/foodSearch.php?num='+str(i)+'&ak=detail'
  try:
    page = urllib.request.urlopen(url, context=ctx).read()
  except urllib.error.HTTPError as err:
    if err.code == 404:
      print(err.code)
      print('Not found')
    else:
      print('Other error')
    continue



  # Check if food url id is in Database
  cur.execute("SELECT id, food_name FROM GI WHERE id= ?", (i,))

  try:
    data = cur.fetchone()
    print("Found in database, food name: %s, # With id: %s" % (data[1], data[0]))
    continue
  except:
    pass

  soup = BeautifulSoup(page, 'html.parser')

  # Path to Food Data:
  table43 = soup.find(id='table43')
  tr = list(table43.children)[7]
  table = list(tr.children)[1]
  tr = list(table.children)[3]

  # Start Scraping Food Data

  # Food Name
  td = list(tr.children)[1]
  food_name = list(td.children)[3].get_text()
  print('Inserting %s into Database' %(food_name))

  # Food Manufacturer
  td = list(tr.children)[3]
  food_man = list(td.children)[3].get_text()

  # GI (vs Glucose)
  td = list(tr.children)[7]
  gi_vs_gluc = list(td.children)[3].get_text()

  # Standard Serve Size (g)
  td = list(tr.children)[11]
  st_serv_size = list(td.children)[3].get_text()

  # Carbohydrate per Serve (g)
  td = list(tr.children)[13]
  carb_per_serv = list(td.children)[3].get_text()

  # Glycemic Load (GL)
  td = list(tr.children)[15]
  gl_load = list(td.children)[3].get_text()

  # Country
  td = list(tr.children)[19]
  country = list(td.children)[3].get_text()

  # Product Category
  td = list(tr.children)[21]
  prod_cat = list(td.children)[3].get_text()

  # Year of Test
  td = list(tr.children)[25]
  year_test = list(td.children)[3].get_text()

  # SEM
  td = list(tr.children)[27]
  sem = list(td.children)[3].get_text()

  # Time Period of Test
  td = list(tr.children)[29]
  time_period_test = list(td.children)[3].get_text()

  # Number of Subjects in Test
  td = list(tr.children)[31]
  num_of_sub = list(td.children)[3].get_text()

  # Type of Subjects in Test
  td = list(tr.children)[33]
  type_of_sub = list(td.children)[3].get_text()

  # Reference / Source of Data
  td = list(tr.children)[35]
  source_of_data = list(td.children)[3].get_text()


  # Insert to Database
  cur.execute('''
  INSERT INTO GI (
    id, food_name, food_man, gi_vs_gluc, 
    st_serv_size, carb_per_serv, gl_load, 
    country, prod_cat, year_test, sem, time_period_test, 
    num_of_sub, type_of_sub, source_of_data, url)
  VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
  (i, food_name, food_man, gi_vs_gluc, st_serv_size, carb_per_serv, gl_load, country, prod_cat, year_test, sem, time_period_test, num_of_sub, type_of_sub, source_of_data, url))
  conn.commit()
