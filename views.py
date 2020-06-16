import models.config as models
import common
from sqlalchemy import *
from models.config import session
from flask import Flask, flash, redirect, render_template, \
     request, url_for, redirect
import os
from werkzeug.utils import secure_filename

PATH_DEFAULT = 'D:/30. Work/31. TODO/PYTHON_SANGO/sango/'
UPLOAD_FOLDER = 'static/img_info/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['UPLOAD_FOLDER'] = PATH_DEFAULT + UPLOAD_FOLDER

class web():
   @app.route('/')
   def index():
      list_origin = common.LIST_ORIGIN
      data = session.query(models.Info).all()
      return render_template('sango/web/index.html', data=data, list_origin=list_origin)

   @app.route('/detail-info-<id>')
   def detail_info(id):
      list_origin = common.LIST_ORIGIN
      data = session.query(models.Info).filter(models.Info.id == id).first()
      return render_template('sango/web/detail-info.html', data=data, list_origin=list_origin)

   @app.route('/list-product-filter-<typep>-<origin>')
   def list_product(typep, origin=None):
      list_origin = common.LIST_ORIGIN
      if origin != 'False':
         data = session.query(models.Product).filter(models.Product.type == typep, models.Product.origin == origin).order_by(models.Product.id).all()
      elif typep == 'nep-chantuong':
         data = session.query(models.Product).filter(or_(models.Product.type == 'nep', models.Product.type == 'chan-tuong')).order_by(models.Product.id).all()
      else:
         data = session.query(models.Product).filter(models.Product.type == typep).order_by(models.Product.id).all()
      return render_template('sango/web/list-product.html', data=data, list_origin=list_origin)

   @app.route('/detail-product-<id>')
   def detail_product(id):
      list_origin = common.LIST_ORIGIN
      data = session.query(models.Product).filter(models.Product.id == id).first()
      return render_template('sango/web/detail-product.html', data=data, list_origin=list_origin)
   
   ##################################################################################################
   # Login =======================
   @app.route('/login')
   def login():
      return render_template('sango/admin/login.html')

   # Todo
   # Chức năng login
   # Logout
   # Import file image
   # Paging 

   # Product ===
   @app.route('/admin')
   def admin():
      data = session.query(models.Product).all()
      return render_template('sango/admin/managerment.html', data=data)

   @app.route('/admin-add-product')
   def admin_add_product():
      list_origin = common.LIST_ORIGIN
      data = session.query(models.Product).all()
      return render_template('sango/admin/add-product.html', data=data, list_origin=list_origin)

   @app.route('/add-product', methods=['POST'])
   def add_product():
      try:
         type = request.form.get("type")
         name = request.form.get("name")
         price = request.form.get("price")
         color = request.form.get("color")
         origin = request.form.get("origin")
         mainten = request.form.get("mainten")
         image = request.form.get("image")
         wood_type = request.form.get("wood_type")
         short_info = request.form.get("short_info")
         long_info = request.form.get("long_info")

         product = models.Product()
         product.type = type
         product.name = name
         product.price = price
         product.color = int(color) if color else None
         product.origin = origin
         product.mainten = int(mainten) if color else None
         product.image = image
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
   def admin_detail_product(id):
      data = session.query(models.Product).filter(models.Product.id == id).first()
      return render_template('sango/admin/detail-product.html', data=data)

   @app.route('/admin-edit-product-<id>')
   def admin_edit_product(id):
      list_origin = common.LIST_ORIGIN
      data = session.query(models.Product).filter(models.Product.id == id).first()
      return render_template('sango/admin/edit-product.html', data=data, list_origin=list_origin)

   @app.route('/edit-product', methods=['POST'])
   def edit_product():
      try:
         id = request.form.get("id")
         typep = request.form.get("type")
         name = request.form.get("name")
         price = request.form.get("price")
         color = request.form.get("color")
         origin = request.form.get("origin")
         mainten = request.form.get("mainten")
         image = request.form.get("image")
         wood_type = request.form.get("wood_type")
         short_info = request.form.get("short_info")
         long_info = request.form.get("long_info")

         product = session.query(models.Product).filter(models.Product.id == int(id)).first()
         product.type = typep
         product.name = name
         product.price = price
         product.color = int(color) if color else None
         product.origin = origin
         product.mainten = int(mainten) if color else None
         product.image = image
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
   def info():
      data = session.query(models.Info).all()
      return render_template('sango/admin/list-info.html', data=data)

   @app.route('/admin-add-info')
   def add_info():
      return render_template('sango/admin/add-info.html')

   @app.route('/add-info', methods=['POST'])
   def admin_add_info():
      # try:
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
      # except Exception as e:
      #    flash('Hệ thống lỗi, nhờ báo cáo sự cố với bộ phận kỹ thuật.')
      return redirect("/list-info")

   @app.route('/admin-detail-info-<id>')
   def ad_detail_info(id):
      data = session.query(models.Info).filter(models.Info.id == id).first()
      return render_template('sango/admin/detail-info.html', data=data)

   @app.route('/admin-edit-info-<id>')
   def edit_info(id):
      data = session.query(models.Info).filter(models.Info.id == id).first()
      return render_template('sango/admin/edit-info.html', data=data)

   @app.route('/edit-info', methods=['POST'])
   def ad_edit_info():
      try:
         id = request.form.get("id")
         name = request.form.get("name")
         image = request.form.get("image")
         short_info = request.form.get("short_info")
         long_info = request.form.get("long_info")

         info = session.query(models.Info).filter(models.Info.id == int(id)).first()
         info.name = name
         info.image = image
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
