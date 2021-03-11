# Put your app in here.
from flask import Flask


app = Flask(__name__)

@app.route('/welcome')
def say_welcome():
    html = "<html><body><h1>Welcome</h><body><html>"
    return html

@app.route('/welcome/home')
def say_welcome():
    html = "<html><body><h1>Welcome home</h><body><html>"
    return html

@app.route('/welcome/back')
def say_welcome():
    html = "<html><body><h1>Welcome back</h><body><html>"
    return html