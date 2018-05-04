from flask import Flask,request,jsonify,redirect,abort,render_template
from pymongo import MongoClient
from datetime import datetime
import random


monogclient=MongoClient('mongodb://localhost:27017/')
db=monogclient['FlaskShort']

app=Flask(__name__)
urls=db.urls

def already_exist(url):
    if urls.find_one({'short_url':url}):
        return True
    return False

def url_shortener(url):
    while already_exist(url) or url=='':
        url=''.join (random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqstuvwxyz') for i in range(7))
    return url

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/url',methods=['POST'])
def add_url_into_db():
    urls=db.urls
    #json
    if request.json:
        long_url=request.json['long-url']
        if request.json['short-url']:
            short_url=request.json['short-url']
        else:
            short_url=url_shortener('')

    #from
    if request.form:
        long_url=request.form['long-url']
        if request.form['short-url']:
            short_url=request.form['short-url']
        else:
            short_url=url_shortener('')

    #insert into mongodb
    url_id=urls.insert({
        'long_url':long_url,
        'short_url':short_url,
        'clicks':0,
        'created_at':datetime.now()
    })

    new_url = urls.find_one({'_id': url_id})

    output = {
        'long_url': new_url['long_url'],
        'short_url': new_url['short_url'],
        'clicks': new_url['clicks'],
        'created_at': new_url['created_at']
    }
    status = 200
    if request.json:
        return jsonify({'result':output}),status
    return render_template('index.html', shorted_url=request.url_root+output['short_url'])


if __name__=="__main__":
    app.run(debug=True)
