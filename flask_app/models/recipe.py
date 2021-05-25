from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')



class Recipe:  
    def __init__(self,data):
        self.id = data["id"]
        self.name = data["name"]
        self.description = data["description"]
        self.instructions = data["instructions"]
        self.under = data["under"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.users_id = data["users_id"]



    @classmethod
    def show_recipe(cls,data):
        query ="SELECT * FROM recipes WHERE users_id = %(id)s"
        recipe = connectToMySQL("beltprep").query_db(query,data)
        return (recipe)

    @classmethod
    def show_instructions(cls,data):
        query = "SELECT * FROM recipes WHERE id=%(id)s;"

        recipe = connectToMySQL("beltprep").query_db(query,data)