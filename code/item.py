import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

# GET /items
class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('mydata.db')
        cursor = connection.cursor()
        select_query = "SELECT * FROM items"
        result = cursor.execute(select_query)

        items = []
        for row in result:
            items.append({'name': row[0], 'price': row[1]})

        connection.close()
        return {'items': items}


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left!")

    # GET /item/<sting:name>
    @jwt_required()
    def get(self, name):
        item = self.find_by_name(name)
        if item is None:
            return {'message': "Item '{}' does not find".format(name)}
        return item

    # POST /item/<sting:name>
    def post(self, name):
        if self.find_by_name(name):
            return {'message': "Item name '{}' already exist".format(name)}

        post_data = Item.parser.parse_args()
        post_item = {'name': name, 'price': post_data['price']}
        try:
            self.insert_item(post_item)
        except:
            return {'message': "An error occurred inserting the item."}
        return post_item


    # PUT /item/<sting:name>
    def put(self, name):
        put_data = Item.parser.parse_args()

        check_item = self.find_by_name(name)
        put_item = {'name': name, 'price': put_data['price']}

        if check_item is None:
            try:
                self.insert_item(put_item)
            except:
                return {'message': "An error occurred inserting the item."}
        else:
            try:
                self.update_item(put_item)
            except:
                return {'message': "An error occurred updating the item."}
        return put_item


    # Delete /item/<string:name>
    def delete(self, name):
        connection = sqlite3.connect('mydata.db')
        cursor = connection.cursor()

        delete_query = "DELETE FROM items WHERE name=?"
        result = cursor.execute(delete_query, (name,))
        connection.commit()
        connection.close()

        if result:
            return {'message': "Item '{}' deleted".format(name)}
        return {'message': "Item '{}' not existed".format(name)}


    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('mydata.db')
        cursor = connection.cursor()

        select_table = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(select_table, (name,))
        row = result.fetchone()
        connection.close()
        if row:
            return {'name': row[0], 'price': row[1]}

    @classmethod
    def insert_item(cls, item):
        connection = sqlite3.connect('mydata.db')
        cursor = connection.cursor()

        insert_query = "INSERT INTO items VALUES (?,?)"
        cursor.execute(insert_query, (item['name'], item['price']))

        connection.commit()
        connection.close()

    @classmethod
    def update_item(cls,items):
        connection = sqlite3.connect('mydata.db')
        cursor = connection.cursor()

        update_query = "UPDATE items SET price=? where name=?"
        cursor.execute(update_query, (items['price'], items['name']))

        connection.commit()
        connection.close()



