import sqlite3


class UserModel:

    def __init__(self, id, username, password, address, sex, shoe_size, shirt_size,pant_size_waist, pant_size_length):
        self.id = id
        self.username = username
        self.password = password
        self.address = address
        self.sex = sex
        self.shoe_size = shoe_size
        self.shirt_size = shirt_size
        self.pant_size_waist = pant_size_waist
        self.pant_size_length = pant_size_length


    @classmethod
    def find_by_name(cls, name, db_path='./db/pineapplestore.db'):
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        query = 'SELECT * FROM user WHERE username=?;'
        result = cursor.execute(query, (name,))
        rows = result.fetchall()
        if rows:
            for row in rows:
                user = UserModel(row[0], row[1], row[2],row[3], row[4], row[5], row[6], row[7], row[8])
            connection.close()
            return user


    @classmethod
    def find_by_id(cls, id, db_path='./db/pineapplestore.db'):
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        query = 'SELECT * FROM user WHERE id=?'
        result = cursor.execute(query, (id,))
        rows = result.fetchall()
        if rows:
            for row in rows:
                user = UserModel(row[0], row[1], row[2],row[3], row[4], row[5], row[6], row[7], row[8])
            connection.close()
            return user

    @classmethod
    def insert_into_table(cls, username, password, db_path='./db/pineapplestore.db'):
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        query = 'INSERT INTO user VALUES(NULL, ?, ?,NULL,NULL,NULL,NULL,NULL,NULL)'
        cursor.execute(query, (username, password))
        connection.commit()
        connection.close()

    @classmethod
    def find_all(cls, db_path='./db/pineapplestore.db'):
        users = list()
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        query = 'SELECT * FROM user;'
        result = cursor.execute(query)
        rows = result.fetchall()
        if rows:
            for row in rows:
                users.append(UserModel(row[0], row[1], row[2],row[3], row[4], row[5], row[6], row[7], row[8]))
            return users
        connection.close()

    @classmethod
    def delete_user(self, name, db_path='./db/pineapplestore.db'):
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        user_id_query_for_purchase_his = 'SELECT id FROM user WHERE username=?;'
        user_id = cursor.execute(user_id_query_for_purchase_his, (name,))
        result_user_id = str(user_id.fetchone()[0])

        purchase_history_deletion = 'DELETE FROM purchase_history WHERE user_id=?;'
        delete_user_history = cursor.execute(purchase_history_deletion, (result_user_id))

        user_to_delete = 'DELETE FROM user WHERE username=?;'
        delete_user = cursor.execute(user_to_delete, (name,))
        connection.commit()
        connection.close()

    def json(self):
        return {
            'id': self.id,
            'username': self.username,
            'address': self.address,
            'sex': self.sex,
            'shoe_size': self.shoe_size,
            'shirt_size': self.shirt_size,
            'pant_size_waist': self.pant_size_waist,
            'pant_size_length': self.pant_size_length 
            # 'password': self.password
        }