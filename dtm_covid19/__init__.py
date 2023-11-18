from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from geopy.geocoders import Nominatim

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY']= b'\x13],\x9a2QV23\xcbP\x85Q\xbd\xe1\xf9'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
geolocator = Nominatim(user_agent="DTM_Covid19")

from dtm_covid19 import routes

