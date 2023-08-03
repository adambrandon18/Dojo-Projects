from flask_app.config.mysqlconnection import connectToMySQL
import pprint, re
from flask_app.models import users_model
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
#THE CODE ABOVE HAS A METHOD REFERRED TO AS MATCH THAT WILL RETURN NONE IF THEIR IS NO MATCH LOCATED
from flask import flash

db = "recipes_schema"

class Recipe:
    db ="recipes_schema"
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.under_30 = data['under_30']
        self.date = data['date']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.chef = None #where we will store the one making it (user we are creating from the dictionary)
        
#...........................................................................................
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes;"
        results = connectToMySQL(cls.db).query_db(query)
        print(results)
        recipes = []
        for r in results:
            recipes.append( cls(r) )
        return recipes

    #........................................................................................
    
    @classmethod
    def save(cls, data):
        query = "INSERT INTO recipes (name,description, instructions, under_30, date, user_id) VALUES (%(name)s,%(description)s, %(instructions)s, %(under_30)s, %(date)s, %(user_id)s);"

        # comes back as the new row id
        result = connectToMySQL(cls.db).query_db(query,data) #should return the interger which id database row and should be put into session
        return result
    
    #........................................................................................
    @classmethod
    def update(cls, data):
        query = "UPDATE recipes SET  name = %(name)s, description = %(description)s, instructions = %(instructions)s, under_30 = %(under_30)s, date = %(date)s, user_id = %(user_id)s WHERE id = %(id)s;"
        result = connectToMySQL(cls.db).query_db(query,data)
        return result
    

    #....................................................................................
    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls(results[0])
    
    #...........................................................................................
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM recipes WHERE id = %(id)s";
        result = connectToMySQL(cls.db).query_db(query,data)
        return cls(result[0])
    #..............................................................................................
    
    
    @classmethod
    def get_one_recipe_w_user(cls, data):
        query = "SELECT * FROM recipes LEFT JOIN users ON recipes.user_id = users.id WHERE recipes.id = %(id)s"
        result = connectToMySQL(db).query_db(query, data)
        single_recipe = cls(result[0])
        
        for row in result:
            user_data = {
                "id": row["users.id"],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": row['password'],
                "created_at": row['created_at'],
                "updated_at": row['updated_at']
            }
   
   
        single_recipe.chef = users_model.User(user_data)
        print('single_recipe', single_recipe)
        return single_recipe
    
    
   
   
   
    #@staticmethod
    #def validate_recipe(recipe):
    #    is_valid = True
    #    query = "SELECT * FROM recipes WHERE email = %(email)s;"
    #    results = connectToMySQL("recipes_schema").query_db(query,recipe)
            
    #    if len(recipe['name']) < 3:
    #        flash("name must be at least 3 characters","recipe")
    #        is_valid = False
    #    if len(recipe['description']) < 3:
    #        flash("description must be at least 3 characters long","recipe")
    #        is_valid = False
    #    if len(recipe['instructions']) < 3:
    #        flash("Instructions needs to be atleast 3 characters!!!!","register")
    #        is_valid = False


    #................................................................................    
    @classmethod
    def get_all_w_users(cls): #no need to insert data specifically since its literally grabbing everything
        query = "SELECT * FROM recipes LEFT JOIN users ON recipes.user_id = users.id" 
        result = connectToMySQL(db).query_db(query)
        recipes = []  #this is the new list that we want to return with a list of recipe classes
        for row in result: #row variable(called row by how we get back data in row form) We must loop through a list to extract information 
            new_recipe = cls(row) #we want to create a class from the recipe data from the first dictionary(row), row will also represent second dictionary
            user_data = {
                "id": row["users.id"],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": row['password'],
                "created_at": row['created_at'],
                "updated_at": row['updated_at']
            }
            new_recipe.chef = users_model.User(user_data) 
            recipes.append(new_recipe)
        return recipes


    @classmethod
    def delete(cls, data):
        #print("data", type(data['id']))
        query  = "DELETE FROM recipes WHERE id = %(id)s"
        #data = {'id': data['id']}
        result = connectToMySQL(cls.db).query_db(query, data)
        print("result", result)
        return result