#!/usr/bin/python3

from flask import Blueprint, Response, request
from db_handler import DbHandler
from error_response import ErrorResponse

import token_encoder
import json
import jwt

appStory = Blueprint("api_story",__name__)

@appStory.route("/api/story",methods = ['GET'])
def story():

	response = {}

	#get user authentification

	userToken = request.headers.get('Authorization')
	if userToken == None:
		return ErrorResponse.authorization_required()

	#check user authentification

	key = token_encoder.read_key_from_file()

	try:
		userAcc = jwt.decode(userToken,key)
	except jwt.ExpiredSignatureError:
		return ErrorResponse.token_expired()
	except jwt.InvalidTokenError:
		return ErrorResponse.invalid_token()

	#get friend email and check it's validity
	friendshipId = request.args.get('friendship_id')
#	if friendshipId == None :
#		response['error'] = "Invalid friendship"
#		response['description'] = "Please provide a friendship id"
#		response['status_code'] = 400
#	return Response(json.dumps(response, sort_keys = True), mimetype = 'application/json'), 400

	#connect to db
	db = DbHandler.get_instance().get_connection()
	cursor = db.cursor()

	#get id of user
	query = "SELECT id FROM users WHERE auth_token = '%s'" % (userToken)
	cursor.execute(query)
	userData = cursor.fetchone()

	#check if token is assigned to a user
	if userData == None :
		response['status'] = "Invalid token"
		response['description'] = "Token is not assigned to any user"
		response['status_code'] = 401
		return Response(json.dumps(response,sort_keys = True), mimetype = 'application/json'),401

	userId = userData[0]


	if friendshipId != None:

		#get friend id by excluding user id
		query = "SELECT user_1, user_2 from friendships WHERE id = '%s'" % (friendshipId)
		cursor.execute(query)
		ids = cursor.fetchone()

		#check we have a friendship for specified friendship id
		if ids == None :
			response['status'] = "No friendships found for this id"
			response['description'] = "Please provide a valid friendship id"
			response['status_code'] = 400
			return Response(json.dumps(response,sort_keys = True), mimetype = 'application/json'), 400
		else:
			if ids[0] == userId[0] :
				friendId = ids[0]
			else :
				friendId = ids[1]
	else:
		friendId = userAcc["sub"] # daca nu a dat un friendship id, atunci ii intoarcem story-ul lui

	query = "SELECT text,feel,image,date FROM story WHERE user_id = '%d'" % (friendId)
	cursor.execute(query)
	story = cursor.fetchone()

	response['status'] = "ok"

	if story == None :
		response["error"] = "No story"
		response["description"] = "User doesn't have a story"
		return Response(json.dumps(response,sort_keys = True),mimetype = 'application/json'), 200

	#only return story parameters that are not null
	text = story[0]
	feel = story[1]
	image = story[2]
	date = story[3]

	if text != None and text != "" and text != "None" :
		response['text'] = text
	if feel != None and feel != "" and feel != "None" :
		response['feel'] = feel
	if image != None and image != "" :

		image = str(image)
		if image[0] == 'b':
			image = image[1:]
		if image[0] == "'":
			image = image[1:len(image)-1]
		if image != "None":
			response['image'] = image

	response['date'] = str(date)

	return Response(json.dumps(response,sort_keys = True),mimetype = 'application/json'), 200
