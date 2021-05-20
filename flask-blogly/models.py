"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
import datetime


db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):

    __tablename__ = "users"
    user_id = db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True)
    first_name = db.Column(db.String(50), 
                           nullable=False)
    last_name = db.Column(db.String(50),
                           nullable=False)
    image_url = db.Column(db.String,
                           nullable=False)

class Post(db.Model):
    
    __tablename__ = "posts"
    post_id = db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True)
    title = db.Column(db.String(100),
                      nullable=False)
    content = db.Column(db.String,
                        nullable=False)
    created_at = db.Column(db.DateTime,
                           nullable=False,
                           default=datetime.datetime.now)
    user_id = db.Column(db.Integer, 
                        db.ForeignKey("users.user_id"))
    
    user = db.relationship('User', backref='posts')

    @property
    def friendly_date(self):
        return self.created_at.strftime('%a %b %-d %Y, %-I:%M %p')

class Tag(db.Model):

    __tablename__ = "tags"
    tag_id = db.Column(db.Integer,
                       primary_key=True,
                       autoincrement=True)
    tag_name = db.Column(db.String,
                        nullable=False)
    post = db.relationship('Post', 
                            secondary='post_tags',
                            backref='tags')

class PostTag(db.Model):

    __tablename__ = "post_tags"
    post_id = db.Column(db.Integer,
                        db.ForeignKey("posts.post_id"),
                        primary_key=True)
    tag_id = db.Column(db.Integer,
                        db.ForeignKey("tags.tag_id"),
                        primary_key=True)




