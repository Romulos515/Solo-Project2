from flask import redirect
from flask_app import app

@app.route('/')
def index():
    return "<h1>This is / route.<br/> <a href='/login'>Login</a>"