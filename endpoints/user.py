from models.user import UserModel, AddressModel
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required


class User(Resource):

    @jwt_required()
    def get(self, name):
        users = UserModel.find_by_name(name)
        if users:
            return {'user': users.json()}, 200
        return {'message': 'User not found!'}, 404

    def delete(self, name):
        user_to_delete = UserModel.delete_user(name)
        return {'message': 'User {0} was successfully deleted from database!'.format(name)}

class UserList(Resource):

    def get(self):
        users = UserModel.find_all()
        if users:
            return {'users': [user.json() for user in users]}, 200
        return {'message': 'No users found!'}, 404

class UserRegister(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        arguments = ['username', 'password', 'sex', 'shoe_size', 'pant_size_waist', 'pant_size_length', 'shirt_size', 'shipping_address', 'billing_address']
        for i in arguments:
            parser.add_argument(i,
                type=str,
                required=True,
                help='This field is required!')

        data_payload = parser.parse_args()

        if UserModel.find_by_name(data_payload['username']):
            return {'message': 'User with the same name already exists in database!'}, 400
        else:
            for n in arguments:
                UserModel.insert_into_table(data_payload[n])
            return {'message': 'User successfully added to the database!'}, 201
            # UserModel.insert_into_table(data_payload['username'],
            #                             data_payload['password'],
            #                             data_payload['sex'])
            # return {'message': 'User successfully added to the database!'}, 201

class ShippingAddress(Resource):
    def get(self, user_id):
        shipping_address = AddressModel.retrieve_user_billing_address_by_id(user_id)
        if shipping_address:
            return {
                'shipping_address': shipping_address.json()}, 200
        else:
            return {'message': 'Shipping address not found!'}, 404

class BillingAddress(Resource):
    def get(self, user_id):
        billing_address = AddressModel.retrieve_user_billing_address_by_id(user_id)
        if billing_address:
            return {
                'billing_address': billing_address.json()}, 200
        else:
            return {'message': 'Shipping address not found!'}, 404

class ShippingRegister(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id',
                            type=str,
                            required=True,
                            help='This field is required!')
        parser.add_argument('full_name',
                            type=str,
                            required=True,
                            help='This field is required!')
        parser.add_argument('address1',
                            type=str,
                            required=True,
                            help='This field is required!')
        parser.add_argument('address2',
                            type=str,
                            required=False)
        parser.add_argument('city',
                            type=str,
                            required=True,
                            help='This field is required!')
        parser.add_argument('state',
                            type=str,
                            required=True,
                            help='This field is required!')
        parser.add_argument('zipcode',
                            type=str,
                            required=True,
                            help='This field is required!')

        data_payload = parser.parse_args()

        AddressModel.insert_user_shipping_address(data_payload['user_id'],
                                                data_payload['full_name'],
                                                data_payload['address1'],
                                                data_payload['address2'],
                                                data_payload['city'],
                                                data_payload['state'],
                                                data_payload['zipcode'])
        return {'message': 'Shipping address successfully added to the database!'}, 201

class BillingRegister(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id',
                            type=str,
                            required=True,
                            help='This field is required!')
        parser.add_argument('full_name',
                            type=str,
                            required=True,
                            help='This field is required!')
        parser.add_argument('address1',
                            type=str,
                            required=True,
                            help='This field is required!')
        parser.add_argument('address2',
                            type=str,
                            required=False)
        parser.add_argument('city',
                            type=str,
                            required=True,
                            help='This field is required!')
        parser.add_argument('state',
                            type=str,
                            required=True,
                            help='This field is required!')
        parser.add_argument('zipcode',
                            type=str,
                            required=True,
                            help='This field is required!')

        data_payload = parser.parse_args()

        AddressModel.insert_user_billing_address(data_payload['user_id'],
                                                data_payload['full_name'],
                                                data_payload['address1'],
                                                data_payload['address2'],
                                                data_payload['city'],
                                                data_payload['state'],
                                                data_payload['zipcode'])
        return {'message': 'Billing address successfully added to the database!'}, 201
