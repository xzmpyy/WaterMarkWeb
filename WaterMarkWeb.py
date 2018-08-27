import os
import shutil
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
download_folder = r'D:\design\WaterMarkWeb\static\done'


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
    # return render_template('500.html')


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
        try:
            file.save(os.path.join(upload_folder, file_save_name))
        except:
            return render_template('error.html')
        # 保存完成图片
        file_deal_name = filename.split('.')[0] + time_now + '.' + filename.split('.')[1]
        try:
            shutil.move(os.path.join(upload_folder, file_save_name), os.path.join(download_folder, file_deal_name))
        except:
            os.remove(os.path.join(upload_folder, file_save_name))
            return render_template('error.html')
        # 删除原始图片
        # os.remove(os.path.join(upload_folder, file_save_name))
        # request.files ImmutableMultiDict([('file_button', <FileStorage: 'pyy.jpg' ('image/jpeg')>)])
        # 前端图片推送地址
        file_path = 'static/done/' + file_save_name
        return render_template('download.html', file_path=file_path, file_save_name=file_save_name)
    else:
        return redirect(url_for('index_page'))


# 下载完成删除图片
@app.route('/done', methods=['POST'])
def image_delete():
    if request.method == 'POST':
        file_deal_name = request.form.get('data')
        os.remove(os.path.join(download_folder, file_deal_name))
        return '/'


# 404页面
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# 405页面
@app.errorhandler(405)
def page_bad_response(e):
    return render_template('500.html'), 405


# 500页面
@app.errorhandler(500)
def page_bad_response(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run()
