from flask import Flask, render_template, request, redirect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from datetime import date



app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:hamza-100@localhost/blog_db"


Base = declarative_base()

class Blogs(Base):

    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True)
    author_name = Column(String(120), unique=False)
    title = Column(String(120), unique=False)
    content = Column(String(120), unique=False)
    upload_date = Column(String(120), unique=False)



@app.route("/")
def home():
    engine = sqlalchemy.create_engine("mysql+mysqlconnector://root:hamza-100@localhost/blog_db")
    Session = sessionmaker(bind=engine)
    session = Session()
    blogs = session.query(Blogs).all()
    return render_template("index.html",blogs=blogs)


@app.route("/blog/<string:id>",methods=["GET"])
def get_blog(id,search_by=None):
        engine = sqlalchemy.create_engine("mysql+mysqlconnector://root:hamza-100@localhost/blog_db")
        Session = sessionmaker(bind=engine)
        session = Session()
        if search_by == None:
            blogs = session.query(Blogs).filter(Blogs.id == int(id)).all()
        elif search_by == "author_name":
            blogs = session.query(Blogs).filter(Blogs.author_name == id).all()
        elif search_by == "date":
            blogs = session.query(Blogs).filter(Blogs.upload_date == id).all()
        elif search_by == "title":
            blogs = session.query(Blogs).filter(Blogs.title == id).all()
        return render_template("content_page.html",blogs=blogs)

    
@app.route("/search_by_id",methods = ["GET","POST"])
def search_by_id():
    if request.method == 'POST':
        search_option = request.form.get('search_option')
        search_value = request.form.get("ID")

        if search_option == 'id':
            return get_blog(search_value)
        elif search_option == 'author_name':
            return get_blog(search_value,"author_name")
        elif search_option == 'date':
            return get_blog(search_value,"date")
        else:
            return get_blog(search_value,"title")
        



@app.route("/post-blog",methods = ["GET","POST"])
def post_blog():
    if request.method == 'POST':
        name = request.form.get("author_name")
        blog_title= request.form.get("title")
        blog_content = request.form.get("content")
        blog_date = date.today()
        blog_post = Blogs(author_name= name,
                          title = blog_title,
                          content = blog_content,
                          upload_date = blog_date)
        
        engine = sqlalchemy.create_engine("mysql+mysqlconnector://root:hamza-100@localhost/blog_db")
        Session = sessionmaker(bind=engine)
        session = Session()
        session.add(blog_post)
        session.commit()

        return redirect("/") 
    else:
        home()





app.run(debug=True)




# class blogs(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     author_name = db.Column(db.String(120), unique=False)
#     title = db.Column(db.String(120), unique=False)
#     content = db.Column(db.String(120), unique=False)
#     upload_date = db.Column(db.String(120), unique=False)
