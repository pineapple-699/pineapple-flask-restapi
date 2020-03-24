from models.user import UserModel
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
        # parser.add_argument('username',
        #                     type=str,
        #                     required=True,
        #                     help='This field is required!')

        # parser.add_argument('password',
        #                     type=str,
        #                     required=True,
        #                     help='This field is required!')
        
        # parser.add_argument('sex',
        #                     type=str,
        #                     required=True,
        #                     help='This field is required!')
        
        # parser.add_argument('shoe_size',
        #                     type=str,
        #                     required=True,
        #                     help='This field is required!')

        # parser.add_argument('pant_size_waist',
        #                     type=str,
        #                     required=True,
        #                     help='This field is required!')

        # parser.add_argument('pant_size_length',
        #                     type=str,
        #                     required=True,
        #                     help='This field is required!')
        
        # parser.add_argument('shirt_size',
        #                     type=str,
        #                     required=True,
        #                     help='This field is required!')

        data_payload = parser.parse_args()

        if UserModel.find_by_name(data_payload['username']):
            return {'message': 'User with the same name already exists in database!'}, 400
        else:
            arguments = ['username', 'password', 'sex', 'shoe_size', 'pant_size_waist', 'pant_size_length', 'shirt_size', 'shipping_address', 'billing_address']
    
            UserModel.insert_into_table(
                data_payload['username'], 
                data_payload['password'],
                data_payload['sex'],
                data_payload['shoe_size'],
                data_payload['pant_size_waist'],
                data_payload['pant_size_length'],
                data_payload['shirt_size'],
                data_payload['shipping_address'],
                data_payload['billing_address'])
            return {'message': 'User successfully added to the database!'}, 201