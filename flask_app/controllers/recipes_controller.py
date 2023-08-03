from flask import render_template,redirect,session,request,flash
from flask_app import app
from flask_app.models import users_model, recipes_model

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)  #importinf bcrypt and making a instance and passing in app

@app.route('/')
def index():
    return render_template('users.html')

#@app.route('/_login', methods =['POST'])
#def _login():
#    data = {
#        "email": request.form['email']
#    }
#    user = users_model.User.get_by_email(data)
#    if not user:
#        flash("Wrong Login Information!!!!!!!!", "Login" ) 
#        return redirect('/')
#    if not bcrypt.check_password_hash(user.password, request.form['password']):
#        flash("Invalid login information, Sorry")
#        return redirect('/')
#    session['user_id'] = user.id
#    return redirect('/user_dashboard')



#@app.route('/user_dashboard')
#def user_dashboard():
#    if not 'user_id' in session: #they nave no buiness in the login if their are not insession/active user
#        print("user not logged in")
#        return redirect('/logout') #redirects to logout and clears the ession in the logout
#    data ={
#        'id': session['user_id'] #we are retrieving the info with the session id
#    }
#    print("Logging in")
#    return render_template("user_dashboard.html",user=users_model.User.get_by_id(data))

@app.route('/registration',methods=['POST'])    #user controller
def registration():

    if not users_model.User.validate_register(request.form):  #is_valid was not defined so i have to use validate_register
        return redirect('/')
    data ={                 #creation of our user object
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = users_model.User.save(data)  #here we are saving the user object we just created on the line above
    session['user_id'] = id # put into session because on the dashboard page we wanna make sure they are in session

    return redirect('/user_dashboard') #once redirected to the dashboard session should be active and our user should be logged in


@app.route('/recipe/new')  #route the create recipe button uses to get to create recipe page
def new():
    return render_template("new_recipe.html")

@app.route('/recipe/create',methods=['POST'])
def create():
    print(request.form)
    recipes_model.Recipe.save(request.form)
    return redirect('/user_dashboard')

@app.route('/recipe/edit/<int:id>')   #recipe id
def edit(id):
    data ={
        "id":id
    }
    return render_template("edit_recipe.html", recipe=recipes_model.Recipe.get_one_recipe_w_user(data))

@app.route('/recipe/update',methods=['POST'])
def update():
    print(request.form)
    recipes_model.Recipe.update(request.form)
    return redirect('/user_dashboard')

@app.route('/recipe/show/<int:id>')
def show(id):
    data ={ 
        "id":id
    }
    return render_template("show_recipe.html",recipe=recipes_model.Recipe.get_one_recipe_w_user(data))



@app.route('/recipe/delete/<int:id>')
def delete(id):
    data ={
        'id': id
    }
    print("data controller", data)
    recipes_model.Recipe.delete(data)
    return redirect('/user_dashboard')