from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_mail import Mail

app = Flask(__name__)

app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

#creating the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jeffBlog.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = ('obengboatengjohnson')
app.config['MAIL_PASSWORD'] = ('johnnysimple')

mail = Mail(app)


from project.models import Posts, Comments, Subscribers

admin = Admin(app)
admin.add_view(ModelView(Posts, db.session))
admin.add_view(ModelView(Comments, db.session))
admin.add_view(ModelView(Subscribers, db.session))

from project import routes