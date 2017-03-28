from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from farmer import db


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)

    def __init__(self, content):
        self.content = content


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(80))

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get_by_username(username):
        return User.query.filter_by(username=username).first()

    def avatar(self, size):
        return 'http://www.gravatar.com/avatar/{}?d=mm&s={}'.format(md5(self.email.encode('utf-8')).hexdigest(), size)

    def __repr__(self):
        return '<User %r>' % self.username

class Disease(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    symptoms = db.Column(db.Text)
    remedy = db.Column(db.Text)

    def __init__(self, name, symptoms, remedy):
        self.name = name
        self.symptoms = symptoms
        self.remedy = remedy

    def __repr__(self):
        return '<{}>'.format(self.name)

class Farmer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    surname = db.Column(db.String(50))
    location = db.Column(db.String(50))

    def __init__(self, number, name, surname, location):
        self.number = number
        self.name = name
        self.surname = surname
        self.location = location

    def isUnique(self, number):
        test = Farmer.query.filter_by(number=number)
        if test:
            return True 
        else:
            return False 
    

