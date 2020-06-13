import models.config as models
import common
from models.config import session
from flask import Flask, flash, redirect, render_template, \
     request, url_for

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

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
      else:
         data = session.query(models.Product).filter(models.Product.type == typep).order_by(models.Product.id).all()
      return render_template('sango/web/list-product.html', data=data, list_origin=list_origin)

   @app.route('/detail-product-<id>')
   def detail_product(id):
      list_origin = common.LIST_ORIGIN
      data = session.query(models.Product).filter(models.Product.id == id).first()
      return render_template('sango/web/detail-product.html', data=data, list_origin=list_origin)

if __name__ == '__main__':
   app.run(debug = True)