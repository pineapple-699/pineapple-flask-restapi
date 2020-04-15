from models.cart import CartModel
from flask_restful import Resource, reqparse


class Cart(Resource):

    def get(self, userid):
        cart = CartModel.retrieve_cart_by_user_id(userid)
        if cart:
            return {
                'cart': cart.json()
            }, 200
        else:
            return {'message': 'Cart not found!'}, 404
    
    def post(self, userid):
        parser = reqparse.RequestParser()

        parser.add_argument('product_upc',
                            type=int,
                            required=True,
                            help='This field is mandatory!')
        parser.add_argument('quantity',
                            type=int,
                            required=False,
                            help='This field is necessary only when adding product and updating product quantity.')
        parser.add_argument('new_size',
                            type=int,
                            required=False,
                            help='This field is necessary only when changing product size.')
        parser.add_argument('new_color',
                            type=int,
                            required=False,
                            help='This field is necessary only when changing product color.')
        parser.add_argument('type',
                            type=str,
                            required=True,
                            help='This field is mandatory!')

        data_payload = parser.parse_args()

        if data_payload['type'] == 'add_product_for_user':
            CartModel.add_product_for_user(userid,
                                data_payload['product_upc'],
                                data_payload['quantity'])
            return {'message': 'Product successfully added to database!'}, 201
        
        if data_payload['type'] == 'remove_product_for_user':
            CartModel.remove_product_for_user(userid,
                                data_payload['product_upc'])
            return {'message': 'Product successfully removed from database!'}, 201

        if data_payload['type'] == 'increment_product_amt_for_user':
            CartModel.increment_product_amt_for_user(userid,
                                data_payload['product_upc'])
            return {'message': 'Product amt successfully updated in database!'}, 201

        if data_payload['type'] == 'decrement_product_amt_for_user':
            CartModel.decrement_product_amt_for_user(userid,
                                data_payload['product_upc'])
            return {'message': 'Product amt successfully updated in database!'}, 201

        if data_payload['type'] == 'update_product_size_for_user':
            CartModel.update_product_size_for_user(userid,
                                data_payload['product_upc'],
                                data_payload['new_size'])
            return {'message': 'Product size successfully updated in database!'}, 201

        if data_payload['type'] == 'update_product_color_for_user':
            CartModel.update_product_color_for_user(userid,
                                data_payload['product_upc'],
                                data_payload['new_color'])
            return {'message': 'Product color successfully updated in database!'}, 201

        if data_payload['type'] == 'update_product_quantity_for_user':
            CartModel.update_product_quantity_for_user(userid,
                                data_payload['product_upc'],
                                data_payload['quantity'])
            return {'message': 'Product quantity successfully updated in database!'}, 201

        else:
            return {'message': 'Womp, you typed in the type wrong'}, 201   

