from datetime import datetime
from atnu import db, login_manager, bcrypt
from flask_login import UserMixin 
from hashlib import md5
from wtforms import BooleanField, widgets, TextAreaField
from flask_sqlalchemy import SQLAlchemy
from flask_whooshalchemy import whoosh_index
from app import app

db = SQLAlchemy()

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

#followers = db.Table('followers',
#    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
#    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
#)


class User(db.Model, UserMixin):
	__searchable__ = ['username']
	id = db.Column(db. Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)																																																			
	password = db.Column(db.String(60), nullable=False)
	admin = db.Column(db.Boolean())
	whoosh_index(app, User)


	def __init__(self, username, password, email, admin=False):
		self.username = username
		#self.pwdhash = generate_password_hash(password)
		self.email = email
		self.password = password
		self.admin = admin
#		self.notes = notes
	
	def is_admin(self):
		return self.admin
		
	def __repr__(self):
		return "User('{self.username}', '{self.email}')"


class Person(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	bday = db.Column(db.DateTime)
	residence = db.Column(db.String(70), nullable=False)
	work_place = db.Column(db.String(50), nullable=False)	
	position = db.Column(db.Text, nullable=False)
	degree = db.Column(db.String(20), nullable=False)
	academic_status = db.Column(db.String(30), nullable=False) 
	scientific_specialty = db.Column(db.Text, nullable=False)
	phone = db.Column(db.String(15))	
	status = db.Column(db.String(20))	
	id_number = db.Column(db.String(20))	
	solution_number = db.Column(db.String(15))	
	date_of_decision = db.Column(db.DateTime)																																										

	
	def __repr__(self):
		return "Person('{self.name}', '{self.email}', '{self.bday}', '{self.residence}', '{self.work_place}', '{self.position}', '{self.degree}', '{self.academic_status}', '{self.scientific_specialty}', '{self.phone}', '{self.status}', '{self.id_number}', '{self.solution_number}', '{self.date_of_decision}')"




	#tags = db.relationship('Tag', secondary=post_tags, backref('posts', lazy='dynamic'))

class CKTextAreaWidget(widgets.TextArea):
	def __call__(self, field, **kwargs):
		kwargs.setdefault('class_', 'ckeditor')
		return super(CKTextAreaWidget, self).__call__(field, **kwargs)

class CKTextAreaField(TextAreaField):
	widget = CKTextAreaWidget()




