from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Pet
from forms import AddPetForm, EditPetForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///pets'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "ilovedogs"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.debug = True
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def homepage():
    pets = Pet.query.all()
    return render_template('/homepage.html', pets=pets)

@app.route('/pets/add', methods=["GET", "POST"])
def add_pet_form():

    form = AddPetForm()

    if form.validate_on_submit():
        data = {field: val for field, val in form.data.items() if field != "csrf_token"}
        new_pet = Pet(**data)
        db.session.add(new_pet)
        db.session.commit()

        return redirect('/')

    else:
        return render_template('add-pet-form.html', form=form)

@app.route('/pets/edit/<int:id>', methods=["GET", "POST"])
def edit_pet_form(id):

    pet = Pet.query.get_or_404(id)
    form = EditPetForm(obj=pet)

    if form.validate_on_submit():
        data = {field: val for field, val in form.data.items() if field != "csrf_token"}
        db.session.commit()

        return redirect(f"/pets/{id}")

    else:
        return render_template('edit-pet-form.html', form=form, pet=pet)

@app.route('/pets/<int:id>')
def pet_detail(id):
    pet = Pet.query.get_or_404(id)
    return render_template('pet-detail.html', pet=pet)
