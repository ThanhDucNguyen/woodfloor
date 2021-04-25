from flask import Flask, flash, redirect, render_template, \
     request, url_for, redirect
import os
from werkzeug.utils import secure_filename

PATH_DEFAULT = 'C:/Users/OS/Desktop/Data/0.Work/woodfloor/'
UPLOAD_FOLDER = 'static/img_upload/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['UPLOAD_FOLDER'] = PATH_DEFAULT + UPLOAD_FOLDER

LIST_ORIGIN = {
    "USA": "Mỹ",
    "Thailand": "Thái Lan",
    "Germany": "Đức",
    "Malaysia": "Malaysia",
    "China": "Trung Quốc",
    "India": "Ấn Độ",
    "VietNam": "Việt Nam",
    "Lao": "Lào"
}

def upload_file(image, file_old=None):
    file_name = UPLOAD_FOLDER + image.filename[0:len(image.filename)]
    filename = image.filename[2:len(image.filename)]
    filename = '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    if file_old:
        os.remove(os.path.join(PATH_DEFAULT, file_old))
    if image and filename:
        filename = secure_filename(image.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return file_name
