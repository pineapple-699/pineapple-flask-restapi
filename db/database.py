import sqlite3
import csv
import sys

connection = sqlite3.connect("./db/pineapplestore.db")
cursor = connection.cursor()
create_user_table = '{}{}{}'.format(
    'CREATE TABLE IF NOT EXISTS',
    ' user(id INTEGER PRIMARY KEY,',
    ' username text NOT NULL, password text NOT NULL, address text, sex text, shoe_size FLOAT, pant_size_waist INTEGER, pant_size_length INTEGER, shirt_size TEXT);'
)

cursor.execute(create_user_table)

create_history_table ='{}{}{}{}{}{}'.format(
    'CREATE TABLE IF NOT EXISTS',
    ' purchase_history(id INTEGER PRIMARY KEY,',
    ' product text, user_id INTEGER NOT NULL,',
    ' product_id INTEGER NOT NULL,',
    ' FOREIGN KEY (user_id) REFERENCES user(id),',
    ' FOREIGN KEY (product_id) REFERENCES inventory(id));'
)
cursor.execute(create_history_table)

create_inventory_table = '{}{}{}{}'.format(
    'CREATE TABLE IF NOT EXISTS',
    ' inventory(id INTEGER PRIMARY KEY, sku text, upc INTEGER,',
    ' rando text, product text, description text, price FLOAT,', 
    ' size text, color text, amt INTEGER);'
)
cursor.execute(create_inventory_table)

cursor.execute('INSERT OR REPLACE INTO user VALUES(1, "hope_tambala", "qwert", "Ann Arbor", "Male", "12", "30","30","XL");')
cursor.execute('INSERT OR REPLACE INTO user VALUES(2, "chance_murphy", "qwaszx", "Ann Arbor", "Male", "12", "30","30","XL");')
cursor.execute('INSERT OR REPLACE INTO user VALUES(3, "jalin_parker", "zxasqw", "Ann Arbor", "Male", "12", "30","30","XL");')
cursor.execute('INSERT OR REPLACE INTO user VALUES(4, "kangning_chen", "asdfg", "Ann Arbor", "Male", "12", "30","30","XL");')
cursor.execute('INSERT OR REPLACE INTO user VALUES(5, "yunqi_qian", "qwerty", "Ann Arbor", "Male", "12", "30","30","XL");')
cursor.execute('INSERT OR REPLACE INTO user VALUES(6, "tayloir_thompson", "aqwerva", "Ann Arbor", "Male", "12", "30","30","XL");')

with open("./db/pineapple_inventory.csv", "rt") as f:
    rows = csv.reader(f)
    next(rows) # Skip the header row.
    for row in rows:
        query = "INSERT OR REPLACE INTO inventory VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        cursor.execute(query, row)

cursor.execute('INSERT OR REPLACE INTO purchase_history VALUES(1, "tshirt", 1, 1);')

connection.commit()
connection.close()

print('Database successfully created and populated with data!')