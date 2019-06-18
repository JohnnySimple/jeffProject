from project import db, login_manager
from datetime import datetime
from flask_login import UserMixin
from project import app
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView




# table for posts
class Posts(db.Model,UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(200), nullable=False)
	content = db.Column(db.Text, nullable=False)
	date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
	image_name = db.Column(db.String(300))
	image_data = db.Column(db.LargeBinary)
	comments = db.relationship('Comments', backref='comment')

	def __repr__(self):
		return format("Post(" + str(self.id) + "," + self.title + "," + str(self.date) + ")")


# table for comments
class Comments(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	content = db.Column(db.Text, nullable=False)
	date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
	post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

	def __repr__(self):
		return format("Comment(" + str(self.id) + "," + self.name + "," + str(self.date) + ")")

# table for subscribers
class Subscribers(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(200),unique=True, nullable=False)

	def __repr__(self):
		return format("Subscriber(" + str(self.id) + "," + self.email + ")")