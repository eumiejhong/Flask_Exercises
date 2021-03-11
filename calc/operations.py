"""Basic math operations."""
from flask import Flask, request
from operations import add, sub, mult, div

app = Flask(__name__)

@app.route('/add')
def add(a, b):
    a = int(request.args.get('a'))
    b = int(request.args.get('b'))
    """Add a and b."""
    
    return a + b

@app.route('/sub')
def sub(a, b):
    """Substract b from a."""
    a = int(request.args.get('a'))
    b = int(request.args.get('b'))
    return a - b

@app.route('/mult')
def mult(a, b):
    """Multiply a and b."""
    a = int(request.args.get('a'))
    b = int(request.args.get('b'))
    return a * b

@app.route('/div')
def div(a, b):
    """Divide a by b."""
    a = int(request.args.get('a'))
    b = int(request.args.get('b'))
    return a / b

# Further study
operators = {
    "add": add(a,b),
    "sub": sub(a,b),
    "mult": mult(a,b),
    "div": div(a,b)
}

@app.route(/math/<operator>)
def url_operator(operator):
    a = request.args.get('a')
    b = request.args.get('b')
    result = operators[operator](a,b)
    return str(result)
