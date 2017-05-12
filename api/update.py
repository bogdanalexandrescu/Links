#!/usr/bin/python3

from flask import Response,request,Blueprint
from db_handler import DbHandler
from datetime import datetime
from error_response import ErrorResponse
import token_encoder
import jwt
import json

appUpdate = Blueprint('api_update',__name__)

@appUpdate.route("/api/update",methods=['POST'])
def update():
	response = {}

	userToken = request.headers.get("Authorization")

	if userToken == None:
		return ErrorResponse.authorization_required()

	key = token_encoder.read_key_from_file()

	try:
		userAcc = jwt.decode(userToken,key)
	except jwt.ExpiredSignatureError:
		return ErrorResponse.token_expired()
	except jwt.InvalidTokenError:
		return ErrorResponse.invalid_token()

	name = request.form.get("name")
	birthDay = request.form.get("birth_day")
	birthMonth = request.form.get("birth_month")
	birthYear = request.form.get("birth_year")
	passw = request.form.get("password")
	avatar = request.form.get("avatar")

	db = DbHandler.get_instance().get_connection()
	cursor = db.cursor()

	if birthDay != None and birthMonth != None and birthYear != None:
		birthday = birthDay + "-" + birthMonth + "-" + birthYear
		try:
			birthdayDate = datetime.strptime(birthday,'%d-%B-%Y')
		except:
			response["error"] = "Invalid date"
			response["description"] = "Bad format for date. It should be %d for Day, %B for Month, %Y for Year"
			response["status_code"] = 400
			return Response(json.dumps(response,sort_keys=True),mimetype="application/json"),400
		birthday_date = birthdayDate.strftime('%Y-%m-%d')

		query = "UPDATE users SET name = '%s', birthday_date = str_to_date('%s','%%Y-%%m-%%d') WHERE auth_token = '%s'" % (name,birthday_date,userToken)
		cursor.execute(query)
		db.commit()
	if passw != None and passw != '':
		query = "UPDATE users SET password = '%s' WHERE auth_token = '%s'" % (passw,userToken)
		cursor.execute(query)
		db.commit()
	if name != None and name != '':
		query = "UPDATE users SET name = '%s' WHERE auth_token = '%s'" % (name,userToken)
		cursor.execute(query)
		db.commit()
	if avatar != None:
		query = "UPDATE users SET avatar = '%s' WHERE auth_token = '%s'" % (avatar,userToken)
		cursor.execute(query)
		db.commit()

	response["status"] = 'ok'
	return Response(json.dumps(response,sort_keys=True),mimetype="application/json")


