import sqlite3
import datetime
from models.inventory import InventoryModel

class CartModel:

    def __init__(self, id, products, total):
        self.id = id
        #self.products is a dict - {product_id: amt in cart}
        self.products = products
        self.total = total
    
    def add_product(self, product_id, quantity):
        # add a certain quantity of a certain product to cart 
        if product_id not in self.products.keys():
            self.products[product_id] = 0  
        self.products[product_id] += quantity
        self.save_cart_items()
        self.total += quantity * InventoryModel.find_by_id(product_id).json()['price']
        
    def increment_product_amt(self, product_id):
        # increment product amt by 1
        if product_id not in self.products.keys():
            self.products[product_id] = 0
        self.products[product_id] += 1
        self.save_cart_items()
        self.total += InventoryModel.find_by_id(product_id).json()['price']
        
    def remove_product(self, product_id):
        # remove a product
        if product_id in self.products.keys():
            before_quantity = self.products[product_id]
            self.products[product_id] = 0
            self.save_cart_items()
            del self.products[product_id]
            self.total -= before_quantity * InventoryModel.find_by_id(product_id).json()['price']
    
    def decrement_product_amt(self, product_id):
        # decrement product amt by 1
        if product_id in self.products.keys():
            quantity = self.products[product_id]
            if quantity >= 1:
                self.products[product_id] -= 1
                self.save_cart_items()
                after_quantity = self.products[product_id]
                if after_quantity == 0:                 
                    del self.products[product_id]
                self.total -= InventoryModel.find_by_id(product_id).json()['price']   
    
    def get_products(self):
        # can be used to display product info in cart on the front end
        products = list()
        for product_id in self.products.keys():
            # append tuple - (product, amt in cart)
            products.append((InventoryModel.find_by_id(product_id), self.products[product_id]))
        return products
    
    def get_total(self):
        # can be used  to display total on the front end
        return self.total

    def checkout(self):
        # Stripe?
        pass

    def save_cart_items(self):
        # method to update database
        connection = sqlite3.connect('./db/pineapplestore.db')
        cursor = connection.cursor()
        for product_id in self.products.keys():
            query = 'SELECT * FROM cart_item WHERE cart_id=? AND product_id=?;'
            result = cursor.execute(query, (self.id, product_id))
            row = result.fetchall()
            if row:
                # remove entry if quantity is 0
                if self.products[product_id] == 0:
                    query = 'DELETE FROM cart_item WHERE cart_id=? AND product_id=?'
                    cursor.execute(query, (self.id, product_id))
                else:
                    # update quantity if entry exists and quantity isn't 0
                    query = '{}{}{}'.format(
                        'UPDATE cart_item',
                        ' SET quantity=?',
                        ' WHERE cart_id=? AND product_id=?')
                    cursor.execute(query, (self.products[product_id], self.id, product_id))
            else:
                # make a new entry if no result
                query = 'INSERT INTO cart_item VALUES(NULL, ?, ?, ?);'
                cursor.execute(query, (self.products[product_id], product_id, self.id))
        connection.commit()
        connection.close()

    @classmethod 
    def find_cart_by_id(cls, id):
        # construct a CartModel instance by cart id
        product_dict = {}
        total = 0
        connection = sqlite3.connect('./db/pineapplestore.db')
        cursor = connection.cursor()
        query = 'SELECT * FROM cart_item WHERE id=?;'
        result = cursor.execute(query, (id,))
        rows = result.fetchall()
        if rows:
            for row in rows:
                # row[2] is product_id and row[1] is quantity
                product_dict[row[2]] = row[1]
                total += InventoryModel.find_by_id(row[2]).json()['price'] * row[1]
        connection.close()
        return CartModel(id, product_dict, total)

    @classmethod
    def add_cart(cls, user_id):
        # create a cart for user in the cart table
        connection = sqlite3.connect('./db/pineapplestore.db')
        cursor = connection.cursor()
        query = 'SELECT * FROM cart WHERE user_id=?;'
        result = cursor.execute(query, (user_id,))
        row = result.fetchall()
        if not row:
            query = 'INSERT INTO cart VALUES(NULL, ?, ?);'
            cursor.execute(query, (datetime.datetime.now().isoformat(), user_id,))
            connection.commit()
        connection.close()
    
    @classmethod
    def get_cart(cls, user_id):
        connection = sqlite3.connect('./db/pineapplestore.db')
        cursor = connection.cursor()
        query = 'SELECT * FROM cart WHERE user_id=?;'
        result = cursor.execute(query, (user_id,))
        row = result.fetchall()
        if row:
            return CartModel.find_cart_by_id(row[0][0])
    

