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
    
    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('user_id',
                            type=int,
                            required=True,
                            help='This field is mandatory!')
        parser.add_argument('product_upc',
                            type=str,
                            required=True,
                            help='This field is mandatory!')
        parser.add_argument('quantity',
                            type=int,
                            required=True,
                            help='This field is mandatory!')
        parser.add_argument('type',
                            type=str,
                            required=True,
                            help='This field is mandatory!')

        data_payload = parser.parse_args()

        if data_payload['type'] == 'add_product_for_user':
            CartModel.add_product_for_user(data_payload['user_id'],
                                data_payload['product_upc'],
                                data_payload['quantity'])
            return {'message': 'Product successfully added to database!'}, 201
        
        if data_payload['type'] == 'remove_product_for_user':
            CartModel.remove_product_for_user(data_payload['user_id'],
                                data_payload['product_upc'],
                                data_payload['quantity'])
            return {'message': 'Product successfully removed from database!'}, 201
        if data_payload['type'] == 'increment_product_amt_for_user':
            CartModel.increment_product_amt_for_user(data_payload['user_id'],
                                data_payload['product_upc'],
                                data_payload['quantity'])
            return {'message': 'Product successfully updated in database!'}, 201
        if data_payload['type'] == 'decrement_product_amt_for_user':
            CartModel.decrement_product_amt_for_user(data_payload['user_id'],
                                data_payload['product_upc'],
                                data_payload['quanity'])
            return {'message': 'Product successfully updated in database!'}, 201

        else:
            return {'message': 'Womp, you typed in the type wrong'}, 201        