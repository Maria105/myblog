from datetime import datetime
from myblog import db, login_manager, bcrypt
from flask_login import UserMixin 
from hashlib import md5
from wtforms import BooleanField, widgets, TextAreaField



@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)


class User(db.Model, UserMixin):
	id = db.Column(db. Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	image_file = db.Column(db.String(20), nullable=False, default='default.jpg')																																																			
	password = db.Column(db.String(60), nullable=False)
	posts = db.relationship( 'Post', backref='author', lazy=True)
	about_me = db.Column(db.String(140))
	last_seen = db.Column(db.DateTime, default=datetime.utcnow)	
	admin = db.Column(db.Boolean())



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
		return f"User('{self.username}', '{self.email}', '{self.image_file}')"

	def avatar(self, size):
		digest = md5(self.email.lower().encode('utf-8')).hexdigest()
		return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)
	


class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	image_file = db.Column(db.String(20), nullable=True, default='default.jpg')
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	content = db.Column(db.Text, nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	comments = db.relationship('Comment', backref='article', cascade="all,delete", lazy=True)

	def __repr__(self):
		return f"Post('{self.title}', '{self.date_posted}')"

class Comment(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.String(100), nullable=False)
	timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	
	

	def __repr__(self):
		return f"Comment('{self.body}', '{self.timestamp}')"


	#tags = db.relationship('Tag', secondary=post_tags, backref('posts', lazy='dynamic'))

class CKTextAreaWidget(widgets.TextArea):
	def __call__(self, field, **kwargs):
		kwargs.setdefault('class_', 'ckeditor')
		return super(CKTextAreaWidget, self).__call__(field, **kwargs)

class CKTextAreaField(TextAreaField):
	widget = CKTextAreaWidget()

