import sqlite3
import csv
import sys

connection = sqlite3.connect("./db/pineapplestore.db")
cursor = connection.cursor()
create_user_table = '{}{}{}'.format(
    'CREATE TABLE IF NOT EXISTS',
    ' user(id INTEGER PRIMARY KEY AUTOINCREMENT,',
    ' username text NOT NULL, password text NOT NULL, sex text, shoe_size FLOAT, pant_size_waist INTEGER, pant_size_length INTEGER, shirt_size TEXT, shipping_address text, billing_address text);'
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
    ' size text, color text, amt INTEGER, store text, picture text);'
)
cursor.execute(create_inventory_table)

'''Database Design for Cart:

https://dba.stackexchange.com/questions/133626/which-way-is-better-to-design-shopping-cart-table-sql-server
http://www.mikesdotnetting.com/article/210/razor-web-pages-e-commerce-adding-a-shopping-cart-to-the-bakery-template-site

'''
create_cart_table = '{}{}{}{}{}'.format(
    'CREATE TABLE IF NOT EXISTS',
    ' cart(id INTEGER PRIMARY KEY,',
    # https://stackoverflow.com/questions/17227110/how-do-datetime-values-work-in-sqlite
    ' date_created text,',
    ' user_id INTEGER NOT NULL,',
    ' FOREIGN KEY (user_id) REFERENCES user(id));'
)
cursor.execute(create_cart_table)

create_cart_item_table = '{}{}{}{}{}{}{}'.format(
    'CREATE TABLE IF NOT EXISTS',
    ' cart_item(id INTEGER PRIMARY KEY,',
    ' quantity INTEGER,',
    ' product_upc INTEGER NOT NULL,',
    ' cart_id INTEGER NOT NULL,',
    ' FOREIGN KEY (product_upc) REFERENCES inventory(upc)',
    ' FOREIGN KEY (cart_id) REFERENCES cart(id));'
)
cursor.execute(create_cart_item_table)


cursor.execute('INSERT INTO user (username, password, sex, shoe_size, pant_size_waist, pant_size_length, shirt_size, shipping_address, billing_address) VALUES("hope_tambala", "qwert", "Male", "12", "30","30","XL", "Ann Arbor", "MI");')
cursor.execute('INSERT INTO user (username, password, sex, shoe_size, pant_size_waist, pant_size_length, shirt_size, shipping_address, billing_address) VALUES("chance_murphy", "qwaszx", "Male", "12", "30","30","XL", "Ann Arbor", "MI");')
cursor.execute('INSERT INTO user (username, password, sex, shoe_size, pant_size_waist, pant_size_length, shirt_size, shipping_address, billing_address) VALUES("jalin_parker", "zxasqw", "Male", "12", "30","30","XL", "Ann Arbor", "MI");')
cursor.execute('INSERT OR REPLACE INTO user (username, password, sex, shoe_size, pant_size_waist, pant_size_length, shirt_size, shipping_address, billing_address) VALUES("kangning_chen", "asdfg", "Female", "12", "30","30","XL", "Ann Arbor", "MI");')
cursor.execute('INSERT OR REPLACE INTO user (username, password, sex, shoe_size, pant_size_waist, pant_size_length, shirt_size, shipping_address, billing_address) VALUES("yunqi_qian", "qwerty", "Female", "12", "30","30","XL", "Ann Arbor", "MI");')
cursor.execute('INSERT OR REPLACE INTO user (username, password, sex, shoe_size, pant_size_waist, pant_size_length, shirt_size, shipping_address, billing_address) VALUES("tayloir_thompson", "aqwerva", "Female", "12", "30","30","XL", "Ann Arbor", "MI");')

with open("./db/pineapple_inventory.csv", "rt") as f:
    rows = csv.reader(f)
    next(rows) # Skip the header row.
    for row in rows:
        query = "INSERT OR REPLACE INTO inventory VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        cursor.execute(query, row)

cursor.execute('INSERT OR REPLACE INTO purchase_history VALUES(1, "tshirt", 1, 1);')

create_shipping_address_table = '{}{}{}{}{}'.format(
    'CREATE TABLE IF NOT EXISTS',
    ' shipping_address(id INTEGER PRIMARY KEY, username text NOT NULL,',
    ' full_name text, address1 text, address2 text,',
    ' city text, state text, zipcode text,',
    ' FOREIGN KEY (username) REFERENCES user(username));'
)

create_billing_address_table = '{}{}{}{}{}'.format(
    'CREATE TABLE IF NOT EXISTS',
    ' billing_address(id INTEGER PRIMARY KEY, username text NOT NULL,',
    ' full_name text, address1 text, address2 text,',
    ' city text, state text, zipcode text,',
    ' FOREIGN KEY (username) REFERENCES user(username));'
)

cursor.execute(create_shipping_address_table)
cursor.execute(create_billing_address_table)

cursor.execute('INSERT OR REPLACE INTO shipping_address VALUES(1, "hope_tambala", "Hope Tambala", "123 Python St", "", "Ann Arbor", "MI", "48109");')
cursor.execute('INSERT OR REPLACE INTO shipping_address VALUES(2, "chance_murphy", "Chance Murphy", "456 SQL St", "F", "Ann Arbor", "MI", "48104");')
cursor.execute('INSERT OR REPLACE INTO shipping_address VALUES(3, "jalin_parker", "Jalin Parker", "789 Javascript St", "", "Ann Arbor", "MI", "48104");')
cursor.execute('INSERT OR REPLACE INTO shipping_address VALUES(4, "kangning_chen", "Kangning Chen", "101 CPP St", "Apt. 3", "Ann Arbor", "MI", "48109");')
cursor.execute('INSERT OR REPLACE INTO shipping_address VALUES(5, "yunqi_qian", "Yunqi Qian", "112 Java St", "", "Ann Arbor", "MI", "48104");')
cursor.execute('INSERT OR REPLACE INTO shipping_address VALUES(6, "tayloir_thompson", "Tayloir Thompson", "131 PHP St", "2A", "Ann Arbor", "MI", "48109");')

cursor.execute('INSERT OR REPLACE INTO billing_address VALUES(1, "hope_tambala", "Hope Tambala", "345 Python St", "", "Ann Arbor", "MI", "48109");')
cursor.execute('INSERT OR REPLACE INTO billing_address VALUES(2, "chance_murphy", "Chance Murphy", "678 SQL St", "F", "Ann Arbor", "MI", "48104");')
cursor.execute('INSERT OR REPLACE INTO billing_address VALUES(3, "jalin_parker", "Jalin Parker", "910 Javascript St", "", "Ann Arbor", "MI", "48104");')
cursor.execute('INSERT OR REPLACE INTO billing_address VALUES(4, "kangning_chen", "Kangning Chen", "112 CPP St", "Apt. 3", "Ann Arbor", "MI", "48109");')
cursor.execute('INSERT OR REPLACE INTO billing_address VALUES(5, "yunqi_qian", "Yunqi Qian", "131 Java St", "", "Ann Arbor", "MI", "48104");')
cursor.execute('INSERT OR REPLACE INTO billing_address VALUES(6, "tayloir_thompson", "Tayloir Thompson", "415 PHP St", "2A", "Ann Arbor", "MI", "48109");')

connection.commit()
connection.close()

print('Database successfully created and populated with data!')