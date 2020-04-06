import sqlite3, sys
from models.user import UserModel
from models.purchase_history import PurchaseHistoryModel

class InventoryModel:

    def __init__(self, id, sku, upc, rando, product, description, price, size, color, amt, store):
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
        self.store = store

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
                    row[4], row[5], row[6], row[7], row[8], row[9],row[10]))
            return products
        connection.close()

    @classmethod
    def find_by_id(cls, id):
        connection = sqlite3.connect('./db/pineapplestore.db')
        cursor = connection.cursor()
        query = 'SELECT * FROM inventory WHERE id=?;'
        result = cursor.execute(query, (id,))
        row = result.fetchall()
        if row:
            return InventoryModel(row[0][0], row[0][1], row[0][2], row[0][3], 
            row[0][4], row[0][5], row[0][6], row[0][7], row[0][8], row[0][9],row[0][10])
        connection.close()

    @classmethod
    def find_product_by_upc(cls, upc):
        connection = sqlite3.connect('./db/pineapplestore.db')
        cursor = connection.cursor()
        query = 'SELECT * FROM inventory WHERE upc=?;'
        result = cursor.execute(query, (upc,))
        row = result.fetchall()
        if row:
            return InventoryModel(row[0][0], row[0][1], row[0][2], row[0][3], 
            row[0][4], row[0][5], row[0][6], row[0][7], row[0][8], row[0][9], row[0][10])
        connection.close()
    
    @classmethod
    def find_product_by_new_size(cls, sku, color, new_size):
        connection = sqlite3.connect('./db/pineapplestore.db')
        cursor = connection.cursor()
        query = 'SELECT * FROM inventory WHERE sku=? and color=? and size=?;'
        result = cursor.execute(query, (sku, color, new_size))
        row = result.fetchall()
        if row:
            return InventoryModel(row[0][0], row[0][1], row[0][2], row[0][3], 
            row[0][4], row[0][5], row[0][6], row[0][7], row[0][8], row[0][9], row[0][10])
        connection.close()
    
    @classmethod
    def find_product_by_new_color(cls, sku, size, new_color):
        connection = sqlite3.connect('./db/pineapplestore.db')
        cursor = connection.cursor()
        query = 'SELECT * FROM inventory WHERE sku=? and size=? and color=?;'
        result = cursor.execute(query, (sku, size, new_color))
        row = result.fetchall()
        if row:
            return InventoryModel(row[0][0], row[0][1], row[0][2], row[0][3], 
            row[0][4], row[0][5], row[0][6], row[0][7], row[0][8], row[0][9], row[0][10])
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
                    row[4], row[5], row[6], row[7], row[8], row[9],row[10]))
            return products
        connection.close()

    @classmethod
    def add_product(self, product, price):
        connection = sqlite3.connect('./db/pineapplestore.db')
        cursor = connection.cursor()
        query = 'INSERT INTO inventory VALUES(NULL, ?, ?);'
        cursor.execute(query, (product, price,))
        connection.commit()
        connection.close()

    def json(self):
        return {
            'id': self.id,
            'sku': self.sku,
            'upc': self.upc,
            'rando': self.rando,
            'product': self.product,
            'description': self.description,
            'price': self.price,
            'size': self.size,
            'color': self.color,
            'amt': self.amt,
            "store":self.store
        }


class ShoppingInventory:

    # def __init__(id, product, user_id, product_id):
    #     self.id = id
    #     self.product = product
    #     self.user_id = user_id
    #     self.product_id = product_id

    @classmethod
    def buy_product(cls, username, product):
        user = UserModel.find_by_name(username)
        if user:
            products = InventoryModel.find_by_product(product)
            if products:
                connection = sqlite3.connect('./db/pineapplestore.db')
                cursor = connection.cursor()
                query = 'INSERT INTO purchase_history VALUES(NULL, ?, ?, ?);'
                cursor.execute(query, (product, user.id, products[0].id,))
                connection.commit()
                connection.close()
                return {'message': 'Selected product was bought!'}, 200
            else:
                return {'message': 'No product in database!'}, 404
        else:
            return {'message': 'Shopping impossible, no user in database!'}, 404