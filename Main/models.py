from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from Main import db,login_manager
from datetime import datetime
from flask_login import UserMixin
from flask import current_app
import flask_whooshalchemy as wa 
@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class User(db.Model,UserMixin):
	id = db.Column(db.Integer,primary_key=True)
	username = db.Column(db.String(20),unique=True, nullable= False)
	email = db.Column(db.String(120),unique=True,nullable=False)
	image_file = db.Column(db.String(20),nullable=False,default= 'default.jpg')
	password = db.Column(db.String(30),nullable=False) 
	posts = db.relationship('Post',backref='author',lazy=True)
	def __repr__(self):
		return f"User('{self.username}','{self.email}','{self.image_file}')"
	def get_reset_token(self,expire_sec=1500):
		s = Serializer(current_app.config['SECRET_KEY'],expire_sec)
		return s.dumps({'user_id':self.id}).decode('utf-8')

	@staticmethod
	def verify_reset_token(token):
		s = Serializer(current_app.config['SECRET_KEY'])	
		try:
			user_id = s.loads(token)['user_id']
		except:
			return None
		return User.query.get(user_id)
	liked = db.relationship('PostLike',foreign_keys='PostLike.user_id',backref='user',lazy='dynamic')	
	disliked = db.relationship('PostDisLike',foreign_keys='PostDisLike.user_id', backref='user', lazy='dynamic')
	def like_post(self,post):
		if not self.has_liked_post(post) and not self.has_disliked_post(post):
			like = PostLike(user_id=self.id,post_id=post.id)
			db.session.add(like)	
	def unlike_post(self,post):
		if self.has_liked_post(post):
			PostLike.query.filter_by(user_id=self.id,post_id=post.id).delete()
	def has_liked_post(self,post):
		return PostLike.query.filter(PostLike.user_id == self.id,PostLike.post_id == post.id).count() > 0	
	def dislike_post(self,post):
		if not self.has_liked_post(post) and not self.has_disliked_post(post):
			dislike = PostDisLike(user_id=self.id,post_id=post.id)
			db.session.add(dislike)	
	def has_disliked_post(self,post):
		return PostDisLike.query.filter(PostDisLike.user_id == self.id,PostDisLike.post_id == post.id).count() > 0	
	def Undislike_post	(self,post):
		if self.has_disliked_post(post):
			PostDisLike.query.filter_by(user_id=self.id,post_id=post.id).delete()						
class Post(db.Model):
	__searchable__ = ['title']
	id = db.Column(db.Integer,primary_key=True)
	title = db.Column(db.String(120),nullable=False)
	content = db.Column(db.Text,nullable=False)
	date_posted = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
	user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
	def __repr__(self):
		return f"Post('{self.title}','{self.date_posted}')"
	likes = db.relationship('PostLike',backref='post',lazy='dynamic')	
	dislikes = db.relationship('PostDisLike',backref='post',lazy='dynamic')	
class PostLike(db.Model):
	__tablename__ = 'like_post'
	id = db.Column(db.Integer,primary_key=True)
	user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
	post_id = db.Column(db.Integer,db.ForeignKey('post.id'))

class PostDisLike(db.Model):
	__tablename__ = 'dislike_post'
	id = db.Column(db.Integer,primary_key=True)
	user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
	post_id = db.Column(db.Integer,db.ForeignKey('post.id'))

wa.search_index(current_app,Post)		
