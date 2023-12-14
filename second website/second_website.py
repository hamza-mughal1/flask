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
limit = 5
page_no = 1
previous_page = False
next_page_condition = True

class Blogs(Base):

    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True)
    author_name = Column(String(120), unique=False)
    title = Column(String(120), unique=False)
    content = Column(String(120), unique=False)
    upload_date = Column(String(120), unique=False)

def blog_limit(page_no,limit):
    a = (page_no-1)*limit
    b = page_no*limit
    return a,b

@app.route("/next-page/<int:page_no>",methods=["GET"])
def next_page(page_no):
    page_no+=1
    redirect("/")
    return home(page_reset=False,page_no = page_no)


@app.route("/previous-page/<int:page_no>",methods=["GET"])
def previous_page_func(page_no):
    print(page_no)
    page_no-=1
    redirect("/")
    return home(page_reset=False,page_no = page_no)

@app.route("/")
def home(page_reset=True,page_no = 1):
    global next_page_condition
    global previous_page

    if page_reset == True:
        page_no = 1
    

    if page_no > 1:
        previous_page = True
    else:
        previous_page = False

    start, stop = blog_limit(page_no,limit)
    start2, stop2 = blog_limit(page_no+1,limit)
    engine = sqlalchemy.create_engine("mysql+mysqlconnector://root:hamza-100@localhost/blog_db")
    Session = sessionmaker(bind=engine)
    session = Session()
    blogs = session.query(Blogs).order_by(Blogs.upload_date.desc()).all()
    
    if len(blogs[start2:stop2]) == 0:
        next_page_condition = False   
    else:
        next_page_condition = True

    blogs = blogs[start:stop] 

    return render_template("index.html",page_en = page_reset,blogs=blogs,previous_page=previous_page,next_page=next_page_condition,page_no=page_no)


@app.route("/blog/<string:id>",methods=["GET"])
def get_blog(id,search_by=None):
        engine = sqlalchemy.create_engine("mysql+mysqlconnector://root:hamza-100@localhost/blog_db")
        Session = sessionmaker(bind=engine)
        session = Session()
        if search_by == None:
            blogs = session.query(Blogs).filter(Blogs.id == int(id)).order_by(Blogs.upload_date.desc()).all()
        elif search_by == "author_name":
            blogs = session.query(Blogs).filter(Blogs.author_name == id).order_by(Blogs.upload_date.desc()).all()
        elif search_by == "date":
            blogs = session.query(Blogs).filter(Blogs.upload_date == id).order_by(Blogs.upload_date.desc()).all()
        elif search_by == "title":
            blogs = session.query(Blogs).filter(Blogs.title == id).order_by(Blogs.upload_date.desc()).all()
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




if __name__ == "__main__":
    app.run(debug=True)




# class blogs(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     author_name = db.Column(db.String(120), unique=False)
#     title = db.Column(db.String(120), unique=False)
#     content = db.Column(db.String(120), unique=False)
#     upload_date = db.Column(db.String(120), unique=False)
