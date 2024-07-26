from flask import render_template, request

def render_page():
    if request.method == 'GET':
        return render_template('genai.html')