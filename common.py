from flask import Flask, flash, redirect, render_template, \
     request, url_for, redirect
import os
from werkzeug.utils import secure_filename

PATH_DEFAULT = 'D:/30. Work/31. TODO/PYTHON_SANGO/sango/'
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

def upload_file(image):
    # if user does not select file, browser also
    # submit an empty part without filename
    if image.filename == '':
        flash('No selected file')
        return redirect("/admin-add-info")
    file_name = UPLOAD_FOLDER + image.filename[0:len(image.filename)]
    filename = image.filename[2:len(image.filename)]
    filename = '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    if image and filename:
        filename = secure_filename(image.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return file_name
