from flask import Flask,request,jsonify,redirect,abort,render_template
from pymongo import MongoClient
from datetime import datetime
import random


monogclient=MongoClient('mongodb://localhost:27017/')
db=monogclient['FlaskShort']

app=Flask(__name__)

@app.route('/')
def index():
    print db
    return '<h1>Hi</h1>'

if __name__=="__main__":
    app.run(debug=True)
