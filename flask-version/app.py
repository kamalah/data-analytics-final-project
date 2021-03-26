# -*- coding: utf-8 -*-
"""
Created on Wed Mar 24 20:41:14 2021

@author: k
"""

from flask import Flask, render_template, request

app = Flask(__name__)
options = ["Number of Steps", "Number of Ingredients", "Ratings", "Exoticness of Ingredients", "Time to Prepare"]
recipe = ""
priorities = []

@app.route('/', methods = ['GET','POST'])

def index():
    return render_template("index.html")

@app.route('/step_2', methods = ['GET','POST'])
def step_2():
    if request.method == 'POST':
        recipe = request.form['recipe']
        return render_template("step_2.html", recipe = recipe, options = options)

@app.route('/step_3', methods = ['GET','POST'])
def step_3():
    if request.method == 'POST':
        priorities.append(request.form['pref_1'])
        print(request.form.to_dict(flat=False))
        list_options = list(set(options) - set(priorities))
        return render_template("step_3.html", recipe = recipe, options = list_options, priorities = priorities)

@app.route('/step_4', methods = ['GET','POST'])
def step_4():
    if request.method == 'POST':
        priorities.append(request.form['pref_2'])
        list_options = list(set(options) - set(priorities))
        return render_template("step_4.html", recipe = recipe, options = list_options, priorities = priorities)

@app.route('/step_5', methods = ['GET','POST'])
def step_5():
    if request.method == 'POST':
        priorities.append(request.form['pref_3'])
        list_options = list(set(options) - set(priorities))
        return render_template("step_5.html", recipe = recipe, options = list_options, priorities = priorities)

    
if __name__ == '__main__':
    app.run(debug = True)
