import sqlite3

conn = sqlite3.connect('food_data.sqlite')
cur = conn.cursor()

# How many ID's to check?
count = 3000
missing_ids = list()
# Loop starts here:

for i in range(count):
  # Check if for empty IDs in Database
  cur.execute("SELECT id, food_name FROM GI WHERE id= ?", (i,))

  try:
    data = cur.fetchone()
    print("Found in database, food name: %s, # With id: %s" % (data[1], data[0]))
    continue
  except:
    pass
  missing_ids.append(i)
print(missing_ids)
