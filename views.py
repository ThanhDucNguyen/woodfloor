from models.config import connection
from flask import Flask, flash, redirect, render_template, \
     request, url_for

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

class web():
   @app.route('/')
   def index():
      ducnt = "nguyenthanhduc"
      conn = connection()
      conn.execute("Select * from info")
      flash("okay")
      data = conn.fetchall()
      
      for d in data:
         flash(d)

      flash(data)
      return render_template('sango/web/index.html', ducnt=ducnt)

   @app.route('/list-product-filter-<typep>')
   def list_product(typep):
      return render_template('sango/web/list-product.html')

   @app.route('/detail-product-<id>')
   def detail_product(id):
      return render_template('sango/web/detail-product.html')

   @app.route('/detail-info-<id>')
   def detail_info(id):
      return render_template('sango/web/detail-info.html')

if __name__ == '__main__':
   app.run(debug = True)