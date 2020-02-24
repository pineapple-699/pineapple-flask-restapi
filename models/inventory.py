import sqlite3, sys
from models.user import UserModel
from models.purchase_history import PurchaseHistoryModel

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
            'amt': self.amt
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