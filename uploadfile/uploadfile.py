# _*_ coding:utf-8 _*_
from flask import Flask, request, redirect, url_for, render_template
from flask_uploads import UploadSet, ARCHIVES, SCRIPTS, IMAGES, configure_uploads, patch_request_class
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SubmitField
import os


SERVER_DIR = 'E:\\tmp\\uploadfile.temp'

app = Flask(__name__)
app.config['UPLOADS_DEFAULT_DEST'] = 'E:\\tmp\\uploadfile.temp'
app.config['SECRET_KEY'] = 'a random string'
file = UploadSet('file', ARCHIVES + SCRIPTS + IMAGES)
configure_uploads(app, file)
patch_request_class(app, size=64 * 1024 * 1024)


class UploadForm(FlaskForm):
    file = FileField(validators=[
        FileAllowed(file, u'只能上传压缩包和脚本文件！'),
        FileRequired(u'文件未选择！')])
    submit = SubmitField(u'上传')


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
        all_file[parent] = filenames
    print(all_file)
    return render_template('index.html', form=form, file_url=file_url, allfile=all_file)


if __name__ == '__main__':
    app.run(host='127.0.0.1')