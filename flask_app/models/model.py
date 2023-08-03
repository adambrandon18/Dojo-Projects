from flask_app.config.mysqlconnection import connectToMySQL
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
#THE CODE ABOVE HAS A METHOD REFERRED TO AS MATCH THAT WILL RETURN NONE IF THEIR IS NO MATCH LOCATED
from flask import flash

class User:
    db ="recipes_schema"
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db).query_db(query)
        print(results)
        users = []
        for u in results:
            users.append( cls(u) )
        return users

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name,last_name,email, password) VALUES (%(first_name)s,%(last_name)s,%(email)s, %(password)s);"

        # comes back as the new row id
        result = connectToMySQL(cls.db).query_db(query,data) #should return the interger which id database row and should be put into session
        return result
    
   # @staticmethod
    #def validate_email(information):
     #   is_valid = True 
     #   if information['password']  
     #   if len(information['email']) <= 0:
     #       flash("Field cannot be left blank", "Login")
     #       is_valid = False   
     #   return is_valid 
    
    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls(results[0])
    
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        print(results)
        if len(results) < 1:
            print(results)
            return False
        return cls(results[0])
    
    @staticmethod
    def validate_register(data):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(User.db).query_db(query,data)
        if len(results) >= 1:
            flash("Email already taken.","register")
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid Email!!!","register")
            is_valid = False
        if len(data['first_name']) < 3:
            flash("First name must be at least 3 characters","register")
            is_valid = False
        if len(data['last_name']) < 3:
            flash("Last name must be at least 3 characters","register")
            is_valid = False
        if len(data['password']) < 8:
            flash("Password must be at least 8 characters","register")
            is_valid = False
        if data['password']  != data['comfirm']:
            flash("Please make sure your passwords match!! ","register")
            is_valid = False
        return is_valid