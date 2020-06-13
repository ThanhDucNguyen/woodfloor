from flaskext.mysql import MySQL
# from flask import Flask

# app = Flask(__name__)

# mysql = MySQL()
 
# # MySQL configurations
# app.config['MYSQL_DATABASE_USER'] = 'root'
# app.config['MYSQL_DATABASE_PASSWORD'] = '12345678'
# app.config['MYSQL_DATABASE_DB'] = 'sango'
# app.config['MYSQL_DATABASE_HOST'] = 'localhost'
# mysql.init_app(app)

# def connection():
#     conn = mysql.connect()
#     cursor = conn.cursor()
#     return cursor

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import re
import datetime

from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import exists

engine = create_engine('mysql+pymysql://root:12345678@localhost/sango', echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


app = Flask(__name__)
app.config['SECRET_KEY'] = 'p9Bv<3Eid9%$i01'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:12345678@localhost/sango'

db = SQLAlchemy(app)

class Info(db.Model):
    __tablename__ = 'info'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(455))
    short_info = db.Column(db.String(500))  
    long_info = db.Column(db.String(1500))
    image = db.Column(db.String(500))

    def __init__(self, name, short_info, long_info, image):
        self.name = name
        self.short_info = short_info
        self.long_info = long_info
        self.image = image

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(100))
    name = db.Column(db.String(255))
    price = db.Column(db.String(30))
    color = db.Column(db.String(45))
    origin = db.Column(db.String(255))
    mainten = db.Column(db.Integer)
    image = db.Column(db.String(255))
    wood_type = db.Column(db.String(455))
    short_info = db.Column(db.String(500))  
    long_info = db.Column(db.String(1500))
    image_description = db.Column(db.String(455))

    def __init__(self, type, price, name, color, origin, mainten, image, wood_type, short_info, long_info, image_description):
        self.type = type
        self.name = name
        self.price = price
        self.color = color
        self.origin = origin
        self.mainten = mainten
        self.image = image
        self.wood_type = wood_type
        self.short_info = short_info
        self.long_info = long_info
        self.image_description = image_description