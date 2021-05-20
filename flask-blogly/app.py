"""Blogly application."""

from flask import Flask, render_template, request, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "blogger"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.debug = True
toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

#USER APP ROUTES***********************************************************

@app.route('/')
def homepage():
    posts = Post.query.order_by(Post.created_at.desc()).limit(10).all()
    return render_template('home.html', posts=posts)

@app.route('/users')
def show_users():
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('show-all-users.html', users=users)

@app.route('/users/new', methods=["GET"])
def new_user_form():
    return render_template('add-user.html')

@app.route('/users/new', methods=["POST"])
def add_user():
    new_user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url'] or None)

    db.session.add(new_user)
    db.session.commit()
    flash(f"User {new_user.first_name} added.")
    return redirect('/users')

@app.route('/users/<int:user_id>')
def show_user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('/user-detail.html', user=user)

@app.route('/users/<int:user_id>/edit')
def show_edited_user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('/edit-user.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']
    db.session.add(user)
    db.session.commit()
    return redirect('/users')

#POST APP ROUTES************************************************* 

@app.route('/users/<int:user_id>/posts/new')
def add_new_post_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('add-post.html', user=user)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def handle_new_post(user_id):
    user = User.query.get_or_404(user_id)
    new_post = Post(
        title = request.form['title'], 
        content = request.form['content'],
        user = user)
    db.session.add(new_post)
    db.session.commit()
    return redirect(f"/posts/{post.post_id}")

@app.route('/posts/<int:post_id>')
def show_new_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post-detail.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('edit-post.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()
    return redirect(f"/users/{post.user_id}")

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash(f"Post {post.title} has been deleted")
    return redirect(f"/users/{post.user_id}")
    
#TAG APP ROUTES**********************************************

@app.route('/tags')
def tag_info():
    tags = Tag.query.all()
    return render_template('tag-info.html', tags=tags)

@app.route('/tags/new')
def add_new_tag_form():
    posts = Post.query.all()
    return render_template('add-tag.html', posts=posts)

@app.route('/tags/new', methods=["POST"])
def handle_new_tags():
    post_ids = [int(num) for num in request.form.getlist('posts')]
    post = Post.query.filter(Post.post_id.in_(post_ids)).all()
    new_tag = Tag(tag_name=request.form['tag_name'], post=post)

    db.session.add(new_tag)
    db.session.commit()
    return redirect('/tags')


