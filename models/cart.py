import sqlite3
from models.user import UserModel
from models.inventory import InventoryModel

class CartModel:
    def __init__(self, id, products, total):
        # this should reference user id
        self.id = id
        #self.products is a dict - {product_id: amt in cart}
        self.products = products
        self.total = total
    
    def add_item(self, product_id, quantity):
        if product_id not in self.products.keys():
            self.products[product_id] = 0  
        self.products[product_id] += quantity
        self.total += quantity * InventoryModel.find_by_id(product_id).get_price() 

    def increment_product_amt(self, product_id):
        if product_id not in self.products.keys():
            self.products[product_id] = 0
        self.products[product_id] += 1
        self.total += InventoryModel.find_by_id(product_id).get_price()
    
    def remove_product(self, product_id):
        if product_id in self.products.keys():
            quantity = self.products[product_id]
            del self.products[product_id]
            self.total -= quantity * InventoryModel.find_by_id(product_id).get_price()
    
    def decrement_product_amt(self, product_id):
        if product_id in self.products.keys():
            quantity = self.products[product_id]
            if quantity > 1:
                self.products[product_id] -= 1
                if self.products[product_id] == 0:
                    del self.products[product_id]
                self.total -= InventoryModel.find_by_id(product_id).get_price()
    
    def get_products(self):
        products = list()
        for product_id in self.products.keys():
            # append tuple - (product, amt in cart)
            products.append((InventoryModel.find_by_id(product_id), self.products[product_id]))
        return products
    
    def get_total(self):
        return self.total

    def checkout(self):
        # Stripe?
        pass

    
    @classmethod
    def find_cart_by_id(cls, id):
        # use this method to construct a cart
        connection = sqlite3.connect('./db/pineapplestore.db')
        cursor = connection.cursor()
        query = 'SELECT * FROM cart WHERE id=?;'
        # how should we design the cart table
        


