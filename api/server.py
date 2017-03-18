#!/usr/bin/python3

from flask import Flask,
from flask_socketio import SocketIO
import json
from login import appLogin
from signup import appSignup
from friendrequest import appFriendRequest
from acceptfriend import appAcceptFriend
from removefriend import appRemoveFriend
from friendrequests import appFriendRequests
from profile import appProfile

app = Flask(__name__)
socketio = SocketIO(app)

app.register_blueprint(appLogin)
app.register_blueprint(appSignup)
app.register_blueprint(appFriendRequest)
app.register_blueprint(appAcceptFriend)
app.register_blueprint(appRemoveFriend)
app.register_blueprint(appFriendRequests)
app.register_blueprint(appProfile)

@app.route("/api/hello")
def hello():
	user = {}
	user["Nume"] = "Andrei"
	user["Varsta"] = 20
	user["Facultate"] = 'Ongoing'
	user["Master"] = 'False'

	studii = ["Gradinita","Scoala Generala","Liceu","Facultate"];
	user["studii"] = studii

	userJson = json.dumps(user)
	return Response(userJson,mimetype='application/json')

@app.route("/api/name")
def name():
	return "Ahoi marinari!!"

if __name__ == "__main__":
	app.run(debug=True)


