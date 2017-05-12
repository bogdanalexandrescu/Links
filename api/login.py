#!/usr/bin/python3
from flask import Blueprint,Response,request,redirect,url_for,render_template
from flask_login import login_user,current_user
from db_handler import DbHandler
import token_encoder
import json
import jwt
import datetime
from User import *

appLogin = Blueprint('api_login',__name__)

@appLogin.route("/api/login", methods =['POST']) #methods=['POST']
def login():

	db= DbHandler.get_instance().get_connection()

	response = {}

	#get the info from request
	email = request.form.get("email")
	password = request.form.get("password")
	rememberMe = request.form.get("remember_me")

	#SQL cmd
	query =  "SELECT id, name, active  FROM users WHERE email='%s' AND password ='%s'" % (email, password)

	#execute SQL cmd
	cursor = db.cursor()
	cursor.execute(query)

	#retrieve DB answer
	data = cursor.fetchone()

	if data != None:
#		user = User(data[0],data[1],data[2])
		active = data[2]
		if active == 0:
			return render_template("account_NotVerified.html")
		response["status"] = 'ok'
#		if rememberMe == "true":
#			login_user(user,remember = True)
#		else:
#			login_user(user)
	else:
		response["error"] = 'Invalid email or password'
		response["status_code"] = 401


	#return redirect(urlfor("api_login.chat"))

	if "error" in response:
		return Response(json.dumps(response, sort_keys=True), mimetype="application/json"),401

	auth_token = str(token_encoder.encode_auth_token(data[0]))
	auth_token = auth_token[2:]
	auth_token = auth_token[:len(auth_token)-1]
	response["access_token"] = auth_token

	query = "UPDATE users SET auth_token = '%s' WHERE id = %d" % (auth_token,data[0])

	cursor.execute(query)
	db.commit()

	#return redirect(url_for("chat"))
	return Response(json.dumps(response, sort_keys=True), mimetype="application/json")

#@appLogin.route("/chat")
#def chat():
#	return render_template("index2.html")
