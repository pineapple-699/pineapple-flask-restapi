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
            UserModel.insert_into_table(data_payload['username'],
                                        data_payload['password'])
            return {'message': 'User successfully added to the database!'}, 201

class Address(Resource):
    def get(self, userid, shipping_address, billing_address):
        shipping_address = AddressModel.get_default_shipping(userid)
        billing_address = AddressModel.get_default_billing(userid)
        if shipping_address:
            return {
                'shipping_address': shipping_address.json()}, 200
        elif billing_address:
            return{
                'billing_address': billing_address.json()}, 200
        else:
            return {'message': 'Address not found!'}, 404

class ShippingRegister(Resource):
    def post(self):
        parser = reqparse.RequestParser()
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

        if AddressModel.get_default_shipping(data_payload['userid']):
            return {'message': 'User with the same address already exists in database!'}, 400
        else:
            AddressModel.insert_shipping(data_payload['userid'],
            data_payload['shipping_address'])
            return {'message': 'Shipping address successfully added to the database!'}, 201

class BillingRegister(Resource):
    def post(self):
        parser = reqparse.RequestParser()
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

        if AddressModel.get_default_billing(data_payload['userid']):
            return {'message': 'User with the same address already exists in database!'}, 400
        else:
            AddressModel.insert_billing(data_payload['userid'],
            data_payload['billing_address'])
            return {'message': 'Billing address successfully added to the database!'}, 201
