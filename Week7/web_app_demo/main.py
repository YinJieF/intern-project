from flask import Flask, render_template

app = Flask(__name__)

# Homepage route
@app.route('/')
def homepage():
    return render_template('homepage.html')

# Data page route
@app.route('/data')
def data():
    return render_template('data.html')

# Training page route
@app.route('/training')
def training():
    return render_template('training.html')

# Inference page route
@app.route('/inference')
def inference():
    return render_template('inference.html')

if __name__ == '__main__':
    app.run(debug=True)
