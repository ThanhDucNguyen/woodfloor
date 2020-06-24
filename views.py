import json
import models.config as models
import common
from sqlalchemy import *
from models.config import session
from flask import Flask, flash, redirect, render_template, \
     request, url_for, redirect
from flask_login import LoginManager, login_required, logout_user, current_user, login_user
import os
from werkzeug.utils import secure_filename
# from flask.ext.login import LoginManager, login_required, logout_user, current_user, login_user


PATH_DEFAULT = 'D:/30. Work/31. TODO/PYTHON_SANGO/sango/'
UPLOAD_FOLDER = 'static/img_info/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['UPLOAD_FOLDER'] = PATH_DEFAULT + UPLOAD_FOLDER
login_manager.login_view = 'login'

class web():
   @app.route('/')
   def index():
      page_size = request.args.get("page_size")
      list_origin = common.LIST_ORIGIN
      page_size = int(page_size) if page_size else 10
      data = session.query(models.Info).order_by(models.Info.id.desc()).all()
      count = len(data)
      page_size = page_size if page_size < len(data) else len(data)
      check_view = True if page_size < len(data) else False
      return render_template('sango/web/index.html',
         data=data, list_origin=list_origin,
         page_size=page_size, check_view=check_view)

   @app.route('/detail-info-<id>')
   def detail_info(id):
      list_origin = common.LIST_ORIGIN
      data = session.query(models.Info).filter(models.Info.id == id).first()
      return render_template('sango/web/detail-info.html', data=data, list_origin=list_origin)

   @app.route('/list-product-filter-<typep>-<origin>')
   def list_product(typep, origin=None):
      list_origin = common.LIST_ORIGIN
      page_size = request.args.get("page_size")
      page_size = int(page_size) if page_size else 12
      if origin != 'False':
         data = session.query(models.Product).filter(models.Product.type == typep, models.Product.origin == origin).order_by(models.Product.id).all()
      elif typep == 'nep-chantuong':
         data = session.query(models.Product).filter(or_(models.Product.type == 'nep', models.Product.type == 'chan-tuong')).order_by(models.Product.id).all()
      else:
         data = session.query(models.Product).filter(models.Product.type == typep).order_by(models.Product.id).all()
      count = len(data)
      flash(count)
      page_size = page_size if page_size < len(data) else len(data)
      check_view = True if page_size < len(data) else False
      return render_template('sango/web/list-product.html', data=data, list_origin=list_origin,
         page_size=page_size, check_view=check_view,
         typep=typep, origin=origin)

   @app.route('/detail-product-<id>')
   def detail_product(id):
      list_origin = common.LIST_ORIGIN
      data = session.query(models.Product).filter(models.Product.id == id).first()
      return render_template('sango/web/detail-product.html', data=data, list_origin=list_origin)
   
   ##################################################################################################
   # Login =======================
   @login_manager.user_loader
   def load_user(user_id):
      return session.query(models.User).filter(
         models.User.id == user_id).first()

   @app.route('/login')
   def login():
      return render_template('sango/admin/login.html')

   @app.route('/login', methods=['POST'])
   def login_process():
      try:
         username = request.form.get("user_name")
         password = request.form.get("password")
         user = session.query(models.User).filter(
            models.User.username == username,
            models.User.password == password).first()
         if user:
            login_user(user)
         else:
            flash('Mật khẩu không chính xác')
            return redirect("/login")
      except Exception as e:
         flash('Hệ thống lỗi, nhờ báo cáo sự cố với bộ phận kỹ thuật.')
         return redirect("/login")
      return redirect("/admin")

   @app.route("/logout")
   def logout():
      logout_user()
      return redirect('/login')

   # Product ===
   @app.route('/admin')
   @login_required 
   def admin():
      data = session.query(models.Product).order_by(models.Product.id.desc()).all()
      return render_template('sango/admin/managerment.html', data=data)

   @app.route('/admin-add-product')
   @login_required
   def admin_add_product():
      list_origin = common.LIST_ORIGIN
      data = session.query(models.Product).all()
      return render_template('sango/admin/add-product.html', data=data, list_origin=list_origin)

   @app.route('/add-product', methods=['POST'])
   @login_required
   def add_product():
      try:
         type = request.form.get("type")
         name = request.form.get("name")
         price = request.form.get("price")
         color = request.form.get("color")
         origin = request.form.get("origin")
         mainten = request.form.get("mainten")
         wood_type = request.form.get("wood_type")
         short_info = request.form.get("short_info")
         long_info = request.form.get("long_info")

         if 'image' not in request.files:
            flash(request.files)
            flash('No file part')
            return redirect("/admin")
         image = request.files['image']
         # if user does not select file, browser also
         # submit an empty part without filename
         if image.filename == '':
            flash('No selected file')
            return redirect("/admin-add-info")
         file_name = common.upload_file(image)

         product = models.Product()
         product.type = type
         product.name = name
         product.price = price
         product.color = int(color) if color else None
         product.origin = origin
         product.mainten = int(mainten) if color else None
         product.image = file_name
         product.wood_type = wood_type
         product.short_info = short_info
         product.long_info = long_info
         session.add(product)
         session.commit()
         session.close()
         flash('Tạo sản phẩm thành công!')
      except Exception as e:
         flash('Hệ thống lỗi, nhờ báo cáo sự cố với bộ phận kỹ thuật.')
      return redirect("/admin")

   @app.route('/admin-detail-product-<id>')
   @login_required
   def admin_detail_product(id):
      data = session.query(models.Product).filter(models.Product.id == id).first()
      return render_template('sango/admin/detail-product.html', data=data)

   @app.route('/admin-edit-product-<id>')
   @login_required
   def admin_edit_product(id):
      list_origin = common.LIST_ORIGIN
      data = session.query(models.Product).filter(models.Product.id == id).first()
      return render_template('sango/admin/edit-product.html', data=data, list_origin=list_origin)

   @app.route('/edit-product', methods=['POST'])
   @login_required
   def edit_product():
      try:
         id = request.form.get("id")
         typep = request.form.get("type")
         name = request.form.get("name")
         price = request.form.get("price")
         color = request.form.get("color")
         origin = request.form.get("origin")
         mainten = request.form.get("mainten")
         wood_type = request.form.get("wood_type")
         short_info = request.form.get("short_info")
         long_info = request.form.get("long_info")

         product = session.query(models.Product).filter(models.Product.id == int(id)).first()
         file_name = product.image
         if 'image' in request.files:
            image = request.files['image']
            if image.filename != '':
               file_old = product.image
               file_name = common.upload_file(image, file_old)
         product.type = typep
         product.name = name
         product.price = price
         product.color = int(color) if color else None
         product.origin = origin
         product.mainten = int(mainten) if color else None
         product.image = file_name
         product.wood_type = wood_type
         product.short_info = short_info
         product.long_info = long_info
         session.merge(product)
         session.commit()
         session.close()
         flash('Chỉnh sửa sản phẩm thành công!')
      except Exception as e:
         flash('Hệ thống lỗi, nhờ báo cáo sự cố với bộ phận kỹ thuật.')
      return redirect("/admin")

   @app.route('/delete-product', methods=['POST'])
   @login_required
   def delete_product():
      try:
         id = request.form.get("id")
         session.query(models.Product).filter(models.Product.id == int(id)).delete()
         flash('Xóa sản phẩm thành công!')
      except Exception as e:
         flash('Hệ thống lỗi, nhờ báo cáo sự cố với bộ phận kỹ thuật.')
      return redirect("/admin")
   
   # INFO ====================================
   @app.route('/list-info')
   @login_required
   def info():
      data = session.query(models.Info).order_by(models.Info.id.desc()).all()
      return render_template('sango/admin/list-info.html', data=data)

   @app.route('/admin-add-info')
   @login_required
   def add_info():
      return render_template('sango/admin/add-info.html')

   @app.route('/add-info', methods=['POST'])
   @login_required
   def admin_add_info():
      try:
         name = request.form.get("name")
         short_info = request.form.get("short_info")
         long_info = request.form.get("long_info")

         if 'image' not in request.files:
            flash('No file part')
            return redirect("/admin-add-info")
         image = request.files['image']
         # if user does not select file, browser also
         # submit an empty part without filename
         if image.filename == '':
            flash('No selected file')
            return redirect("/admin-add-info")
         file_name = common.upload_file(image)

         info = models.Info()
         info.name = name
         info.image = file_name
         info.short_info = short_info
         info.long_info = long_info
         session.add(info)
         session.commit()
         session.close()
         flash('Tạo tin tức thành công!')
      except Exception as e:
         flash('Hệ thống lỗi, nhờ báo cáo sự cố với bộ phận kỹ thuật.')
      return redirect("/list-info")

   @app.route('/admin-detail-info-<id>')
   @login_required
   def ad_detail_info(id):
      data = session.query(models.Info).filter(models.Info.id == id).first()
      return render_template('sango/admin/detail-info.html', data=data)

   @app.route('/admin-edit-info-<id>')
   @login_required
   def edit_info(id):
      data = session.query(models.Info).filter(models.Info.id == id).first()
      return render_template('sango/admin/edit-info.html', data=data)

   @app.route('/edit-info', methods=['POST'])
   @login_required
   def ad_edit_info():
      try:
         id = request.form.get("id")
         name = request.form.get("name")
         short_info = request.form.get("short_info")
         long_info = request.form.get("long_info")

         info = session.query(models.Info).filter(models.Info.id == int(id)).first()
         # if user does not select file, browser also
         # submit an empty part without filename
         file_name = info.image
         if 'image' in request.files:
            image = request.files['image']
            if image.filename != '':
               file_old = info.image
               flash(file_old)
               file_name = common.upload_file(image, file_old)
               
         info.name = name
         info.image = file_name
         info.short_info = short_info
         info.long_info = long_info
         session.add(info)
         session.commit()
         session.close()
         flash('Chỉnh sửa tin tức thành công!')
      except Exception as e:
         flash('Hệ thống lỗi, nhờ báo cáo sự cố với bộ phận kỹ thuật.')
      return redirect("/list-info")

   @app.route('/delete-info', methods=['POST'])
   @login_required
   def delete_info():
      try:
         id = request.form.get("id")
         session.query(models.Info).filter(models.Info.id == int(id)).delete()
         flash('Xóa tin tức thành công!')
      except Exception as e:
         flash('Hệ thống lỗi, nhờ báo cáo sự cố với bộ phận kỹ thuật.')
      return redirect("/list-info")

if __name__ == '__main__':
   app.run(debug = True)
