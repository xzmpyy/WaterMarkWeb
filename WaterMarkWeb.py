import os
import time
from flask import Flask
from flask import render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, DataRequired, FileAllowed
from flask_wtf.csrf import CSRFProtect
from wtforms import FileField, SubmitField, StringField
import MarkIn
import MarkOut

app = Flask(__name__)
CSRF_ENABLED = True
# 随机生成秘钥
SECRET_KEY = os.urandom(24)
app.config['SECRET_KEY'] = SECRET_KEY
csrf = CSRFProtect()
csrf.init_app(app)
upload_folder = r'D:\design\WaterMarkWeb\static\upload'
download_folder = r'D:\design\WaterMarkWeb\static\done'


# 表单
class UploadForm(FlaskForm):
    # 标签、表单验证
    file_button = FileField('图片', validators=[FileRequired(),  FileAllowed(['jpg', 'png', 'jpeg'])])
    code_filed = StringField('水印码', render_kw={'placeholder': '请输入15位以内的英文水印码，只能由英文及空格组成'}, validators=[DataRequired()])
    submit_button = SubmitField('提交')


class DecodeForm(FlaskForm):
    decode_button = FileField('图片', validators=[FileRequired(),  FileAllowed(['jpg', 'png', 'jpeg'])])
    decode_submit = SubmitField('提交')


class IndexForm(UploadForm, DecodeForm):
    pass


# 文件夹大小判断
def get_file_size(file_path, size=0):
    for root, dirs, files in os.walk(file_path):
        for f in files:
            size += os.path.getsize(os.path.join(root, f))
    return size


@app.route('/')
def index_page():
    form = IndexForm()
    return render_template('index.html', form=form)
    # return render_template('result.html')


@app.route('/upload', methods=['POST'])
def upload():
    # 判断文件夹空间大小
    d_size = get_file_size(upload_folder)
    # 文件夹存储图像大于100兆时停止服务 104856975
    if d_size > 104856975:
        return render_template('overflow.html')
    # print(UploadForm().validate())
    if request.method == 'POST'and UploadForm().validate():
        # 水印码
        code_str = request.form.get('code_filed')
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
        file_deal_name = filename.split('.')[0] + time_now
        # 嵌入对象 原图片 水印码 保存名 保存路径
        process_in = MarkIn.LazyMarkIn(os.path.join(upload_folder, file_save_name), code_str, file_deal_name,
                                       download_folder, is_delete=True)
        try:
            info_num = process_in.water_mark_in()
            if info_num == 101:
                return render_template('oversmall.html')
        except:
            os.remove(os.path.join(upload_folder, file_save_name))
            return render_template('error.html')
        # 删除原始图片
        # os.remove(os.path.join(upload_folder, file_save_name))
        # request.files ImmutableMultiDict([('file_button', <FileStorage: 'pyy.jpg' ('image/jpeg')>)])
        # 前端图片推送地址
        file_path = 'static/done/' + file_deal_name + '.png'
        file_save_name = file_deal_name + '.png'
        return render_template('download.html', file_path=file_path, file_save_name=file_save_name)
    else:
        return redirect(url_for('index_page'))


# 解码路由
@app.route('/decode', methods=['POST'])
def decode_get():
    # 判断文件夹空间大小
    d_size = get_file_size(upload_folder)
    # 文件夹存储图像大于100兆时停止服务
    if d_size > 104856975:
        return render_template('overflow.html')
    if request.method == 'POST' and DecodeForm().validate():
        # 文件对象
        file = request.files['decode_button']
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
        # 解码
        process_out = MarkOut.LazyMarkOut(os.path.join(upload_folder, file_save_name), is_delete=True)
        try:
            info_num = process_out.decode()
            if info_num == 400:
                return render_template('none.html')
        except:
            os.remove(os.path.join(upload_folder, file_save_name))
            return render_template('error.html')
        return render_template('result.html', info_num=info_num)


# 下载完成删除图片
@csrf.exempt
@app.route('/done', methods=['POST'])
def image_delete():
    if request.method == 'POST':
        file_deal_name = request.form.get('data')
        # print(os.path.join(download_folder, file_deal_name))
        while os.path.exists(os.path.join(download_folder, file_deal_name)):
            os.remove(os.path.join(download_folder, file_deal_name))
        return '/'


# 离开页面时删除已处理完成的图片
@csrf.exempt
@app.route('/leave', methods=['POST'])
def leave_delete():
    if request.method == 'POST':
        file_deal_name = request.form.get('data')
        if os.path.exists(os.path.join(download_folder, file_deal_name)):
            while os.path.exists(os.path.join(download_folder, file_deal_name)):
                os.remove(os.path.join(download_folder, file_deal_name))
            return 'success'
        else:
            return 'file not'
    else:
        return render_template('index.html')


# 404页面
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# 405页面
@app.errorhandler(405)
def page_405_response(e):
    return render_template('500.html'), 405


# 400页面
@app.errorhandler(400)
def page_400_found(e):
    return render_template('404.html'), 400


# 500页面
@app.errorhandler(500)
def page_bad_response(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run()
