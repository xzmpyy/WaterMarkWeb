from flask import Flask
from flask import render_template, request, redirect, url_for
import os

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
