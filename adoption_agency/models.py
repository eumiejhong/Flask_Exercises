from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

default_image = "https://cdn.pixabay.com/photo/2021/05/06/16/13/children-6233868_1280.png"

def connect_db(app):
    db.app = app
    db.init_app(app)

class Pet(db.Model):
    
    __tablename__ = "pets"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    species = db.Column(db.Text, nullable=False, unique=True)
    photo_url = db.Column(db.Text)
    age = db.Column(db.Integer)
    notes = db.Column(db.Text)
    available = db.Column(db.Boolean, nullable=False, default=True)

    def photo(self):
        return self.photo_url or default_image