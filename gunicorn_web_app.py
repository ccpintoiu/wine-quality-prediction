"""
filename: 
author: cosminP
date: aug 2018
"""


from flask import Flask
from flask import render_template

from os import environ

#pip install wtforms
from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField

import dill as pickle 
import numpy as np
import pandas as pd


app = Flask(__name__)

app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176b'

#@app.route('/users/<string:username>')
@app.route("/")
#def main(username=None):
def main():
#	return("Hello {}!" .format(username))
	return render_template('index.html')
#def main():
#	return render_template('index.html')
 
@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')


class ReusableForm(Form):
    Alcohol = TextField('Alcohol:', validators=[validators.required()])
    acidity = TextField('acidity:', validators=[validators.required()])
    sugar = TextField('sugar:', validators=[validators.required()])
    Sulphates = TextField('Sulphates:', validators=[validators.required()])
 
@app.route("/enterWine", methods=['GET', 'POST'])
def enterWine():
    form = ReusableForm(request.form)
    
    #data = ('fixed acidity' = _acidity, 'volatile acidity' = 0.2, 'citric acid' = 0.4, 'residual sugar' = _sugar, 'chlorides' = 0.058, 'free sulfur dioxide' = 30.0,'total sulfur dioxide' = 93.0,'density' = 0.99322,'pH' = 3.03,'sulphates' = _sulphates,'alcohol' = _alcohol )
    #data = [ _alcohol , _sulphates , _sugar , _acidity]
    #print(data)

    print form.errors
    if request.method == 'POST':
        #name=request.form['Alcohol']
        #name2=request.form['acidity']
        _alcohol = request.form['Alcohol']
        _acidity = request.form['acidity']
        _sugar = request.form['sugar']
        _sulphates = request.form['Sulphates']
        data = [ _alcohol, _sulphates, _sugar, _acidity]
        print data
        # create final dataset
        data_f = [ int(_acidity), 0.2, 0.4, int(_sugar), 0.058, 30.0, 93.0, 0.99322, 3.03, int(_sulphates), int(_alcohol) ]
        print data_f
        
        #data_f2 = np.array(data_f)
        data_f2 = pd.DataFrame(data_f).T.values
        print data_f2

        data_f3 = np.array([[7.0000e+00, 2.0000e-01, 4.0000e-01, 1.1000e+00, 5.8000e-02, 3.0000e+01, 9.3000e+01, 9.9322e-01, 3.0300e+00, 3.8000e-01, 9.2000e+00]])
        print data_f3

        clf = 'model_v3.pk'
        
        print("Loading the model...")
        loaded_model = None
        with open('./models/'+clf,'rb') as f:
            loaded_model = pickle.load(f)

        print("The model has been loaded...doing predictions now...")
        predictions = loaded_model.predict(data_f2)

        print predictions
        #flash('Wine quality prediction (1 to 10): ', + predictions)
        if form.validate():
            # Save the comment here.
            flash('Wine quality prediction (1 to 10): {}'.format(predictions))
        else:
            flash('All the form fields are required. ')
 
    return render_template('enterWine.html', form=form)


@app.route('/predict', methods=['POST'])
def apicall():
    """API Call
    """
    try:
        test = request.args.getlist()
    except Exception as e:
        raise e

    clf = 'model_v1.pk'

    if test.empty:
        return(bad_request())
    else:
        #Load the saved model
        print("Loading the model...")
        loaded_model = None
        with open('./models/'+clf,'rb') as f:
            loaded_model = pickle.load(f)

        print("The model has been loaded...doing predictions now...")
        predictions = loaded_model.predict(test)
        responses.status_code = 200
        return (predictions)


if __name__ == "__main__":
	   # Bind to PORT if defined, otherwise default to 5000.
    port = int(environ.get('PORT', 8002))
    app.run(host='', port=port, debug=True)
	#app.run()
