import csv
import sys
# from models.inventory import InventoryModel

class InventoryModel:

    def __init__(self, id, sku, upc, rando, product, description, price, size, color, amt):
        self.id = id
        self.sku = sku
        self.upc = upc
        self.rando = rando
        self.product = product
        self.description = description
        self.price = price
        self.size = size
        self.color = color
        self.amt = amt

    @classmethod
    def find_by_product(cls, product):
        products = list()
        connection = sqlite3.connect('./db/pineapplestore.db')
        cursor = connection.cursor()
        query = 'SELECT * FROM inventory WHERE product=?;'
        result = cursor.execute(query, (product,))
        rows = result.fetchall()
        if rows:
            for row in rows:
                products.append(InventoryModel(row[0], row[1], row[2], row[3], 
                row[4], row[5], row[6], row[7], row[8], row[9]))
            return products
        connection.close()

    @classmethod
    def find_all_products(cls):
        products = list()
        connection = sqlite3.connect('./db/pineapplestore.db')
        cursor = connection.cursor()
        query = 'SELECT * FROM inventory;'
        result = cursor.execute(query)
        rows = result.fetchall()
        if rows:
            for row in rows:
                products.append(InventoryModel(row[0], row[1], row[2], row[3], 
                row[4], row[5], row[6], row[7], row[8], row[9]))
            return products
        connection.close()

    @classmethod
    def add_product(self, id, sku, upc, rando, product, description, price, size, color, amt):
        connection = sqlite3.connect('./db/pineapplestore.db')
        cursor = connection.cursor()
        query = 'INSERT INTO inventory VALUES(NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'
        cursor.execute(query, (id, sku, upc, rando, product, description, price, size, color, amt))
        connection.commit()
        connection.close()

    def json(self):
        return {'id': self.id,
        'sku': self.sku,
        'upc': self.upc,
        'rando': self.rando,
        'product': self.product,
        'description': self.description,
        'price': self.price,
        'size': self.size,
        'color': self.color,
        'amt': self.amt
        }
# reader = csv.DictReader(open("pineapple_inventory.csv", encoding="utf-8"))
# for raw in reader:
#     print(raw)

data = open("pineapple_inventory.csv", "rt", encoding="ascii")
# data = pd.read_csv("pineapple_inventory.csv", encoding= 'unicode_escape')
# open_data = csv.reader(data)
# loader = next(open_data)
# print(loader)
# content = loader.decode(encoding='UTF-8',errors='strict')
inventory = []

# with open('pineapple_inventory.csv') as csvfile:
readcsv = csv.reader(data, delimiter=',')
for line in readcsv:
    inventory.append(line)
# print(type(content))
# for inst in content:
#     inventory.append(InventoryModel(inst))

