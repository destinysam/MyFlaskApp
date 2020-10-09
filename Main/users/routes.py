from flask import  render_template,url_for,flash,redirect,request, abort,Blueprint
from flask_login import login_user,current_user,logout_user,login_required
from Main import db,bcrypt
from Main.users.forms import RegisterForm, LoginForm, UpdateAccountForm, RequestResetPassword,ResetPasswordForm
from Main.models import User,Post
from Main.users.utils import SavePicture,send_reset_email

users = Blueprint('users',__name__)
@users.route('/register',methods =['GET','POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index.home'))
	form = RegisterForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username = form.username.data,email=form.email.data,password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash(f'Your Account has been Created!','primary')
		return redirect(url_for('users.login'))
	return render_template('register.html',title = 'Register',form=form)

@users.route('/login',methods =['GET','POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index.home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email = form.email.data).first()
		if user and bcrypt.check_password_hash(user.password,form.password.data):
			login_user(user,remember=form.remember.data)
			next_page =request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('index.home'))	
			flash(f'Logged Successfully!','success')
		else:
			flash(f'Logged Unsuccessfully The Email or Password is incorrect!','danger')
	return render_template('login.html',title='Login',form=form)

@users.route('/logout')
def logout():
	logout_user()
	flash(f'Logout Successfully','info')
	return redirect(url_for('index.home'))

@users.route('/account',methods=['GET','POST'])
@login_required
def account():
	form = UpdateAccountForm()
	if form.validate_on_submit():
		if form.picture.data:
			picture_file = SavePicture(form.picture.data)
			current_user.image_file = picture_file
		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		flash(f"Your Account Has Been Updated",'success')
		return redirect(url_for('users.account'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
	image_file = url_for('static',filename='Profile-pics/'+current_user.image_file)
	return render_template('account.html',image_file=image_file,form=form)

@users.route('/user_posts/<string:username>')
def user_posts(username):
	page = request.args.get('Page',1,type=int)
	user = User.query.filter_by(username=username).first_or_404()
	posts = Post.query.filter_by(author=user)\
	.order_by(Post.date_posted.desc())\
	.paginate(page=page,per_page=3)
	return render_template('user_posts.html',posts=posts,user=user)

@users.route('/reset_password',methods=['GET','POST'])
def reset_request():
	if current_user.is_authenticated:
		return redirect(url_for('index.home'))
	form = RequestResetPassword()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		send_reset_email(user)
		flash(f'An Email has been sent to change your Password','primary')
		return redirect(url_for('users.login'))	
	return render_template('reset_password.html',title='Reset Password',form=form)				

@users.route('/reset_password/<token>',methods=['GET','POST'])
def reset_token(token):
	if current_user.is_authenticated:
		return redirect(url_for('index.home'))
	user = User.verify_reset_token(token)
	if user is None:
		flash(f'Invalid Token please try again','warning')
		return redirect(url_for('users.reset_request'))
	form = ResetPasswordForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(password=form.password.data).decode('utf-8')
		user.password = hashed_password
		db.session.commit()
		flash(f'Your password was Successfully changed','success')
		return redirect(url_for('users.login'))
	return render_template('reset_token.html',title='Reset Password',form=form)		