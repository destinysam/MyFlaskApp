from flask import render_template, request, Blueprint,flash,redirect,url_for
from flask_login import login_required,current_user
from Main import db
from Main.models import User,Post,PostLike
import flask_whooshalchemy
from newsapi import NewsApiClient
index = Blueprint('index',__name__)
@index.route('/')
@index.route('/home')
def home():
	page = request.args.get('page',1,type=int) 
	posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page,per_page=3)
	return render_template('home.html',posts = posts)

@index.route('/about')
def about():
	return render_template('about.html')

@index.route('/articles')
def articles():
	newsapi = NewsApiClient(api_key='1c307ad0d0444e4fa8aeeba31d3d356e')
	topheadlines = newsapi.get_top_headlines(sources='al-jazeera-english')
	articles = topheadlines['articles']
	disc = [ ]
	news = [ ]
	img = [ ]
	for i in range(len(articles)):
		myarticles = articles[i]
		news.append(myarticles['title'])
		disc.append(myarticles['description'])
		img.append(myarticles['urlToImage'])
	data = zip(news,disc,img)			
	return render_template('articles.html',context = data)
@index.route('/search',methods=['GET'])
def search():
	posts = Post.query.filter(Post.title.like("%"+ request.args.get('query') + "%")).paginate()
	if  posts.items:
		return render_template('home.html',posts = posts)
	else:
		flash(f"Post not found",'info')
		return redirect(url_for('index.home'))

@index.route('/reaction/<int:post_id>/<action>')
@login_required
def reaction(post_id,action):
	post = Post.query.filter_by(id = post_id).first_or_404()
	if action == 'like':
		current_user.like_post(post)
		db.session.commit()
	if action == 'dislike':
			current_user.unlike_post(post)
			db.session.commit()	
	return redirect(request.referrer)

@index.route('/Dislike/<int:post_id>/<action>')
@login_required
def Dislike(post_id,action):
	post = Post.query.filter_by(id = post_id).first_or_404()
	if action == 'dislike':
		current_user.dislike_post(post)
		db.session.commit()
	if action == 'Undislike':
			current_user.Undislike_post(post)
			db.session.commit()	
	return redirect(request.referrer)
