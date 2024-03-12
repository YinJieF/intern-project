from underthesea import ner
from flask import Flask, render_template, request
from name_birth_identify import named_entity_recognition, find_elements, combination

app = Flask(__name__)

# Define the route for the index page
@app.route('/')
def index():
    return render_template('index.html')

# Define the route for the /extract page with both GET and POST methods
@app.route('/extract', methods=['GET', 'POST'])
def extract():
    if request.method == 'POST':
        sentence = request.form['input_text']
        # extract named entities from the input text
        ner_sentence = named_entity_recognition(sentence)
        names, sinh, dates = find_elements(ner_sentence)
        result = combination(names, sinh, dates)
        #print(result)
        if result:
            name = result[0]
            birthdate = result[1]
        else:
            name = "No name found"
            birthdate = "No birthdate found"
        return render_template('extract.html', input_text=sentence, name=name, birthdate=birthdate)
    else:
        # Render the extract.html template with no text initially
        return render_template('extract.html', input_text='', name='', birthdate='')

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
