"""
filename: gcp app engine wine prediction with Lentiq Model Server API calls
author: cosminP
date: 20 May 2019
"""

from flask import Flask
from flask import render_template

from os import environ

#pip install wtforms
from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField

#import dill as pickle 
#import numpy as np
#import pandas as pd
#import requests
import pprint

endpoint = 'http://35.234.79.201:65327/transform'
headers = {'accept': 'application/json', 'content-type': 'application/json'}
obj2 = '{"schema": {"fields": [{"name": "fixed acidity", "type": "double"}, {"name": "volatile acidity", "type": "double"}, {"name": "citric acid", "type": "double"}, {"name": "residual sugar", "type": "double"}, {"name": "chlorides", "type": "double"}, {"name": "free sulfur dioxide", "type": "double"}, {"name": "total sulfur dioxide", "type": "double"}, {"name": "density", "type": "double"}, {"name": "pH", "type": "double"}, {"name": "sulphates", "type": "double"}, {"name": "alcohol", "type": "double"}]}, "rows": [[1, 0.2, 0.4, 1, 0.058, 30.0, 93.0, 0.99322, 3.03, 1, 1]]}'

#import requests
#import requests_toolbelt.adapters.appengine
#requests_toolbelt.adapters.appengine.monkeypatch()

from requests_toolbelt.adapters import appengine
appengine.monkeypatch(validate_certificate=False)
import requests

r = requests.post(endpoint, headers=headers, data=obj2)
print (r)

app = Flask(__name__)

app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176b'
headers = {'accept': 'application/json', 'content-type': 'application/json'}
#endpoint = 'http://35.234.79.201:65327/transform'
endpoint = environ['ENDPOINT']		   
		   
class ReusableForm(Form):
    Alcohol = TextField('Alcohol:', validators=[validators.required()])
    acidity = TextField('acidity:', validators=[validators.required()])
    sugar = TextField('sugar:', validators=[validators.required()])
    Sulphates = TextField('Sulphates:', validators=[validators.required()])

def getprediction(features):
    print(features)
    obj = '{"schema": {"fields": [{"name": "fixed acidity", "type": "double"}, {"name": "volatile acidity", "type": "double"}, {"name": "citric acid", "type": "double"}, {"name": "residual sugar", "type": "double"}, {"name": "chlorides", "type": "double"}, {"name": "free sulfur dioxide", "type": "double"}, {"name": "total sulfur dioxide", "type": "double"}, {"name": "density", "type": "double"}, {"name": "pH", "type": "double"}, {"name": "sulphates", "type": "double"}, {"name": "alcohol", "type": "double"}]}, "rows": ['+str(features)+']}'
    response = requests.post(endpoint, headers=headers, data=obj)
    response2 = response.json()
    return response2['rows'][0][-1]
    
@app.route("/")
def main():
	return render_template('index.html')
 
@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route("/enterWine", methods=['GET', 'POST'])
def enterWine():
    form = ReusableForm(request.form)
    if request.method == 'POST':
        _alcohol = request.form['Alcohol']
        _acidity = request.form['acidity']
        _sugar = request.form['sugar']
        _sulphates = request.form['Sulphates']
        data = [ _alcohol, _sulphates, _sugar, _acidity]
        # create final dataset
        data_f = [ int(_acidity), 0.2, 0.4, int(_sugar), 0.058, 30.0, 93.0, 0.99322, 3.03, int(_sulphates), int(_alcohol) ]
        predictions = getprediction(data_f)
        if form.validate():
            flash('Wine quality prediction (1 to 10): {}'.format(predictions))
        else:
            flash('All the form fields are required. ')
    return render_template('enterWine.html', form=form)
