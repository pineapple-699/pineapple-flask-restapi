import sqlite3
from models.user import UserModel
from models.inventory import InventoryModel


class ScanHistoryModel:

    db_path = './db/pineapplestore.db'

    def __init__(self, id, upc, user_id):
        self.id = id
        self.upc = upc
        self.user_id = user_id

    @classmethod
    def add_scanned_product_by_userid(self, upc, user_id):
        connection = sqlite3.connect('./db/pineapplestore.db')
        cursor = connection.cursor()
        query = 'INSERT INTO scan_history VALUES(NULL, ?, ?);'
        cursor.execute(query, (upc, user_id,))
        connection.commit()
        connection.close()
        
    @classmethod
    def find_scanhistory_product_by_userid(cls, user_id):

        scanhistory_products = list()

        connection = sqlite3.connect(cls.db_path)
        cursor = connection.cursor()
        query = 'SELECT * FROM scan_history WHERE user_id=?;'
        results = cursor.execute(query, (user_id))
        rows = results.fetchall()

        if rows:
            for row in rows:
                scannedproduct = ScanHistoryModel(row[0], row[1], row[2])
                
                product_query = 'SELECT * FROM inventory WHERE upc=?;'
                product_results = cursor.execute(product_query, (scannedproduct.upc,))
                product_rows = product_results.fetchall()

                # if product_rows:
                #     for row in product_rows:
                #         print(row)
                #         product = InventoryModel(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9],row[10], row[11])
                #         scannedproduct.append(product)

                scanhistory_products.append(scannedproduct)

            connection.close()

            return scanhistory_products


    def json(self):
        return {
            'scanned product id': self.id,
            'scanned product upc': self.upc,
            'scanned product user id': self.user_id
        }