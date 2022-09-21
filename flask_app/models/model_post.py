from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from flask_app import bcrypt
from flask_app.models import model_user

from flask_app.models import model_message


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class Post:
    def __init__( self , data ):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.type = data['type']
        self.date = data['date']
        self.street = data['street']
        self.city = data['city']
        self.state = data['state']
        self.zip = data['zip']
        self.image = data['image']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM posts JOIN users on users.id = user_id;"
        result = connectToMySQL('postings_db').query_db(query)
        posts = []

        if result:
            for row_from_db in result:
                current_post = cls(row_from_db)
                user_data = {
                    **row_from_db,
                    'id': row_from_db['users.id'],
                    'created_at': row_from_db['users.created_at'],
                    'updated_at': row_from_db['users.updated_at']
                }
                posts_user = model_user.User(user_data)
                current_post.owner = posts_user
                posts.append(current_post)
        return posts
    
    @classmethod
    def get_one_by_id(cls,data):
        query = "SELECT * FROM posts JOIN users on users.id = posts.user_id WHERE posts.id = %(id)s;"

        result = connectToMySQL('postings_db').query_db(query,data)
        post = cls(result[0])
        row_from_db = result[0]

        user_data = {
            **row_from_db,
            'id': row_from_db['users.id'],
            'created_at': row_from_db['users.created_at'],
            'updated_at': row_from_db['users.updated_at']
        }
        owner = model_user.User(user_data)
        post.owner = owner
        return post

    @classmethod
    def delete_by_id(cls, data):
        query = "DELETE FROM posts WHERE id = %(id)s;"
        return connectToMySQL('postings_db').query_db(query,data)

    @classmethod
    def save(cls,data):
        query = "INSERT INTO posts (title, description, type, date, street, city, state, zip, user_id) VALUES (%(title)s, %(description)s, %(type)s, %(date)s, %(street)s, %(city)s, %(state)s, %(zip)s, %(image)s, %(user_id)s);"
        return connectToMySQL('postings_db').query_db(query,data)

    @classmethod
    def update(cls,data):
        query = "UPDATE posts SET title = %(title)s, description = %(description)s, type = %(type)s, date = %(date)s, street = %(street)s, city = %(city)s, state = %(state)s, zip = %(zip)s, image = %(image)s WHERE id = %(id)s;"
        return connectToMySQL('postings_db').query_db(query,data)

    @staticmethod
    #data is request.form
    def is_valid(data):
        is_valid = True

        if len(data['title']) < 3:
            flash('Title Must Be Minimum 3 characters')
            is_valid = False
        if len(data['description']) < 5:
            flash('Description Must Be Minimum 5 characters')
            is_valid = False

        if len(data['type']) < 1:
            flash('Type is Required')
            is_valid = False
        if len(data['date']) < 1:
            flash('Date is Required')
            is_valid = False
        if len(data['street']) < 8:
            flash('Street Must Be Minimum 8 characters')
            is_valid = False
        if len(data['city']) < 2:
            flash('City Info is Required')
            is_valid = False
        if len(data['state']) < 1:
            flash('State is Required')
            is_valid = False
        if len(data['image']) < 15:
            flash('Image URL is Required')
            is_valid = False
        if len(str(data['zip'])) <5:
            flash('5 Digit ZIP is Required')
            is_valid = False

        return is_valid 