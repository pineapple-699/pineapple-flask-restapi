from models.scan_history import ScanHistoryModel
from flask_restful import Resource, reqparse


class ScanHistory(Resource):

    def get(self, user_id):
        list_of_scannedproducts = ScanHistoryModel.find_scanhistory_product_by_userid(user_id)
        if list_of_scannedproducts:
            return {
                'scan_history': [product.json() for product in list_of_scannedproducts]
            }, 200
        else:
            return {
                'message': 'Users scanned products not found in database!'
            }, 404

class ScanHistoryRegister(Resource):

    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('upc',
                            type=int,
                            required=True,
                            help='This UPC field is mandatory!')

        parser.add_argument('user_id',
                            type=int,
                            required=True,
                            help='This User ID field is mandatory!')

        data_payload = parser.parse_args()

        scannedproduct = ScanHistoryModel.add_scanned_product_by_userid(data_payload['upc'],data_payload['user_id'])

        if scannedproduct:
            return {'message': 'Scanned product already in database!'}

        ScanHistoryModel.add_scanned_product_by_userid(data_payload['upc'],
                                data_payload['user_id'])

        return {'message': 'Scanned Product successfully added to database!'}, 201