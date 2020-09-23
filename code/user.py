import sqlite3
from flask_restful import Resource, reqparse

class User():
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    # User class is using so, make @classmethod
    @classmethod
    def find_by_name(cls, username):
        connection = sqlite3.connect('mydata.db')
        cursor = connection.cursor()

        select_query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(select_query, (username,))
        row = result.fetchone()

        if row:
            # user = (row[0], row[1], row[2])
            user = cls(*row)  # passing parameter
        else:
            user = None
        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('mydata.db')
        cursor = connection.cursor()

        select_query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(select_query, (_id,))
        row = result.fetchone()
        if row:
            user_id = cls(*row)
        else:
            user_id = None
        connection.close()
        return user_id


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help="This field cannot be left!")
    parser.add_argument('password', type=str, required=True, help="This field cannot be left!")

    def post(self):
        data = UserRegister.parser.parse_args()
        if (User.find_by_name(data['username'])) is not None:
            return {'message': "This username '{}' already existed".format(data['username'])}

        connection = sqlite3.connect('mydata.db')
        cursor = connection.cursor()

        insert_table = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(insert_table, (data['username'], data['password'],))

        connection.commit()
        connection.close()
        return {'message': 'User successfully registered.'}
