from dtm_covid19 import db, app, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), unique=False, nullable=False)
    last_name = db.Column(db.String(255), unique=False, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    status = db.Column(db.String(255), nullable=False, default='Green')

    def __repr__(self):
        return f"User('{self.first_name}, {self.last_name}, {self.email}, {self.status}')"

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=False, nullable=False)
    address = db.Column(db.String(255), unique=False, nullable=True)
    city = db.Column(db.String(30), unique=False, nullable=True)
    state = db.Column(db.String(2), unique=False, nullable=True)
    zip_code = db.Column(db.String(5), unique=False, nullable=True)
    full_address = db.Column(db.String(255), unique=False, nullable=True)
    datetime = db.Column(db.DateTime(), unique=False, nullable=True)

    def __repr__(self):
        return f"Entry('{self.user_id}, {self.address}, {self.datetime}')"