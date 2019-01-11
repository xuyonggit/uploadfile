# _*_ coding:utf-8 _*_
from flask import Flask, request, redirect, url_for, render_template
from flask_uploads import UploadSet, ARCHIVES, SCRIPTS, IMAGES, configure_uploads, patch_request_class
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SubmitField
import os, json
import configparser
import hashlib

cf = configparser.ConfigParser()
cf.read('../config', encoding='utf-8')
conf = cf.sections()
filetypes = cf.get('app', 'filetypes')
myselfset = ARCHIVES = tuple(filetypes.split())

bindip = cf.get('app', 'app_bind_ip')
bindport = cf.get('app', 'app_bind_port')
app = Flask(__name__, static_folder='', static_path='')
app.config['UPLOADS_DEFAULT_DEST'] = cf.get('app', 'file_dir')
app.config['SECRET_KEY'] = 'a random string'
file = UploadSet('file', ARCHIVES + SCRIPTS + IMAGES + myselfset)
configure_uploads(app, file)
limit_size = cf.get('app', 'file_limit_size')
if not limit_size:
    limit_size = 64
patch_request_class(app, size=int(limit_size) * 1024 * 1024)
clear_key = cf.get('app', 'clear_key')

class UploadForm(FlaskForm):
    file = FileField(validators=[
        FileAllowed(file, u'只能上传压缩包和脚本文件！'),
        FileRequired(u'文件未选择！')])
    submit = SubmitField(u'上传')


def getfilemd5(filename):
    if not os.path.isfile(filename):
        return
    with open(filename, 'rb') as f:
        myhash = hashlib.md5(f.read())
    return myhash.hexdigest()


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    all_file = {}
    form = UploadForm()
    if form.validate_on_submit():
        filename = file.save(form.file.data)
        file_url = file.url(filename)
    else:
        file_url = None
    # list all file
    base_dir = app.config.get('UPLOADS_DEFAULT_DEST')
    main_dir = os.path.join(base_dir, 'file')
    for parent, dirnames, filenames in os.walk(main_dir):
        for name in filenames:
            md5 = getfilemd5(os.path.join(parent, name))
            file_url = file.url(name)
            all_file[name] = {'url': file_url, 'md5': md5}
    return render_template('index.html', form=form, allfile=all_file)


@app.route('/clear', methods=['POST'])
def clear():
    data = json.loads(request.form.get('data'))
    if data['key'] == clear_key:
        file_dir = os.path.join(app.config.get('UPLOADS_DEFAULT_DEST'), 'file')
        for i in os.listdir(file_dir):
            path_file = os.path.join(file_dir, i)
            os.remove(path_file)
        res = 'success'
    else:
        res = {'res': 'error'}
    return res


if __name__ == '__main__':
    app.run(host=bindip, port=int(bindport), threaded=True)
