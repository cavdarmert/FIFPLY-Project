from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from flask_app import bcrypt
from flask_app.models import model_post

from flask_app.models import model_message


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.fullname = f"{self.first_name} {self.last_name}"

    @classmethod
    def get_one_by_id_with_posts(cls, data):
        query = "SELECT * FROM users LEFT JOIN posts ON users.id = posts.user_id WHERE users.id = %(id)s;"
        results = connectToMySQL('postings_db').query_db(query,data)
        user = cls(results[0])
        list_posts = []

        if results:
            for row_from_db in results:
                post_data = {
                    **row_from_db,
                    'id': row_from_db['posts.id'],
                    'created_at': row_from_db['posts.created_at'],
                    'updated_at': row_from_db['posts.updated_at']
                }
                current_post = model_post.Post(post_data)
                list_posts.append(current_post)
            user.posts = list_posts
            return user

    @classmethod
    def get_one_by_id(cls, id):
        query = "SELECT * FROM users WHERE users.id = %(id)s;"
        data = {'id': id}
        result = connectToMySQL('postings_db').query_db(query,data)
        if result:
            user = cls(result[0])
            return user
        return False

    @classmethod  ## ---- ANY PROBLEMS HERE??
    def get_one_by_email(cls, email):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        data = {'email': email}
        result = connectToMySQL('postings_db').query_db(query,data)
        if not result:
            return result
        return cls(result[0])

    @classmethod
    def get_user_with_messages_recived(cls,data):
        query = "SELECT * FROM messages LEFT JOIN users AS sender ON messages.sender_id = sender.id RIGHT JOIN users AS	receiver ON messages.receiver_id = receiver.id WHERE receiver.id = %(id)s;"
        results = connectToMySQL("postings_db").query_db(query,data)
        print(results)
        messages = []
        if results:
            for row_from_db in results:
                message = model_message.Message(row_from_db)
                sender_data = {
                    "id" : row_from_db['sender.id'],
                    "first_name" : row_from_db['first_name'],
                    "last_name" : row_from_db['last_name'],
                    "email" : row_from_db['email'],
                    "password" : row_from_db['password'],
                    "created_at" : row_from_db['sender.created_at'],
                    "updated_at" : row_from_db['sender.updated_at']
                }
                message.sender = cls(sender_data)
                messages.append(message)
        return messages

    @classmethod
    def get_user_with_messages_sent(cls,data):
        query = "SELECT * FROM messages LEFT JOIN users AS sender ON messages.sender_id = sender.id RIGHT JOIN users AS	receiver ON messages.receiver_id = receiver.id WHERE sender.id = %(id)s;"
        results = connectToMySQL("postings_db").query_db(query,data)
        messages = []
        if results:
            for row_from_db in results:
                message = model_message.Message(row_from_db)
                receiver_data = {
                    "id" : row_from_db['receiver.id'],
                    "first_name" : row_from_db['receiver.first_name'],
                    "last_name" : row_from_db['receiver.last_name'],
                    "email" : row_from_db['receiver.email'],
                    "password" : row_from_db['receiver.password'],
                    "created_at" : row_from_db['receiver.created_at'],
                    "updated_at" : row_from_db['receiver.updated_at']
                }
                message.receiver = cls(receiver_data)
                messages.append(message)
        return messages


    @classmethod
    def new_user(cls,data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL('postings_db').query_db(query,data)

##NEW USER VALIDATIONS
    @staticmethod
    def is_valid(data):
        is_valid = True

        if len(data['first_name']) < 2:
            flash('First Name Must Be Minimum 2 Characters')
            is_valid = False

        if len(data['last_name']) < 2:
            flash('Last Name Must Be Minimum 2 Characters')
            is_valid = False

        if len(data['email']) < 1:
            flash('Email Cannot Be Empty')
            is_valid = False
        elif not EMAIL_REGEX.match(data['email']): 
            flash("Invalid Email Address!")
            is_valid = False
        else:
            potential_user = User.get_one_by_email(data['email'])

            if potential_user:
                flash("Email Already in Use!")
                is_valid = False

        if len(data['password']) < 8:
            flash('Password Name Must Be Minimum 8 Characters')
            is_valid = False

        if len(data['password2']) < 1:
            flash('Confirm Password is Required')
            is_valid = False
        if data['password'] != data['password2']:
            flash('Passwords do not Match!')
            is_valid = False

        return is_valid 