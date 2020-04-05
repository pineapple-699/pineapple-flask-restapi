from models.inventory import InventoryModel, ShoppingInventory
from flask_restful import Resource, reqparse


class Inventory(Resource):

    def get(self, product):
        products = InventoryModel.find_by_product(product)
        if products:
            return {
                'product': [product.json() for product in products]
            }, 200
        else:
            return {'message': 'Product not found!'}, 404

    def post(self, product):
        product = InventoryModel.find_by_product(product)
        if product:
            return {'message': 'Product already in database!'}
        else:
            parser = reqparse.RequestParser()
            parser.add_argument('product',
                                type=str,
                                required=True,
                                help='This field is mandatory!')
            parser.add_argument('price',
                                type=float,
                                required=True,
                                help='This field is mandatory!')

            data_payload = parser.parse_args()

            InventoryModel.add_product(data_payload['product'],
                                    data_payload['price'])
            return {'message': 'Product successfully added to database!'}, 201

class InventoryProductList(Resource):

    def get(self):
        products = InventoryModel.find_all_products()
        if products:
            return {'products': [product.json() for product in products]}, 200
        else:
            return {'message': 'No products found!'}, 404


class Shopping(Resource):

    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('username',
                            type=str,
                            required=True,
                            help='This field is mandatory!')

        parser.add_argument('product',
                            type=str,
                            required=True,
                            help='This field is mandatory!')

        data_payload = parser.parse_args()

        return ShoppingInventory.buy_product(data_payload['username'],
                                         data_payload['product'])