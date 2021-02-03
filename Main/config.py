class config:
	SECRET_KEY = SECRET_KEY
	SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
	WHOOSH_BASE = 'whoosh'
	TESTING = False 
	MAIL_SERVER = 'smtp.sendgrid.net'
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	MAIL_USE_SSL = False
	MAIL_USERNAME = 'apikey'
	MAIL_PASSWORD = PASSWORD
	MAIL_DEFAULT_SENDER = EMAIL
	MAIL_MAX_EMAILS = None
	MAIL_ASCII_ATTACHMENTS = False
