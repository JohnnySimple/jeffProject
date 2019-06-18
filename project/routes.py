from flask import render_template, url_for, flash, redirect, request, send_file, send_from_directory
from datetime import datetime
from project import app
from project import db, mail
from project.forms import adminLogin, postForm, commentForm, contactForm, subscriptionForm
from flask_login import login_user, current_user, logout_user
from project.models import Posts, Comments, Subscribers
from io import BytesIO
import os
from werkzeug.utils import secure_filename
from flask_mail import Message



UPLOAD_FOLDER = 'D:/personalWebsite/projs/jeffBlog/project/static/img'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER




@app.route('/')
@app.route('/index')
def index():
	stuff = Posts.query.all()
	posts = []
	post_five = []
	for i in reversed(stuff):
		posts.append(i)

	if posts !=[]:
		if len(posts) < 5:
			for i in range(0,len(posts)):
				post_five.append(posts[i])
		else:
			for a in range(0,5):
				post_five.append(posts[a])


	form = subscriptionForm()

	return render_template("index.html", title='Home', posts=posts, post_five=post_five, form=form)


#route for contact us page
@app.route('/contact', methods=['GET', 'POST'])
def contact():
	form = contactForm()
	sub_form = subscriptionForm()
	return render_template("contact.html", title='Contact Us', form=form, sub_form=sub_form)

#route for user to contact us
@app.route('/send_mail', methods=['GET', 'POST'])
def send_mail():
	form = contactForm()
	msg = Message(form.email.data, sender='obengboatengjohnson@gmail.com', recipients=['obengjohnsonboateng@gmail.com'])
	msg.body = form.message.data
	mail.send(msg)
	return 'Email Sent!'


#route for subscription
@app.route('/subscribe', methods=['GET', 'POST'])
def subscribe():
	form = subscriptionForm()

	if form.validate_on_submit():
		new_subscriber = Subscribers(email=form.email.data)
		db.session.add(new_subscriber)
		db.session.commit()
	return 'Subscribed Successfully'


@app.route('/single_post/<content>', methods=['GET', 'POST'])
def single_post(content):
	post = Posts.query.filter_by(id=content).first()
	comments = Comments.query.all()
	form = commentForm()
	sub_form = subscriptionForm()
	comment_post = content
	c_ment = []

	for a in comments:
		if a.post_id == post.id:
			c_ment.append(a)

	if form.validate_on_submit():
		new_comment = Comments(name=form.name.data, content=form.content.data, post_id=post.id)
		db.session.add(new_comment)
		db.session.commit()

		# return redirect('single_post')
	return render_template('single_post.html', post=post, form=form,c_ment=c_ment, comment_post=comment_post, sub_form=sub_form)


# route fo html body in email
@app.route('/subscriber_email/<picture>')
def subscriber_email(picture):
	pic = Posts.query.filter_by(id=picture).first()
	return render_template('email.html', pic=pic)


@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
	if current_user.is_authenticated:
		return redirect(url_for('admin'))
	form = adminLogin()

	if form.validate_on_submit():
		if form.admin_username.data == "simple" and form.admin_password.data == "adminsimple":
			return redirect(url_for('adminPage'))
		else:
			flash('Username or password incorrect!!!', 'danger')
	return render_template('admin-login.html', title='Admin Login', form=form)

@app.route('/adminPage', methods=['GET', 'POST'])
def adminPage():
	form = postForm()
	return render_template("admin.html", form=form)


def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET','POST'])
def upload():
	form = postForm()
	subs_form = subscriptionForm()
	sub = Subscribers.query.all()
	subs = []
	for a in sub:
		subs.append(a.email)
	# file = request.files['inputFile']

	if request.method == 'POST':
		# check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect(url_for('adminPage'))
		file = request.files['file']
		# if user does not select file, browser also
		# submit an empty part without filename
		if file.filename == '':
			flash('No selected file')
			return redirect(url_for('adminPage'))
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			
			newFile = Posts(title= form.title.data, content= form.content.data, image_name=file.filename, image_data=file.read())
			db.session.add(newFile)
			db.session.commit()
			
			# sending post to subscribers' email
			# msg = Message(form.title.data, sender='obengboatengjohnson@gmail.com', recipients=subs)
			
			# msg.body = form.content.data
			# msg.html = render_template('/email.html', picture=file.filename)
			# # with app.open_resource(file.filename) as fp:
			# # 	msg.attach(file.filename, 'img', fp.read())
			# mail.send(msg)

			return redirect(url_for('uploaded_file', filename=filename))

	return 'successful'
	
		
	# flash(format('Update posted successfully! ' ), 'success')

	# return "saved!!!"
	
	# return "Saved successfully in the database"

@app.route('/uploads/<filename>')
def uploaded_file(filename):
	return send_from_directory(app.config['UPLOAD_FOLDER'], filename)