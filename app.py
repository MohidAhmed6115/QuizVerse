from flask import Flask,session,render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, mapped_column
from sqlalchemy import Integer, String, Text
from dotenv import load_dotenv
from urllib.parse import quote_plus
import os

app = Flask(__name__)

@app.route("/")
def home():
	return render_template("home.html")


@app.route("/login", methods = ["GET","POST"])
def login():
	if request.method == 'POST':
		pass


	return render_template("login.html")

@app.route("/signup", methods = ["GET","POST"])
def signup():
	if request.method == "POST":
		pass

	return render_template("signup.html")

if __name__ == "__main__":
	app.run(debug=True)