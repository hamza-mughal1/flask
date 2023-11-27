# Importing flask
from sqlalchemy.exc import IntegrityError
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

# """ initializing flask app """
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:hamza-100@localhost/website_email'
db = SQLAlchemy(app)

class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False)
    age = db.Column(db.Integer)
    email = db.Column(db.String(120), unique=False)
    phone = db.Column(db.String(120), unique=False)
    request = db.Column(db.String(120), unique=False)


@app.route("/email",methods = ["GET","POST"])
def email_submit():
    if request.method == 'POST':
        name = request.form.get("name")
        age = request.form.get("age")
        mail = request.form.get("email")
        phone = request.form.get("phone")
        user_request = request.form.get("request")

        entry = Email(name = name, age = age, email = mail, phone = phone, request = user_request)
        try:
            db.session.add(entry)
            db.session.commit()    
        except IntegrityError:
            return "invalid perameters"
        
    return render_template("index.html")


""" Home page """
@app.route("/")
def home():
    return render_template("index.html")

""" About page """
@app.route("/about")
def about():
    return render_template("about.html")

""" Work page """
@app.route("/work")
def work():
    return render_template("work.html")

""" Category page """
@app.route("/category")
def category():
    return render_template("category.html")

""" starting flask app with debuging enable """
app.run(debug=True)