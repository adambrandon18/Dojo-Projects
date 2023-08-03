from flask import render_template,redirect,session,request,flash
from flask_app import app
from flask_app.models.recipes_model import Recipe #importing recipe class
from flask_app.models.users_model import User #importing User class
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)  #importinf bcrypt and making a instance and passing in app

@app.route('/start')
def start():
    return render_template('users.html')


#...............................................................................................
@app.route('/login', methods =['POST'])
def login():
    data = {
        "email": request.form['email']
    }
    user = User.get_by_email(data)
    if not user:
        flash("Wrong Login Information!!!!!!!!", "Login" ) 
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid login information, Sorry")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/user_dashboard')
#...................................................................................................

@app.route('/user_dashboard')
def user_dashboard():
    if not 'user_id' in session: #they nave no buiness in the login if their are not insession/active user 
        return redirect('/logout') #redirects to logout and clears the ession in the logout
    data ={
        'id': session['user_id'] #we are retrieving the info with the session id
    }
    print("Logging in")
    return render_template("user_dashboard.html", recipes = Recipe.get_all_w_users(), user = User.get_by_id(data)) 

#the extras code in the parenthesis are simlpy things we are passing over to our html so we can access it there.
#we do not need to pass anything into the parenthesis since we are calling everything and not one specific instance

#.........................................................................................

@app.route('/logout')
def logout():
    session.clear()  #ends the user info and stops and prevents unwanted eyes on provate information
    return redirect('/start')

#.........................................................................................................

#@app.route('/registration',methods=['POST'])
#def registration():

#    if not User.validate_register(request.form):  #is_valid was not defined so i have to use validate_register
#        return redirect('/start')
#    data ={                 #creation of our user object
#        "first_name": request.form['first_name'],
#        "last_name": request.form['last_name'],
#        "email": request.form['email'],
#        "password": bcrypt.generate_password_hash(request.form['password'])
#    }
#    id = User.save(data)  #here we are saving the user object we just created on the line above
#    session['user_id'] = id # put into session because on the dashboard page we wanna make sure they are in session

#    return redirect('/user_dashboard') #once redirected to the dashboard session should be active and our user should be logged in