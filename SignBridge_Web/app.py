import os
import numpy as np
import pandas as pd
import pymongo
from flask import Flask, redirect, render_template, request, session
from datetime import timedelta
from functools import wraps
from flask import Flask, render_template


#### Defining Flask App
app = Flask(__name__)
app.secret_key = 'Reign@2023'

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=5)

client = pymongo.MongoClient("localhost", 27017)
db = client.user_login_system

# Decorators
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect('/authenticate/')

    return wrap



################## ROUTING FUNCTIONS #########################


from user import routes

#### Our main page
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/authenticate', methods=['GET'])
def authenticate():
    return render_template('authentication.html')

if __name__ == '__main__':
    app.run(debug=True)
