import os
import time
from flask import Flask
from flask import render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms import FileField, SubmitField


app = Flask(__name__)
CSRF_ENABLED = True
# 随机生成秘钥
SECRET_KEY = os.urandom(24)
app.config['SECRET_KEY'] = SECRET_KEY
upload_folder = r'D:\design\WaterMarkWeb\static\upload'


# 表单
class UploadForm(FlaskForm):
    # 标签、表单验证
    file_button = FileField('图片', validators=[FileRequired()])
    submit_button = SubmitField('提交')


# 文件夹大小判断
def get_file_size(file_path, size=0):
    for root, dirs, files in os.walk(file_path):
        for f in files:
            size += os.path.getsize(os.path.join(root, f))
    return size


@app.route('/')
def index_page():
    form = UploadForm()
    return render_template('index.html', form=form)


@app.route('/upload', methods=['POST'])
def upload():
    # 判断文件夹空间大小
    d_size = get_file_size(upload_folder)
    # 文件夹存储图像大于100兆时停止服务
    if d_size > 104856975:
        return '<p>storage error'
    if request.method == 'POST':
        # 文件对象
        file = request.files['file_button']
        # 文件名
        filename = file.filename
        # 获取时间戳
        time_now = str(int(time.time()))
        # 保证文件名不重复
        file_save_name = filename.split('.')[0] + time_now + '.' + filename.split('.')[1]
        # 保存至本地
        file.save(os.path.join(upload_folder, file_save_name))
        # request.files ImmutableMultiDict([('file_button', <FileStorage: 'pyy.jpg' ('image/jpeg')>)])
    # 重定向
    return '<p>success</p>'


if __name__ == '__main__':
    app.run()
