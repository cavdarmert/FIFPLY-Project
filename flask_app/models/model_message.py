from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from flask_app import bcrypt
from flask_app.models import model_user
from flask_app.models import model_post

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class Message:
    def __init__( self , data ):
        self.id = data['id']
        self.message_title = data['message_title']
        self.content = data['content']
        self.is_read = data['is_read']
        self.receiver_id = data['receiver_id']
        self.sender_id = data['sender_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all_messages(cls):
        query = "SELECT * FROM messages JOIN users on users.id = sender_id;"
        # query = "SELECT users.id as sender_id, users.id as receiver_id, messages.* FROM users LEFT JOIN messages ON users.id = messages.sender_id LEFT JOIN users as  ON users.id = messages.receiver_id WHERE users.id =  %(id)s"
        result = connectToMySQL('postings_db').query_db(query)
        messages = []

        if result:
            for row_from_db in result:
                current_message = cls(row_from_db)
                user_data = {
                    **row_from_db,
                    'id': row_from_db['users.id'],
                    'created_at': row_from_db['users.created_at'],
                    'updated_at': row_from_db['users.updated_at']
                }
                messages_user = model_user.User(user_data)
                current_message.owner = messages_user
                messages.append(current_message)
        return messages
    
    @classmethod
    def get_one_message_by_id(cls,data):
        query = "SELECT * FROM messages JOIN users on users.id = messages.sender_id WHERE messages.id = %(id)s;"

        result = connectToMySQL('postings_db').query_db(query,data)
        if not result:
            return False
        message = cls(result[0])
        row_from_db = result[0]

        user_data = {
            **row_from_db,
            'id': row_from_db['users.id'],
            'created_at': row_from_db['users.created_at'],
            'updated_at': row_from_db['users.updated_at']
        }
        owner = model_user.User(user_data)
        message.owner = owner
        return message

    # LET'S DON'T DELETE MESSAGES FOR NOW
    # @classmethod
    # ##TO DELETE A MESSAGE IF WE'RE THE SENDER
    # def delete_message_by_sender_id(cls, data):
    #     query = "DELETE FROM messages WHERE id = %(id)s;"
    #     return connectToMySQL('postings_db').query_db(query,data)

    # @classmethod
    # ##TO DELETE A MESSAGE IF WE'RE THE RECEIVER
    # def delete_message_by_receiver_id(cls, data):
    #     query = "DELETE FROM messages WHERE id = %(id)s;"
    #     return connectToMySQL('postings_db').query_db(query,data)

    @classmethod
    def save_message(cls,data):
        query = "INSERT INTO messages (message_title, content, sender_id, receiver_id) VALUES (%(message_title)s, %(content)s, %(sender_id)s, %(receiver_id)s);"
        return connectToMySQL('postings_db').query_db(query,data)

    # INSERT INTO messages (message_title, content, sender_id, receiver_id) VALUES ("tittle here", "content here", 3, 3);


    @staticmethod
    #data is request.form
    def is_valid(data):
        is_valid = True

        if len(data['message_title']) < 5:
            flash('Message Title Must Be Minimum 5 characters')
            is_valid = False
        if len(data['content']) < 5:
            flash('Message Content Must Be Minimum 5 characters')
            is_valid = False

        return is_valid 