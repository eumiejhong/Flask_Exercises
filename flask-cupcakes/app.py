"""Flask app for Cupcakes"""
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from models import db, connect_db, Cupcake

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "cupcakes"
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

def serialize(cupcake):
    return {
        "id": cupcake.id,
        "flavor": cupcake.flavor,
        "size": cupcake.size,
        "rating": cupcake.rating,
        "image": cupcake.image
    }

@app.route('/')
def show_cupcakes():
    return render_template('index.html')

@app.route('/api/cupcakes')
def get_all_cupcakes():
    cupcakes = Cupcake.query.all()
    serialized = [serialize(cupcake) for cupcake in cupcakes]

    return jsonify(cupcakes=serialized)

@app.route('/api/cupcakes/<int:id>')
def get_cupcake(id):
    cupcake = Cupcake.query.get_or_404(id)
    serialized = serialize(cupcake)

    return jsonify(cupcake=serialized)

@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake(): 
    flavor = request.json['flavor']
    size = request.json['size']
    rating = request.json['rating']
    image = request.json['image'] or None

    new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)
    db.session.add(new_cupcake)
    db.session.commit()
    
    serialized = serialize(new_cupcake)

    return (jsonify(cupcake=serialized), 201)

@app.route('/api/cupcakes/<int:id>', methods=['PATCH'])
def update_cupcake(id):
    cupcake = Cupcake.query.get_or_404(id)
    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.image = request.json.get('image', cupcake.image)
    db.session.add(cupcake)
    db.session.commit()

    serialized = serialize(cupcake)

    return jsonify(cupcake=serialized)

@app.route('/api/cupcakes/<int:id>', methods=['DELETE'])
def delete_cupcake(id):
    cupcake = Cupcake.query.get_or_404(id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message='Deleted')


