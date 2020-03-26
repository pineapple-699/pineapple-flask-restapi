from models.cart import CartModel
from flask_restful import Resource, reqparse


class Cart(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id',
                            type=int,
                            required=True,
                            help='This field is mandatory!')

        data_payload = parser.parse_args()
        cart = CartModel.retrieve_cart_by_user_id(data_payload['user_id'])
        if cart:
            return {
                'cart': cart.json()
            }, 200
        else:
            return {'message': 'Cart not found!'}, 404


# class CartItem(Resource):
#     def post(self, user_id, cart_id):
        
#         parser = reqparse.RequestParser()
#         parser.add_argument('user_id',
#                             type=int,
#                             required=True,
#                             help='This field is mandatory!')

#         parser.add_argument('product_upc',
#                             type=int,
#                             required=True,
#                             help='This field is mandatory!')
        
#         parser.add_argument('quantity',
#                             type=int,
#                             required=True,
#                             help='This field is mandatory!')

#         data_payload = parser.parse_args()
#         cart = CartModel.retrieve_cart_by_user_id(data_payload['user_id'])

#         if (data_payload['type'] =='add_product'):
#             cart.add_product(data_payload['product_upc'], data_payload['quanity'])
#             return {'message': 'Cart Item successfully added to database!'}, 201
            
#         if (data_payload['type'] =='remove_product'):
#             cart.remove_product(data_payload['product_upc'])
#             return {'message': 'Cart Item successfully removed from database!'}, 201


# class CartItemQuanity(Resource):
#     def post(self, user_id, cart_id, product_id):
        
#         parser = reqparse.RequestParser()
#         parser.add_argument('cart_id',
#                             type=int,
#                             required=True,
#                             help='This field is mandatory!')

#         parser.add_argument('product_id',
#                             type=int,
#                             required=True,
#                             help='This field is mandatory!')
        
#         parser.add_argument('type',
#                             type=str,
#                             required=True,
#                             help='This field is mandatory!')
        
#         parser.add_argument('quantity',
#                             type=int,
#                             required=True,
#                             help='This field is mandatory!')

#         data_payload = parser.parse_args()

#         cart = CartModel.retrieve_cart_by_user_id(data_payload['user_id'])

#         if (data_payload['type'] =='increment'):
#             cart.increment_product_amt(data_payload['product_id'])
            
#         if (data_payload['type'] =='decrement'):
#             cart.increment_product_amt(data_payload['product_id'])
        
#         return {'message': 'Cart Item Quanitity successfully updated in database!'}, 201


# class InventoryProductList(Resource):

#     def get(self):
#         products = InventoryModel.find_all_products();
#         if products:
#             return {'products': [product.json() for product in products]}, 200
#         else:
#             return {'message': 'No products found!'}, 404


# class Shopping(Resource):

#     def post(self):
#         parser = reqparse.RequestParser()

#         parser.add_argument('username',
#                             type=str,
#                             required=True,
#                             help='This field is mandatory!')

#         parser.add_argument('product',
#                             type=str,
#                             required=True,
#                             help='This field is mandatory!')

#         data_payload = parser.parse_args()

#         return ShoppingInventory.buy_product(data_payload['username'],
#                                          data_payload['product'])