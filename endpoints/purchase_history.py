from models.purchase_history import PurchaseHistoryModel
from flask_restful import Resource, reqparse


class PurchaseHistory(Resource):

    def get(self, user_id):
        # list_of_products = PurchaseHistoryModel.find_products_related_with_user_name(name)
        list_of_products = PurchaseHistoryModel.find_history_product_by_userId(user_id)
        if list_of_products:
            return {
            'purchase_history': [product.json() for product in list_of_products]
            }, 200
        else:
            return {
            'message': 'User and purchased products not found in database!'
            }, 404

    def post(self, user_id):
        parser = reqparse.RequestParser()
        parser.add_argument('product_id',
                            type=str,
                            required=True,
                            help='This field is mandatory!')

        data_payload = parser.parse_args()

        PurchaseHistoryModel.add_purchase(user_id,
                                data_payload['product_id'])
        return {'message': 'Purchase successfully added to database!'}, 201