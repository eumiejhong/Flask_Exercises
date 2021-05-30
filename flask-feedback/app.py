from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Feedback
from forms import RegisterForm, LoginForm, DeleteForm, FeedbackForm
from werkzeug.exceptions import Unauthorized

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///feedback_db"
app.config["SQLALCHEMY_TRACK_MODIFICIATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "feedback123"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)

@app.route('/')
def homepage():
    return redirect('/register')

@app.route('/register', methods=['GET', 'POST'])
def register():

    if "username" in session:
        return redirect(f"/users/{session['username']}")
    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        
        new_user = User.register(username, password, email, first_name, last_name)

        session['username'] = new_user.username
        db.session.commit()

        return redirect(f"/users/{session['username']}")

    else:
        return render_template("register.html", form=form)



@app.route('/login', methods=['GET', 'POST'])
def login():
    if "username" in session:
        return redirect(f"/users/{session['username']}")
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            session['username'] = user.username
            return redirect(f"/users/{session['username']}")
        else:
            form.username.errors = ["Invalid username/password!"]
            return render_template("login.html", form=form)
    return render_template('login.html', form=form)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('username')
    return redirect('/login')

@app.route('/users/<username>')
def show_user(username):
    if "username" not in session or username != session['username']:
        raise Unauthorized()
    user = User.query.get(username)
    form = DeleteForm()

    return render_template('show-user.html', user=user, form=form)

@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    if "username" not in session or username != session['username']:
        raise Unauthorized()
    user = User.query.get(username)
    db.session.delete(user)
    db.session.commit()
    session.pop("username")
    return redirect('/login')

@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def feedback_form(username):
    if "username" not in session or username != session['username']:
        raise Unauthorized()
    form = FeedbackForm()
    
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        
        feedback = Feedback(title=title, content=content, username=username)
        db.session.add(feedback)
        db.session.commit()
        return redirect(f"/users/{feedback.username}")

    return render_template('feedback-form.html', form=form)

@app.route('/feedback/<int:feedback_id>/update', methods=['GET', 'POST'])
def update_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized()
    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.commit()

        return redirect(f"/users/{feedback.username}")
    return render_template('edit.html', form=form, feedback=feedback)

@app.route('/feedback/<int:feedback_id>/delete', methods=['POST'])
def delete_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized()
    form = DeleteForm()

    if form.validate_on_submit():
        db.session.delete(feedback)
        db.session.commit()
    return redirect(f"/users/{feedback.username}")