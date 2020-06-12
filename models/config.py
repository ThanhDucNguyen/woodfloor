from flaskext.mysql import MySQL
from flask import Flask

app = Flask(__name__)

mysql = MySQL()
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '12345678'
app.config['MYSQL_DATABASE_DB'] = 'sango'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

def connection():
    conn = mysql.connect()
    cursor = conn.cursor()
    return cursor