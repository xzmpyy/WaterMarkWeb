from flask import Flask
from flask import render_template, request


app = Flask(__name__)


@app.route('/')
def index_page():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    print(0)
    if request.method == 'POST':
        print(1)
        img = request.files['pic']
        print(img)
    print(2)


if __name__ == '__main__':
    app.run()
