from flask import Flask, render_template, redirect, url_for,request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from datetime import date
from flask import jsonify
today = date.today()


app = Flask(__name__)
ckeditor = CKEditor(app)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

# CREATE DATABASE
class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# CONFIGURE TABLE
class BlogPost(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)
    
class Contact(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=False, nullable=False)
    email: Mapped[str] = mapped_column(String(250), nullable=False)
    number: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
   


with app.app_context():
    db.create_all()


@app.route('/')
def get_all_posts():
    posts=BlogPost.query.all()
    # TODO: Query the database for all the posts. Convert the data to a python list.
    # posts = []
    return render_template("index.html", all_posts=posts)

# TODO: Add a route so that you can click on individual posts.
@app.route('/show/<int:post_id>')
def show_post(post_id):
    # TODO: Retrieve a BlogPost from the database based on the post_id
    # requested_post = db.session.execute(db.select(BlogPost).where(BlogPost.id==post_id)).scalar()
    requested_post = db.get_or_404(BlogPost, post_id)
    print(requested_post)
    return render_template("post.html", post=requested_post)


# TODO: add_new_post() to create a new blog post
@app.route("/add-post",methods=['POST','GET'])
def add_new_post():
    global today
    
    if request.method == 'POST':
        title=request.form.get("title")
        subtitle=request.form.get("subtitle")
        name=request.form.get("name")
        content = request.form.get('ckeditor')
        imgurl = request.form.get('imgurl')
        date=today.strftime("%B %d, %Y")
        d=BlogPost(title=title,subtitle=subtitle,author=name,body=content,img_url=imgurl,date=date)
        db.session.add(d)
        db.session.commit()
        return redirect('/')

    return render_template("make-post.html")
# TODO: edit_post() to change an existing blog post
@app.route("/edit-post", methods=["GET", "POST"])
def edit_post():
    edit_post_id=request.args.get('post_id')
    post = db.get_or_404(BlogPost, edit_post_id)
    if request.method == 'POST':
        post.title=request.form.get("title")
        post.subtitle=request.form.get("subtitle")
        post.author=request.form.get("name")
        post.body = request.form.get('ckeditor')
        post.img_url = request.form.get('imgurl')
        post.date=today.strftime("%B %d, %Y")
        
        db.session.commit()
        return redirect('/')
    return render_template("make-post.html",id=edit_post_id,post=post,)
# TODO: delete_post() to remove a blog post from the database
@app.route("/delete/<int:id>")
def delete_post(id):
    secret_code=request.args.get('secrect-code')
    post=db.get_or_404(BlogPost,id)
    if post:
        db.session.delete(post)
        db.session.commit()
        return redirect("/")
        # if secret_code=='DeleteKrDo':
            
        # else:
        # return jsonify({'Failed':'Secret Code not Matched'})
    else:
        return jsonify({'Failed':'Id Didnot Matched'})
    
# Below is the code from previous lessons. No changes needed.
@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == 'POST':
        name=request.form.get("name")
        email=request.form.get("email")
        message = request.form.get('message')
        number = request.form.get('phone')
        date=today.strftime("%B %d, %Y")
        d=Contact(name=name,email=email,message=message,number=number,date=date)
        db.session.add(d)
        db.session.commit()
        msg_sent=True
    else:
        msg_sent=False
    return render_template("contact.html",msg_sent=msg_sent)


if __name__ == "__main__":
    app.run(debug=True, port=5003)
