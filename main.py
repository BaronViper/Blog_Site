from flask import Flask, render_template
import forms
from datetime import datetime

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/blog')
def blog():
    return render_template('generic.html')


@app.route('/elements')
def elements():
    return render_template('elements.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)
