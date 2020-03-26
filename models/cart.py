import sqlite3
import datetime
from inventory import InventoryModel

class CartModel:

    def __init__(self, id, products, total):
        # this is cart id NOT user id
        self.id = id
        # products is a list of dictionaries 
        self.products = products
        # total price for all cart items
        self.total = total
    
    def add_product(self, product_upc, quantity):
        # add a certain quantity of a certain product to cart
        product_already_in_cart = False 
        for product in self.products:
            if product["product_info"]["upc"] == product_upc:
                product["quantity"] += quantity
                product_already_in_cart = True
                break
        if not product_already_in_cart:
            product_info = InventoryModel.find_product_by_upc(product_upc).json()
            self.products.append({"product_info": product_info, "quantity": quantity})
        self.save_cart_items_into_db()
        self.total += quantity * InventoryModel.find_product_by_upc(product_upc).json()['price']
        
    def increment_product_amt(self, product_upc):
        # increment product amt by 1
        for product in self.products:
            if product["product_info"]["upc"] == product_upc:
                product["quantity"] += 1
                self.save_cart_items_into_db()
                self.total += InventoryModel.find_product_by_upc(product_upc).json()['price']
                break 
        
    def remove_product(self, product_upc):
        print("remove called")
        # remove a product
        for product in self.products:
            if product["product_info"]["upc"] == product_upc:
                before_quantity = product["quantity"]
                product["quantity"] = 0
                self.save_cart_items_into_db()
                self.products.remove(product)
                self.total -= before_quantity * InventoryModel.find_product_by_upc(product_upc).json()['price']
                break 

    def decrement_product_amt(self, product_upc):
        # decrement product amt by 1
        for product in self.products:
            if product["product_info"]["upc"] == product_upc:
                if product["quantity"] > 1:
                    product["quantity"] -= 1
                    self.save_cart_items_into_db()
                    self.total -= InventoryModel.find_product_by_upc(product_upc).json()['price']
                    break 
                else:
                    self.remove_product(product_upc)
                    break

    
    def update_product_size(self, product_upc, new_size):
        for product in self.products:
            if product["product_info"]["upc"] == product_upc:
                quantity = product["quantity"]
                print(f"quant is {quantity}")
                current_color = InventoryModel.find_product_by_upc(product_upc).json()['color']
                print("color is " + current_color)
                product_index = self.products.index(product)
                print(f"product index is {product_index}")
                sku = InventoryModel.find_product_by_upc(product_upc).json()['sku']
                product_info = InventoryModel.find_product_by_new_size(sku, current_color, new_size).json()
                if product_info:
                    self.remove_product(product_upc)
                    self.products.insert(product_index, {"product_info": product_info, "quantity": quantity})
    

    def update_product_color(self, product_upc, new_color):
        for product in self.products:
            if product["product_info"]["upc"] == product_upc:
                quantity = product["quantity"]
                print(f"quant is {quantity}")
                current_size = InventoryModel.find_product_by_upc(product_upc).json()['size']
                print("size is " + current_size)
                product_index = self.products.index(product)
                print(f"product index is {product_index}")
                sku = InventoryModel.find_product_by_upc(product_upc).json()['sku']
                product_info = InventoryModel.find_product_by_new_color(sku, current_size, new_color).json()
                if product_info:
                    self.remove_product(product_upc)
                    self.products.insert(product_index, {"product_info": product_info, "quantity": quantity})


    def save_cart_items_into_db(self):
        # method to update database
        connection = sqlite3.connect('../db/pineapplestore.db')
        cursor = connection.cursor()
        for product in self.products:
            query = 'SELECT * FROM cart_item WHERE cart_id=? AND product_upc=?;'
            result = cursor.execute(query, (self.id, product["product_info"]["upc"]))
            row = result.fetchall()
            if row:
                # remove entry if quantity is 0
                if product["quantity"] == 0:
                    query = 'DELETE FROM cart_item WHERE cart_id=? AND product_upc=?'
                    cursor.execute(query, (self.id, product["product_info"]["upc"]))
                else:
                    # update quantity if entry exists and quantity isn't 0
                    query = '{}{}{}'.format(
                        'UPDATE cart_item',
                        ' SET quantity=?',
                        ' WHERE cart_id=? AND product_upc=?')
                    cursor.execute(query, (product["quantity"], self.id, product["product_info"]["upc"]))
            else:
                # make a new entry if no result
                query = 'INSERT INTO cart_item VALUES(NULL, ?, ?, ?);'
                cursor.execute(query, (product["quantity"], product["product_info"]["upc"], self.id))
        connection.commit()
        connection.close()
    
    def json(self):
        return {
            "cart_id": self.id,
            "products": self.products,
            "total": self.total
        }

    @classmethod 
    def construct_cart_by_cart_id(cls, cart_id):
        # construct a Cart instance by cart id
        products = []
        total = 0
        connection = sqlite3.connect('../db/pineapplestore.db')
        cursor = connection.cursor()
        query = 'SELECT * FROM cart_item WHERE cart_id=?;'
        result = cursor.execute(query, (cart_id,))
        rows = result.fetchall()
        if rows:
            for row in rows:
                quantity = row[1]
                product_upc = row[2]
                product_info = InventoryModel.find_product_by_upc(product_upc).json()
                products.append({"product_info": product_info, "quantity": quantity})
                total += product_info["price"] * quantity
        connection.close()
        return CartModel(cart_id, products, total)
    
    @classmethod
    def retrieve_cart_by_user_id(cls, user_id):
        connection = sqlite3.connect('../db/pineapplestore.db')
        cursor = connection.cursor()
        query = 'SELECT * FROM cart WHERE user_id=?;'
        result = cursor.execute(query, (user_id,))
        row = result.fetchall()
        if row:
            # if this user already has a cart, return it
            connection.close()
            # row[0][0] is cart id
            return CartModel.construct_cart_by_cart_id(row[0][0])
        else:
            # if this user doesn't already have a cart, create one and return it
            query = 'INSERT INTO cart VALUES(NULL, ?, ?);'
            cursor.execute(query, (datetime.datetime.now().isoformat(), user_id,))
            connection.commit()
            query = 'SELECT * FROM cart WHERE user_id=?;'
            result = cursor.execute(query, (user_id,))
            row = result.fetchall()
            connection.close()
            return CartModel.construct_cart_by_cart_id(row[0][0])

### methods for endpoint below
        
    @classmethod 
    def add_product_for_user(cls, user_id, product_upc, quantity):
        cart = CartModel.retrieve_cart_by_user_id(user_id)
        cart.add_product(product_upc, quantity)
    
    @classmethod
    def remove_product_for_user(cls, user_id, product_upc, quantity):
        cart = CartModel.retrieve_cart_by_user_id(user_id)
        cart.remove_product(product_upc, quantity)
    
    @classmethod
    def increment_product_amt_for_user(cls, user_id, product_upc, quantity):
        cart = CartModel.retrieve_cart_by_user_id(user_id)
        cart.increment_product_amt(product_upc, quantity)
    
    @classmethod
    def decrement_product_amt_for_user(cls, user_id, product_upc, quantity):
        cart = CartModel.retrieve_cart_by_user_id(user_id)
        cart.decrement_product_amt(product_upc, quantity)

    @classmethod
    def retrieve_products_in_cart_for_user(cls, user_id):
        cart = CartModel.retrieve_cart_by_user_id(user_id) 
        return cart.json()




cart = CartModel.retrieve_cart_by_user_id(1)
cart.add_product(1468826073, 2)
cart.add_product(7281589674, 3)
cart.update_product_size(111, "M")
print(cart.json())

