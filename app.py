from flask import Flask,session,render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from dotenv import load_dotenv
from urllib.parse import quote_plus
import os
from flask_bcrypt import Bcrypt
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import InputRequired, Length, ValidationError
from datetime import timedelta
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


if __name__ == "__main__":
	app.run(debug=True)