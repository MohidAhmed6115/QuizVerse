from flask import Flask,session,render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, DateTime, func
from dotenv import load_dotenv
from urllib.parse import quote_plus
import os
from flask_bcrypt import Bcrypt
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, RadioField
from wtforms.validators import InputRequired, Length, ValidationError
import math
from datetime import timedelta, datetime
load_dotenv()

password = quote_plus(os.getenv('DB_PASSWORD'))
database = os.getenv("DB_NAME")

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = "Secret"

app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://root:{password}@localhost/{database}"

app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=14)

class Base(DeclarativeBase):
	pass
db = SQLAlchemy(app, model_class=Base)
login_manager = LoginManager()
login_manager.init_app(app)
# If someone hasn't login  and tries to visit a page that requires login redirect them to route name login
login_manager.login_view = 'login'

# Function for checking who is the current logged-in user actually is, it automatically called on every request
@login_manager.user_loader
def load_user(user_id):
	return db.session.get(Users, int(user_id))

class Questions(db.Model):
	__tablename__ = "questions"

	id:Mapped[int] = mapped_column(primary_key=True)
	category: Mapped[str] = mapped_column(String(100))
	question_text: Mapped[str] = mapped_column(Text)
	option_a : Mapped[str] = mapped_column(Text)
	option_b : Mapped[str] = mapped_column(Text)
	option_c : Mapped[str] = mapped_column(Text)
	option_d : Mapped[str] = mapped_column(Text)
	correct_option : Mapped[str] = mapped_column(String(1))

class QuizAttempts(db.Model):
	__tablename__ = "quiz_attempts"
	id:Mapped[int] = mapped_column(primary_key=True)
	user_id: Mapped[int] = mapped_column(unique = True)
	category: Mapped[str] = mapped_column(String(100))
	score: Mapped[int] = mapped_column(nullable = True)
	taken_at : Mapped[datetime] = mapped_column(DateTime,server_default = func.now())

class Users(UserMixin,db.Model):
	__tablename__ = "users"

	id: Mapped[int] = mapped_column(primary_key=True)
	email: Mapped[str] = mapped_column(String(100), unique=True)
	username : Mapped[str] = mapped_column(String(20), unique=True)
	password : Mapped[str] = mapped_column(String(255))
	highest_score: Mapped[int] = mapped_column(nullable=True)


class LoginForm(FlaskForm):
	username = StringField(validators=[InputRequired(), Length(min = 4, max = 20)], render_kw={"placeholder": "username"})

	password = PasswordField(validators=[InputRequired(), Length(min = 4, max = 20)], render_kw={"placeholder": "password"})

	submit = SubmitField('Log in')


class RegisterForm(FlaskForm):
	email = EmailField(validators=[InputRequired(), Length(min = 4, max = 100)], render_kw={"placeholder":"Email"})

	username = StringField(validators=[InputRequired(), Length(min = 4, max = 20)], render_kw={"placeholder": "username"})

	password = PasswordField(validators=[InputRequired(), Length(min = 4, max = 20)], render_kw={"placeholder": "password"})

	submit = SubmitField('Sign Up')

	def validate_username(self, username):
		existing_user_name = Users.query.filter_by(username = username.data).first()
		if existing_user_name:
			raise ValidationError(
				"Username already taken. Please Choose a different one."
			)
	def validate_email(self,email):
		existing_mail = Users.query.filter_by(email = email.data).first()
		if existing_mail:
			raise ValidationError(
				"Email already used."
			)

class QuizQuestionChoice(FlaskForm):
	answer = RadioField('Choose an Answer', validators=[InputRequired()])

	submit = SubmitField("Next") 

@app.route("/")
def home():
	if current_user.is_authenticated:
		return redirect(url_for('dashboard'))
	return render_template("home.html")


@app.route("/login", methods = ["GET","POST"])
def login():
	form = LoginForm()
	if current_user.is_authenticated:
			return redirect(url_for('dashboard'))
	if form.validate_on_submit():
		user = Users.query.filter_by(username = form.username.data).first()
		if user:
			if bcrypt.check_password_hash(user.password, form.password.data):
				login_user(user, remember = True)
				return redirect(url_for('dashboard'))
			else:
				flash("You Entered wrong Password")
		else:
			flash("Wrong Username")
	return render_template("login.html", form = form)


@app.route("/signup", methods = ["GET","POST"])
def signup():
	form = RegisterForm()
	if current_user.is_authenticated:
			return redirect(url_for('dashboard'))
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		new_user = Users(username = form.username.data, password = hashed_password, email = form.email.data)

		db.session.add(new_user)
		db.session.commit()
		return redirect(url_for('login'))

	return render_template("signup.html", form = form)

@app.route("/logout")
@login_required
def logout():
	logout_user()
	return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
	return render_template("dashboard.html")

@app.route('/categories')
@login_required
def categories():
	return render_template("categories.html")

@app.route('/quiz/<category>', methods = ["GET","POST"])
@login_required
def start_quiz(category):

	questions = Questions.query.filter_by(category = category).all()
	last = len(questions) - 1
	page = request.args.get('page')
	if not str(page).isnumeric():
		page = 0
	else:
		page = int(page)

	# Slicing of array questions
	# [arg * no of question in a page : arg * no of question in a page + no of question in a page]
	# Only One Question Per page
	questions = questions[page*1:page*1+1]
	current_question = questions[0] 
	form = QuizQuestionChoice()
	form.answer.choices = [
		('a',current_question.option_a),
		('b',current_question.option_b),
		('c',current_question.option_c),
		('d',current_question.option_d)
	]
	if page == 0 and page == last:
		prev = "#"
		next = "#"
	elif page == 0:
		prev = "#"
		next = url_for('start_quiz',category = category) + "?page=" + str(page + 1)
	elif page == last:
		prev = url_for('start_quiz',category = category) + "?page=" + str(page - 1)
		next = "#"
	else:
		prev = url_for('start_quiz',category = category) + "?page=" + str(page - 1)
		next = url_for('start_quiz',category = category) + "?page=" + str(page + 1)
	
	if form.validate_on_submit():
		selected_answer = form.answer.data
		answers = session.get('quiz_answers',{})
		answers[str(current_question.id)] = selected_answer
		session['quiz_answers'] = answers
				
		if page == last:
			return redirect(url_for('quiz_results'))
		return redirect(next)
	return render_template("quiz.html", question = current_question, prev = prev, next = next, form = form)

if __name__ == "__main__":
	app.run(debug=True)