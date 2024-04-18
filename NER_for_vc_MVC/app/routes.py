from flask import render_template, request

def index():
    return render_template('index.html')

def model_monitor():
    return "Developing..."