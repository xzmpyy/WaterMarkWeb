from flask import Flask
from flask import render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms import FileField, SubmitField

app = Flask(__name__)
CSRF_ENABLED = True
app.config['SECRET_KEY'] = 'xzmpyy'


# 表单
class UploadForm(FlaskForm):
    # 标签、表单验证
    file_button = FileField('图片', validators=[FileRequired()])
    submit_button = SubmitField('提交')


@app.route('/')
def index_page():
    form = UploadForm()
    return render_template('index.html', form=form)


@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        filename = request.files
        # request.files ImmutableMultiDict([('file_button', <FileStorage: 'pyy.jpg' ('image/jpeg')>)])
        print(filename)
    print(2)
    # 重定向
    return redirect(url_for('index_page'))


if __name__ == '__main__':
    app.run()
