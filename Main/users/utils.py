from PIL import Image
import secrets
import os
from flask import url_for,current_app
from flask_mail import Message
from Main import mail

def SavePicture(PictureFile):
	random_hex = secrets.token_hex(8)
	_,f_ext = os.path.splitext(PictureFile.filename)
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(current_app.root_path,'static/Profile-pics',picture_fn)
	output_size = (125,125)
	i = Image.open(PictureFile)
	i.thumbnail(output_size)
	i.save(picture_path)
	return picture_fn

def send_reset_email(user):
	token = user.get_reset_token()
	msg = Message('Reset Password',sender='sams44802@gmail.com',recipients=[user.email])
	msg.body = f'''To reset your password click on this link:
{url_for('users.reset_token',token=token,_external=True)}
if You don't want to change please ignore this email'''
	mail.send(msg)
