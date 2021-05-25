from flask_app import app
from flask import render_template,redirect,request,session,flash 
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.register import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)




@app.route("/create")
def create():
    return render_template("create.html")


@app.route("/createrecipe", methods = ["POST"])
def create_recipe():
    mysql = connectToMySQL("beltprep")
    query = "INSERT INTO recipes (name, description, instructions, under, users_id, created_at, updated_at) VALUES (%(name)s, %(desc)s, %(instruct)s, %(under)s, %(id)s, NOW(), NOW())"
    data = {
        "name" : request.form["name"],
        "desc" : request.form["description"],
        "instruct" : request.form["instructions"],
        "under" : request.form["under"],
        "id" : session ['user_id']
    }
    mysql.query_db(query, data)
    return redirect("/dashboard")


@app.route("/instructions/<id>")
def instructions(id):
    if "user_id" not in session:
        flash("Please login or register before continuing on.")
        return redirect("/")
    mysql = connectToMySQL("beltprep")
    query = "SELECT * FROM recipes WHERE id=%(id)s;"
    data ={
        "id" : int(id)
    }
    recipe = mysql.query_db(query,data)
    return render_template("instructions.html", recipe = recipe)


@app.route("/edit/<id>")
def edit(id):
    if "user_id" not in session:
        flash("Please login or register before continuing on.")
        return redirect("/")
    mysql = connectToMySQL("beltprep")
    query = "SELECT * FROM recipes WHERE id=%(id)s;"
    data = {
        "id" : int(id)
    }
    recipe = mysql.query_db(query,data)
    return render_template("edit.html", recipe = recipe[0])


@app.route("/update/<id>", methods = ["POST"])
def update(id):
    mysql = connectToMySQL('beltprep')
    query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, under = %(under)s WHERE id = %(id)s;"
    data = {
        "name" : request.form['name'],
        "description" : request.form['description'],
        "instructions" : request.form['instructions'],
        "under" : request.form['under'],
        "id" : int(id)
    }
    mysql.query_db(query, data)
    return redirect("/dashboard")


@app.route ("/delete/<id>")
def delete(id):
    if "user_id" not in session:
        flash("Please login or register before continuing on.")
        return redirect("/")
    mysql = connectToMySQL('beltprep')
    query = "DELETE FROM recipes WHERE id = %(id)s"
    data = {
        "id" : int(id)
    }
    mysql.query_db(query,data)
    return redirect("/dashboard")