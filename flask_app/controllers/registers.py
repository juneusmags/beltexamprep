from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.register import User
from flask_app.models.recipe import Recipe
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)






@app.route("/")
def index():
    return render_template("home.html")


@app.route("/register", methods = ["POST"])
def register():
    if not User.validate_register(request.form):
        return redirect("/")

    data = { 
        "email" : request.form["email"] 
    }
    user_in_db = User.get_by_email(data)
    if user_in_db:
        flash("Email already in use.")
        return redirect("/")
    


    hashed_pw = bcrypt.generate_password_hash(request.form["password"])

    data = {
        "first_name" : request.form["first_name"],
        "last_name" : request.form["last_name"],
        "email" : request.form["email"],
        "password" : hashed_pw
    }

    user_id =  User.register_user(data)

    session ['user_id'] = user_id
    
    return redirect("/dashboard")



@app.route('/login', methods=['POST'])
def login():
    # see if the username provided exists in the database
    data = { 
        "email" : request.form["email"] 
    }
    user_in_db = User.get_by_email(data)
    # user is not registered in the db
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        # if we get False after checking the password
        flash("Invalid Email/Password")
        return redirect('/')
    # if the passwords matched, we set the user_id into session
    session['user_id'] = user_in_db.id
    # never render on a post!!!
    return redirect("/dashboard")

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        flash("Please login or register before continuing on.")
        return redirect("/")
    mysql = connectToMySQL("beltprep")
    data = {
        "id" : session["user_id"]
    }
    user_in_session = User.one_user(data)
    
    recipe = Recipe.show_recipe(data)
    


    return render_template("dashboard.html", user = user_in_session, all_recipes = recipe)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")